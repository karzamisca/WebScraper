from markdown2 import markdown
from html2text import html2text

def convert_html_to_markdown(html_file, md_file):
    """Convert HTML file to Markdown file."""
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    markdown_content = markdown(html_content)
    with open(md_file, 'w', encoding='utf-8') as file:
        file.write(markdown_content)

def convert_markdown_to_txt(md_file, txt_file):
    """Convert Markdown file to plain text file."""
    with open(md_file, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    text_content = markdown(markdown_content)
    with open(txt_file, 'w', encoding='utf-8') as file:
        file.write(text_content)

def convert_html_to_text(html_file_path, txt_file_path):
    """Convert HTML file to a plain text file."""
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    
    text_content = html2text(html_content)
    
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

    print(f"Converted HTML to Text successfully as '{txt_file_path}'")
