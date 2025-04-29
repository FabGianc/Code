"""
Script Python che funziona completamente in locale per tradurre un file PDF dall'inglese all'italiano.

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
    pdf_input = input("Inserisci il nome del file PDF da tradurre (con estensione): ").strip().strip('"').strip("'")
    pdf_output = input("Inserisci il nome del file PDF tradotto da creare (con estensione): ").strip().strip('"').strip("'")

    if not os.path.exists(pdf_input):
        print(f"Errore: il file {pdf_input} non esiste.")
        exit(1)

    if os.path.exists(pdf_output):
        confirm = input(f"Attenzione: il file {pdf_output} esiste già. Vuoi sovrascriverlo? (s/n): ").strip().lower()
        if confirm != 's':
            print("Operazione annullata.")
            exit(0)

    print("Estrazione testo dal PDF...")
    pages = extract_pages_from_pdf(pdf_input)

    total_pages = len(pages)
    print(f"Il documento contiene {total_pages} pagine.")

    print("Caricamento modello di traduzione...")
    tokenizer = load_tokenizer(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)

    translated_pages = []
    print("Traduzione delle pagine...")

    for idx, page_text in enumerate(pages):
        translated_page = translate_text(page_text, model, tokenizer)
        translated_pages.append(translated_page)
        print_progress(idx + 1, total_pages)

    print("\nCreazione del PDF tradotto...")
    create_pdf(translated_pages, pdf_output)

    print(f"Fatto! File salvato come {pdf_output}")

