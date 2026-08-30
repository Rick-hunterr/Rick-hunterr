#!/usr/bin/env python3

from pathlib import Path
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont, ImageFilter


# ============================================================
# CONFIGURACIÓN
# ============================================================

WIDTH = 1536
HEIGHT = 768

FRAMES = 40
FRAME_DURATION = 90  # milisegundos

OUTPUT = (
    Path.home()
    / "Dev"
    / "GitHub"
    / "Rick-hunterr"
    / "profile_animation.gif"
)


# ============================================================
# FUENTES
# ============================================================

FONT_PATHS = {
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


def get_font(kind: str, size: int):
    for path in FONT_PATHS[kind]:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)

    raise FileNotFoundError(
        f"No se encontró una fuente válida para '{kind}'."
    )


FONT_NAME = get_font("bold", 62)
FONT_MAIN = get_font("bold", 32)
FONT_SUB = get_font("regular", 23)
FONT_MONO = get_font("mono", 16)
FONT_SMALL = get_font("mono", 14)
FONT_PROJECT = get_font("bold", 40)


# ============================================================
# COLORES
# ============================================================

BG_TOP = (7, 11, 17)
BG_BOTTOM = (18, 27, 38)

WHITE = (240, 244, 248)
LIGHT = (194, 207, 219)
ACCENT = (120, 190, 235)
MUTED = (125, 145, 162)

GRID = (90, 125, 155, 20)
NETWORK = (80, 150, 205, 90)
NODE = (125, 200, 240)
PANEL = (24, 33, 44, 205)


# ============================================================
# RED DE NODOS
# ============================================================

NODES = [
    (980, 115),
    (1095, 180),
    (1220, 95),
    (1340, 165),
    (1040, 315),
    (1160, 365),
    (1300, 300),
    (1420, 395),
    (970, 500),
    (1100, 555),
    (1245, 490),
    (1380, 560),
    (1040, 675),
    (1200, 650),
    (1340, 690),
]

EDGES = [
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


# ============================================================
# FONDO
# ============================================================

def create_background():
    image = Image.new("RGBA", (WIDTH, HEIGHT))

    draw = ImageDraw.Draw(image)

    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)

        r = int(BG_TOP[0] * (1 - t) + BG_BOTTOM[0] * t)
        g = int(BG_TOP[1] * (1 - t) + BG_BOTTOM[1] * t)
        b = int(BG_TOP[2] * (1 - t) + BG_BOTTOM[2] * t)

        draw.line(
            (0, y, WIDTH, y),
            fill=(r, g, b, 255),
        )

    # Cuadrícula
    spacing = 48

    for x in range(0, WIDTH, spacing):
        draw.line(
            (x, 0, x, HEIGHT),
            fill=GRID,
            width=1,
        )

    for y in range(0, HEIGHT, spacing):
        draw.line(
            (0, y, WIDTH, y),
            fill=GRID,
            width=1,
        )

    return image


# ============================================================
# RED
# ============================================================

def draw_network(image, frame_index):
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    # Conexiones
    for a, b in EDGES:
        draw.line(
            (NODES[a], NODES[b]),
            fill=NETWORK,
            width=2,
        )

    # Nodo activo
    active_node = frame_index % len(NODES)

    pulse = (
        math.sin(
            (frame_index / FRAMES) * math.pi * 2
        )
        + 1
    ) / 2

    # Nodos
    for index, (x, y) in enumerate(NODES):

        radius = 5

        if index == active_node:
            radius = 6 + int(pulse * 3)

            ring = 18 + int(pulse * 10)

            draw.ellipse(
                (
                    x - ring,
                    y - ring,
                    x + ring,
                    y + ring,
                ),
                outline=(100, 185, 235, 80),
                width=2,
            )

        draw.ellipse(
            (
                x - radius,
                y - radius,
                x + radius,
                y + radius,
            ),
            fill=(130, 205, 245, 220),
        )

    # Pulsos viajando por la red
    pulse_edges = [0, 4, 8, 12, 16, 21]

    travel_base = frame_index / FRAMES

    for offset, edge_index in enumerate(pulse_edges):

        a, b = EDGES[edge_index]

        t = (travel_base + offset * 0.14) % 1.0

        x1, y1 = NODES[a]
        x2, y2 = NODES[b]

        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t

        draw.ellipse(
            (
                x - 4,
                y - 4,
                x + 4,
                y + 4,
            ),
            fill=(150, 220, 255, 230),
        )

    glow = layer.filter(
        ImageFilter.GaussianBlur(6)
    )

    image.alpha_composite(glow)
    image.alpha_composite(layer)


# ============================================================
# DETALLES TERMINAL
# ============================================================

def draw_terminal(image, frame_index):
    draw = ImageDraw.Draw(image)

    lines = [
        "$ whoami",
        "developer",
        "",
        "$ focus --now",
        "cybersecurity",
        "software",
        "",
        "$ system.status",
        "learning...",
    ]

    visible = min(
        len(lines),
        2 + frame_index // 5,
    )

    x = 1030
    y = 215

    for index, line in enumerate(lines[:visible]):

        if line == "":
            y += 10
            continue

        alpha = 150

        if "$" in line:
            alpha = 200

        draw.text(
            (x, y),
            line,
            font=FONT_MONO,
            fill=(
                ACCENT[0],
                ACCENT[1],
                ACCENT[2],
                alpha,
            ),
        )

        y += 27


# ============================================================
# TEXTO PRINCIPAL
# ============================================================

def draw_text(image):

    draw = ImageDraw.Draw(image)

    draw.text(
        (105, 95),
        "RICK-HUNTERR // SECURITY & DEV",
        font=FONT_SMALL,
        fill=(150, 170, 185, 220),
    )

    draw.text(
        (105, 175),
        "PABLO DANIEL SANTELLAN",
        font=FONT_NAME,
        fill=WHITE,
    )

    draw.text(
        (108, 270),
        "CYBERSECURITY",
        font=FONT_MAIN,
        fill=ACCENT,
    )

    draw.text(
        (108, 315),
        "SOFTWARE DEVELOPMENT",
        font=FONT_MAIN,
        fill=WHITE,
    )

    draw.text(
        (108, 360),
        "GAME DEVELOPMENT",
        font=FONT_MAIN,
        fill=LIGHT,
    )

    draw.line(
        (108, 415, 820, 415),
        fill=(100, 165, 220, 120),
        width=2,
    )

    draw.text(
        (108, 445),
        "Linux · Python · Git · Databases · Godot",
        font=FONT_SUB,
        fill=LIGHT,
    )

    draw.text(
        (108, 690),
        "BUILDING · LEARNING · IMPROVING",
        font=FONT_SMALL,
        fill=MUTED,
    )

    # Proyecto destacado
    draw.text(
        (1080, 55),
        "FEATURED PROJECT",
        font=FONT_SMALL,
        fill=ACCENT,
    )

    draw.text(
        (1080, 92),
        "SEÑALES",
        font=FONT_PROJECT,
        fill=WHITE,
    )

    draw.text(
        (1082, 142),
        "EL UMBRAL DEL BARRIO",
        font=FONT_SMALL,
        fill=LIGHT,
    )

    draw.line(
        (1082, 178, 1390, 178),
        fill=(100, 165, 220, 85),
        width=1,
    )

    draw.text(
        (1080, 700),
        "GODOT 4 · 2D · NARRATIVE RPG",
        font=FONT_SMALL,
        fill=MUTED,
    )


# ============================================================
# LÍNEA DE ESCANEO
# ============================================================

def draw_scanline(image, frame_index):

    overlay = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(overlay)

    y = int(
        (frame_index / (FRAMES - 1))
        * (HEIGHT - 1)
    )

    draw.line(
        (0, y, WIDTH, y),
        fill=(120, 200, 240, 30),
        width=2,
    )

    image.alpha_composite(overlay)


# ============================================================
# DECORACIÓN
# ============================================================

def draw_decorations(image):

    draw = ImageDraw.Draw(image)

    # Barra lateral
    draw.rectangle(
        (76, 88, 81, HEIGHT - 88),
        fill=(100, 180, 230, 150),
    )

    # Esquina superior
    draw.line(
        (52, 52, 145, 52),
        fill=(105, 145, 180, 70),
        width=2,
    )

    draw.line(
        (52, 52, 52, 145),
        fill=(105, 145, 180, 70),
        width=2,
    )

    # Esquina inferior
    draw.line(
        (
            WIDTH - 145,
            HEIGHT - 52,
            WIDTH - 52,
            HEIGHT - 52,
        ),
        fill=(105, 145, 180, 70),
        width=2,
    )

    draw.line(
        (
            WIDTH - 52,
            HEIGHT - 145,
            WIDTH - 52,
            HEIGHT - 52,
        ),
        fill=(105, 145, 180, 70),
        width=2,
    )


# ============================================================
# FRAME
# ============================================================

def create_frame(frame_index):

    image = create_background()

    draw_decorations(image)
    draw_network(image, frame_index)
    draw_terminal(image, frame_index)
    draw_text(image)
    draw_scanline(image, frame_index)

    return image.convert("P", palette=Image.Palette.ADAPTIVE)


# ============================================================
# MAIN
# ============================================================

def main():

    try:
        OUTPUT.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        frames = []

        print("Generando frames...")

        for index in range(FRAMES):

            print(
                f"\rFrame {index + 1}/{FRAMES}",
                end="",
                flush=True,
            )

            frames.append(
                create_frame(index)
            )

        print()
        print("Guardando GIF...")

        frames[0].save(
            OUTPUT,
            save_all=True,
            append_images=frames[1:],
            duration=FRAME_DURATION,
            loop=0,
            optimize=True,
        )

        size_kb = OUTPUT.stat().st_size / 1024

        print()
        print("======================================")
        print(" GIF generado correctamente")
        print("======================================")
        print(f"Archivo: {OUTPUT}")
        print(f"Tamaño : {WIDTH}x{HEIGHT}")
        print(f"Frames : {FRAMES}")
        print(f"Peso   : {size_kb:.1f} KB")
        print()

        return 0

    except Exception as error:

        print()
        print(
            f"Error al generar el GIF: {error}",
            file=sys.stderr,
        )

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
