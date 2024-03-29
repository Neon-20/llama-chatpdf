import PyPDF2
from langchain.text_splitter import TokenTextSplitter
from src.scrapers.scraper import Scraper
import os


class PDFScraper(Scraper):
    def __init__(self, pdf_file_path):
        self.pdf_file_path = pdf_file_path

    def scrape(self):
        text = ""
        try:
            with open(self.pdf_file_path, 'rb') as pdf_file:
                reader = PyPDF2.PdfFileReader(pdf_file)
                for _, page in enumerate(reader.pages, start=1):
                    page_text = page.extractText()
                    if page_text.strip():
                        text += page_text
                text = "\n".join(line for line in text.splitlines() if line.strip())

                text_splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=0)
                return text_splitter.split_text(text)
        except FileNotFoundError:
            print(f"Error: File '{os.path.basename(self.pdf_file_path)}' not found.")
            return None
        except PyPDF2.utils.PdfReadError:
            print(f"Error: Unable to read PDF file '{os.path.basename(self.pdf_file_path)}'.")
            return None

# Example usage:
pdf_file_path = 'path/to/pdf_file.pdf'  # Specify the path to your PDF file here
scraper = PDFScraper(pdf_file_path)
chunks = scraper.scrape()
if chunks:
    print("Text extracted successfully.")
else:
    print("Text extraction failed.")
