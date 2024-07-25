import tkinter as tk
from tkinter import filedialog, messagebox
import asyncio
from file_handling import read_urls_from_file
from playwright_integration import process_urls

# Global variables
url_file_path = None
html_output_path = None
pdf_output_path = None
txt_output_path = None
translated_txt_path = None
download_folder = None
headless_mode = True
skip_pdf = False
skip_text = False
skip_translation = False
skip_download = False
target_language = 'en'  # Default language

def select_url_file():
    global url_file_path
    url_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    lbl_url_file.config(text=url_file_path)

def select_html_output_dir():
    global html_output_path
    html_output_path = filedialog.askdirectory()
    lbl_html_dir.config(text=html_output_path)

def select_pdf_output_dir():
    global pdf_output_path
    pdf_output_path = filedialog.askdirectory()
    lbl_pdf_dir.config(text=pdf_output_path)

def select_txt_output_dir():
    global txt_output_path
    txt_output_path = filedialog.askdirectory()
    lbl_txt_dir.config(text=txt_output_path)

def select_translated_txt_output_dir():
    global translated_txt_path
    translated_txt_path = filedialog.askdirectory()
    lbl_translated_txt_dir.config(text=translated_txt_path)

def select_download_dir():
    global download_folder
    download_folder = filedialog.askdirectory()
    lbl_download_dir.config(text=download_folder)

def toggle_headless_mode():
    global headless_mode
    headless_mode = not headless_mode

def toggle_skip_pdf():
    global skip_pdf
    skip_pdf = not skip_pdf

def toggle_skip_text():
    global skip_text
    skip_text = not skip_text

def toggle_skip_translation():
    global skip_translation
    skip_translation = not skip_translation

def toggle_skip_download():
    global skip_download
    skip_download = not skip_download

def update_target_language(*args):
    global target_language
    target_language = language_var.get()

async def start_processing():
    if not url_file_path:
        messagebox.showerror("Error", "URL file is not selected.")
        return
    if not html_output_path:
        messagebox.showerror("Error", "HTML output directory is not selected.")
        return
    if not txt_output_path and not skip_text:
        messagebox.showerror("Error", "Text output directory is not selected.")
        return
    if not translated_txt_path and not skip_translation:
        messagebox.showerror("Error", "Translated Text output directory is not selected.")
        return
    if not download_folder and not skip_download:
        messagebox.showerror("Error", "Download directory is not selected.")
        return

    urls = read_urls_from_file(url_file_path)
    
    await process_urls(
        urls,
        html_output_path,
        pdf_output_path,
        txt_output_path,
        translated_txt_path,
        download_folder,
        headless_mode,
        skip_pdf,
        skip_text,
        skip_translation,
        skip_download,
        target_language
    )

    messagebox.showinfo("Success", "Processing completed.")

def setup_ui():
    """Setup the Tkinter UI for user input and processing."""
    global lbl_url_file, lbl_html_dir, lbl_pdf_dir, lbl_txt_dir, lbl_translated_txt_dir, lbl_download_dir
    global language_var

    root = tk.Tk()
    root.title("Web Scraper and Converter")

    # URL file
    tk.Button(root, text="Select URL File", command=select_url_file).pack()
    lbl_url_file = tk.Label(root, text="No URL File Selected")
    lbl_url_file.pack()

    # HTML output directory
    tk.Button(root, text="Select HTML Output Directory", command=select_html_output_dir).pack()
    lbl_html_dir = tk.Label(root, text="No HTML Output Directory Selected")
    lbl_html_dir.pack()

    # PDF output directory
    tk.Button(root, text="Select PDF Output Directory", command=select_pdf_output_dir).pack()
    lbl_pdf_dir = tk.Label(root, text="No PDF Output Directory Selected")
    lbl_pdf_dir.pack()

    # Text output directory
    tk.Button(root, text="Select Text Output Directory", command=select_txt_output_dir).pack()
    lbl_txt_dir = tk.Label(root, text="No Text Output Directory Selected")
    lbl_txt_dir.pack()

    # Translated Text output directory
    tk.Button(root, text="Select Translated Text Output Directory", command=select_translated_txt_output_dir).pack()
    lbl_translated_txt_dir = tk.Label(root, text="No Translated Text Output Directory Selected")
    lbl_translated_txt_dir.pack()

    # Download directory
    tk.Button(root, text="Select Download Directory", command=select_download_dir).pack()
    lbl_download_dir = tk.Label(root, text="No Download Directory Selected")
    lbl_download_dir.pack()

    # Options
    tk.Checkbutton(root, text="Headless Mode", variable=tk.BooleanVar(value=headless_mode), command=toggle_headless_mode).pack()
    tk.Checkbutton(root, text="Skip PDF", variable=tk.BooleanVar(value=skip_pdf), command=toggle_skip_pdf).pack()
    tk.Checkbutton(root, text="Skip Translation", variable=tk.BooleanVar(value=skip_translation), command=toggle_skip_translation).pack()
    tk.Checkbutton(root, text="Skip Download", variable=tk.BooleanVar(value=skip_download), command=toggle_skip_download).pack()

    # Language selection
    language_var = tk.StringVar(value='en')
    tk.Label(root, text="Select Target Language:").pack()
    language_options = ['en', 'vi', 'es', 'fr', 'de', 'zh-cn', 'ja', 'ko', 'ru', 'ar']
    language_menu = tk.OptionMenu(root, language_var, *language_options, command=update_target_language)
    language_menu.pack()

    # Start processing
    tk.Button(root, text="Start Processing", command=lambda: asyncio.run(start_processing())).pack()

    root.mainloop()
