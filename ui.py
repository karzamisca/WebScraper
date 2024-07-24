import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import asyncio
from conversion import convert_html_to_markdown, convert_markdown_to_txt, translate_text_file
from file_handling import read_urls_from_file
from playwright_integration import process_urls

# Global variables to store user selections
url_file_path = ''
html_output_path = ''
pdf_output_path = ''
md_output_path = ''
txt_output_path = ''
download_folder = ''
headless_mode = True
skip_pdf = False
skip_md = False
skip_download = False
skip_translation = False
translation_lang = 'en'

def select_url_file():
    global url_file_path
    url_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if url_file_path:
        lbl_url_file.config(text=f"Selected URL File: {url_file_path}")

def select_html_output_dir():
    global html_output_path
    html_output_path = filedialog.askdirectory()
    if html_output_path:
        lbl_html_dir.config(text=f"Selected HTML Output Directory: {html_output_path}")

def select_pdf_output_dir():
    global pdf_output_path
    pdf_output_path = filedialog.askdirectory()
    if pdf_output_path:
        lbl_pdf_dir.config(text=f"Selected PDF Output Directory: {pdf_output_path}")

def select_md_output_dir():
    global md_output_path
    md_output_path = filedialog.askdirectory()
    if md_output_path:
        lbl_md_dir.config(text=f"Selected Markdown Output Directory: {md_output_path}")

def select_txt_output_dir():
    global txt_output_path
    txt_output_path = filedialog.askdirectory()
    if txt_output_path:
        lbl_txt_dir.config(text=f"Selected Text Output Directory: {txt_output_path}")

def select_download_dir():
    global download_folder
    download_folder = filedialog.askdirectory()
    if download_folder:
        lbl_download_dir.config(text=f"Selected Download Directory: {download_folder}")

def toggle_headless_mode():
    global headless_mode
    headless_mode = not headless_mode

def toggle_skip_pdf():
    global skip_pdf
    skip_pdf = not skip_pdf

def toggle_skip_md():
    global skip_md
    skip_md = not skip_md

def toggle_skip_download():
    global skip_download
    skip_download = not skip_download

def toggle_skip_translation():
    global skip_translation
    skip_translation = not skip_translation

def update_translation_lang(event):
    global translation_lang
    translation_lang = lang_combobox.get()

async def start_processing():
    """Start processing URLs based on selected options and preferences."""
    if not url_file_path:
        messagebox.showerror("Error", "URL file is not selected.")
        return
    if not html_output_path:
        messagebox.showerror("Error", "HTML output directory is not selected.")
        return
    if not pdf_output_path and not skip_pdf:
        messagebox.showerror("Error", "PDF output directory is not selected.")
        return
    if not md_output_path and not skip_md:
        messagebox.showerror("Error", "Markdown output directory is not selected.")
        return
    if not txt_output_path and not skip_md:
        messagebox.showerror("Error", "Text output directory is not selected.")
        return
    if not download_folder and not skip_download:
        messagebox.showerror("Error", "Download directory is not selected.")
        return

    urls = read_urls_from_file(url_file_path)
    await process_urls(urls, html_output_path, pdf_output_path, md_output_path, txt_output_path, download_folder, headless_mode, skip_pdf, skip_md, skip_download)

    if not skip_md and not skip_translation:
        for file_name in os.listdir(md_output_path):
            if file_name.endswith('.md'):
                input_path = os.path.join(md_output_path, file_name)
                output_path = os.path.join(txt_output_path, file_name.replace('.md', '.txt'))
                translate_text_file(input_path, output_path, translation_lang)
    
    messagebox.showinfo("Info", "Processing complete!")

def setup_ui():
    root = tk.Tk()
    root.title("Web Scraper and Converter")

    # UI Elements for URL file selection
    btn_select_url_file = tk.Button(root, text="Select URL File", command=select_url_file)
    btn_select_url_file.pack(pady=5)

    global lbl_url_file
    lbl_url_file = tk.Label(root, text="No URL File Selected")
    lbl_url_file.pack(pady=5)

    # UI Elements for HTML output directory
    btn_select_html_dir = tk.Button(root, text="Select HTML Output Directory", command=select_html_output_dir)
    btn_select_html_dir.pack(pady=5)

    global lbl_html_dir
    lbl_html_dir = tk.Label(root, text="No HTML Output Directory Selected")
    lbl_html_dir.pack(pady=5)

    # UI Elements for PDF output directory
    btn_select_pdf_dir = tk.Button(root, text="Select PDF Output Directory", command=select_pdf_output_dir)
    btn_select_pdf_dir.pack(pady=5)

    global lbl_pdf_dir
    lbl_pdf_dir = tk.Label(root, text="No PDF Output Directory Selected")
    lbl_pdf_dir.pack(pady=5)

    # UI Elements for Markdown output directory
    btn_select_md_dir = tk.Button(root, text="Select Markdown Output Directory", command=select_md_output_dir)
    btn_select_md_dir.pack(pady=5)

    global lbl_md_dir
    lbl_md_dir = tk.Label(root, text="No Markdown Output Directory Selected")
    lbl_md_dir.pack(pady=5)

    # UI Elements for Text output directory
    btn_select_txt_dir = tk.Button(root, text="Select Text Output Directory", command=select_txt_output_dir)
    btn_select_txt_dir.pack(pady=5)

    global lbl_txt_dir
    lbl_txt_dir = tk.Label(root, text="No Text Output Directory Selected")
    lbl_txt_dir.pack(pady=5)

    # UI Elements for download directory
    btn_select_download_dir = tk.Button(root, text="Select Download Directory", command=select_download_dir)
    btn_select_download_dir.pack(pady=5)

    global lbl_download_dir
    lbl_download_dir = tk.Label(root, text="No Download Directory Selected")
    lbl_download_dir.pack(pady=5)

    # Checkbox for headless mode
    chk_headless = tk.Checkbutton(root, text="Headless Mode", variable=tk.BooleanVar(value=True), command=toggle_headless_mode)
    chk_headless.pack(pady=5)

    # Checkboxes for skipping functionality
    chk_skip_pdf = tk.Checkbutton(root, text="Skip PDF", variable=tk.BooleanVar(value=False), command=toggle_skip_pdf)
    chk_skip_pdf.pack(pady=5)

    chk_skip_md = tk.Checkbutton(root, text="Skip Markdown", variable=tk.BooleanVar(value=False), command=toggle_skip_md)
    chk_skip_md.pack(pady=5)

    chk_skip_download = tk.Checkbutton(root, text="Skip Download", variable=tk.BooleanVar(value=False), command=toggle_skip_download)
    chk_skip_download.pack(pady=5)

    chk_skip_translation = tk.Checkbutton(root, text="Skip Translation", variable=tk.BooleanVar(value=False), command=toggle_skip_translation)
    chk_skip_translation.pack(pady=5)

    # Dropdown for translation language
    global lang_combobox
    lang_combobox = ttk.Combobox(root, values=['en', 'es', 'fr', 'de', 'zh-cn', 'vi'], state='normal')
    lang_combobox.set('en')  # Default language
    lang_combobox.bind('<<ComboboxSelected>>', update_translation_lang)
    lang_combobox.pack(pady=5)

    # Start processing button
    btn_start_processing = tk.Button(root, text="Start Processing", command=lambda: asyncio.run(start_processing()))
    btn_start_processing.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()
