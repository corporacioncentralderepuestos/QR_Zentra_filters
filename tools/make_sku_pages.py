# tools/make_sku_pages.py
import os, re, argparse, pandas as pd
LOGO = "/assets/zentra-logo.png"
from jinja2 import Template

parser = argparse.ArgumentParser(description="Generar páginas por SKU/SLUG desde CSV")
parser.add_argument("--csv", default="data/skus.csv")
parser.add_argument("--public", default="public")
args = parser.parse_args()

def get_ci(row, *names):
    for n in names:
        # admite nombre exacto o case-insensitive
        for k in row.index:
            if str(k).strip().lower() == str(n).strip().lower():
                v = str(row[k]).strip()
                if v and v.lower() != "nan":
                    return v
    return ""

def norm_slug(s: str) -> str:
    s = (s or "").upper().strip()
    s = re.sub(r"[^A-Z0-9-]", "-", s)
    return re.sub(r"-{2,}", "-", s).strip("-")

TEMPLATE = Template("""<!doctype html>
<html lang="es"><head>
  <meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
  <title>{{ titulo }}</title>
  <link rel="stylesheet" href="/styles.css">
  <meta name="description" content="Aplicaciones y equivalencias del código {{ display_code }}.">
</head>
<body>
  <header class="container">
    <a href="/">← Volver</a>
    <h1>{{ titulo }} <span class="badge">{{ display_code }}</span></h1>
    <p>Ficha rápida, aplicaciones y equivalencias.</p>
  </header>
  <main class="container grid">
    <section class="card">
      <div class="meta">
        <div class="kv"><strong>Código OEM:</strong> {{ display_code }}</div>
        <div class="kv"><strong>Slug:</strong> {{ slug }}</div>
      </div>
    </section>
    <section class="card">
      <h2>Aplicaciones</h2>
      {% if apps %}
        <table><thead><tr><th>Detalle</th></tr></thead><tbody>
          {% for a in apps %}<tr><td>{{ a }}</td></tr>{% endfor %}
        </tbody></table>
      {% else %}
        <p>—</p>
      {% endif %}

      <h2>Equivalencias</h2>
      {% if equivs %}
        <table><thead><tr><th>Código</th></tr></thead><tbody>
          {% for e in equivs %}<tr><td>{{ e }}</td></tr>{% endfor %}
        </tbody></table>
      {% else %}
        <p>—</p>
      {% endif %}
    </section>
  </main>
  <footer class="container"><small>© <span id="y"></span> Filtros Zentra • <a href="/">Catálogo</a></small></footer>
  <script>document.getElementById('y').textContent=new Date().getFullYear()</script>
</body></html>
""")

df = pd.read_csv(args.csv)

out_base = os.path.join(args.public, "sku")
os.makedirs(out_base, exist_ok=True)

count = 0
for _, row in df.iterrows():
    oem = get_ci(row, "CODIGO OEM", "OEM CODE", "OEM", "SKU")
    slug = get_ci(row, "SLUG")
    if not slug:
        slug = norm_slug(oem)
    slug = norm_slug(slug)
    if not slug:
        continue

    apps_raw = get_ci(row, "APLICACIONES", "APPLICATIONS", "APLICACION")
    apps = [a.strip() for a in re.split(r"[;|\n]", apps_raw) if a.strip()]

    equivs = []
    for col in df.columns:
        if "equivalencia" in str(col).lower():
            v = str(row[col]).strip()
            if v and v.lower() != "nan":
                equivs.append(v)

    titulo = f"Filtro {oem or slug}"
    outdir = os.path.join(out_base, slug)
    os.makedirs(outdir, exist_ok=True)
    html = TEMPLATE.render(titulo=titulo, display_code=oem or slug, slug=slug, apps=apps, equivs=equivs)
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    count += 1

print(f"Páginas generadas: {count}")
