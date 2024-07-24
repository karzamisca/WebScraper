import os
import requests
from urllib.parse import urlparse, urljoin

def read_urls_from_file(file_path):
    """Read URLs from a text file, one per line."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def download_file(url, download_folder):
    """Download file from a URL if it's a supported type."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        content_type = response.headers.get('content-type')

        # Determine file extension based on content type
        file_extension = determine_file_extension(content_type, url)
        if not file_extension:
            return False  # Unsupported file type

        file_name = os.path.join(download_folder, os.path.basename(urlparse(url).path) + file_extension)

        with open(file_name, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)  # Write file content in chunks
        
        return True

    except requests.exceptions.RequestException as e:
        print(f"Failed to download file from {url}: {e}")
        return False

def determine_file_extension(content_type, url):
    """Determine the file extension based on content type."""
    if 'application/pdf' in content_type:
        return '.pdf'
    elif 'application/epub+zip' in content_type:
        return '.epub'
    elif 'application/x-mobipocket-ebook' in content_type:
        return '.mobi'
    elif 'application/vnd.amazon.ebook' in content_type:
        return '.azw'
    elif 'application/vnd.ms-htmlhelp' in content_type:
        return '.chm'
    elif 'application/octet-stream' in content_type:
        if url.endswith('.azw3'):
            return '.azw3'
        elif url.endswith('.kf8'):
            return '.kf8'
        elif url.endswith('.lit'):
            return '.lit'
        elif url.endswith('.prc'):
            return '.prc'
        elif url.endswith('.ibooks'):
            return '.ibooks'
    return None
