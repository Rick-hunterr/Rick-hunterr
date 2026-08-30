#!/usr/bin/env python3
"""
Banner de perfil de GitHub para Rick-hunterr.

Enfoque visual:
- Cybersecurity
- Software Development
- Game Development

Salida:
    ~/Dev/GitHub/Rick-hunterr/profile_banner.png

Requisito:
    Pillow

Instalación:
    sudo apt install python3-pil
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# CONFIGURACIÓN
# ============================================================

WIDTH = 1536
HEIGHT = 768

OUTPUT_DIR = Path.home() / "Dev" / "GitHub" / "Rick-hunterr"
OUTPUT_FILE = OUTPUT_DIR / "profile_banner.png"

FONT_CANDIDATES = {
    "bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    ],
    "regular": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ],
    "mono": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ],
}


# ============================================================
# UTILIDADES
# ============================================================

def find_font(
    candidates: Iterable[str],
    size: int,
) -> ImageFont.FreeTypeFont:
    """Busca la primera fuente disponible."""
    for path in candidates:
        if os.path.isfile(path):
            return ImageFont.truetype(path, size=size)

    raise FileNotFoundError(
        "No se encontró ninguna fuente compatible:\n"
        + "\n".join(candidates)
    )


def text_size(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
) -> tuple[int, int]:
    """Devuelve el tamaño del texto."""
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


# ============================================================
# FONDO
# ============================================================

def create_background() -> Image.Image:
    """Genera un fondo oscuro con degradado y cuadrícula."""
    image = Image.new("RGBA", (WIDTH, HEIGHT), (8, 12, 18, 255))

    # Degradado vertical
    gradient = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    top = (8, 12, 18)
    bottom = (18, 26, 36)

    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)

        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)

        draw.line(
            [(0, y), (WIDTH, y)],
            fill=(r, g, b, 255),
        )

    image = Image.alpha_composite(image, gradient)

    # Cuadrícula tecnológica
    grid = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)

    spacing = 48

    for x in range(0, WIDTH, spacing):
        gd.line(
            [(x, 0), (x, HEIGHT)],
            fill=(90, 130, 165, 18),
            width=1,
        )

    for y in range(0, HEIGHT, spacing):
        gd.line(
            [(0, y), (WIDTH, y)],
            fill=(90, 130, 165, 16),
            width=1,
        )

    image = Image.alpha_composite(image, grid)

    return image


# ============================================================
# RED DE SEGURIDAD
# ============================================================

def draw_network(image: Image.Image) -> None:
    """
    Genera una red de nodos inspirada en:
    redes, sistemas y ciberseguridad.
    """
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    nodes = [
        (980, 105),
        (1100, 180),
        (1230, 90),
        (1340, 165),
        (1030, 310),
        (1160, 360),
        (1290, 300),
        (1410, 390),
        (970, 500),
        (1100, 540),
        (1240, 485),
        (1370, 550),
        (1040, 675),
        (1190, 650),
        (1330, 690),
    ]

    edges = [
        (0, 1),
        (0, 4),
        (1, 2),
        (1, 4),
        (1, 5),
        (2, 3),
        (2, 6),
        (3, 6),
        (3, 7),
        (4, 5),
        (4, 8),
        (5, 6),
        (5, 9),
        (6, 7),
        (6, 10),
        (7, 11),
        (8, 9),
        (8, 12),
        (9, 10),
        (9, 13),
        (10, 11),
        (10, 14),
        (11, 14),
        (12, 13),
        (13, 14),
    ]

    # Líneas
    for start, end in edges:
        draw.line(
            [nodes[start], nodes[end]],
            fill=(85, 155, 205, 95),
            width=2,
        )

    # Nodos
    for index, (x, y) in enumerate(nodes):
        if index % 4 == 0:
            fill = (100, 200, 235, 220)
        else:
            fill = (120, 175, 215, 185)

        draw.ellipse(
            (x - 6, y - 6, x + 6, y + 6),
            fill=fill,
        )

        draw.ellipse(
            (x - 18, y - 18, x + 18, y + 18),
            outline=(90, 160, 215, 55),
            width=2,
        )

    glow = overlay.filter(ImageFilter.GaussianBlur(5))

    image.alpha_composite(glow)
    image.alpha_composite(overlay)


# ============================================================
# DETALLES DE TERMINAL / CÓDIGO
# ============================================================

def draw_code_details(image: Image.Image) -> None:
    """Añade pequeños detalles de terminal sin saturar el diseño."""
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font = find_font(FONT_CANDIDATES["mono"], 14)

    lines = [
        "$ whoami",
        "developer",
        "$ focus --now",
        "cybersecurity",
        "software",
        "game-development",
        "$ status",
        "learning...",
    ]

    x = 1010
    y = 220

    for index, line in enumerate(lines):
        alpha = 75 if index % 3 else 110

        draw.text(
            (x, y),
            line,
            font=font,
            fill=(135, 180, 210, alpha),
        )

        y += 23

    image.alpha_composite(overlay)


# ============================================================
# DECORACIÓN
# ============================================================

def draw_decorations(image: Image.Image) -> None:
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    accent = (100, 180, 230, 150)
    muted = (110, 140, 165, 65)

    # Línea lateral izquierda
    draw.rectangle(
        (76, 88, 81, HEIGHT - 88),
        fill=accent,
    )

    # Marcas pequeñas
    for y in (90, 180, 625, 680):
        draw.line(
            [(81, y), (112, y)],
            fill=accent,
            width=2,
        )

    # Esquinas
    draw.line(
        [(52, 52), (145, 52)],
        fill=muted,
        width=2,
    )

    draw.line(
        [(52, 52), (52, 145)],
        fill=muted,
        width=2,
    )

    draw.line(
        [(WIDTH - 145, HEIGHT - 52), (WIDTH - 52, HEIGHT - 52)],
        fill=muted,
        width=2,
    )

    draw.line(
        [(WIDTH - 52, HEIGHT - 145), (WIDTH - 52, HEIGHT - 52)],
        fill=muted,
        width=2,
    )

    image.alpha_composite(overlay)


# ============================================================
# TEXTO
# ============================================================

def draw_text_content(image: Image.Image) -> None:
    draw = ImageDraw.Draw(image)

    font_name = find_font(FONT_CANDIDATES["bold"], 68)
    font_category = find_font(FONT_CANDIDATES["bold"], 32)
    font_description = find_font(FONT_CANDIDATES["regular"], 23)
    font_small = find_font(FONT_CANDIDATES["mono"], 15)
    font_project = find_font(FONT_CANDIDATES["bold"], 39)
    font_project_small = find_font(FONT_CANDIDATES["regular"], 19)

    white = (239, 243, 247, 255)
    light = (195, 205, 216, 255)
    accent = (125, 190, 235, 255)
    muted = (130, 150, 168, 220)

    # Identificador
    draw.text(
        (104, 94),
        "RICK-HUNTERR // SECURITY & DEV",
        font=font_small,
        fill=(145, 165, 180, 210),
    )

    # Nombre
    draw.text(
        (108, 175),
        "PABLO DANIEL SANTELLAN",
        font=font_name,
        fill=white,
    )

    # Enfoque principal
    draw.text(
        (111, 278),
        "CYBERSECURITY",
        font=font_category,
        fill=accent,
    )

    draw.text(
        (111, 323),
        "SOFTWARE DEVELOPMENT  ·  GAME DEVELOPMENT",
        font=font_category,
        fill=light,
    )

    # Descripción
    draw.text(
        (111, 378),
        "Linux · Python · Git · Databases · Godot · GDScript",
        font=font_description,
        fill=(175, 190, 204, 255),
    )

    # Divisor
    draw.line(
        [(111, 425), (825, 425)],
        fill=(100, 165, 220, 115),
        width=2,
    )

    # Etiquetas
    tags = [
        "LINUX",
        "PYTHON",
        "GIT",
        "DATABASES",
        "GODOT",
        "GDSCRIPT",
        "CYBERSECURITY",
    ]

    x = 111
    y = 460

    for tag in tags:
        tw, _ = text_size(draw, tag, font_small)

        padding_x = 14
        width = tw + padding_x * 2
        height = 34

        if x + width > 850:
            x = 111
            y += 47

        draw.rounded_rectangle(
            (x, y, x + width, y + height),
            radius=7,
            fill=(25, 34, 45, 210),
            outline=(100, 135, 165, 95),
            width=1,
        )

        draw.text(
            (x + padding_x, y + 8),
            tag,
            font=font_small,
            fill=(215, 224, 232, 255),
        )

        x += width + 9

    # Proyecto destacado
    draw.text(
        (1090, 55),
        "FEATURED PROJECT",
        font=font_small,
        fill=accent,
    )

    draw.text(
        (1088, 92),
        "SEÑALES",
        font=font_project,
        fill=white,
    )

    draw.text(
        (1090, 140),
        "EL UMBRAL DEL BARRIO",
        font=font_project_small,
        fill=light,
    )

    draw.line(
        [(1090, 180), (1390, 180)],
        fill=(100, 165, 220, 80),
        width=1,
    )

    draw.text(
        (1090, 704),
        "BUILDING · LEARNING · IMPROVING",
        font=font_small,
        fill=muted,
    )

    draw.text(
        (1110, 665),
        "GODOT 4  ·  2D  ·  NARRATIVE RPG",
        font=font_small,
        fill=muted,
    )


# ============================================================
# EJECUCIÓN
# ============================================================

def main() -> int:
    try:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        image = create_background()

        draw_network(image)
        draw_code_details(image)
        draw_decorations(image)
        draw_text_content(image)

        image.convert("RGB").save(
            OUTPUT_FILE,
            format="PNG",
            optimize=True,
        )

        print()
        print("========================================")
        print(" Banner generado correctamente")
        print("========================================")
        print(f"Archivo : {OUTPUT_FILE}")
        print(f"Tamaño  : {WIDTH}x{HEIGHT}")
        print()

        return 0

    except Exception as error:
        print(f"Error al generar el banner: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
