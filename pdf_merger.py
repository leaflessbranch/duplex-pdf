import PyPDF2
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class PDFMerger:
    @staticmethod
    def merge_pdfs(file1, file2, output_file, reverse_file2=True):
        try:
            # Validate file existence and encryption
            for f in [file1, file2]:
                if not Path(f).exists():
                    raise FileNotFoundError(f"File not found: {f}")
                if PDFMerger.is_encrypted(f):
                    raise ValueError(f"PDF is encrypted: {f}")
            
            with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
                reader1 = PyPDF2.PdfReader(f1)
                reader2 = PyPDF2.PdfReader(f2)
                
                if len(reader1.pages) != len(reader2.pages):
                    raise ValueError(f"Page count mismatch: {len(reader1.pages)} vs {len(reader2.pages)}")
                
                writer = PyPDF2.PdfWriter()
                total_pages = len(reader1.pages)
                
                for i in range(total_pages):
                    writer.add_page(reader1.pages[i])
                    page_index = total_pages - i - 1 if reverse_file2 else i
                    writer.add_page(reader2.pages[page_index])
                
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, 'wb') as output_f:
                    writer.write(output_f)
                
                logger.info(f"Merged {total_pages*2} pages successfully")
                return True, "Merge successful"
        
        except PyPDF2.errors.PdfReadError as e:
            logger.error(f"PDF read error: {str(e)}")
            return False, f"Invalid PDF file: {str(e)}"
        except Exception as e:
            logger.exception("Merge failed")
            return False, f"Error: {str(e)}"

    @staticmethod
    def is_encrypted(file_path):
        try:
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return reader.is_encrypted
        except Exception as e:
            logger.error(f"Encryption check failed: {str(e)}")
            return True