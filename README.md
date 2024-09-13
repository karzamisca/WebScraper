## Web Scraper with Playwright and Google Translate

## WARNING: Use sites with https only

### Classes and Functions

#### Functions

1. **`scrape_url(export_html, export_pdf, export_text, export_original_text, url, export_path, target_lang)`**
   - **Purpose**: Scrapes a single URL and exports the content based on selected options.
   - **Parameters**:
     - `export_html`: Boolean to determine if HTML should be exported.
     - `export_pdf`: Boolean to determine if PDF should be exported.
     - `export_text`: Boolean to determine if translated text should be exported.
     - `export_original_text`: Boolean to determine if original text should be exported.
     - `url`: The URL to scrape.
     - `export_path`: Path where the exported files will be saved.
     - `target_lang`: Target language code for text translation.

2. **`scrape(export_html, export_pdf, export_text, export_original_text, urls, export_path, target_lang)`**
   - **Purpose**: Manages the scraping of multiple URLs concurrently.
   - **Parameters**:
     - `export_html`: Boolean to determine if HTML should be exported.
     - `export_pdf`: Boolean to determine if PDF should be exported.
     - `export_text`: Boolean to determine if translated text should be exported.
     - `export_original_text`: Boolean to determine if original text should be exported.
     - `urls`: List of URLs to scrape.
     - `export_path`: Path where the exported files will be saved.
     - `target_lang`: Target language code for text translation.

3. **`choose_url_file()`**
   - **Purpose**: Opens a file dialog to select a text file containing URLs.
   - **Parameters**: None (uses Tkinter file dialog).

4. **`choose_export_path()`**
   - **Purpose**: Opens a directory dialog to select the export directory.
   - **Parameters**: None (uses Tkinter directory dialog).

5. **`start_scraping()`**
   - **Purpose**: Initiates the scraping process based on user input from the GUI.
   - **Parameters**: None (uses values from Tkinter GUI elements).

#### Main GUI Elements

- **`root`**: The main Tkinter window for the GUI.
- **`html_var`**: Boolean variable for the HTML export option.
- **`pdf_var`**: Boolean variable for the PDF export option.
- **`text_var`**: Boolean variable for the translated text export option.
- **`original_text_var`**: Boolean variable for the original text export option.
- **`url_file_entry`**: Entry field for the URL text file path.
- **`export_path_entry`**: Entry field for the export directory path.
- **`language_var`**: String variable for the target language selection.
- **`language_dropdown`**: Dropdown menu for selecting the target language.
- **`start_button`**: Button to start the scraping process.

### Usage

1. **Select URL File**: Click "Browse..." to choose a text file containing URLs to scrape.
2. **Select Export Directory**: Click "Browse..." to choose the directory where files will be saved.
3. **Choose Export Options**: Check the boxes for HTML, PDF, translated text, and/or original text.
4. **Select Target Language**: Use the dropdown menu to select the language for text translation.
5. **Start Scraping**: Click "Start Scraping" to begin the process.

