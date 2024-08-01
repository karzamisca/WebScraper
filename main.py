import asyncio
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from googletrans import Translator

translator = Translator()

async def scrape_url(export_html, export_pdf, export_text, export_original_text, url, export_path, target_lang):
    async with async_playwright() as p:
        # Launch the browser with the specified arguments and user agent
        browser = await p.chromium.launch(
            headless=False,
            args=[
                '--disable-dev-shm-usage',
                '--no-sandbox'
            ]
        )
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.73 Safari/537.36'
        )
        
        page = await context.new_page()
        await page.goto(url.strip())

        # Generate a safe file name based on the URL
        parsed_url = urlparse(url)
        safe_name = parsed_url.netloc.replace('.', '_') + parsed_url.path.replace('/', '_')
        if not safe_name:
            safe_name = 'index'

        # Export HTML if selected
        if export_html:
            html_content = await page.content()
            with open(f'{export_path}/{safe_name}.html', 'w', encoding='utf-8') as html_file:
                html_file.write(html_content)
            print(f'HTML content saved to {export_path}/{safe_name}.html')

        # Export PDF if selected
        if export_pdf:
            await page.pdf(path=f'{export_path}/{safe_name}.pdf', format='A4')
            print(f'PDF saved to {export_path}/{safe_name}.pdf')

        # Export text if selected
        if export_text or export_original_text:
            text_content = await page.inner_text('body')

            # Export original text if selected
            if export_original_text:
                with open(f'{export_path}/{safe_name}_original.txt', 'w', encoding='utf-8') as text_file:
                    text_file.write(text_content)
                print(f'Original text content saved to {export_path}/{safe_name}_original.txt')

            # Export translated text if selected
            if export_text:
                translated_text = translator.translate(text_content, dest=target_lang).text
                with open(f'{export_path}/{safe_name}.txt', 'w', encoding='utf-8') as text_file:
                    text_file.write(translated_text)
                print(f'Translated text content saved to {export_path}/{safe_name}.txt')

        # Close the browser
        await browser.close()

async def scrape(export_html, export_pdf, export_text, export_original_text, urls, export_path, target_lang):
    tasks = []
    for url in urls:
        tasks.append(scrape_url(export_html, export_pdf, export_text, export_original_text, url, export_path, target_lang))
    await asyncio.gather(*tasks)

def choose_url_file():
    file_path = filedialog.askopenfilename(title="Select URL Text File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if file_path:
        url_file_entry.delete(0, tk.END)
        url_file_entry.insert(0, file_path)

def choose_export_path():
    directory = filedialog.askdirectory(title="Select Export Directory")
    if directory:
        export_path_entry.delete(0, tk.END)
        export_path_entry.insert(0, directory)

def start_scraping():
    export_html = html_var.get()
    export_pdf = pdf_var.get()
    export_text = text_var.get()
    export_original_text = original_text_var.get()
    file_path = url_file_entry.get()
    export_path = export_path_entry.get()
    target_lang = language_var.get()

    # Check if no export option is selected
    if not (export_html or export_pdf or export_text or export_original_text):
        messagebox.showwarning("Warning", "Please select at least one export option.")
        return

    if file_path and export_path and target_lang:
        with open(file_path, 'r') as file:
            urls = file.readlines()
        asyncio.run(scrape(export_html, export_pdf, export_text, export_original_text, urls, export_path, target_lang))

# Create the main window
root = tk.Tk()
root.title("Web Scraper Options")

# Create and place the checkboxes
html_var = tk.BooleanVar()
pdf_var = tk.BooleanVar()
text_var = tk.BooleanVar()
original_text_var = tk.BooleanVar()

html_check = ttk.Checkbutton(root, text="Export HTML", variable=html_var)
pdf_check = ttk.Checkbutton(root, text="Export PDF", variable=pdf_var)
text_check = ttk.Checkbutton(root, text="Export Translated Text", variable=text_var)
original_text_check = ttk.Checkbutton(root, text="Export Original Text", variable=original_text_var)

html_check.grid(column=0, row=0, padx=10, pady=10)
pdf_check.grid(column=1, row=0, padx=10, pady=10)
text_check.grid(column=2, row=0, padx=10, pady=10)
original_text_check.grid(column=3, row=0, padx=10, pady=10)

# Create and place the URL file selection
url_file_label = ttk.Label(root, text="URL Text File:")
url_file_label.grid(column=0, row=1, padx=10, pady=10)
url_file_entry = ttk.Entry(root, width=40)
url_file_entry.grid(column=1, row=1, padx=10, pady=10)
url_file_button = ttk.Button(root, text="Browse...", command=choose_url_file)
url_file_button.grid(column=2, row=1, padx=10, pady=10)

# Create and place the export path selection
export_path_label = ttk.Label(root, text="Export Directory:")
export_path_label.grid(column=0, row=2, padx=10, pady=10)
export_path_entry = ttk.Entry(root, width=40)
export_path_entry.grid(column=1, row=2, padx=10, pady=10)
export_path_button = ttk.Button(root, text="Browse...", command=choose_export_path)
export_path_button.grid(column=2, row=2, padx=10, pady=10)

# Create and place the language dropdown menu
language_label = ttk.Label(root, text="Target Language:")
language_label.grid(column=0, row=3, padx=10, pady=10)
language_var = tk.StringVar()
language_dropdown = ttk.Combobox(root, textvariable=language_var)
language_dropdown['values'] = ['en', 'vi', 'es', 'fr', 'de', 'zh-cn', 'ja', 'ko', 'ru']  # Add more languages as needed
language_dropdown.grid(column=1, row=3, padx=10, pady=10)
language_dropdown.current(0)  # Set the default value to English

# Create and place the start button
start_button = ttk.Button(root, text="Start Scraping", command=start_scraping)
start_button.grid(column=0, row=4, columnspan=4, pady=10)

# Run the Tkinter event loop
root.mainloop()
