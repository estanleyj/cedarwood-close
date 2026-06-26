from PIL import Image, ImageDraw, ImageFilter
import math
import random


random.seed(18)


def lerp(a, b, t):
    return int(a + (b - a) * t)


def mix(c1, c2, t):
    return tuple(lerp(a, b, t) for a, b in zip(c1, c2))


def make_hero(path):
    width, height = 2200, 1400
    base = Image.new("RGB", (width, height), "#1f2f29")
    px = base.load()

    top = (22, 44, 40)
    middle = (95, 82, 58)
    bottom = (216, 201, 167)

    for y in range(height):
        v = y / (height - 1)
        if v < 0.55:
            color = mix(top, middle, v / 0.55)
        else:
            color = mix(middle, bottom, (v - 0.55) / 0.45)
        for x in range(width):
            wave = math.sin((x * 0.011) + (y * 0.002)) * 9
            fine = random.randint(-8, 8)
            warm = math.sin((x * 0.021) + 5) * 5
            r = max(0, min(255, color[0] + int(wave + fine + warm)))
            g = max(0, min(255, color[1] + int(wave * 0.5 + fine * 0.55)))
            b = max(0, min(255, color[2] + int(fine * 0.4 - warm)))
            px[x, y] = (r, g, b)

    draw = ImageDraw.Draw(base, "RGBA")

    # Cedar-grain bands.
    for i in range(95):
        x = random.randint(-120, width + 120)
        amp = random.uniform(14, 58)
        period = random.uniform(0.004, 0.011)
        phase = random.uniform(0, math.tau)
        color = random.choice(
            [
                (239, 224, 184, 22),
                (44, 68, 55, 40),
                (148, 104, 62, 34),
                (12, 28, 25, 48),
            ]
        )
        points = []
        for y in range(-80, height + 90, 16):
            drift = math.sin(y * period + phase) * amp
            points.append((x + drift, y))
        draw.line(points, fill=color, width=random.randint(3, 11))

    # Long diagonal cedar silhouettes.
    for i in range(34):
        start_x = random.randint(-300, width)
        start_y = random.randint(-120, int(height * 0.55))
        length = random.randint(780, 1700)
        angle = random.uniform(0.42, 0.68)
        end_x = start_x + math.cos(angle) * length
        end_y = start_y + math.sin(angle) * length
        draw.line(
            [(start_x, start_y), (end_x, end_y)],
            fill=random.choice([(10, 27, 25, 72), (236, 220, 175, 28), (51, 82, 68, 54)]),
            width=random.randint(5, 17),
        )

    # Subtle ring geometry, kept low contrast so text remains legible.
    cx, cy = int(width * 0.77), int(height * 0.58)
    for radius in range(120, 950, 56):
        alpha = max(8, 34 - radius // 36)
        bbox = [cx - radius, cy - radius, cx + radius, cy + radius]
        draw.ellipse(bbox, outline=(245, 229, 190, alpha), width=2)

    # Darken the left side for copy.
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for x in range(width):
        t = 1 - min(1, x / (width * 0.7))
        alpha = int(172 * (t**1.65))
        od.line([(x, 0), (x, height)], fill=(7, 19, 18, alpha))
    base = Image.alpha_composite(base.convert("RGBA"), overlay)

    vignette = Image.new("L", (width, height), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-380, -320, width + 380, height + 420), fill=255)
    vignette = Image.eval(vignette.filter(ImageFilter.GaussianBlur(130)), lambda p: 255 - p)
    dark = Image.new("RGBA", (width, height), (0, 0, 0, 86))
    base = Image.composite(dark, base, vignette)

    base = base.convert("RGB")
    base.save(path, quality=92, optimize=True)


def make_favicon(path):
    size = 512
    img = Image.new("RGBA", (size, size), (20, 37, 32, 255))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([42, 42, size - 42, size - 42], radius=78, fill=(24, 54, 47, 255))
    draw.arc([112, 118, 400, 406], 128, 316, fill=(223, 199, 148, 255), width=30)
    draw.arc([154, 158, 358, 362], 130, 314, fill=(236, 226, 200, 255), width=22)
    draw.line([164, 256, 348, 256], fill=(223, 199, 148, 255), width=26)
    img.save(path)


if __name__ == "__main__":
    make_hero("assets/cedarwood-hero.jpg")
    make_favicon("assets/favicon.png")
