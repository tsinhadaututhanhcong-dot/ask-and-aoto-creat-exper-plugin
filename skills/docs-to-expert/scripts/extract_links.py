import argparse
import urllib.request
import urllib.parse
import re
from collections import deque
import sys
import json
import os

try:
    import warnings
    from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
    warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)
    from markdownify import markdownify as md
except ImportError:
    BeautifulSoup = None
    md = None

def extract_links(start_url, max_pages):
    visited = set()
    html_visited = set()
    queue = deque([start_url])
    pages_scanned = 0
    
    ignore_exts = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip', '.mp4', '.mp3')

    while queue and pages_scanned < max_pages:
        url = queue.popleft()
        # Remove fragment identifier
        url = url.split('#')[0]
        
        if url in visited or url.lower().split('?')[0].endswith(ignore_exts):
            continue
        visited.add(url)
        pages_scanned += 1
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=10)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
            html = response.read().decode('utf-8')
            html_visited.add(url)
        except Exception as e:
            # Silently ignore fetching errors like 404s to avoid console spam
            continue
            
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
        for link in links:
            absolute_link = urllib.parse.urljoin(url, link)
            absolute_link = absolute_link.split('#')[0]
            
            # Only crawl within the given start_url domain and path
            if absolute_link.startswith(start_url) and absolute_link not in visited and absolute_link not in queue:
                queue.append(absolute_link)

    return sorted(html_visited)

def main():
    parser = argparse.ArgumentParser(description="Extract all links recursively from a given starting docs URL.")
    parser.add_argument('--url', required=True, help="The starting URL to crawl.")
    parser.add_argument('--output', required=True, help="Output file path (.txt or .json)")
    parser.add_argument('--export-md', help="Path to save the extracted content of all crawled links as a single Markdown file.")
    parser.add_argument('--export-dir', help="Path to a directory to save each crawled link as a separate Markdown file and generate a Knowledge Graph.")
    parser.add_argument('--max-pages', type=int, default=1000, help="Maximum number of pages to scan (default 1000)")
    
    args = parser.parse_args()
    
    sys.stderr.write(f"Starting crawl from {args.url} (max {args.max_pages} pages)...\n")
    links = extract_links(args.url, args.max_pages)
    
    if args.output.endswith('.json'):
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump({"start_url": args.url, "total_links": len(links), "links": links}, f, indent=2)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            for l in links:
                f.write(l + '\n')
                
    print(f"Success! Found {len(links)} links. Data written to: {args.output}")

    if args.export_md:
        if not BeautifulSoup or not md:
            sys.stderr.write("Error: beautifulsoup4 and markdownify are required for --export-md.\n")
        else:
            sys.stderr.write(f"Exporting content to {args.export_md}...\n")
            with open(args.export_md, 'w', encoding='utf-8') as md_file:
                for link in links:
                    try:
                        req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                        response = urllib.request.urlopen(req, timeout=10)
                        html = response.read().decode('utf-8')
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        title = soup.title.string.strip() if soup.title and soup.title.string else link
                        md_file.write(f"# {title}\n")
                        md_file.write(f"**Source:** [{link}]({link})\n\n")
                        
                        content = soup.find('main') or soup.find('article') or soup.find('div', role='main') or soup.find('body')
                        if content:
                            for elem in content(['script', 'style', 'nav', 'header', 'footer']):
                                elem.extract()
                            markdown_content = md(str(content), heading_style="ATX")
                            md_file.write(markdown_content)
                            md_file.write("\n\n---\n\n")
                    except Exception as e:
                        # sys.stderr.write(f"Error extracting content from {link}: {e}\n")
                        pass
            print(f"Success! Markdown content exported to: {args.export_md}")

    if args.export_dir:
        if not BeautifulSoup or not md:
            sys.stderr.write("Error: beautifulsoup4 and markdownify are required for --export-dir.\n")
        else:
            os.makedirs(args.export_dir, exist_ok=True)
            sys.stderr.write(f"Exporting individual files and building Knowledge Graph to {args.export_dir}...\n")
            
            url_to_data = {}
            url_to_title = {}
            
            for link in links:
                try:
                    req = urllib.request.Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urllib.request.urlopen(req, timeout=10)
                    html = response.read().decode('utf-8')
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    title = soup.title.string.strip() if soup.title and soup.title.string else link
                    url_to_title[link] = title
                    
                    parsed_url = urllib.parse.urlparse(link)
                    path = parsed_url.path.strip('/')
                    if not path:
                        slug = "index"
                    else:
                        slug = path.replace('/', '-')
                        slug = re.sub(r'[^a-zA-Z0-9\-]', '', slug)
                    
                    filename = f"{slug}.md"
                    
                    content = soup.find('main') or soup.find('article') or soup.find('div', role='main') or soup.find('body')
                    internal_links = []
                    
                    if content:
                        for elem in content(['script', 'style', 'nav', 'header', 'footer']):
                            elem.extract()
                            
                        for a in content.find_all('a', href=True):
                            href = a['href']
                            abs_href = urllib.parse.urljoin(link, href).split('#')[0]
                            if abs_href in links and abs_href != link:
                                internal_links.append(abs_href)
                                
                        markdown_content = md(str(content), heading_style="ATX")
                    else:
                        markdown_content = ""
                    
                    filepath = os.path.join(args.export_dir, filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"# {title}\n")
                        f.write(f"**Source:** [{link}]({link})\n\n")
                        f.write(markdown_content)
                        
                        if internal_links:
                            f.write("\n\n## Related Files\n")
                            f.write("> **LLM Navigation:** Các tệp dưới đây được liên kết trực tiếp từ tài liệu này. Hãy đọc chúng nếu cần thêm ngữ cảnh.\n\n")
                            unique_links = sorted(list(set(internal_links)))
                            for target_link in unique_links:
                                target_parsed = urllib.parse.urlparse(target_link)
                                target_path = target_parsed.path.strip('/')
                                if not target_path:
                                    target_slug = "index"
                                else:
                                    target_slug = target_path.replace('/', '-')
                                    target_slug = re.sub(r'[^a-zA-Z0-9\-]', '', target_slug)
                                target_filename = f"{target_slug}.md"
                                f.write(f"- [{target_link}](./{target_filename})\n")
                        
                    url_to_data[link] = {'filename': filename, 'internal_links': list(set(internal_links))}
                except Exception as e:
                    # sys.stderr.write(f"Error extracting content from {link}: {e}\n")
                    pass
            
            kg_path = os.path.join(args.export_dir, 'knowledge_graph.md')
            with open(kg_path, 'w', encoding='utf-8') as kg:
                kg.write("# Knowledge Graph\n\n")
                kg.write("## Table of Contents\n\n")
                for link in links:
                    if link in url_to_data:
                        data = url_to_data[link]
                        title = url_to_title.get(link, data['filename'])
                        kg.write(f"- [{title}](./{data['filename']})\n")
                
                kg.write("\n## Graph\n\n")
                kg.write("```mermaid\n")
                kg.write("graph TD;\n")
                
                link_to_id = {l: f"node{i}" for i, l in enumerate(links) if l in url_to_data}
                
                for link in links:
                    if link in url_to_data:
                        data = url_to_data[link]
                        node_id = link_to_id[link]
                        # Remove quotes that break mermaid syntax
                        safe_title = url_to_title.get(link, data['filename']).replace('"', "'").replace('[', '(').replace(']', ')')
                        kg.write(f"    {node_id}[\"{safe_title}\"];\n")
                        
                        for target in data['internal_links']:
                            if target in link_to_id:
                                kg.write(f"    {node_id} --> {link_to_id[target]};\n")
                
                kg.write("```\n")
            print(f"Success! Knowledge Graph and Markdown files exported to: {args.export_dir}")

if __name__ == "__main__":
    main()
