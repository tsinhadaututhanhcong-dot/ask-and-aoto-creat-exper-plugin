#!/usr/bin/env python3
"""Detect and tag multiple "surfaces" (platforms/products) within one docs
mirror, and regroup INDEX.md accordingly.

Generalizes two one-off scripts written by hand this session: reorganize.py
(claude-expert, ~156 pages, no filename structure, needed manual per-page
classification) and tag_antigravity.py (antigravity-expert-claude, 88 pages,
clear "docs-cli-*"/"docs-ide-*" filename prefixes, classifiable by structure
alone). Classifying a page by surface is fundamentally a semantic judgment,
not always recoverable from filenames - so this script only ever proposes;
a human/agent must confirm before --apply runs.

Usage:
    python tag_by_surface.py --detect --index <INDEX.md>
        Prints a clustering proposal and writes surface_mapping.json next to
        INDEX.md (review/edit it before applying). Prints TIER1_UNCLEAR when
        filename structure doesn't yield a confident grouping - the caller
        should read INDEX.md's titles/descriptions and classify by hand
        instead of trusting a low-confidence guess.

    python tag_by_surface.py --apply --index <INDEX.md> --mapping <surface_mapping.json> [--comparison-files a.md,b.md]
        Tags each concept file's frontmatter with `platform: <surface>` and
        regenerates INDEX.md grouped by surface. If --comparison-files names
        pages that authoritatively compare surfaces (e.g. Claude Code's
        feature-availability page), that section is pinned first. Otherwise
        INDEX.md carries an explicit "no comparison page - silence means
        unconfirmed" notice, matching what was done by hand for
        antigravity-expert-claude.
"""
import argparse
import json
import re
import sys
from collections import defaultdict, Counter
from pathlib import Path

INDEX_LINE_RE = re.compile(r'^- \[(?P<title>[^\]]+)\]\(concepts/(?P<file>[^)]+)\)\s*:\s*(?P<desc>.*)$')

MIN_TOKEN_COUNT = 3       # a token must recur in at least this many filenames to be a cluster candidate
MAX_TOKEN_RATIO = 0.6     # tokens shared by more than this fraction of files are too generic (e.g. "docs")
CONFIDENT_COVERAGE = 0.5  # need at least this fraction of files clustered to trust Tier 1

COMPARISON_KEYWORDS = re.compile(
    r'\b(compare|comparison|vs\.?|versus|choose|choosing|which (one|should)|'
    r'feature availability|platforms? and integrations?|differences?)\b', re.IGNORECASE)


def parse_index(index_path):
    entries = []
    for line in index_path.read_text(encoding='utf-8').splitlines():
        m = INDEX_LINE_RE.match(line.strip())
        if m:
            entries.append({'title': m.group('title'), 'file': m.group('file'), 'desc': m.group('desc')})
    return entries


def tokenize(filename):
    stem = filename[:-3] if filename.endswith('.md') else filename
    return [t for t in stem.split('-') if t and not t.isdigit()]


def propose_clusters(entries):
    """Group files by a shared CONTIGUOUS filename prefix of >= 2 tokens
    (e.g. "docs-cli-overview" and "docs-cli-install" share prefix "docs-cli").
    Deliberately does NOT match on a single recurring token anywhere in the
    name: words like "overview", "settings", "getting-started", "plugins", or
    a shared brand name ("product-antigravity-cli" vs "-ide" vs "-sdk") recur
    across EVERY surface as generic topic/suffix words, not as a surface
    identifier - matching on those alone merges unrelated surfaces into one
    wrong bucket (confirmed by testing against a real corpus). A confidently
    wrong cluster is worse than reporting nothing, so this only trusts the
    prefix pattern and leaves everything else for manual review."""
    total = len(entries)
    file_tokens = {e['file']: tokenize(e['file']) for e in entries}

    prefix_count = Counter()
    for parts in file_tokens.values():
        for length in range(2, len(parts) + 1):
            prefix_count['-'.join(parts[:length])] += 1

    candidates = {p: c for p, c in prefix_count.items() if MIN_TOKEN_COUNT <= c <= total * MAX_TOKEN_RATIO}

    assignment = {}
    for e in entries:
        parts = file_tokens[e['file']]
        # longest (most specific) qualifying prefix wins
        for length in range(len(parts), 1, -1):
            prefix = '-'.join(parts[:length])
            if prefix in candidates:
                assignment[e['file']] = parts[length - 1]  # label = last token of the matched prefix
                break

    clustered = [e for e in entries if e['file'] in assignment]
    unclustered = [e for e in entries if e['file'] not in assignment]
    coverage = len(clustered) / total if total else 0
    cluster_names = sorted(set(assignment.values()))
    confident = coverage >= CONFIDENT_COVERAGE and len(cluster_names) >= 2

    return {
        'confident': confident,
        'coverage': coverage,
        'clusters': {name: [e for e in clustered if assignment[e['file']] == name] for name in cluster_names},
        'unclustered': unclustered,
        'assignment': assignment,
    }


def propose_comparison_pages(entries):
    hits = []
    for e in entries:
        text = f"{e['title']} {e['desc']}"
        if COMPARISON_KEYWORDS.search(text):
            hits.append(e['file'])
    return hits


def cmd_detect(args):
    index_path = Path(args.index)
    entries = parse_index(index_path)
    if not entries:
        print("Khong doc duoc muc nao tu INDEX.md", file=sys.stderr)
        sys.exit(1)

    result = propose_clusters(entries)
    comparison_candidates = propose_comparison_pages(entries)

    print(f"Tong so trang: {len(entries)}")
    print(f"Do phu cua Tier 1: {result['coverage']:.0%}")
    if comparison_candidates:
        print(f"\nCo the la trang doi chieu chinh thuc (kiem tra lai truoc khi tin):")
        for f in comparison_candidates:
            print(f"  - {f}")
    else:
        print("\nKhong tim thay trang nao co dau hieu la trang doi chieu chinh thuc.")

    if not result['confident']:
        print(f"\nTIER1_UNCLEAR: khong tim duoc cau truc ro rang qua ten file "
              f"(do phu {result['coverage']:.0%} < nguong {CONFIDENT_COVERAGE:.0%}, "
              f"hoac chua du 2 nhom). Doc tieu de + mo ta tung dong trong INDEX.md "
              f"va tu phan loai thu cong, roi ghi surface_mapping.json.")
        if result['clusters']:
            print("Cac nhom yeu tim duoc (chi de tham khao, khong nen tin mu):")
            for name, items in sorted(result['clusters'].items(), key=lambda kv: -len(kv[1])):
                print(f"  - {name}: {len(items)} trang")
    else:
        print(f"\nTIER1_CONFIDENT: tim duoc {len(result['clusters'])} nhom:")
        for name, items in sorted(result['clusters'].items(), key=lambda kv: -len(kv[1])):
            print(f"  - {name}: {len(items)} trang")
        if result['unclustered']:
            print(f"  - (chua ro, {len(result['unclustered'])} trang): can xem lai tay, vi du:")
            for e in result['unclustered'][:5]:
                print(f"      {e['file']}: {e['title']}")

    mapping = {}
    for name, items in result['clusters'].items():
        for e in items:
            mapping[e['file']] = name
    for e in result['unclustered']:
        mapping[e['file']] = 'UNCLASSIFIED'

    mapping_path = index_path.parent / 'surface_mapping.json'
    mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"\nDa ghi de xuat nhap vao {mapping_path} - xem lai va sua truoc khi chay --apply. "
          f"Bat buoc xoa het gia tri 'UNCLASSIFIED' truoc khi apply.")


def cmd_apply(args):
    index_path = Path(args.index)
    mapping = json.loads(Path(args.mapping).read_text(encoding='utf-8'))
    if 'UNCLASSIFIED' in mapping.values():
        print("Con file chua duoc phan loai (UNCLASSIFIED) trong mapping - "
              "sua xong roi chay lai --apply.", file=sys.stderr)
        sys.exit(1)

    entries = parse_index(index_path)
    concepts_dir = index_path.parent / 'concepts'
    comparison_files = set(args.comparison_files.split(',')) if args.comparison_files else set()

    tagged = 0
    for e in entries:
        platform = mapping.get(e['file'])
        if not platform:
            print(f"WARNING: {e['file']} khong co trong mapping, bo qua gan nhan", file=sys.stderr)
            continue
        path = concepts_dir / e['file']
        if not path.exists():
            print(f"WARNING: khong tim thay file {e['file']}", file=sys.stderr)
            continue
        text = path.read_text(encoding='utf-8')
        if not text.startswith('---\n'):
            continue
        end = text.index('\n---\n', 4)
        frontmatter = text[4:end].rstrip('\n')
        body = text[end + 5:]
        if 'platform:' in frontmatter:
            continue
        frontmatter += f"\nplatform: {platform}\n"
        path.write_text(f"---\n{frontmatter}---\n{body}", encoding='utf-8')
        tagged += 1

    by_platform = defaultdict(list)
    for e in entries:
        platform = mapping.get(e['file'], 'misc')
        by_platform[platform].append(e)

    out = ["# Master Index", ""]
    if comparison_files:
        out.append("## Trang doi chieu chinh thuc giua cac be mat (tra truoc tien)")
        out.append("")
        for e in entries:
            if e['file'] in comparison_files:
                out.append(f"- [{e['title']}](concepts/{e['file']}): {e['desc']}")
        out.append("")
    else:
        out.append("KHONG co trang doi chieu chinh thuc giua cac be mat trong tai lieu nguon. "
                    "Neu mot tinh nang chi thay nhac o mot be mat, KHONG duoc suy dien la be mat "
                    "khac cung co - phai tra loi ro la chi xac nhan cho be mat do, chua xac nhan cho be mat kia.")
        out.append("")

    other_platforms = sorted(p for p in by_platform if p not in comparison_files)
    for platform in other_platforms:
        items = [e for e in by_platform[platform] if e['file'] not in comparison_files]
        if not items:
            continue
        out.append(f"## {platform}")
        out.append("")
        for e in items:
            out.append(f"- [{e['title']}](concepts/{e['file']}): {e['desc']}")
        out.append("")

    index_path.write_text("\n".join(out).rstrip() + "\n", encoding='utf-8')
    print(f"Da gan nhan {tagged} file, sinh lai INDEX.md voi {len(other_platforms)} nhom "
          f"({'co' if comparison_files else 'khong co'} trang doi chieu chinh thuc).")


def main():
    parser = argparse.ArgumentParser(description="Detect and tag multi-surface docs mirrors.")
    parser.add_argument('--detect', action='store_true')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--index', required=True, help="Path to INDEX.md")
    parser.add_argument('--mapping', help="Path to surface_mapping.json (required for --apply)")
    parser.add_argument('--comparison-files', help="Comma-separated concept filenames that are official comparison pages")
    args = parser.parse_args()

    if args.detect:
        cmd_detect(args)
    elif args.apply:
        if not args.mapping:
            print("--apply can --mapping", file=sys.stderr)
            sys.exit(1)
        cmd_apply(args)
    else:
        print("Chon --detect hoac --apply", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
