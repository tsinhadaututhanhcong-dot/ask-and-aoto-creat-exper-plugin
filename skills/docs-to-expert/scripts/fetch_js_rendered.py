#!/usr/bin/env python3
"""Fallback for docs sites whose content is rendered client-side by
JavaScript (observed: antigravity.google - an Angular/React-style single-page
app where the raw HTTP response is just an empty app shell). fetch_llms_docs.py
and extract_links.py both do a plain HTTP GET, so they see nothing a JS
framework injects after the page loads. This uses a real headless browser
(Playwright) to render each page before extracting content.

Reuses the parsing/conversion helpers from fetch_llms_docs.py so both scripts
stay consistent (same frontmatter shape, same slug scheme, same HTML->markdown
conversion).

Requires: pip install playwright && playwright install chromium

Usage:
    python fetch_js_rendered.py --llms-txt <url_to_llms.txt_or_local_file> --output <references_dir>
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_llms_docs import fetch_text, parse_llms_txt, slug_from_url, convert_html_to_markdown  # noqa: E402

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

MIN_CONTENT_CHARS = 200


def render_page(page, url, settle_ms=2000):
    page.goto(url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(settle_ms)  # let post-networkidle client-side rendering finish
    return page.content()


def main():
    parser = argparse.ArgumentParser(description="Mirror a JS-rendered docs site with a headless browser.")
    parser.add_argument('--llms-txt', required=True, help="URL (or local file path) to the site's llms.txt.")
    parser.add_argument('--output', required=True, help="references/ directory to write INDEX.md + concepts/ into.")
    args = parser.parse_args()

    if sync_playwright is None:
        print("Can cai dat Playwright: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    if args.llms_txt.startswith('http'):
        llms_text = fetch_text(args.llms_txt)
    else:
        llms_text = Path(args.llms_txt).read_text(encoding='utf-8')

    entries = parse_llms_txt(llms_text)
    if not entries:
        print(f"Khong doc duoc danh sach trang tu {args.llms_txt}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    concepts_dir = output_dir / 'concepts'
    concepts_dir.mkdir(parents=True, exist_ok=True)

    index_lines = ["# Master Index", "",
                   f"Nguon: {args.llms_txt} (render qua headless browser - trang can JavaScript)",
                   f"Cap nhat lan cuoi: {datetime.now().strftime('%Y-%m-%d')}", ""]

    ok = failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for entry in entries:
            filename = f"{slug_from_url(entry['url'])}.md"
            try:
                html = render_page(page, entry['url'])
                markdown = convert_html_to_markdown(html, entry['url']) or ""
                if len(markdown.strip()) < MIN_CONTENT_CHARS:
                    raise ValueError(f"noi dung qua ngan sau khi render ({len(markdown.strip())} ky tu)")
            except Exception as e:
                print(f"  WARN: {entry['url']}: {e}", file=sys.stderr)
                failed += 1
                continue
            frontmatter = (
                "---\n"
                f"title: {entry['title']}\n"
                f"date_created: {datetime.now().strftime('%Y-%m-%d')}\n"
                f"source_url: {entry['url']}\n"
                f"description: {entry['description']}\n"
                "tags: [concept, llms-txt, js-rendered]\n"
                "---\n\n"
            )
            (concepts_dir / filename).write_text(frontmatter + markdown, encoding='utf-8')
            index_lines.append(f"- [{entry['title']}](concepts/{filename}): {entry['description']}")
            ok += 1
        browser.close()

    (output_dir / 'INDEX.md').write_text("\n".join(index_lines) + "\n", encoding='utf-8')
    print(f"Render xong: {ok} trang, {failed} loi.")


if __name__ == '__main__':
    main()
