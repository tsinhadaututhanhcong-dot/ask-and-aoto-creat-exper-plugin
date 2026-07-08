import os
import re
import argparse
from datetime import datetime

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = re.sub(r'^-+|-+$', '', text)
    return text

def parse_and_split(input_file, output_dir):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by level-1 headings
    # The regex looks for lines starting with exactly one '#' followed by space
    sections = re.split(r'\n(?=#\s+)', '\n' + content)
    
    concepts_dir = os.path.join(output_dir, 'concepts')
    os.makedirs(concepts_dir, exist_ok=True)
    
    index_entries = []
    created_count = 0
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Extract title
        match = re.match(r'^#\s+(.+)$', section, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            slug = slugify(title)
            
            if not slug:
                continue
                
            filename = f"{slug}.md"
            filepath = os.path.join(concepts_dir, filename)
            
            # Prepare metadata (Karpathy style)
            metadata = f"---\ntitle: {title}\ndate_created: {datetime.now().strftime('%Y-%m-%d')}\ntags: [concept, auto-generated]\n---\n\n"
            
            # Write concept file
            with open(filepath, 'w', encoding='utf-8') as cf:
                cf.write(metadata + section)
                
            index_entries.append(f"- [{title}](concepts/{filename})")
            created_count += 1
            
    # Write index.md
    index_path = os.path.join(output_dir, 'index.md')
    with open(index_path, 'w', encoding='utf-8') as idxf:
        idxf.write("# Master Index\n\n")
        idxf.write("This index was automatically generated from the monolithic document.\n\n")
        idxf.write("## Concepts\n\n")
        idxf.write("\n".join(index_entries))
        
    print(f"Success! Created {created_count} concept files and index.md in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split a monolithic markdown file into a Karpathy LLM Wiki structure.')
    parser.add_argument('--input', '-i', required=True, help='Path to the input markdown file')
    parser.add_argument('--output', '-o', required=True, help='Path to the output wiki directory')
    
    args = parser.parse_args()
    parse_and_split(args.input, args.output)

