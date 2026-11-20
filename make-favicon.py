"""Regenerate favicon.ico, favicon.png and apple-touch-icon-v2.png from interlock-rounded.png.

The rounded interlock design (black on white) becomes the site's accent blue.
Requires Pillow:  python3 make-favicon.py
"""
from PIL import Image

BLUE = (31, 111, 235)  # --accent

src = Image.open("interlock-rounded.png").convert("L")
# Dark pixels are the shape: use darkness as the alpha mask (keeps smooth edges).
alpha = src.point(lambda v: 255 - v)
icon = Image.new("RGBA", src.size, BLUE + (0,))
icon.putalpha(alpha)
icon = icon.crop(icon.getbbox())


def fit(size, pad, bg=None):
    inner = int(size * (1 - 2 * pad))
    scale = inner / max(icon.size)
    img = icon.resize((round(icon.width * scale), round(icon.height * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    canvas.alpha_composite(img, ((size - img.width) // 2, (size - img.height) // 2))
    return canvas


fit(512, 0.08, (255, 255, 255, 255)).convert("RGB").save("favicon.png")
fit(180, 0.14, (255, 255, 255, 255)).convert("RGB").save("apple-touch-icon-v2.png")
fit(256, 0.02).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
print("wrote favicon.ico, favicon.png, apple-touch-icon-v2.png")
