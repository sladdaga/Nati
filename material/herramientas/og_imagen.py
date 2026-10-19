"""Genera las imágenes de vista previa para redes sociales (1200x630).

Uso: python og_imagen.py <logo.png> <salida.jpg> "<título>" "<subtítulo>" ["<antetítulo>"]
"""
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1200, 630
FONTS = 'C:/Windows/Fonts/'
PRIMARY_DARK, PRIMARY = (16, 55, 47), (23, 75, 63)
LIGHT_GREEN, WHITE = (203, 227, 213), (255, 255, 255)

def fondo():
    bg = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(bg)
    for x in range(W):
        t = x / (W - 1)
        d.line([(x, 0), (x, H)], fill=tuple(round(a + (b - a) * t) for a, b in zip(PRIMARY_DARK, (30, 92, 77))))
    # halo detrás del logo
    halo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(halo).ellipse([40, 55, 560, 575], fill=90)
    halo = halo.filter(ImageFilter.GaussianBlur(70))
    bg = Image.composite(Image.new('RGB', (W, H), (60, 130, 105)), bg, halo)
    # franja tricolor inferior
    d = ImageDraw.Draw(bg)
    for i, c in enumerate([(0, 140, 69), (244, 245, 240), (205, 33, 42)]):
        d.rectangle([i * W // 3, H - 14, (i + 1) * W // 3, H], fill=c)
    return bg

def main():
    logo_path, out, title, subtitle = sys.argv[1:5]
    eyebrow = sys.argv[5] if len(sys.argv) > 5 else ''
    img = fondo()

    # logo circular con borde blanco y sombra
    size = 380
    logo = Image.open(logo_path).convert('RGBA').resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size, size), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size - 1, size - 1], fill=255)
    disc = Image.new('RGBA', (size + 24, size + 24), (0, 0, 0, 0))
    ImageDraw.Draw(disc).ellipse([0, 0, size + 23, size + 23], fill=WHITE)
    disc.paste(logo, (12, 12), Image.composite(logo.getchannel('A'), Image.new('L', (size, size), 0), mask))
    shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).ellipse([102, 133, 102 + size + 24, 133 + size + 24], fill=(0, 0, 0, 110))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    img = Image.alpha_composite(img.convert('RGBA'), shadow)
    img.alpha_composite(disc, (100, (H - size - 24) // 2 - 6))

    d = ImageDraw.Draw(img)
    x = 560
    f_eyebrow = ImageFont.truetype(FONTS + 'seguisb.ttf', 24)
    f_title = ImageFont.truetype(FONTS + 'segoeuib.ttf', 66)
    f_sub = ImageFont.truetype(FONTS + 'segoeui.ttf', 32)
    lines = title.split('|')
    y = 190 if eyebrow else 215
    if eyebrow:
        d.text((x, y), eyebrow.upper(), font=f_eyebrow, fill=LIGHT_GREEN)
        y += 48
    for i, line in enumerate(lines):
        d.text((x, y), line, font=f_title, fill=WHITE if i == 0 else (143, 217, 176))
        y += 78
    # mini franja tricolor
    y += 8
    for i, c in enumerate([(0, 140, 69), WHITE, (205, 33, 42)]):
        d.rectangle([x + i * 44, y, x + (i + 1) * 44, y + 7], fill=c)
    y += 30
    for line in subtitle.split('|'):
        d.text((x, y), line, font=f_sub, fill=(213, 228, 220))
        y += 44

    img.convert('RGB').save(out, 'JPEG', quality=88, optimize=True, progressive=True)
    print(out)

main()
