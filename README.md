# Duplex PDF Merger Pro

A Windows application for merging duplex-scanned PDF documents. Designed for users who scan double-sided documents using a single-sided scanner, this tool interleaves pages from two PDFs (front and back scans) into a single, properly ordered PDF.

## Features
- **Reverse Page Order Toggle**: Automatically reverses the order of back pages for correct duplex merging.
- **User-Friendly Interface**: Clean and intuitive Windows 11-style UI.
- **Validation**: Ensures PDFs are valid, unencrypted, and have matching page counts.
- **Logging**: Detailed logging for troubleshooting.
- **Production-Grade**: Robust error handling and input validation.

## Installation
1. **Prerequisites**:
   - Python 3.8 or higher
   - Windows 10/11

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt

3. **Run the Application**:
   ```bash
   python main.py

## Usage
1. Select the Front Pages PDF (scanned in normal order).
2. Select the Back Pages PDF (scanned in reverse order).
3. Choose the Output File location.
4. Toggle the Reverse Back Pages checkbox if needed.
5. Click Merge Documents.

## Packaging for Distribution

To create a standalone Windows executable:
    ```bash
    pip install pyinstaller
    pyinstaller --onefile --windowed --name "PDF Duplex Merger" main.py

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Screenshots

[Screenshot.png]