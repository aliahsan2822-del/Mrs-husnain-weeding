#!/usr/bin/env python3
"""
Re-embeds the pictures in assets/images/ into index.html (window.WEDDING_IMAGES block),
so the invitation stays ONE standalone file.

  python3 tools/embed_images.py            # from the repo root

File name -> where the picture is used
  couple.webp   page right after the book opens + the last page (transparent cut-out, portrait)
  card.webp     inside-right page of the book (transparent cut-out, portrait)
  g1..g5.webp   the five "Moments" frames, in order (portrait photos / illustrations)
Any image format works (webp, png, jpg); the file name (without extension) is the key.
Tip: keep each picture under ~250 KB (about 900 px wide) so the page loads fast on phones.
"""
import base64, mimetypes, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parent.parent
html = root / "index.html"
imgs = root / "assets" / "images"
ORDER = ["couple", "g1", "g2", "g3", "g4", "g5", "card"]

found = {p.stem: p for p in imgs.iterdir() if p.suffix.lower() in (".webp", ".png", ".jpg", ".jpeg")}
if not found:
    sys.exit("No images found in assets/images/")
keys = [k for k in ORDER if k in found] + sorted(k for k in found if k not in ORDER)

def uri(p):
    mime = mimetypes.guess_type(p.name)[0] or ("image/webp" if p.suffix.lower() == ".webp" else "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()

block = "window.WEDDING_IMAGES = {\n" + ",\n".join(f"  {k}: '{uri(found[k])}'" for k in keys) + "\n};"
s = html.read_text(encoding="utf-8")
new, n = re.subn(r"window\.WEDDING_IMAGES = \{.*?\n\};", lambda m: block, s, count=1, flags=re.S)
if n != 1:
    sys.exit("Could not find the window.WEDDING_IMAGES block in index.html")
html.write_text(new, encoding="utf-8")
print(f"Embedded {len(keys)} images ({', '.join(keys)}) -> {html.name} ({len(new)//1024} KB)")
