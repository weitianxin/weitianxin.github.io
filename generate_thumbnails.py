import json
from PIL import Image
from pathlib import Path

GALLERY_DIR = Path(__file__).parent / "gallery"
THUMB_DIR = GALLERY_DIR / "thumbs"
THUMB_DIR.mkdir(exist_ok=True)

MAX_SIZE = (600, 600)
EXTS = {".jpg", ".jpeg", ".png", ".webp"}

images = []
for src in sorted(GALLERY_DIR.iterdir()):
    if src.suffix.lower() not in EXTS:
        continue
    images.append(src.name)
    dest = THUMB_DIR / (src.stem + ".jpg")
    if dest.exists():
        print(f"skip {src.name}")
        continue
    print(f"processing {src.name} ...", end=" ", flush=True)
    with Image.open(src) as img:
        img = img.convert("RGB")
        img.thumbnail(MAX_SIZE, Image.LANCZOS)
        img.save(dest, "JPEG", quality=80, optimize=True)
    print(f"-> {dest.stat().st_size // 1024} KB")

manifest = GALLERY_DIR / "manifest.json"
manifest.write_text(json.dumps(images, ensure_ascii=False, indent=2), encoding='utf-8')
print(f"manifest: {len(images)} images -> {manifest}")
print("done.")
