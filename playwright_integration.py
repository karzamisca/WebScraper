import os
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright, Page

from conversion import convert_html_to_text
from file_handling import download_file, translate_text_file

async def process_urls(urls, html_path, pdf_path, txt_path, translated_txt_path, download_folder, headless_mode, skip_pdf, skip_text, skip_translation, skip_download, target_language):
    """Process each URL to save HTML, convert to PDF, extract links, and download files."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=headless_mode,
            args=[
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        page = await browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.73 Safari/537.36')
        
        for url in urls:
            try:
                await page.goto(url)  # Navigate to the URL
                html_content = await page.content()  # Get the HTML content

                base_filename = url.replace("https://", "").replace("http://", "").replace("/", "_")
                html_file_path = os.path.join(html_path, f'{base_filename}.html')
                pdf_file_path = os.path.join(pdf_path, f'{base_filename}.pdf') if not skip_pdf else None
                txt_file_path = os.path.join(txt_path, f'{base_filename}.txt') if not skip_text else None
                translated_txt_file_path = os.path.join(translated_txt_path, f'{base_filename}_translated.txt') if not skip_translation and translated_txt_path else None

                # Always process HTML
                with open(html_file_path, 'w', encoding='utf-8') as file:
                    file.write(html_content)  # Save HTML content

                if not skip_pdf and pdf_file_path:
                    await convert_html_to_pdf(page, html_content, pdf_file_path)  # Convert HTML to PDF
                    print(f"HTML converted to PDF successfully as '{pdf_file_path}'")

                if not skip_text and txt_file_path:
                    convert_html_to_text(html_file_path, txt_file_path)  # Convert HTML to Text
                    print(f"HTML converted to Text successfully as '{txt_file_path}'")

                if not skip_translation and translated_txt_file_path:
                    if txt_file_path:
                        await translate_text_file(txt_file_path, translated_txt_file_path, dest_lang=target_language)
                        print(f"Text translated successfully as '{translated_txt_file_path}'")

                if not skip_download:
                    external_links = await extract_links_from_html(page, url)
                    for link in external_links:
                        print(f"Following link: {link}")
                        if download_file(link, download_folder):
                            print(f"Downloaded file from: {link}")
                        else:
                            print(f"No downloadable file found or failed to download from: {link}")

            except Exception as e:
                print(f"An error occurred with URL {url}: {e}")

        await browser.close()

async def extract_links_from_html(page: Page, base_url):
    """Extract all valid links from HTML content using Playwright."""
    anchor_tags = await page.query_selector_all("a[href]")
    links = set()
    for tag in anchor_tags:
        href = await tag.get_attribute("href")
        if href and bool(urlparse(href).netloc):
            link = urljoin(base_url, href)  # Resolve relative URLs
            links.add(link)
    return links

async def convert_html_to_pdf(page: Page, html_content, output_file):
    """Convert HTML content to PDF using Playwright."""
    await page.set_content(html_content)  # Set the content of the page
    await page.pdf(path=output_file)  # Save the page as a PDF
