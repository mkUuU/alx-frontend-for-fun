#!/usr/bin/env python3

import sys
import os
import hashlib
import re

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def remove_character(text, char):
    return re.sub(f'[{char}]', '', text, flags=re.IGNORECASE)

def parse_markdown_to_html(md_content):
    html_content = []
    in_ulist = False
    in_olist = False
    in_paragraph = False

    for line in md_content.splitlines():
        stripped_line = line.strip()
        
        if stripped_line.startswith("#"):
            if in_ulist:
                html_content.append("</ul>")
                in_ulist = False
            if in_olist:
                html_content.append("</ol>")
                in_olist = False
            if in_paragraph:
                html_content.append("</p>")
                in_paragraph = False
            heading_level = len(stripped_line.split()[0])
            if 1 <= heading_level <= 6:
                heading_text = stripped_line[heading_level:].strip()
                html_content.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            else:
                html_content.append(line)
        elif stripped_line.startswith("-"):
            if in_olist:
                html_content.append("</ol>")
                in_olist = False
            if in_paragraph:
                html_content.append("</p>")
                in_paragraph = False
            if not in_ulist:
                html_content.append("<ul>")
                in_ulist = True
            list_item = stripped_line[1:].strip()
            html_content.append(f"<li>{list_item}</li>")
        elif stripped_line.startswith("*"):
            if in_ulist:
                html_content.append("</ul>")
                in_ulist = False
            if in_paragraph:
                html_content.append("</p>")
                in_paragraph = False
            if not in_olist:
                html_content.append("<ol>")
                in_olist = True
            list_item = stripped_line[1:].strip()
            html_content.append(f"<li>{list_item}</li>")
        else:
            if in_ulist:
                html_content.append("</ul>")
                in_ulist = False
            if in_olist:
                html_content.append("</ol>")
                in_olist = False
            if stripped_line == "":
                if in_paragraph:
                    html_content.append("</p>")
                    in_paragraph = False
            else:
                if not in_paragraph:
                    html_content.append("<p>")
                    in_paragraph = True

                # Process bold syntax
                stripped_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', stripped_line)
                stripped_line = re.sub(r'__(.*?)__', r'<em>\1</em>', stripped_line)
                stripped_line = re.sub(r'\[\[(.*?)\]\]', lambda m: md5_hash(m.group(1)), stripped_line)
                stripped_line = re.sub(r'\(\((.*?)\)\)', lambda m: remove_character(m.group(1), 'c'), stripped_line)
                
                html_content.append(stripped_line)

    if in_ulist:
        html_content.append("</ul>")
    if in_olist:
        html_content.append("</ol>")
    if in_paragraph:
        html_content.append("</p>")
    
    return "\n".join(html_content)

def main():
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    
    md_file = sys.argv[1]
    html_file = sys.argv[2]
    
    if not os.path.isfile(md_file):
        print(f"Missing {md_file}", file=sys.stderr)
        exit(1)
    
    with open(md_file, 'r') as f:
        md_content = f.read()
    
    html_content = parse_markdown_to_html(md_content)
    
    with open(html_file, 'w') as f:
        f.write(html_content)
    
    exit(0)

if __name__ == "__main__":
    main()
