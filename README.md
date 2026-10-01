# 📄 PDF Converter CLI

A versatile, lightweight command-line tool built with Python to convert, extract, merge, and split PDF documents with ease.

---

## ✨ Features

| Command | Description | Notes |
| :--- | :--- | :--- |
| `img2pdf` | Convert one or multiple images into a single PDF | Supports JPG, PNG, RGBA, etc. |
| `txt2pdf` | Convert plain text files into formatted PDF documents | Word wrapping & A4 pagination |
| `office2pdf` | Convert Word, PowerPoint, and Excel files to PDF | Requires [LibreOffice](https://www.libreoffice.org/) |
| `pdf2img` | Extract pages from a PDF as individual image files | Customizable `--dpi` and `--format` (PNG/JPG) |
| `pdf2txt` | Extract textual content from a PDF file | Outputs clean UTF-8 text |
| `merge` | Combine multiple PDF files into one | Maintains original document order |
| `split` | Extract specific pages or page ranges from a PDF | Supports ranges like `1-3,5` |

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/brekhnaafridi/pdfconverter.git
cd pdfconverter
```

### 2. Create and Activate a Virtual Environment (Optional but recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

*(Direct package installation: `pip install pillow pymupdf reportlab`)*

> [!NOTE]  
> To use `office2pdf` (converting `.docx`, `.pptx`, `.xlsx` to PDF), make sure [LibreOffice](https://www.libreoffice.org/) is installed and added to your system `PATH`.

---

## 💻 Usage Examples

### 1. Images to PDF (`img2pdf`)
Convert multiple images into a single PDF document:
```bash
python pdf_converter.py img2pdf photo1.jpg photo2.png -o photos.pdf
```

### 2. Text File to PDF (`txt2pdf`)
Convert a `.txt` file into a formatted PDF:
```bash
python pdf_converter.py txt2pdf notes.txt -o notes.pdf
```

### 3. Office Documents to PDF (`office2pdf`)
Batch convert Word, Excel, or PowerPoint presentations:
```bash
python pdf_converter.py office2pdf report.docx presentation.pptx data.xlsx
```

### 4. PDF to Images (`pdf2img`)
Render each page of a PDF into high-quality images:
```bash
python pdf_converter.py pdf2img document.pdf --dpi 200 --format png -o extracted_pages
```

### 5. Extract Text from PDF (`pdf2txt`)
Extract text content to a `.txt` file:
```bash
python pdf_converter.py pdf2txt document.pdf -o output.txt
```

### 6. Merge Multiple PDFs (`merge`)
Combine several PDFs into a single file:
```bash
python pdf_converter.py merge document1.pdf document2.pdf document3.pdf -o merged.pdf
```

### 7. Split / Extract Pages (`split`)
Extract specific pages or page ranges from a PDF:
```bash
# Extract pages 1 to 3 and page 5
python pdf_converter.py split document.pdf --pages 1-3,5 -o extracted_selection.pdf
```

---

## 📁 Project Structure

```
pdfconverter/
├── pdf_converter.py     # Main CLI script
├── requirements.txt     # Python dependencies
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/brekhnaafridi/pdfconverter/issues).

## 📝 License
This project is open source and available under the [MIT License](LICENSE).
