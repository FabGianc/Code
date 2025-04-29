"""
Script Python che funziona completamente in locale per tradurre un file PDF dall'inglese all'italiano.
Traduce tutti i file PDF che trova in una directory.
Salva i nuovi file PDF nella stessa cartella, aggiungendo il suffisso _tradotto al nome.
"""

import fitz  # PyMuPDF
from transformers import MarianMTModel, MarianTokenizer
from fpdf import FPDF
import os

# --- Configurazioni ---
MODEL_NAME = "Helsinki-NLP/opus-mt-en-it"

# --- Step 1: Estrai testo e struttura dal PDF ---
def extract_pages_from_pdf(file_path):
    doc = fitz.open(file_path)
    pages_text = []
    for page in doc:
        pages_text.append(page.get_text("text"))
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
    pdf.set_font("Arial", size=12)

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
        print("Sacremoses trovato: caricamento ottimizzato.")
    except ImportError:
        print("Sacremoses non trovato: il caricamento prosegue comunque.")
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return tokenizer

# --- Funzione per barra di avanzamento ---
def print_progress(current, total, bar_length=40):
    progress = int(bar_length * current / total)
    bar = "#" * progress + "-" * (bar_length - progress)
    print(f"\r[{bar}] {current}/{total} pagine", end="")

# --- Main ---
if __name__ == "__main__":
    directory = input("Inserisci il percorso della directory contenente i file PDF da tradurre: ").strip().strip('"').strip("'")

    if not os.path.isdir(directory):
        print(f"Errore: la directory {directory} non esiste.")
        exit(1)

    print("Caricamento modello di traduzione...")
    tokenizer = load_tokenizer(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)

    pdf_files = [f for f in os.listdir(directory) if f.lower().endswith('.pdf')]

    if not pdf_files:
        print("Nessun file PDF trovato nella directory.")
        exit(0)

    for pdf_file in pdf_files:
        pdf_input_path = os.path.join(directory, pdf_file)
        pdf_output_path = os.path.join(directory, os.path.splitext(pdf_file)[0] + "_tradotto.pdf")

        print(f"\nProcessing: {pdf_file}")

        pages = extract_pages_from_pdf(pdf_input_path)
        total_pages = len(pages)
        print(f"Il documento contiene {total_pages} pagine.")

        translated_pages = []
        print("Traduzione delle pagine...")

        for idx, page_text in enumerate(pages):
            translated_page = translate_text(page_text, model, tokenizer)
            translated_pages.append(translated_page)
            print_progress(idx + 1, total_pages)

        print("\nCreazione del PDF tradotto...")
        create_pdf(translated_pages, pdf_output_path)

        print(f"Fatto! File salvato come {pdf_output_path}")
