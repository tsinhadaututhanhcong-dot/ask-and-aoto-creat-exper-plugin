import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

DOC_EXTS = {'.md', '.mdx', '.txt', '.rst'}
CODE_EXTS = {'.py', '.ts', '.js', '.json'}
TOOL_HINT_RE = re.compile(r'(tool|schema|mcp|server)', re.IGNORECASE)
SKIP_DIR_NAMES = {'node_modules', 'dist', 'build', '__pycache__', 'venv', '.venv', 'test', 'tests', '.github'}
MAX_FILE_SIZE = 60_000


def slugify(relpath):
    slug = relpath.strip('/').replace('/', '-')
    slug = re.sub(r'[^a-zA-Z0-9\-\.]', '', slug)
    return slug


def clone_repo(repo_url, dest):
    subprocess.run(
        ['git', 'clone', '--depth', '1', repo_url, dest],
        check=True, capture_output=True, text=True, timeout=120,
    )
    branch = subprocess.run(
        ['git', '-C', dest, 'branch', '--show-current'],
        check=True, capture_output=True, text=True, timeout=10,
    ).stdout.strip() or 'main'
    return branch


def collect_candidates(tmp_dir, max_files):
    candidates = []
    for root, dirs, files in os.walk(tmp_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not d.startswith('.')]
        rel_root = os.path.relpath(root, tmp_dir)
        for fname in files:
            fpath = os.path.join(root, fname)
            relpath = fname if rel_root == '.' else os.path.normpath(os.path.join(rel_root, fname))
            relpath = relpath.replace('\\', '/')
            ext = os.path.splitext(fname)[1].lower()

            is_readme_root = rel_root == '.' and fname.lower().startswith('readme')
            is_under_docs = relpath.lower().startswith('docs/')
            is_tool_hint = ext in CODE_EXTS.union(DOC_EXTS) and TOOL_HINT_RE.search(fname)

            if not (is_readme_root or is_under_docs or is_tool_hint):
                continue
            try:
                size = os.path.getsize(fpath)
            except OSError:
                continue
            if size == 0 or size > MAX_FILE_SIZE:
                continue
            candidates.append((relpath, fpath, ext))
            if len(candidates) >= max_files:
                return candidates
    return candidates


def main():
    parser = argparse.ArgumentParser(
        description="Ingest README + docs/ + tool-definition-hinted files from a GitHub repo "
                    "into an existing expert skill's references/concepts/ directory."
    )
    parser.add_argument('--repo', required=True, help="GitHub repo URL")
    parser.add_argument('--output', required=True, help="Path to the expert's references/ directory")
    parser.add_argument('--max-files', type=int, default=30, help="Max files to ingest (default 30)")
    args = parser.parse_args()

    concepts_dir = os.path.join(args.output, 'concepts')
    os.makedirs(concepts_dir, exist_ok=True)

    tmp_dir = tempfile.mkdtemp(prefix='repo-docs-')
    try:
        try:
            branch = clone_repo(args.repo, tmp_dir)
        except subprocess.CalledProcessError as e:
            sys.stderr.write(f"Clone failed: {e.stderr}\n")
            sys.exit(1)

        candidates = collect_candidates(tmp_dir, args.max_files)
        if not candidates:
            print("No README/docs/tool-hint files found under the size cap.")
            return

        repo_url = args.repo[:-4] if args.repo.endswith('.git') else args.repo
        written = []
        for relpath, fpath, ext in candidates:
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except OSError:
                continue

            outname = 'repo-' + slugify(relpath)
            if not outname.endswith('.md'):
                outname += '.md'
            outpath = os.path.join(concepts_dir, outname)

            with open(outpath, 'w', encoding='utf-8') as out:
                out.write(f"# {relpath} (repo source)\n")
                out.write(f"**Source:** {repo_url}/blob/{branch}/{relpath}\n\n")
                if ext in DOC_EXTS:
                    out.write(content)
                else:
                    out.write(f"```{ext.lstrip('.')}\n{content}\n```\n")
            written.append((relpath, outname))

        print(f"Repo ingest done: {len(written)} file(s) from {repo_url} (branch: {branch})")
        for relpath, outname in written:
            print(f"  {relpath} -> concepts/{outname}")
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
