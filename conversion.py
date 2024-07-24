import html2text
import markdown
from googletrans import Translator

def translate_text_file(input_path, output_path, dest_lang='en'):
    """Translate the content of a text file to the specified language and save to a new file."""
    translator = Translator()
    
    # Read the content of the input text file
    with open(input_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Translate the content
    translated = translator.translate(text, dest=dest_lang).text
    
    # Save the translated content to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated)

    print(f"Translated text saved to: {output_path}")

def convert_html_to_markdown(source_html, output_file):
    """Convert HTML file to Markdown file using html2text."""
    html_to_markdown = html2text.HTML2Text()
    html_to_markdown.ignore_links = False
    with open(source_html, 'r', encoding='utf-8') as file:
        html_content = file.read()  # Read HTML content
    markdown_content = html_to_markdown.handle(html_content)  # Convert HTML to Markdown
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(markdown_content)  # Save Markdown content to file

def convert_markdown_to_txt(source_md, output_file):
    """Convert Markdown file to plain text file using markdown library."""
    with open(source_md, 'r', encoding='utf-8') as file:
        md_content = file.read()  # Read Markdown content
    html_content = markdown.markdown(md_content)  # Convert Markdown to HTML
    text_content = html2text.html2text(html_content)  # Convert HTML to plain text
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(text_content)  # Save plain text content to file
