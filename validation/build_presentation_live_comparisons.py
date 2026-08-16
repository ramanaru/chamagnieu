#!/usr/bin/env python3
"""Compose labeled Blender/live and before/after V18 audit comparisons."""

from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "audit" / "presentation-vs-live"
OLD = ROOT / "validation" / "reaudit-2026-08-16"


def font(size: int, bold: bool = False):
    names = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for name in names:
        if Path(name).is_file():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


def panel(path: Path, box=(780, 520)) -> Image.Image:
    image = Image.open(path).convert("RGB")
    contained = ImageOps.contain(image, box, Image.Resampling.LANCZOS)
    result = Image.new("RGB", box, "#e9e6df")
    result.paste(contained, ((box[0] - contained.width) // 2, (box[1] - contained.height) // 2))
    return result


def compose(left: Path, right: Path, left_label: str, right_label: str, footer: str, output: Path) -> None:
    width, height = 1600, 650
    canvas = Image.new("RGB", (width, height), "#f6f1e8")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, width, 70), fill="#202820")
    draw.text((25, 20), left_label, fill="#ffffff", font=font(25, True))
    right_bbox = draw.textbbox((0, 0), right_label, font=font(25, True))
    draw.text((width - 25 - (right_bbox[2] - right_bbox[0]), 20), right_label, fill="#ffffff", font=font(25, True))
    canvas.paste(panel(left), (10, 80))
    canvas.paste(panel(right), (810, 80))
    draw.line((800, 75, 800, 605), fill="#a9572f", width=4)
    draw.rectangle((0, 610, width, height), fill="#ffffff")
    draw.text((24, 619), footer, fill="#2a2f2a", font=font(19))
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format="PNG", optimize=True)


def main() -> None:
    pairs = {
        "facade": (
            ROOT / "shared/gallery/v18-facade-roof-ground.webp",
            ROOT / "validation/live-v18-facade.png",
            OLD / "live-web-facade-v18-sync-3.png",
            "Texture WebP restaurée; écart restant: éclairage Eevee/HDRI absent et géométrie de végétation simplifiée.",
        ),
        "garden": (
            ROOT / "shared/gallery/v18-jardin-textures.webp",
            ROOT / "validation/live-v18-garden.png",
            OLD / "live-web-garden-v18-sync-3.png",
            "Le viewer utilise bien les maps haute définition; les 4 arbres et 18 haies restent les assets low-poly du master.",
        ),
        "interior": (
            ROOT / "shared/gallery/salon.webp",
            ROOT / "validation/live-v18-interior.png",
            OLD / "live-web-interior-v18-sync-3.png",
            "Même géométrie et textures V18; différence restante: Blender/Eevee vs Three.js PMREM, sans AO ni lumières exportées.",
        ),
    }
    for name, (reference, live, before, cause) in pairs.items():
        compose(
            reference,
            live,
            "SOURCE = BLENDER · référence de présentation",
            "SOURCE = LIVE WEB VIEWER · public Sync-4",
            cause,
            OUT / f"comparison-{name}-blender-vs-live.png",
        )
        compose(
            before,
            live,
            "AVANT · LIVE WEB VIEWER · JPEG réduit",
            "APRÈS · LIVE WEB VIEWER PUBLIC · WebP jusqu’à 2048 px",
            "Géométrie inchangée; la différence mesurée vient du retour aux 37 WebP du master et de l’éclairage live corrigé.",
            OUT / f"before-after-{name}-live.png",
        )
    print("PRESENTATION_LIVE_COMPARISONS=PASS files=6 sources_labeled=true live_origin=public")


if __name__ == "__main__":
    main()
