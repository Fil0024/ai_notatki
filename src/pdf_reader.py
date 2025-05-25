import os
import pdfplumber
import pytesseract
from utils import get_root_path, get_pdf_path
import re
import logging
logging.getLogger('pdfminer').setLevel(logging.ERROR)


output_path = get_root_path() + "/transcripts/"

def read_pdf_text(pdf_path: str) -> str:
    """
    Odczytuje tekst z PDF, numerując slajdy (strony) i stosując OCR jako fallback.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            else:
                # Fallback do OCR dla skanowanych stron
                try:
                    pil_image = page.to_image(resolution=300).original
                    ocr_text = pytesseract.image_to_string(pil_image)
                    text += ocr_text + "\n"
                except Exception as e:
                    text += f"[Błąd OCR na slajdzie {page.page_number}: {e}]\n"
            text += "\n"  # oddziel slajdy pustym wierszem
    return text

def clean_lecture_text(text: str) -> str:
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        # Usuń linie z błędami OCR
        if "Błąd OCR" in line:
            continue
        # Usuń cytaty dekoracyjne
        if "Type a quote here" in line or "Johnny Appleseed" in line:
            continue
        # Usuń nagłówki instytucji
        if re.search(r"(Jakub Urbanik|Katedra|Wydziału|Prawo rzymskie)", line, re.IGNORECASE):
            continue
        # Usuń powtarzające się ❖ bez treści
        if line.strip() in ["❖", "☞"]:
            continue
        if not line or len(line) == 1:
            continue
        line = re.sub(r"^❖\s*", "- ", line)
        # Usuń linie będące samymi symbolami, np. numery stron, tab I itp.
        if re.match(r'^\s*(tab|TPSulp|C\(AIO\))', line):
            continue
        # Usuń linie składające się wyłącznie z dużych liter łacińskich i cyfr (np. inskrypcje łacińskie)
        if re.fullmatch(r'[A-Z0-9\s\[\]\(\)\.]*', line.strip()):
            continue

        cleaned_lines.append(line.strip())

    cleaned_text = "\n".join(cleaned_lines)
    
    # Opcjonalnie: usuń zduplikowane linie
    deduped_lines = []
    prev_line = ""
    for line in cleaned_text.splitlines():
        if line != prev_line:
            deduped_lines.append(line)
            prev_line = line

    return "\n".join(deduped_lines)

if __name__ == "__main__":
    print(get_root_path())
    output_dir = os.path.join(get_root_path(), "transcripts")
    os.makedirs(output_dir, exist_ok=True)

    # Wczytanie i ekstrakcja tekstu
    pdf_path = get_pdf_path()
    pdf_text = read_pdf_text(pdf_path)
    pdf_text = clean_lecture_text(pdf_text)

    if pdf_text:
        # Zapis do pliku .txt w katalogu transcripts
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_file = os.path.join(output_dir, f"{base_name}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(pdf_text)
            f.write("\n\n--- Transkrypcja zakończona ---\n")
        print(f"Transkrypcja została zapisana do: {output_file}")
    else:
        print("Nie udało się odczytać tekstu z pliku PDF.")
