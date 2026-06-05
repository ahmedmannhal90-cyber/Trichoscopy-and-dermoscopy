#!/usr/bin/env python3
"""
Run this once to generate all required icons and splash screens.
  pip install Pillow
  python generate_assets.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ── Dirs ──────────────────────────────────────────────────────
os.makedirs("public/icons", exist_ok=True)
os.makedirs("public/splash", exist_ok=True)

RED_DARK  = "#7a0c0c"
RED_MID   = "#9c1010"
RED_LIGHT = "#c01c1c"
WHITE     = "#ffffff"

# ── Helper: draw the TrichoscaleDX logo onto a canvas ─────────
def draw_logo(draw, cx, cy, box_w, box_h, font_size):
    """Draw the white box with red text centred at (cx, cy)."""
    pad_x = int(box_w * 0.12)
    pad_y = int(box_h * 0.18)
    x0 = cx - box_w // 2
    y0 = cy - box_h // 2
    x1 = cx + box_w // 2
    y1 = cy + box_h // 2
    radius = max(4, int(box_h * 0.12))

    # White rounded rectangle
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=WHITE)

    # Try to load a bold font; fall back gracefully
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except Exception:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

    text = "TrichoscaleDX"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=RED_DARK, font=font)

# ── Icon generator ─────────────────────────────────────────────
def make_icon(size, path):
    img = Image.new("RGB", (size, size), RED_MID)
    draw = ImageDraw.Draw(img)

    # Subtle gradient effect via rectangles
    for i in range(size):
        ratio = i / size
        r = int(0xc0 + (0x7a - 0xc0) * ratio)
        g = int(0x1c + (0x0c - 0x1c) * ratio)
        b = int(0x1c + (0x0c - 0x1c) * ratio)
        draw.line([(0, i), (size, i)], fill=(r, g, b))

    # Logo box — ~55 % of icon width
    box_w = int(size * 0.72)
    box_h = int(size * 0.22)
    font_size = max(8, int(size * 0.09))
    draw_logo(draw, size // 2, size // 2, box_w, box_h, font_size)

    img.save(path, "PNG")
    print(f"  ✓ {path}")

# ── Splash screen generator ────────────────────────────────────
def make_splash(w, h, path):
    img = Image.new("RGB", (w, h), RED_MID)
    draw = ImageDraw.Draw(img)

    # Gradient top→bottom
    for i in range(h):
        ratio = i / h
        r = int(0xc0 + (0x78 - 0xc0) * ratio)
        g = int(0x1c + (0x0a - 0x1c) * ratio)
        b = int(0x1c + (0x0a - 0x1c) * ratio)
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # Logo centred, sized ~42 % of width
    box_w = int(w * 0.58)
    box_h = int(h * 0.07)
    font_size = max(10, int(w * 0.046))
    draw_logo(draw, w // 2, h // 2 - int(h * 0.03), box_w, box_h, font_size)

    # Tagline below
    tagline = "Advanced Dermoscopic Analysis"
    try:
        tfont = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", max(8, int(w * 0.025)))
    except Exception:
        try:
            tfont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(8, int(w * 0.025)))
        except Exception:
            tfont = ImageFont.load_default()

    tbbox = draw.textbbox((0, 0), tagline, font=tfont)
    tw = tbbox[2] - tbbox[0]
    ty = h // 2 + int(h * 0.06)
    draw.text((w // 2 - tw // 2, ty), tagline,
              fill=(255, 255, 255, 180), font=tfont)

    img.save(path, "PNG")
    print(f"  ✓ {path}")

# ── Generate all assets ────────────────────────────────────────
print("\n📱 Generating icons…")
make_icon(192,  "public/icons/icon-192.png")
make_icon(512,  "public/icons/icon-512.png")
make_icon(180,  "public/icons/apple-touch-icon.png")

print("\n🖼  Generating splash screens…")
splash_sizes = [
    (1320, 2868, "splash-1320x2868.png"),   # iPhone 16 Pro Max
    (1206, 2622, "splash-1206x2622.png"),   # iPhone 16 Pro
    (1290, 2796, "splash-1290x2796.png"),   # iPhone 15 Plus / 14 Pro Max
    (1179, 2556, "splash-1179x2556.png"),   # iPhone 15 / 14 Pro
    (1170, 2532, "splash-1170x2532.png"),   # iPhone 14 / 13 / 12
    (750,  1334, "splash-750x1334.png"),    # iPhone SE / 8
]
for w, h, name in splash_sizes:
    make_splash(w, h, f"public/splash/{name}")

print("\n✅  All assets generated successfully!\n")
