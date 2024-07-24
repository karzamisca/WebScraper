import tkinter as tk
from tkinter import filedialog, messagebox
import asyncio
from file_handling import read_urls_from_file
from playwright_integration import process_urls

# Global variables to store selected paths, mode, and preferences
url_file_path = ""
html_output_path = ""
pdf_output_path = ""
md_output_path = ""
txt_output_path = ""
download_folder = ""
headless_mode = True
skip_pdf = False
skip_md = False
skip_download = False

def select_url_file():
    """Open file dialog to select the URL file."""
    global url_file_path
    url_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if url_file_path:
        lbl_url_file.config(text=f"Selected URL File: {url_file_path}")

def select_html_output_dir():
    """Open directory dialog to select the HTML output directory."""
    global html_output_path
    html_output_path = filedialog.askdirectory()
    if html_output_path:
        lbl_html_dir.config(text=f"Selected HTML Output Directory: {html_output_path}")

def select_pdf_output_dir():
    """Open directory dialog to select the PDF output directory."""
    global pdf_output_path
    pdf_output_path = filedialog.askdirectory()
    if pdf_output_path:
        lbl_pdf_dir.config(text=f"Selected PDF Output Directory: {pdf_output_path}")

def select_md_output_dir():
    """Open directory dialog to select the Markdown output directory."""
    global md_output_path
    md_output_path = filedialog.askdirectory()
    if md_output_path:
        lbl_md_dir.config(text=f"Selected Markdown Output Directory: {md_output_path}")

def select_txt_output_dir():
    """Open directory dialog to select the Text output directory."""
    global txt_output_path
    txt_output_path = filedialog.askdirectory()
    if txt_output_path:
        lbl_txt_dir.config(text=f"Selected Text Output Directory: {txt_output_path}")

def select_download_dir():
    """Open directory dialog to select the file download directory."""
    global download_folder
    download_folder = filedialog.askdirectory()
    if download_folder:
        lbl_download_dir.config(text=f"Selected Download Directory: {download_folder}")

def toggle_headless_mode():
    """Toggle headless mode based on checkbox."""
    global headless_mode
    headless_mode = not headless_mode

def toggle_skip_pdf():
    """Toggle skip PDF processing based on checkbox."""
    global skip_pdf
    skip_pdf = not skip_pdf

def toggle_skip_md():
    """Toggle skip Markdown processing based on checkbox."""
    global skip_md
    skip_md = not skip_md

def toggle_skip_download():
    """Toggle skip download processing based on checkbox."""
    global skip_download
    skip_download = not skip_download

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
    messagebox.showinfo("Info", "Processing complete!")

# Set up the Tkinter UI
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

    # Start processing button
    btn_start_processing = tk.Button(root, text="Start Processing", command=lambda: asyncio.run(start_processing()))
    btn_start_processing.pack(pady=20)

    # Start the Tkinter event loop
    root.mainloop()
