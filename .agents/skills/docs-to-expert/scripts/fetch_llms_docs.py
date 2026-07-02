#!/usr/bin/env python3
"""Mirror a docs site via its llms.txt index: one local file per page, no chunking.

Most modern docs sites (Mintlify-based ones especially) publish an llms.txt
index at the site root or under /docs, listing every page as
"- [title](url): description", with url serving clean markdown directly
(often at url + ".md"). This script uses that index instead of scraping and
re-splitting HTML, so pages can never collide (one URL = one file) and
updates only touch pages that actually changed.

Usage:
    python fetch_llms_docs.py --root <any_docs_page_url> --output <references_dir>
    python fetch_llms_docs.py --root <any_docs_page_url> --output <references_dir> --update

Exits with code 2 and prints "NO_LLMS_TXT: ..." if the target site has no
llms.txt. The caller should fall back to extract_links.py --export-dir.
"""
import argparse
import gzip
import re
import sys
import urllib.request
import urllib.parse
import zlib
from datetime import datetime
from pathlib import Path

try:
    from bs4 import BeautifulSoup
    from markdownify import markdownify as html_to_md
except ImportError:
    BeautifulSoup = None
    html_to_md = None

LLMS_LINE_RE = re.compile(r'^- \[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\s*:\s*(?P<desc>.*)$')
INDEX_LINE_RE = re.compile(r'^- \[(?P<title>[^\]]+)\]\((?P<file>[^)]+)\)\s*:\s*(?P<desc>.*)$')


def fetch_text(url, timeout=10):
    """GET a URL as text. Some servers (observed: antigravity.google's Google
    Frontend) send gzip-encoded bodies regardless of the Accept-Encoding we
    ask for, so decompress based on the actual Content-Encoding header rather
    than trusting the request we sent."""
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        encoding = (resp.headers.get('Content-Encoding') or '').lower()
        if 'gzip' in encoding:
            raw = gzip.decompress(raw)
        elif 'deflate' in encoding:
            try:
                raw = zlib.decompress(raw)
            except zlib.error:
                raw = zlib.decompress(raw, -zlib.MAX_WBITS)
        return raw.decode('utf-8', errors='replace')


def looks_like_html(text):
    lowered = text.lstrip().lower()
    return lowered.startswith('<!doctype') or lowered.startswith('<html') or '<body' in lowered[:2000]


MIN_SPLIT_CHAR_RUN = 4  # consecutive single-character paragraphs this long or longer are a render artifact, not content
ICON_LIGATURE_RE = re.compile(r'^[a-z]+(\\?_[a-z]+){0,4}$')  # e.g. "dashboard\_customize" - a Material Symbols icon-font name
ICON_PREFIX_RE = re.compile(r'^[a-z]+(\\?_[a-z]+){0,4}(?=[A-Z])')  # e.g. "play\_arrowPlay video" - icon token fused directly onto a real button label, no separator


def clean_rendered_artifacts(markdown_text):
    """Strip two rendering artifacts seen in headless-browser captures of
    animated/icon-heavy pages (observed on antigravity.google):

    1. Character-by-character duplicate text: some sites animate headings by
       revealing them one letter per DOM node. The correct text already
       appears as an ordinary paragraph right before it, so the exploded
       version is pure duplicate noise, not information - safe to delete
       outright rather than try to rejoin (rejoining risks getting word
       spacing wrong).
    2. Icon-font ligature names: icon components (e.g. Material Symbols)
       render as a lowercase snake_case token like "dashboard_customize"
       when the icon font itself isn't available to the crawler - this is
       never real prose, so any standalone paragraph matching that shape
       is dropped.
    """
    paragraphs = markdown_text.split('\n\n')
    cleaned = []
    i = 0
    while i < len(paragraphs):
        p = paragraphs[i]
        stripped = p.strip()
        if ICON_LIGATURE_RE.match(stripped):
            i += 1
            continue
        stripped = ICON_PREFIX_RE.sub('', stripped, count=1)
        p = stripped
        if len(stripped) == 1 and stripped.isalnum():
            run_end = i
            while run_end < len(paragraphs) and len(paragraphs[run_end].strip()) == 1 and paragraphs[run_end].strip().isalnum():
                run_end += 1
            run_len = run_end - i
            if run_len >= MIN_SPLIT_CHAR_RUN:
                i = run_end
                continue
        cleaned.append(p)
        i += 1
    return '\n\n'.join(cleaned)


def convert_html_to_markdown(html_text, title_hint):
    """Fallback for sites whose llms.txt lists rendered HTML pages instead of
    clean markdown (observed: antigravity.google, unlike Mintlify sites which
    serve markdown directly). Mirrors the extraction logic in extract_links.py."""
    if not BeautifulSoup or not html_to_md:
        return None
    soup = BeautifulSoup(html_text, 'html.parser')
    content = soup.find('main') or soup.find('article') or soup.find('div', role='main') or soup.find('body')
    if not content:
        return None
    for elem in content(['script', 'style', 'nav', 'header', 'footer']):
        elem.extract()
    markdown = html_to_md(str(content), heading_style="ATX")
    return clean_rendered_artifacts(markdown)


def candidate_llms_urls(root):
    parsed = urllib.parse.urlparse(root)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    candidates = [f"{origin}/llms.txt"]
    if '/docs' in parsed.path:
        prefix = parsed.path[:parsed.path.index('/docs') + len('/docs')]
        candidates.append(f"{origin}{prefix}/llms.txt")
    seen = []
    for c in candidates:
        if c not in seen:
            seen.append(c)
    return seen


def parse_llms_txt(text):
    entries = []
    seen_urls = set()
    for line in text.splitlines():
        m = LLMS_LINE_RE.match(line.strip())
        if not m:
            continue
        url = m.group('url').strip()
        if url in seen_urls:
            continue
        seen_urls.add(url)
        entries.append({
            'title': m.group('title').strip(),
            'url': url,
            'description': m.group('desc').strip(),
        })
    return entries


def find_llms_txt(root):
    for url in candidate_llms_urls(root):
        try:
            text = fetch_text(url)
        except Exception:
            continue
        if parse_llms_txt(text):
            return url, text
    return None, None


def slug_from_url(url):
    path = urllib.parse.urlparse(url).path
    if path.endswith('.md'):
        path = path[:-3]
    path = path.strip('/')
    slug = re.sub(r'[^a-zA-Z0-9/_-]', '', path).replace('/', '-')
    return slug or 'index'


def resolve_page_content(url):
    """Return clean markdown for a page, whichever way the site serves it.
    Some llms.txt implementations (Mintlify: code.claude.com) list URLs that
    already serve markdown. Others (observed: antigravity.google) list the
    regular rendered HTML page instead. Try the URL as-is; if it's HTML, try
    appending .md (the Mintlify convention, in case it also works here); if
    that fails too, convert the HTML to markdown directly."""
    text = fetch_text(url)
    if not looks_like_html(text):
        return text
    if not url.endswith('.md'):
        try:
            md_text = fetch_text(url + '.md')
            if not looks_like_html(md_text):
                return md_text
        except Exception:
            pass
    converted = convert_html_to_markdown(text, url)
    return converted if converted is not None else text


MIN_CONTENT_CHARS = 80  # below this, treat as a failed fetch rather than silently shipping an empty page


def write_concept_file(concepts_dir, entry):
    filename = f"{slug_from_url(entry['url'])}.md"
    filepath = concepts_dir / filename
    try:
        content = resolve_page_content(entry['url'])
    except Exception as e:
        print(f"  WARN: khong tai duoc {entry['url']}: {e}", file=sys.stderr)
        return None
    if len(content.strip()) < MIN_CONTENT_CHARS:
        print(f"  WARN: {entry['url']} tra ve noi dung qua ngan ({len(content.strip())} ky tu) - "
              f"trang co the render bang JavaScript, thu scripts/fetch_js_rendered.py", file=sys.stderr)
        return None
    frontmatter = (
        "---\n"
        f"title: {entry['title']}\n"
        f"date_created: {datetime.now().strftime('%Y-%m-%d')}\n"
        f"source_url: {entry['url']}\n"
        f"description: {entry['description']}\n"
        "tags: [concept, llms-txt]\n"
        "---\n\n"
    )
    filepath.write_text(frontmatter + content, encoding='utf-8')
    return filename


def load_previous_index(output_dir):
    """Read back {source_url: description} from a previously generated mirror."""
    index_path = output_dir / 'INDEX.md'
    if not index_path.exists():
        return {}
    prev = {}
    for line in index_path.read_text(encoding='utf-8').splitlines():
        m = INDEX_LINE_RE.match(line.strip())
        if not m:
            continue
        filepath = output_dir / m.group('file')
        if not filepath.exists():
            continue
        text = filepath.read_text(encoding='utf-8')
        um = re.search(r'^source_url:\s*(.+)$', text, re.MULTILINE)
        if um:
            prev[um.group(1).strip()] = m.group('desc').strip()
    return prev


def main():
    parser = argparse.ArgumentParser(description="Mirror a docs site via its llms.txt index, one file per page.")
    parser.add_argument('--root', required=True, help="Any URL within the target docs site.")
    parser.add_argument('--output', required=True, help="references/ directory to write INDEX.md + concepts/ into.")
    parser.add_argument('--update', action='store_true', help="Only (re)fetch pages that are new or whose description changed.")
    args = parser.parse_args()

    output_dir = Path(args.output)
    concepts_dir = output_dir / 'concepts'
    concepts_dir.mkdir(parents=True, exist_ok=True)

    llms_url, llms_text = find_llms_txt(args.root)
    if not llms_url:
        print(f"NO_LLMS_TXT: khong tim thay llms.txt hop le cho {args.root}", file=sys.stderr)
        sys.exit(2)

    entries = parse_llms_txt(llms_text)
    if not entries:
        print(f"NO_LLMS_TXT: {llms_url} khong dung dinh dang mong doi", file=sys.stderr)
        sys.exit(2)

    print(f"Tim thay llms.txt tai {llms_url} ({len(entries)} trang)")

    previous = load_previous_index(output_dir) if args.update else {}

    index_lines = ["# Master Index", "",
                   f"Nguon: {llms_url}",
                   f"Cap nhat lan cuoi: {datetime.now().strftime('%Y-%m-%d')}", ""]
    added = changed = unchanged = failed = 0
    for entry in entries:
        filename = f"{slug_from_url(entry['url'])}.md"
        prev_desc = previous.get(entry['url'])
        already_fresh = (
            args.update
            and prev_desc is not None
            and prev_desc == entry['description']
            and (concepts_dir / filename).exists()
        )
        if already_fresh:
            unchanged += 1
        else:
            if write_concept_file(concepts_dir, entry) is None:
                failed += 1
                continue
            if prev_desc is None:
                added += 1
            else:
                changed += 1
        index_lines.append(f"- [{entry['title']}](concepts/{filename}): {entry['description']}")

    (output_dir / 'INDEX.md').write_text("\n".join(index_lines) + "\n", encoding='utf-8')

    if args.update:
        print(f"Cap nhat xong: {added} moi, {changed} doi, {unchanged} giu nguyen, {failed} loi.")
    else:
        print(f"Tai xong: {added + changed} trang, {failed} loi.")


if __name__ == '__main__':
    main()
