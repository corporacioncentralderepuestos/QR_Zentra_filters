import csv, argparse, os

parser = argparse.ArgumentParser(description="Generar archivo _redirects desde CSV")
parser.add_argument("--csv", default="../data/skus.csv", help="Ruta al CSV de SKUs")
parser.add_argument("--out", default="../_redirects", help="Ruta de salida del archivo _redirects")
args = parser.parse_args()

rows = []
with open(args.csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for r in reader:
        sku = r["SKU"].strip()
        slug = (r.get("slug") or sku).strip()
        rows.append(f"/p/{sku}   /sku/{sku}/index.html   200")

content = "\n".join(rows) + "\n"
os.makedirs(os.path.dirname(args.out), exist_ok=True)
open(args.out, "w", encoding="utf-8").write(content)
print(f"Generado {args.out} con {len(rows)} entradas.")
