import os, csv, argparse
from jinja2 import Template

parser = argparse.ArgumentParser(description="Generar páginas por SKU desde CSV")
parser.add_argument("--csv", default="../data/skus.csv", help="Ruta al CSV de SKUs")
parser.add_argument("--public", default="../public", help="Carpeta 'public'")
args = parser.parse_args()

TEMPLATE = Template('''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ titulo }} – {{ sku }}</title>
  <link rel="stylesheet" href="/styles.css">
  <meta name="description" content="Aplicaciones, equivalencias y ficha técnica del {{ sku }}.">
</head>
<body>
  <header class="container">
    <a href="/" aria-label="Inicio">← Volver</a>
    <h1>{{ titulo }} <span class="badge">{{ sku }}</span></h1>
    <p>Ficha rápida, aplicaciones y equivalencias.</p>
  </header>

  <main class="container grid">
    <section class="card">
      {% if imagen %}<img src="{{ imagen }}" alt="Foto de {{ sku }}" onerror="this.style.display='none'">{% endif %}
      <div class="meta">
        <div class="kv"><strong>Tipo:</strong> —</div>
        <div class="kv"><strong>Rosca:</strong> —</div>
        <div class="kv"><strong>Altura:</strong> —</div>
        <div class="kv"><strong>Ø Exterior:</strong> —</div>
      </div>
      {% if pdf %}<p><a href="{{ pdf }}" download>Descargar ficha técnica (PDF)</a></p>{% endif %}
      {% if whatsapp %}<p><a href="https://wa.me/{{ whatsapp }}?text=Consulta%%20SKU%%20{{ sku }}" rel="noopener">Soporte por WhatsApp</a></p>{% endif %}
    </section>

    <section class="card">
      <h2>Aplicaciones</h2>
      <table>
        <thead><tr><th>Marca</th><th>Modelo</th><th>Detalle</th></tr></thead>
        <tbody>
          {% for item in apps %}
            <tr><td>{{ item[0] }}</td><td>{{ item[1] }}</td><td>{{ item[2] }}</td></tr>
          {% endfor %}
        </tbody>
      </table>

      <h2>Equivalencias</h2>
      <table>
        <thead><tr><th>Marca</th><th>Código</th></tr></thead>
        <tbody>
          {% for item in equivs %}
            <tr><td>{{ item[0] }}</td><td>{{ item[1] }}</td></tr>
          {% endfor %}
        </tbody>
      </table>

      <h2>OEM</h2>
      <table>
        <thead><tr><th>Fabricante</th><th>Código</th></tr></thead>
        <tbody>
          {% for item in oems %}
            <tr><td>{{ item[0] }}</td><td>{{ item[1] }}</td></tr>
          {% endfor %}
        </tbody>
      </table>
    </section>
  </main>

  <footer class="container">
    <small>© <span id="y"></span> Tu Marca • <a href="/">Catálogo</a></small>
  </footer>
<script>document.getElementById('y').textContent = new Date().getFullYear()</script>
</body>
</html>
''')

def parse_pairs(s, sep_pairs=";", sep_kv=":"):
    out = []
    s = (s or "").strip()
    if not s:
        return out
    for chunk in s.split(sep_pairs):
        if not chunk.strip():
            continue
        if sep_kv in chunk:
            k,v = chunk.split(sep_kv,1)
            out.append((k.strip(), v.strip()))
        else:
            out.append(("", chunk.strip()))
    return out

def parse_apps(s):
    # "Marca Modelo Motor/Año; ..." => we'll split into triples with best-effort
    out = []
    s = (s or "").strip()
    if not s:
        return out
    for chunk in s.split(";"):
        c = chunk.strip()
        if not c: 
            continue
        parts = c.split()
        if len(parts) >= 2:
            marca = parts[0]
            modelo = parts[1]
            detalle = " ".join(parts[2:]) if len(parts) > 2 else ""
            out.append((marca, modelo, detalle))
        else:
            out.append((c, "", ""))
    return out

with open(args.csv, newline='', encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sku = row["SKU"].strip()
        outdir = os.path.join(args.public, "sku", sku)
        os.makedirs(outdir, exist_ok=True)
        html = TEMPLATE.render(
            sku=sku,
            titulo=row.get("titulo","SKU"),
            imagen=row.get("imagen",""),
            pdf=row.get("pdf",""),
            whatsapp=(row.get("whatsapp") or "").replace("+",""),
            apps=parse_apps(row.get("aplicaciones","")),
            equivs=parse_pairs(row.get("equivalencias","")),
            oems=parse_pairs(row.get("OEM","")),
        )
        open(os.path.join(outdir, "index.html"), "w", encoding="utf-8").write(html)
        print("Página generada:", sku, "->", os.path.join(outdir, "index.html"))
