from urllib.parse import urlparse
from googletrans import Translator
import os
import re
import requests

def read_urls_from_file(file_path):
    """Read URLs from a text file."""
    with open(file_path, 'r') as file:
        urls = [line.strip() for line in file if line.strip()]
    return urls

def download_file(url, download_folder):
    """Download files from the given URL."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        content_type = response.headers.get('content-type')

        if 'application/pdf' in content_type:
            file_extension = '.pdf'
        elif 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' in content_type:
            file_extension = '.docx'
        elif 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' in content_type:
            file_extension = '.xlsx'
        elif 'application/epub+zip' in content_type:
            file_extension = '.epub'
        elif 'application/x-mobipocket-ebook' in content_type:
            file_extension = '.mobi'
        elif 'application/x-fictionbook+xml' in content_type:
            file_extension = '.fb2'
        elif 'application/x-tpf' in content_type:
            file_extension = '.tpf'
        else:
            return False

        file_name = os.path.join(download_folder, os.path.basename(urlparse(url).path) + file_extension)

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file from {url}: {e}")
        return False

def clean_text(text):
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove special characters and URLs
    text = re.sub(r'http\S+|www\.\S+|\[.*?\]|\(.*?\)|\{.*?\}|\!.*?\)', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text


async def translate_text_file(input_file_path, output_file_path, src_lang='auto', dest_lang='en'):
    """Translate text file content using Google Translate."""
    translator = Translator()

    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        text = input_file.read()

    # Clean the text
    cleaned_text = clean_text(text)
    
    translated_text = translator.translate(cleaned_text, src=src_lang, dest=dest_lang).text
    
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(translated_text)
        
    print(f"Translation complete. Output saved to {output_file}")

