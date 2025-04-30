"""
Script Python che funziona completamente in locale per tradurre un file PDF dall'inglese all'italiano.

Esegue OCR

Versione con WEB

NOTE:   Usa il font DejaVuSans.ttf che supporta pienamente caratteri Unicode (come €, ©, ™).
        Evita errori di codifica durante la generazione del PDF.
        Assicurati di avere il file DejaVuSans.ttf nella stessa cartella dello script.

"""
import fitz  # PyMuPDF
from transformers import MarianMTModel, MarianTokenizer
from fpdf import FPDF
import os
import pytesseract
from PIL import Image
import io
import streamlit as st
import tempfile

# Imposta il percorso a Tesseract-OCR (modifica se necessario su Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

MODEL_NAME = "Helsinki-NLP/opus-mt-en-it"

# Estrai testo dal PDF (OCR fallback)
def extract_pages_from_pdf(file_path):
    doc = fitz.open(file_path)
    pages_text = []
    for page in doc:
        text = page.get_text("text").strip()
        if not text:
            pix = page.get_pixmap(dpi=300)
            image = Image.open(io.BytesIO(pix.tobytes("png")))
            text = pytesseract.image_to_string(image, lang="eng")
        pages_text.append(text)
    return pages_text

# Traduzione
@st.cache_resource
def load_model():
    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)
    return tokenizer, model

def translate_text(text, model, tokenizer, max_length=512):
    sentences = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    translations = []
    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        translations.append(translated_text)
    return " ".join(translations)

# Crea PDF finale con supporto Unicode
class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
        self.set_font("DejaVu", size=12)

# Crea PDF
def create_pdf(pages_text, output_path):
    pdf = UnicodePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for page_text in pages_text:
        pdf.add_page()
        for line in page_text.split("\n"):
            if line.strip():
                pdf.multi_cell(0, 10, line)
    pdf.output(output_path)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Traduttore PDF in Italiano", layout="centered")
st.title("📄 Traduzione PDF (con OCR e MarianMT)")

uploaded_files = st.file_uploader("Carica uno o più file PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button("Avvia Traduzione"):
        tokenizer, model = load_model()
        for uploaded in uploaded_files:
            st.write(f"\n📄 **{uploaded.name}**")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded.read())
                tmp_path = tmp.name

            st.text("Estrazione testo in corso...")
            pages = extract_pages_from_pdf(tmp_path)
            translated_pages = []

            progress = st.progress(0)
            for idx, page in enumerate(pages):
                translated = translate_text(page, model, tokenizer)
                translated_pages.append(translated)
                progress.progress((idx + 1) / len(pages))

            out_path = tmp_path.replace(".pdf", "_tradotto.pdf")
            create_pdf(translated_pages, out_path)

            with open(out_path, "rb") as f:
                st.download_button("📥 Scarica PDF Tradotto", f, file_name=uploaded.name.replace(".pdf", "_tradotto.pdf"))

        st.success("Traduzione completata!")
