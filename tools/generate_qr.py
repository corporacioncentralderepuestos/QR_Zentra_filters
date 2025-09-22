import os, csv, qrcode
import argparse

parser = argparse.ArgumentParser(description="Generar QR por SKU desde un CSV")
parser.add_argument("--csv", default="../data/skus.csv", help="Ruta al CSV de SKUs")
parser.add_argument("--base-url", required=True, help="Base URL (ej: https://tudominio.com/p)")
parser.add_argument("--out", default="../public/qr", help="Carpeta de salida de PNGs")
parser.add_argument("--box-size", type=int, default=10, help="Tamaño de módulo")
parser.add_argument("--border", type=int, default=4, help="Quiet zone (módulos)")
args = parser.parse_args()

os.makedirs(args.out, exist_ok=True)

with open(args.csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sku = row["SKU"].strip()
        url = f"{args.base_url.rstrip('/')}/{sku}"
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_Q,  # robusto para superficies brillantes
            box_size=args.box_size,
            border=args.border,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        out_path = os.path.join(args.out, f"{sku}.png")
        img.save(out_path)
        print("OK:", sku, "->", url, "=>", out_path)
