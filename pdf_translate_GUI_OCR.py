"""
Script Python che funziona completamente in locale per tradurre un file PDF dall'inglese all'italiano.

Esegue OCR

Versione con GUI
"""

import fitz  # PyMuPDF
from transformers import MarianMTModel, MarianTokenizer
from fpdf import FPDF
import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import pytesseract
from PIL import Image
import io

# Imposta il percorso a Tesseract-OCR (modifica se necessario)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

# --- Configurazioni ---
MODEL_NAME = "Helsinki-NLP/opus-mt-en-it"

# --- Step 1: Estrai testo e struttura dal PDF, con fallback OCR ---
def extract_pages_from_pdf(file_path):
    doc = fitz.open(file_path)
    pages_text = []
    for page in doc:
        text = page.get_text("text").strip()
        if not text:
            # fallback OCR
            pix = page.get_pixmap(dpi=300)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image, lang="eng")
        pages_text.append(text)
    return pages_text

# --- Step 2: Traduce il testo per pagina ---
def translate_text(text, model, tokenizer, max_length=512):
    sentences = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    translations = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        translations.append(translated_text)
    return " ".join(translations)

# --- Step 3: Crea nuovo PDF mantenendo pagine ---
def create_pdf(pages_text, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=12)

    for page_text in pages_text:
        pdf.add_page()
        lines = page_text.split("\n")
        for line in lines:
            if line.strip() != "":
                pdf.multi_cell(0, 10, line)
    pdf.output(output_path)

# --- Caricamento tokenizer con gestione sacremoses ---
def load_tokenizer(model_name):
    try:
        import sacremoses
    except ImportError:
        pass
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return tokenizer

# --- Funzione per barra di avanzamento ---
def print_progress(current, total, bar_length=40):
    progress = int(bar_length * current / total)
    bar = "#" * progress + "-" * (bar_length - progress)
    return f"[{bar}] {current}/{total} pagine"

# --- Traduzione multipla ---
def translate_all_pdfs(directory, output_widget):
    try:
        output_widget.insert(tk.END, "Caricamento modello...\n")
        output_widget.update()
        tokenizer = load_tokenizer(MODEL_NAME)
        model = MarianMTModel.from_pretrained(MODEL_NAME)

        pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf') and not f.endswith('_tradotto.pdf')]
        if not pdf_files:
            output_widget.insert(tk.END, "Nessun file PDF da tradurre trovato nella cartella.\n")
            return

        for pdf_file in pdf_files:
            pdf_input_path = os.path.join(directory, pdf_file)
            pdf_output_path = os.path.join(directory, os.path.splitext(pdf_file)[0] + "_tradotto.pdf")

            output_widget.insert(tk.END, f"\n➡️  Traduco: {pdf_file}\n")
            output_widget.update()

            pages = extract_pages_from_pdf(pdf_input_path)
            total_pages = len(pages)
            translated_pages = []

            for idx, page_text in enumerate(pages):
                translated_page = translate_text(page_text, model, tokenizer)
                translated_pages.append(translated_page)
                bar = print_progress(idx + 1, total_pages)
                output_widget.insert(tk.END, f"\r{bar}\n")
                output_widget.see(tk.END)
                output_widget.update()

            create_pdf(translated_pages, pdf_output_path)
            output_widget.insert(tk.END, f"✅  Salvato come: {os.path.basename(pdf_output_path)}\n")
            output_widget.update()

        messagebox.showinfo("Completato", "Traduzione completata per tutti i PDF!")

    except Exception as e:
        messagebox.showerror("Errore", str(e))

# --- GUI ---
def avvia_gui():
    def seleziona_cartella():
        folder = filedialog.askdirectory()
        if folder:
            directory_var.set(folder)

    def avvia_traduzione():
        selected_dir = directory_var.get()
        if not os.path.isdir(selected_dir):
            messagebox.showerror("Errore", "Seleziona una cartella valida.")
            return
        output_text.delete(1.0, tk.END)
        threading.Thread(target=translate_all_pdfs, args=(selected_dir, output_text), daemon=True).start()

    root = tk.Tk()
    root.title("Traduttore PDF in Italiano")
    root.geometry("700x500")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    directory_var = tk.StringVar()
    tk.Label(frame, text="Cartella PDF:").pack(side=tk.LEFT, padx=5)
    tk.Entry(frame, textvariable=directory_var, width=50).pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="Sfoglia", command=seleziona_cartella).pack(side=tk.LEFT)

    tk.Button(root, text="Avvia Traduzione", command=avvia_traduzione, bg="green", fg="white").pack(pady=10)

    output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=20)
    output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()

# --- Main ---
if __name__ == "__main__":
    avvia_gui()
