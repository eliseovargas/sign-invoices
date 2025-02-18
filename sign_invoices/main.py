import pathlib
import configparser
import argparse
from rich import print as rprint

from services import (
    get_pdf_text,
    get_name_signature,
    add_signature_to_pdf,
)


def main_signs(input_folder: str, output_folder: str):
    config = configparser.ConfigParser()
    config.read(".env")
    images_folder = pathlib.Path(config["SIGNATURES_FOLDER_PATH"]["SIGNATURES"])
    rprint(f"{' OPENING PDF INVOICES ':=^50}")
    folder_invoices_without_sign = pathlib.Path(input_folder)
    folder_invoices_with_sign = pathlib.Path(output_folder)
    for input_pdf in folder_invoices_without_sign.iterdir():
        name_invoices = input_pdf.name
        output_pdf = pathlib.Path.joinpath(
            folder_invoices_with_sign, pathlib.Path(name_invoices)
        )
        rprint(f"{name_invoices:=^50}")
        rprint(f"{' GETTING RESPONSIBLE SIGNATURE ':=^50}")
        res_text_pdf = get_pdf_text(input_pdf)
        if not res_text_pdf:
            rprint(f"{' RESPONSIBLE SIGNATURE ':-^50}")
            continue
        name_signature, page_signature, x_position, y_position = res_text_pdf
        rprint(f"{' GETTING NAME IMAGES ':=^50}")
        name_image = get_name_signature(name_signature)
        signature = pathlib.Path.joinpath(
            images_folder, pathlib.Path(name_image + ".png")
        )
        add_signature_to_pdf(
            input_pdf,
            output_pdf,
            signature,
            page_signature,
            x_position + 50,
            y_position - 40,
            0.6,
        )
        rprint(f"{' SIGNATURE ADDED ':-^50}")


if __name__ == "__main__":
    desc = "El script recibe la carpeta con las facturas sin firmar(input_folder) \
        y la carpeta de destino donde se guardaran las facturas \
            firmadas(output_folder)"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "--input_folder",
        type=str,
        help="Carpeta con las facturas sin firmar",
        required=True,
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        help="Carpeta de destino donde se guardaran las facturas firmadas",
        required=True,
    )
    args = parser.parse_args()
    main_signs(args.input_folder, args.output_folder)
