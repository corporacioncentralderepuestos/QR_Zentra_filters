# QR + Netlify para landings por SKU

Proyecto base para publicar landings ultra ligeras por SKU y apuntar QRs a `/p/<SKU>`.

## Estructura
- `public/` -> se publica tal cual en Netlify
- `public/sku/<SKU>/index.html` -> landing por SKU
- `_redirects` o `netlify.toml` -> reglas para `/p/:sku`
- `data/skus.csv` -> tu "CMS" simple
- `tools/` -> scripts opcionales

## Flujo sugerido
1. Edita `data/skus.csv` con tus SKUs.
2. Ejecuta:
   ```bash
   cd tools
   pip install -r requirements.txt
   python make_sku_pages.py
   python build_redirects.py
   python generate_qr.py --base-url "https://tudominio.com/p"
   ```
3. Sube a Netlify (repo Git) y conecta tu dominio.
