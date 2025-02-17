import pdfplumber
import pymupdf
import re

from constants import SignaturesNames


def get_pdf_text(pdf_invoices: str):
    with pdfplumber.open(pdf_invoices) as doc:
        number_pages = doc.pages
        page_signature = len(number_pages) - 1
        signature_field = number_pages[page_signature].search(
            r"Responsable\s*Facturaci[oó]n.+"
        )
        text_page_signature = doc.pages[page_signature].extract_text()

    if responsible_signature := re.search(
        r"responsable\s*facturaci[oó]n[:\s]*(.+)", text_page_signature, re.I
    ):
        name_signature = responsible_signature.group(1)
        return (
            name_signature,
            page_signature,
            signature_field[0]["x0"],
            signature_field[0]["top"],
        )


def get_name_signature(name: str):
    name_image = next(
        (
            image
            for image, name_signature in SignaturesNames.signatures_names.items()
            if name_signature == name
        ),
        None,
    )
    if name_image:
        return name_image


def add_signature_to_pdf(
    pdf_input: str,
    pdf_output: str,
    signature: str,
    page: int,
    x_postion: int,
    y_position: int,
    scale: float,
):
    doc_pdf = pymupdf.open(pdf_input)
    img_signature = pymupdf.open(signature)
    page_pdf = doc_pdf[page]
    rect = pymupdf.Rect(
        x_postion,
        y_position,
        x_postion + img_signature[0].rect.width * scale,
        y_position + img_signature[0].rect.height * scale,
    )
    img_signature.close()
    page_pdf.insert_image(rect, filename=signature)
    doc_pdf.save(pdf_output)
    doc_pdf.close()
    print(f"Invoices {pdf_output}")
    return
