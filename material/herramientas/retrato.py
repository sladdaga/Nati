"""Retrato unificado: quita el fondo, encuadra cabeza y hombros y aplica un fondo común.

Uso: python retrato.py <entrada> <salida.jpg> <cabeza_arriba_y> <menton_y> <centro_x> [recorte_inferior_y]
Coordenadas en píxeles de la foto original.
"""
import os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter
from rembg import remove, new_session

W, H = 600, 750            # tamaño final (4:5)
HEAD_RATIO = float(os.environ.get('HEAD_RATIO', 0.36))          # alto de la cabeza respecto del alto del retrato
TOP_RATIO = float(os.environ.get('TOP_RATIO', 0.12))           # margen sobre la cabeza

def fondo():
    """Degradado verde suave común a todos los retratos."""
    bg = Image.new('RGB', (W, H))
    top, bottom = (246, 249, 247), (205, 224, 212)
    d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(top, bottom)))
    # halo claro detrás de la cabeza
    halo = Image.new('L', (W, H), 0)
    ImageDraw.Draw(halo).ellipse([W * .1, H * .02, W * .9, H * .62], fill=150)
    halo = halo.filter(ImageFilter.GaussianBlur(90))
    return Image.composite(Image.new('RGB', (W, H), (255, 255, 255)), bg, halo)

def main():
    src, out, head_top, chin, cx = sys.argv[1], sys.argv[2], *map(float, sys.argv[3:6])
    img = Image.open(src).convert('RGB')
    cut_y = float(sys.argv[6]) if len(sys.argv) > 6 else img.height

    matting = os.environ.get('MATTING', '0') == '1'
    person = remove(img, session=new_session(os.environ.get('MODEL', 'birefnet-portrait')), alpha_matting=matting,
                    alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=15,
                    alpha_matting_erode_size=8)
    person = person.crop((0, 0, img.width, int(cut_y)))

    s = HEAD_RATIO * H / (chin - head_top)
    # mismo tamaño de cabeza en todos los retratos; el esfumado inferior cubre el corte del cuerpo
    person = person.resize((round(person.width * s), round(person.height * s)), Image.LANCZOS)
    # bordes suaves: contrae apenas el contorno (elimina el halo del fondo viejo) y lo difumina
    feather = float(os.environ.get('FEATHER', 2.5))
    if feather:
        a = person.getchannel('A').filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(feather))
        person.putalpha(a)
    # si el cuerpo toca los bordes laterales de la foto original, esfumar ese corte
    ramp = int(os.environ.get('SIDE_FADE', 70))
    if ramp:
        side = Image.new('L', (person.width, 1), 255)
        for xx in range(min(ramp, person.width // 2)):
            v = round(255 * xx / ramp)
            side.putpixel((xx, 0), v)
            side.putpixel((person.width - 1 - xx, 0), v)
        person.putalpha(ImageChops.multiply(person.getchannel('A'), side.resize(person.size)))
        # mismo esfumado en el borde inferior (fotos en primer plano)
        bottom = Image.new('L', (1, person.height), 255)
        for yy in range(min(ramp, person.height // 2)):
            bottom.putpixel((0, person.height - 1 - yy), round(255 * yy / ramp))
        person.putalpha(ImageChops.multiply(person.getchannel('A'), bottom.resize(person.size)))
    x = round(W / 2 - cx * s)
    y = round(TOP_RATIO * H - head_top * s)

    canvas = fondo().convert('RGBA')
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    layer.paste(person, (x, y))
    # esfumado inferior común: retrato en plano de busto
    fade_from, fade_to = float(os.environ.get('FADE_FROM', .58)), float(os.environ.get('FADE_TO', .74))
    grad = Image.new('L', (1, H))
    for yy in range(H):
        t = (yy / H - fade_from) / (fade_to - fade_from)
        grad.putpixel((0, yy), round(255 * (1 - min(max(t, 0), 1))))
    alpha = ImageChops.multiply(layer.getchannel('A'), grad.resize((W, H)))
    layer.putalpha(alpha)
    canvas = Image.alpha_composite(canvas, layer).convert('RGB').crop((0, 0, W, W))  # cuadrado, como se muestra en la tarjeta
    canvas.save(out, 'JPEG', quality=86, optimize=True, progressive=True)
    print(out, 'escala', round(s, 2))

main()
