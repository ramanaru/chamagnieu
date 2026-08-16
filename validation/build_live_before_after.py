#!/usr/bin/env python3
"""Compose true LIVE WEB VIEWER screenshots into labelled before/after proofs."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PAIRS = (
    ("01_facade_before_after.png", "facade.jpg", "facade.png", "FAÇADE"),
    ("02_garden_before_after.png", "garden.jpg", "garden.png", "JARDIN / VÉGÉTATION"),
    ("03_driveway_before_after.png", "exterior-ground.jpg", "exterior-ground.png", "SOLS EXTÉRIEURS"),
    ("04_living_before_after.png", "living.jpg", "living.png", "SÉJOUR"),
    ("05_floor_before_after.png", "interior-floor-materials.jpg", "interior-floor-materials.png", "SOL INTÉRIEUR"),
    ("06_materials_before_after.png", "kitchen.jpg", "kitchen.png", "MATÉRIAUX / CUISINE"),
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for name in names:
        if name.exists():
            return ImageFont.truetype(str(name), size)
    return ImageFont.load_default()


def fit(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def compose(before: Path, after: Path, output: Path, title: str) -> None:
    width, height, header = 1440, 900, 104
    panel_w = width // 2
    body_h = height - header
    left = fit(Image.open(before).convert("RGB"), (panel_w, body_h))
    right = fit(Image.open(after).convert("RGB"), (panel_w, body_h))
    canvas = Image.new("RGB", (width, height), "#151a16")
    canvas.paste(left, (0, header))
    canvas.paste(right, (panel_w, header))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, width, header), fill="#202720")
    draw.rectangle((panel_w - 2, 0, panel_w + 2, height), fill="#f3a352")
    draw.text((24, 13), f"{title} — VRAIE SCÈNE WEB", font=font(26, True), fill="#f8f3ea")
    draw.text((24, 57), "AVANT · V18-LIVE-SYNC-4", font=font(20, True), fill="#cbd1c5")
    draw.text((panel_w + 24, 57), "APRÈS · V18-WEB-REALISM-1", font=font(20, True), fill="#ffb774")
    source = "SOURCE = LIVE WEB VIEWER"
    source_font = font(17, True)
    bbox = draw.textbbox((0, 0), source, font=source_font)
    badge_w = bbox[2] - bbox[0] + 28
    badge_h = bbox[3] - bbox[1] + 18
    for x in (18, panel_w + 18):
        y = height - badge_h - 16
        draw.rounded_rectangle((x, y, x + badge_w, y + badge_h), radius=10, fill="#101510df", outline="#ffffff55", width=2)
        draw.text((x + 14, y + 7), source, font=source_font, fill="#ffffff")
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent / "live_before_after")
    args = parser.parse_args()
    before_dir = args.root / "before"
    after_dir = args.root / "after"
    failures: list[str] = []
    for output_name, before_name, after_name, title in PAIRS:
        before = before_dir / before_name
        after = after_dir / after_name
        if not before.exists() or not after.exists():
            failures.append(f"{output_name}:missing={before if not before.exists() else after}")
            continue
        compose(before, after, args.root / output_name, title)
    if failures:
        print("BEFORE_AFTER_BUILD=FAIL " + " ".join(failures))
        return 1
    print(f"BEFORE_AFTER_BUILD=PASS composites={len(PAIRS)} source=LIVE_WEB_VIEWER size=1440x900")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
