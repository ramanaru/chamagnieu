#!/usr/bin/env python3
"""Build the two CC0 PBR material pilots used by the Chamagnieu Web viewer.

The script deliberately keeps provider downloads unchanged below ``original``
and writes browser-budget derivatives below ``optimized``.  It can be run more
than once: already downloaded non-empty files are reused, while every output is
recomputed deterministically from the preserved source maps.
"""

from __future__ import annotations

import hashlib
import io
import json
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import requests
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets_external" / "materials"
FACADE_ORIGINAL = ASSETS / "facade" / "white_stucco" / "original"
FACADE_OPTIMIZED = ASSETS / "facade" / "white_stucco" / "optimized"
GRASS_ORIGINAL = ASSETS / "exterior" / "grass005" / "original"
GRASS_TEMP_ROOT = ROOT / "validation" / ".material-pilot-tmp"
GRASS_EXTRACTED = GRASS_TEMP_ROOT / "Grass005_2K-JPG"
GRASS_OPTIMIZED = ASSETS / "exterior" / "grass005" / "optimized"
REPORT_PATH = ROOT / "validation" / "pilot_material_asset_build.json"

USER_AGENT = "Chamagnieu-Asset-Pilot/1.0 (+local-build; CC0-cache)"

FACADE = {
    "provider": "Poly Haven",
    "asset_id": "white_stucco",
    "page_url": "https://polyhaven.com/a/white_stucco",
    "license": "CC0 1.0",
    "license_url": "https://polyhaven.com/license",
    "metadata_url": "https://api.polyhaven.com/info/white_stucco",
    "files_url": "https://api.polyhaven.com/files/white_stucco",
    "physical_dimensions_m": [1.998, 1.998],
    "maps": {
        "color": "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/white_stucco/white_stucco_diff_2k.jpg",
        "normal_gl": "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/white_stucco/white_stucco_nor_gl_2k.jpg",
        "arm": "https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/white_stucco/white_stucco_arm_2k.jpg",
    },
}

GRASS = {
    "provider": "ambientCG",
    "asset_id": "Grass005",
    "page_url": "https://ambientcg.com/a/Grass005",
    "license": "CC0 1.0 Universal",
    "license_url": "https://docs.ambientcg.com/license/",
    "metadata_url": "https://ambientcg.com/api/v3/assets?id=Grass005&include=title,url,tags,dimensions,maps,downloads",
    "archive_url": "https://ambientcg.com/get?file=Grass005_2K-JPG.zip",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def download(url: str, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    reused = destination.exists() and destination.stat().st_size > 0
    if not reused:
        temporary = destination.with_suffix(destination.suffix + ".partial")
        with requests.get(url, headers={"User-Agent": USER_AGENT}, stream=True, timeout=180) as response:
            response.raise_for_status()
            with temporary.open("wb") as handle:
                for chunk in response.iter_content(1024 * 1024):
                    if chunk:
                        handle.write(chunk)
        temporary.replace(destination)
    return {
        "url": url,
        "path": destination.relative_to(ROOT).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
        "reused": reused,
    }


def fetch_json(url: str, destination: Path) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    response.raise_for_status()
    payload = response.json()
    destination.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "url": url,
        "path": destination.relative_to(ROOT).as_posix(),
        "bytes": destination.stat().st_size,
        "sha256": sha256(destination),
        "http_status": response.status_code,
    }


def image_record(path: Path) -> dict:
    with Image.open(path) as image:
        return {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
            "dimensions": list(image.size),
            "mode": image.mode,
            "format": image.format,
        }


def archive_image_record(path: Path, archive: Path) -> dict:
    record = image_record(path)
    record.pop("path", None)
    record["archive_path"] = archive.relative_to(ROOT).as_posix()
    record["archive_member"] = path.relative_to(GRASS_EXTRACTED).as_posix()
    return record


def resize_rgb(source: Path, destination: Path, size: int, quality: int) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("RGB")
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        # PBR textures must remain power-of-two and square for consistent mipmaps.
        if image.size != (size, size):
            image = image.resize((size, size), Image.Resampling.LANCZOS)
        image.save(destination, "WEBP", quality=quality, method=6, exact=True)
    return image_record(destination)


def save_grayscale(source: Path, destination: Path, size: int, quality: int = 90) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        image = image.convert("L").resize((size, size), Image.Resampling.LANCZOS)
        image.save(destination, "WEBP", quality=quality, method=6, exact=True)
    return image_record(destination)


def extract_arm_red(source: Path, destination: Path, size: int) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as image:
        red = image.convert("RGB").getchannel("R").resize((size, size), Image.Resampling.LANCZOS)
        red.save(destination, "WEBP", quality=92, method=6, exact=True)
    return image_record(destination)


def pack_arm(ao_source: Path, roughness_source: Path, destination: Path, size: int) -> dict:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(ao_source) as ao_image, Image.open(roughness_source) as roughness_image:
        ao = ao_image.convert("L").resize((size, size), Image.Resampling.LANCZOS)
        roughness = roughness_image.convert("L").resize((size, size), Image.Resampling.LANCZOS)
        metallic = Image.new("L", (size, size), 0)
        arm = Image.merge("RGB", (ao, roughness, metallic))
        # High-quality WebP keeps AO/roughness gradients stable while removing
        # more than a megabyte from the public payload versus lossless WebP.
        arm.save(destination, "WEBP", quality=92, method=6, exact=True)
    return image_record(destination)


def find_grass_map(parts: list[str]) -> Path:
    candidates = []
    for path in GRASS_EXTRACTED.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        lower = path.name.lower()
        if all(part.lower() in lower for part in parts):
            candidates.append(path)
    if not candidates:
        raise FileNotFoundError(f"Grass005 map not found for tokens {parts!r}")
    return sorted(candidates, key=lambda p: (len(p.name), p.name.lower()))[0]


def main() -> int:
    for directory in (FACADE_ORIGINAL, FACADE_OPTIMIZED, GRASS_ORIGINAL, GRASS_OPTIMIZED):
        directory.mkdir(parents=True, exist_ok=True)

    facade_metadata = [
        fetch_json(FACADE["metadata_url"], FACADE_ORIGINAL / "white_stucco_info.json"),
        fetch_json(FACADE["files_url"], FACADE_ORIGINAL / "white_stucco_files.json"),
    ]
    facade_downloads = {}
    facade_source_paths = {}
    for role, url in FACADE["maps"].items():
        destination = FACADE_ORIGINAL / Path(url).name
        facade_downloads[role] = download(url, destination)
        facade_source_paths[role] = destination

    grass_metadata = fetch_json(GRASS["metadata_url"], GRASS_ORIGINAL / "Grass005_metadata.json")
    grass_archive = GRASS_ORIGINAL / "Grass005_2K-JPG.zip"
    grass_download = download(GRASS["archive_url"], grass_archive)
    if GRASS_TEMP_ROOT.exists():
        shutil.rmtree(GRASS_TEMP_ROOT)
    GRASS_EXTRACTED.mkdir(parents=True)
    with zipfile.ZipFile(grass_archive) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"Grass archive CRC failed at {bad}")
        archive.extractall(GRASS_EXTRACTED)

    grass_sources = {
        "color": find_grass_map(["color"]),
        "normal_gl": find_grass_map(["normalgl"]),
        "roughness": find_grass_map(["roughness"]),
        "ao": find_grass_map(["ambientocclusion"]),
        "displacement": find_grass_map(["displacement"]),
    }
    grass_source_records = {role: archive_image_record(path, grass_archive) for role, path in grass_sources.items()}

    facade_optimized = {
        "color": resize_rgb(facade_source_paths["color"], FACADE_OPTIMIZED / "white_stucco_color_1k.webp", 1024, 84),
        "normal_gl": resize_rgb(facade_source_paths["normal_gl"], FACADE_OPTIMIZED / "white_stucco_normal_gl_1k.webp", 1024, 92),
        "arm": resize_rgb(facade_source_paths["arm"], FACADE_OPTIMIZED / "white_stucco_arm_1k.webp", 1024, 92),
        "ao": extract_arm_red(facade_source_paths["arm"], FACADE_OPTIMIZED / "white_stucco_ao_1k.webp", 1024),
    }
    grass_optimized = {
        "color": resize_rgb(grass_sources["color"], GRASS_OPTIMIZED / "Grass005_color_1k.webp", 1024, 84),
        "normal_gl": resize_rgb(grass_sources["normal_gl"], GRASS_OPTIMIZED / "Grass005_normal_gl_1k.webp", 1024, 92),
        "arm": pack_arm(grass_sources["ao"], grass_sources["roughness"], GRASS_OPTIMIZED / "Grass005_arm_1k.webp", 1024),
        "ao": save_grayscale(grass_sources["ao"], GRASS_OPTIMIZED / "Grass005_ao_1k.webp", 1024, 92),
    }

    report = {
        "schema_version": "1.0",
        "built_at_utc": datetime.now(timezone.utc).isoformat(),
        "builder": Path(__file__).relative_to(ROOT).as_posix(),
        "user_agent": USER_AGENT,
        "policies": {
            "official_sources_only": True,
            "cc0_only": True,
            "provider_hotlinking_at_runtime": False,
            "original_files_preserved": True,
            "optimized_files_are_local_derivatives": True,
        },
        "facade": {
            **FACADE,
            "selection_score": 56,
            "metadata": facade_metadata,
            "downloads": facade_downloads,
            "optimized": facade_optimized,
            "runtime_profile": {
                "material_names": ["V12_PBR_OFFWHITE_STUCCO", "V10_STUCCO_NEW_BUILD"],
                "tiling_by_material": {"V12_PBR_OFFWHITE_STUCCO": [3, 3], "V10_STUCCO_NEW_BUILD": [6, 6]},
                "normal_scale": {"V12_PBR_OFFWHITE_STUCCO": 0.42, "V10_STUCCO_NEW_BUILD": 0.32},
                "ao_intensity": 0.48,
                "roughness": 0.92,
                "metalness": 0.0,
            },
        },
        "grass": {
            **GRASS,
            "selection_score": 55,
            "metadata": grass_metadata,
            "archive": grass_download,
            "archive_crc": "PASS",
            "original_maps": grass_source_records,
            "optimized": grass_optimized,
            "runtime_profile": {
                "material_name": "PBR_B_GRASS",
                "tiling": [8, 8],
                "normal_scale": 0.72,
                "ao_intensity": 0.68,
                "roughness": 0.98,
                "metalness": 0.0,
            },
        },
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.rmtree(GRASS_TEMP_ROOT)
    print(json.dumps({
        "status": "PASS",
        "facade_original_bytes": sum(item["bytes"] for item in facade_downloads.values()),
        "facade_optimized_bytes": sum(item["bytes"] for item in facade_optimized.values()),
        "grass_archive_bytes": grass_download["bytes"],
        "grass_optimized_bytes": sum(item["bytes"] for item in grass_optimized.values()),
        "report": str(REPORT_PATH),
        "report_sha256": sha256(REPORT_PATH),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
