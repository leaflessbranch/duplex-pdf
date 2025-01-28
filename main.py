import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pdf_merger import PDFMerger
import logging
from pathlib import Path
import PyPDF2

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',
    filemode='a'
)

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Duplex PDF Merger")
        self.root.geometry("600x350")
        self.reverse_var = tk.BooleanVar(value=True)
        self.setup_ui()
        self.set_protocols()
        self.configure_styles()
    
    def configure_styles(self):
        style = ttk.Style()
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TLabel', font=('Segoe UI', 9))
        style.configure('TCheckbutton', font=('Segoe UI', 9))
        style.configure('Accent.TButton', foreground='black', background='white')
        style.map('Accent.TButton',
                  foreground=[('active', 'black'), ('disabled', 'gray')],
                  background=[('active', '#005499'), ('disabled', '#AAAAAA')])
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text=" PDF Files ", padding=(15, 10))
        input_frame.pack(fill='x', pady=5)
        
        # File 1
        ttk.Label(input_frame, text="Front Pages:").grid(row=0, column=0, sticky='w', pady=3)
        self.file1_entry = ttk.Entry(input_frame, width=40)
        self.file1_entry.grid(row=0, column=1, padx=5, sticky='ew')
        ttk.Button(input_frame, text="Browse...", command=lambda: self.browse_file(self.file1_entry)).grid(row=0, column=2)
        
        # File 2
        ttk.Label(input_frame, text="Back Pages:").grid(row=1, column=0, sticky='w', pady=10)
        self.file2_entry = ttk.Entry(input_frame, width=40)
        self.file2_entry.grid(row=1, column=1, padx=5, sticky='ew')
        ttk.Button(input_frame, text="Browse...", command=lambda: self.browse_file(self.file2_entry)).grid(row=1, column=2)
        
        # Reverse Toggle
        self.reverse_check = ttk.Checkbutton(
            input_frame, 
            text="Reverse Back Pages", 
            variable=self.reverse_var,
            command=self.toggle_reverse_hint
        )
        self.reverse_check.grid(row=2, column=1, pady=5, sticky='w')
        
        # Output Section
        ttk.Label(input_frame, text="Output File:").grid(row=3, column=0, sticky='w', pady=10)
        self.output_entry = ttk.Entry(input_frame, width=40)
        self.output_entry.grid(row=3, column=1, padx=5, sticky='ew')
        ttk.Button(input_frame, text="Save As...", command=self.save_file).grid(row=3, column=2)
        
        # Merge Button
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill='x', pady=15)
        self.merge_btn = ttk.Button(
            action_frame, 
            text="Merge Documents", 
            command=self.merge,
            style='Accent.TButton'
        )
        self.merge_btn.pack(side='right', ipadx=10)
        
        # Status Bar
        self.status_frame = ttk.Frame(self.root, relief='sunken', padding=(5, 2))
        self.status_frame.pack(side='bottom', fill='x')
        self.status_label = ttk.Label(self.status_frame, text="Ready", anchor='w')
        self.status_label.pack(fill='x')
    
    def set_protocols(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def toggle_reverse_hint(self):
        if self.reverse_var.get():
            status_text = "Back pages will be reversed during merge"
        else:
            status_text = "Back pages will be used in original order"
        self.status_label.config(text=status_text, foreground='gray')
    
    def browse_file(self, entry_widget):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF Files", "*.pdf")],
            defaultextension=".pdf"
        )
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile="merged_document.pdf"
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)
    
    def validate_inputs(self):
        errors = []
        for label, path in [("Front pages", self.file1_entry.get()),
                          ("Back pages", self.file2_entry.get())]:
            if not path:
                errors.append(f"{label} PDF is required")
                continue
            if not Path(path).exists():
                errors.append(f"{label} PDF not found: {path}")
            elif not path.lower().endswith('.pdf'):
                errors.append(f"{label} is not a PDF file: {path}")
        
        output_path = self.output_entry.get()
        if not output_path:
            errors.append("Output file path is required")
        elif not output_path.lower().endswith('.pdf'):
            errors.append("Output file must be a PDF")
        
        return errors
    
    def set_ui_state(self, enabled=True):
        state = 'normal' if enabled else 'disabled'
        widgets = [self.file1_entry, self.file2_entry, self.output_entry,
                 self.reverse_check, self.merge_btn]
        for widget in widgets:
            widget.state(['!disabled' if enabled else 'disabled'])
    
    def merge(self):
        errors = self.validate_inputs()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return
        
        self.set_ui_state(False)
        self.status_label.config(text="Merging PDFs...", foreground='black')
        
        try:
            success, message = PDFMerger.merge_pdfs(
                self.file1_entry.get(),
                self.file2_entry.get(),
                self.output_entry.get(),
                self.reverse_var.get()
            )
            
            if success:
                with open(self.file1_entry.get(), 'rb') as f:
                    page_count = len(PyPDF2.PdfReader(f).pages)
                self.status_label.config(text="Merge completed successfully", foreground='green')
                messagebox.showinfo("Success", 
                    f"Merged PDF created with {page_count*2} pages\n"
                    f"Location: {self.output_entry.get()}")
            else:
                self.status_label.config(text=message, foreground='red')
                messagebox.showerror("Merge Failed", message)
        
        except Exception as e:
            logging.error(f"Critical error: {str(e)}")
            messagebox.showerror("Unexpected Error", 
                "A critical error occurred. Please check the log file.")
        
        finally:
            self.set_ui_state(True)
            self.status_label.config(text="Ready", foreground='gray')
    
    def on_close(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()