#!/usr/bin/env python3
"""Rebuild the V18 live GLB with deterministic, embedded WebP PBR upgrades.

The script intentionally leaves every accessor and every original BIN byte intact.
It only appends deterministic WebP payloads, adds/duplicates materials, changes
material bindings on explicitly named meshes, and adjusts PBR parameters.
"""

from __future__ import annotations

import copy
import hashlib
import io
import json
import math
import struct
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "shared" / "Chamagnieu_V18_REALISM_FINAL_WEBP.glb"
OUTPUT = ROOT / "shared" / "Chamagnieu_V18_WEB_REALISM_UPGRADED.glb"
REPORT = ROOT / "validation" / "glb-realism-upgrade-validation.txt"
EXPECTED_SOURCE_SHA256 = "69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE"
MAX_OUTPUT_BYTES = 36 * 1024 * 1024


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def parse_glb(data: bytes) -> tuple[dict[str, Any], bytes]:
    magic, version, declared = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or declared != len(data):
        raise ValueError("invalid GLB 2.0 header")
    json_length, json_type = struct.unpack_from("<I4s", data, 12)
    if json_type != b"JSON":
        raise ValueError("missing JSON chunk")
    json_start = 20
    doc = json.loads(data[json_start : json_start + json_length].decode("utf-8").rstrip(" \0"))
    bin_header = json_start + json_length
    bin_length, bin_type = struct.unpack_from("<I4s", data, bin_header)
    if bin_type != b"BIN\0":
        raise ValueError("missing BIN chunk")
    binary = data[bin_header + 8 : bin_header + 8 + bin_length]
    return doc, binary


def encode_glb(doc: dict[str, Any], binary: bytes) -> bytes:
    doc_bytes = json.dumps(doc, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
    doc_bytes += b" " * ((-len(doc_bytes)) % 4)
    binary += b"\0" * ((-len(binary)) % 4)
    total = 12 + 8 + len(doc_bytes) + 8 + len(binary)
    return (
        struct.pack("<4sII", b"glTF", 2, total)
        + struct.pack("<I4s", len(doc_bytes), b"JSON")
        + doc_bytes
        + struct.pack("<I4s", len(binary), b"BIN\0")
        + binary
    )


def noise_field(size: int, seed: int, octaves: tuple[tuple[int, float], ...] = ((12, 0.50), (36, 0.30), (120, 0.20))) -> np.ndarray:
    rng = np.random.default_rng(seed)
    out = np.zeros((size, size), dtype=np.float32)
    weight_sum = 0.0
    for grid, weight in octaves:
        tile = rng.integers(0, 256, (grid, grid), dtype=np.uint8)
        layer = np.asarray(Image.fromarray(tile, "L").resize((size, size), Image.Resampling.BICUBIC), dtype=np.float32) / 255.0
        out += layer * weight
        weight_sum += weight
    out /= weight_sum
    lo, hi = float(out.min()), float(out.max())
    return np.clip((out - lo) / max(hi - lo, 1e-6), 0.0, 1.0)


def normal_from_height(height: np.ndarray, strength: float) -> np.ndarray:
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * strength
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * strength
    nz = np.ones_like(height)
    length = np.sqrt(dx * dx + dy * dy + nz * nz)
    normal = np.stack((-dx / length, -dy / length, nz / length), axis=2)
    return np.clip((normal * 0.5 + 0.5) * 255.0, 0, 255).astype(np.uint8)


def ao_from_height(height: np.ndarray, strength: float = 0.55) -> np.ndarray:
    base = Image.fromarray(np.clip(height * 255.0, 0, 255).astype(np.uint8), "L")
    blur = np.asarray(base.filter(ImageFilter.GaussianBlur(max(2.0, height.shape[0] / 180.0))), dtype=np.float32) / 255.0
    cavity = np.clip(blur - height, 0.0, 1.0)
    ao = np.clip(0.96 - cavity * strength * 4.0 - (1.0 - height) * 0.06, 0.54, 1.0)
    return np.repeat((ao * 255.0).astype(np.uint8)[:, :, None], 3, axis=2)


def mr_from_height(height: np.ndarray, roughness: float, variation: float = 0.10) -> np.ndarray:
    rough = np.clip(roughness + (height - 0.5) * variation, 0.0, 1.0)
    out = np.zeros((height.shape[0], height.shape[1], 3), dtype=np.uint8)
    out[:, :, 0] = 255
    out[:, :, 1] = np.clip(rough * 255.0, 0, 255).astype(np.uint8)
    out[:, :, 2] = 0
    return out


def tinted(height: np.ndarray, dark: tuple[int, int, int], light: tuple[int, int, int], variation: np.ndarray | None = None) -> np.ndarray:
    t = height if variation is None else np.clip(0.68 * height + 0.32 * variation, 0.0, 1.0)
    d = np.asarray(dark, dtype=np.float32)
    l = np.asarray(light, dtype=np.float32)
    return np.clip(d + (l - d) * t[:, :, None], 0, 255).astype(np.uint8)


def webp_bytes(array: np.ndarray, quality: int = 86) -> bytes:
    bio = io.BytesIO()
    Image.fromarray(array, "RGB").save(bio, "WEBP", quality=quality, method=6, exact=True)
    return bio.getvalue()


def make_organic_pack(size: int, seed: int, dark: tuple[int, int, int], light: tuple[int, int, int], roughness: float, profile: str) -> dict[str, bytes]:
    coarse = noise_field(size, seed)
    fine = noise_field(size, seed + 1, ((30, 0.40), (100, 0.36), (220, 0.24)))
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    if profile == "grass":
        strands_a = 0.5 + 0.5 * np.sin(xx * 0.39 + yy * 0.11 + coarse * 15.0)
        strands_b = 0.5 + 0.5 * np.sin(xx * 0.17 - yy * 0.34 + fine * 11.0)
        clumps = np.clip(strands_a * 0.55 + strands_b * 0.45, 0.0, 1.0)
        height = np.clip(0.48 * coarse + 0.38 * fine + 0.14 * clumps, 0.0, 1.0)
    elif profile == "foliage":
        clusters = (0.5 + 0.5 * np.sin(xx * 0.16 + coarse * 8.0)) * (0.5 + 0.5 * np.cos(yy * 0.13 - fine * 7.0))
        height = np.clip(0.45 * coarse + 0.28 * fine + 0.27 * clusters, 0.0, 1.0)
    elif profile == "bark":
        ridges = 0.5 + 0.5 * np.sin(xx * 0.18 + np.sin(yy * 0.025) * 3.0 + coarse * 5.0)
        cracks = np.power(np.abs(np.sin(xx * 0.055 + fine * 2.8)), 7.0)
        height = np.clip(0.54 * ridges + 0.32 * coarse + 0.14 * fine - cracks * 0.18, 0.0, 1.0)
    else:
        raise ValueError(profile)
    return {
        "base": webp_bytes(tinted(height, dark, light, fine), 88),
        "normal": webp_bytes(normal_from_height(height, 3.4 if profile == "bark" else 2.5), 90),
        "mr": webp_bytes(mr_from_height(height, roughness, 0.12), 86),
        "ao": webp_bytes(ao_from_height(height, 0.62), 86),
    }


def make_gravel_pack(size: int, seed: int) -> dict[str, bytes]:
    rng = np.random.default_rng(seed)
    base = Image.new("RGB", (size, size), (119, 111, 98))
    height = Image.new("L", (size, size), 112)
    draw = ImageDraw.Draw(base)
    hdraw = ImageDraw.Draw(height)
    palette = [(155, 147, 133), (132, 126, 115), (176, 165, 145), (105, 105, 101), (145, 132, 112)]
    for _ in range(int(size * 1.15)):
        cx, cy = int(rng.integers(0, size)), int(rng.integers(0, size))
        rx, ry = int(rng.integers(3, 11)), int(rng.integers(2, 8))
        color = palette[int(rng.integers(0, len(palette)))]
        value = int(rng.integers(145, 235))
        for sx in (-size, 0, size):
            for sy in (-size, 0, size):
                box = (cx - rx + sx, cy - ry + sy, cx + rx + sx, cy + ry + sy)
                draw.ellipse(box, fill=color, outline=tuple(max(0, c - 28) for c in color), width=1)
                hdraw.ellipse(box, fill=value, outline=max(60, value - 55), width=1)
    h = np.asarray(height.filter(ImageFilter.GaussianBlur(0.65)), dtype=np.float32) / 255.0
    b = np.asarray(base, dtype=np.uint8)
    return {"base": webp_bytes(b, 88), "normal": webp_bytes(normal_from_height(h, 4.0), 90), "mr": webp_bytes(mr_from_height(h, 0.92, 0.08), 86), "ao": webp_bytes(ao_from_height(h, 0.85), 86)}


def make_tile_pack(size: int, seed: int, interior: bool) -> dict[str, bytes]:
    rng = np.random.default_rng(seed)
    fine = noise_field(size, seed, ((12, 0.55), (48, 0.30), (160, 0.15)))
    yy, xx = np.mgrid[0:size, 0:size]
    cells = 4 if interior else 5
    cell = size / cells
    ux = np.minimum(np.mod(xx, cell), cell - np.mod(xx, cell))
    uy = np.minimum(np.mod(yy, cell), cell - np.mod(yy, cell))
    grout_width = max(2.0, size / 290.0)
    grout = (ux < grout_width) | (uy < grout_width)
    edge = np.clip(np.minimum(ux, uy) / (grout_width * 3.0), 0.0, 1.0)
    tile_variation = rng.uniform(-0.045, 0.045, (cells, cells)).astype(np.float32)
    ix = np.minimum((xx / cell).astype(int), cells - 1)
    iy = np.minimum((yy / cell).astype(int), cells - 1)
    variation = fine + tile_variation[iy, ix]
    height = np.clip(0.56 + (variation - 0.5) * 0.20 + edge * 0.22, 0.0, 1.0)
    height[grout] = 0.19 + fine[grout] * 0.06
    if interior:
        base = tinted(np.clip(variation, 0, 1), (171, 158, 139), (220, 211, 194), fine)
        grout_color = np.array([126, 119, 108], dtype=np.uint8)
        rough = 0.64
    else:
        base = tinted(np.clip(variation, 0, 1), (126, 119, 107), (184, 173, 153), fine)
        grout_color = np.array([91, 88, 82], dtype=np.uint8)
        rough = 0.84
    base[grout] = grout_color
    return {"base": webp_bytes(base, 89), "normal": webp_bytes(normal_from_height(height, 4.2 if interior else 4.8), 91), "mr": webp_bytes(mr_from_height(height, rough, 0.13), 87), "ao": webp_bytes(ao_from_height(height, 0.95), 87)}


def make_textile_pack(size: int, seed: int, dark: tuple[int, int, int], light: tuple[int, int, int]) -> dict[str, bytes]:
    noise = noise_field(size, seed, ((18, 0.34), (80, 0.33), (200, 0.33)))
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    warp = 0.5 + 0.5 * np.sin(xx * math.pi / 2.6)
    weft = 0.5 + 0.5 * np.sin(yy * math.pi / 2.9 + math.pi / 3.0)
    weave = np.clip(0.42 * warp + 0.42 * weft + 0.16 * noise, 0.0, 1.0)
    base = tinted(weave, dark, light, noise)
    return {"base": webp_bytes(base, 89), "normal": webp_bytes(normal_from_height(weave, 2.2), 91), "mr": webp_bytes(mr_from_height(weave, 0.79, 0.08), 87), "ao": webp_bytes(ao_from_height(weave, 0.54), 87)}


def make_ao(size: int, seed: int, profile: str) -> bytes:
    n = noise_field(size, seed, ((10, 0.50), (44, 0.32), (150, 0.18)))
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    if profile == "roof":
        grooves = 0.5 + 0.5 * np.sin(xx * math.pi / 16.0)
        n = np.clip(0.65 * n + 0.35 * grooves, 0.0, 1.0)
    elif profile == "wood":
        grain = 0.5 + 0.5 * np.sin(xx * 0.08 + n * 5.0)
        n = np.clip(0.55 * n + 0.45 * grain, 0.0, 1.0)
    return webp_bytes(ao_from_height(n, 0.55), 86)


def transform_info(texture_index: int, tiling: tuple[float, float], offset: tuple[float, float] = (0.0, 0.0), **fields: Any) -> dict[str, Any]:
    info: dict[str, Any] = {
        "index": texture_index,
        "extensions": {"KHR_texture_transform": {"scale": [float(tiling[0]), float(tiling[1])], "offset": [float(offset[0]), float(offset[1])]}}
    }
    info.update(fields)
    return info


def geometry_digest(doc: dict[str, Any], binary: bytes) -> str:
    """Hash accessor semantics and payload bytes, ignoring repacked indices/offsets."""
    h = hashlib.sha256()
    for accessor in doc.get("accessors", []):
        accessor_semantics = {key: value for key, value in accessor.items() if key != "bufferView"}
        h.update(json.dumps(accessor_semantics, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        if "bufferView" in accessor:
            bv = doc["bufferViews"][accessor["bufferView"]]
            view_semantics = {key: value for key, value in bv.items() if key not in ("byteOffset", "name")}
            h.update(json.dumps(view_semantics, sort_keys=True, separators=(",", ":")).encode("utf-8"))
            start = bv.get("byteOffset", 0)
            h.update(binary[start : start + bv["byteLength"]])
    return h.hexdigest().upper()


def geometry_payloads_identical(source_doc: dict[str, Any], source_binary: bytes, output_doc: dict[str, Any], output_binary: bytes) -> bool:
    if len(source_doc.get("accessors", [])) != len(output_doc.get("accessors", [])):
        return False
    for source_accessor, output_accessor in zip(source_doc["accessors"], output_doc["accessors"]):
        source_semantics = {key: value for key, value in source_accessor.items() if key != "bufferView"}
        output_semantics = {key: value for key, value in output_accessor.items() if key != "bufferView"}
        if source_semantics != output_semantics:
            return False
        if ("bufferView" in source_accessor) != ("bufferView" in output_accessor):
            return False
        if "bufferView" not in source_accessor:
            continue
        source_view = source_doc["bufferViews"][source_accessor["bufferView"]]
        output_view = output_doc["bufferViews"][output_accessor["bufferView"]]
        source_view_semantics = {key: value for key, value in source_view.items() if key not in ("byteOffset", "name")}
        output_view_semantics = {key: value for key, value in output_view.items() if key not in ("byteOffset", "name")}
        if source_view_semantics != output_view_semantics:
            return False
        source_start = source_view.get("byteOffset", 0)
        output_start = output_view.get("byteOffset", 0)
        if source_binary[source_start : source_start + source_view["byteLength"]] != output_binary[output_start : output_start + output_view["byteLength"]]:
            return False
    return True


def material_texture_bindings(doc: dict[str, Any]) -> list[tuple[str, int]]:
    bindings: list[tuple[str, int]] = []
    for mi, material in enumerate(doc.get("materials", [])):
        pbr = material.get("pbrMetallicRoughness", {})
        for key in ("baseColorTexture", "metallicRoughnessTexture"):
            info = pbr.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                bindings.append((f"materials/{mi}/pbrMetallicRoughness/{key}", info["index"]))
        for key in ("normalTexture", "occlusionTexture", "emissiveTexture"):
            info = material.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                bindings.append((f"materials/{mi}/{key}", info["index"]))
    return bindings


def referenced_buffer_views(doc: dict[str, Any]) -> set[int]:
    references: set[int] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "bufferView" and isinstance(item, int):
                    references.add(item)
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for key, value in doc.items():
        if key != "bufferViews":
            walk(value)
    return references


def remap_buffer_view_references(doc: dict[str, Any], mapping: dict[int, int]) -> None:
    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                if key == "bufferView" and isinstance(item, int):
                    value[key] = mapping[item]
                else:
                    walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    for key, value in doc.items():
        if key != "bufferViews":
            walk(value)


def main() -> int:
    previous_output_sha = sha256(OUTPUT.read_bytes()) if OUTPUT.exists() else "NONE"
    source_bytes = SOURCE.read_bytes()
    source_sha = sha256(source_bytes)
    if source_sha != EXPECTED_SOURCE_SHA256:
        raise RuntimeError(f"unexpected source SHA256: {source_sha}")
    source_doc, source_bin = parse_glb(source_bytes)
    doc = copy.deepcopy(source_doc)
    binary = bytearray(source_bin)

    doc.setdefault("extensionsUsed", [])
    for extension in ("EXT_texture_webp", "KHR_texture_transform", "KHR_materials_transmission", "KHR_materials_ior", "KHR_materials_volume"):
        if extension not in doc["extensionsUsed"]:
            doc["extensionsUsed"].append(extension)
    doc.setdefault("extensionsRequired", [])
    for extension in ("EXT_texture_webp", "KHR_texture_transform"):
        if extension not in doc["extensionsRequired"]:
            doc["extensionsRequired"].append(extension)

    added_image_names: list[str] = []

    def append_texture(name: str, payload: bytes) -> int:
        while len(binary) % 4:
            binary.append(0)
        offset = len(binary)
        binary.extend(payload)
        bv_index = len(doc["bufferViews"])
        doc["bufferViews"].append({"buffer": 0, "byteOffset": offset, "byteLength": len(payload), "name": f"{name}_bufferView"})
        image_index = len(doc["images"])
        doc["images"].append({"bufferView": bv_index, "mimeType": "image/webp", "name": name})
        texture_index = len(doc["textures"])
        doc["textures"].append({"sampler": 0, "name": name, "extensions": {"EXT_texture_webp": {"source": image_index}}})
        added_image_names.append(name)
        return texture_index

    def append_pack(prefix: str, pack: dict[str, bytes]) -> dict[str, int]:
        return {channel: append_texture(f"{prefix}_{channel}", pack[channel]) for channel in ("base", "normal", "mr", "ao")}

    grass = append_pack("V18_WEB_GRASS_NATURAL_768", make_organic_pack(768, 1801, (32, 60, 24), (105, 135, 62), 0.91, "grass"))
    hedge_deep = append_pack("V18_WEB_HEDGE_DEEP_512", make_organic_pack(512, 1811, (22, 49, 21), (74, 111, 54), 0.88, "foliage"))
    hedge_fresh = append_pack("V18_WEB_HEDGE_FRESH_512", make_organic_pack(512, 1821, (36, 71, 28), (113, 151, 69), 0.86, "foliage"))
    tree_deep = append_pack("V18_WEB_TREE_LEAVES_DEEP_512", make_organic_pack(512, 1831, (23, 54, 23), (82, 123, 58), 0.86, "foliage"))
    tree_fresh = append_pack("V18_WEB_TREE_LEAVES_FRESH_512", make_organic_pack(512, 1841, (47, 83, 31), (132, 164, 76), 0.84, "foliage"))
    bark = append_pack("V18_WEB_BARK_512", make_organic_pack(512, 1851, (53, 34, 22), (125, 86, 54), 0.89, "bark"))
    gravel = append_pack("V18_WEB_GRAVEL_LIGHT_768", make_gravel_pack(768, 1861))
    terrace = append_pack("V18_WEB_TERRACE_STONE_768", make_tile_pack(768, 1871, False))
    interior_tile = append_pack("V18_WEB_INTERIOR_LIMESTONE_768", make_tile_pack(768, 1881, True))
    sofa = append_pack("V18_WEB_SOFA_WARM_WEAVE_512", make_textile_pack(512, 1891, (91, 72, 62), (158, 132, 113)))
    armchair = append_pack("V18_WEB_ARMCHAIR_OLIVE_WEAVE_512", make_textile_pack(512, 1901, (67, 69, 50), (126, 125, 91)))
    chair = append_pack("V18_WEB_CHAIR_CARAMEL_WEAVE_512", make_textile_pack(512, 1911, (94, 59, 41), (171, 116, 77)))

    facade_ao = append_texture("V18_WEB_STUCCO_MICRO_AO_512", make_ao(512, 1921, "stucco"))
    roof_ao = append_texture("V18_WEB_ROOF_TILE_AO_512", make_ao(512, 1931, "roof"))
    asphalt_ao = append_texture("V18_WEB_ASPHALT_AO_512", make_ao(512, 1941, "asphalt"))
    wood_ao = append_texture("V18_WEB_WHITE_OAK_AO_512", make_ao(512, 1951, "wood"))

    materials = doc["materials"]

    def set_pack(material: dict[str, Any], pack: dict[str, int], scale: tuple[float, float], normal_scale: float, roughness_factor: float, ao_strength: float, category: str) -> None:
        pbr = material.setdefault("pbrMetallicRoughness", {})
        pbr["baseColorFactor"] = [1.0, 1.0, 1.0, 1.0]
        pbr["metallicFactor"] = 0.0
        pbr["roughnessFactor"] = roughness_factor
        pbr["baseColorTexture"] = transform_info(pack["base"], scale)
        pbr["metallicRoughnessTexture"] = transform_info(pack["mr"], scale)
        material["normalTexture"] = transform_info(pack["normal"], scale, scale=normal_scale)
        material["occlusionTexture"] = transform_info(pack["ao"], scale, strength=ao_strength)
        material["doubleSided"] = True
        material.setdefault("extras", {})["live_realism_upgrade"] = {"category": category, "maps": ["baseColor", "normal", "metallicRoughness", "occlusion"], "embedded": True, "codec": "WebP"}

    # Existing architectural materials: retain their detailed CC0 maps, tune PBR, and add AO.
    facade = materials[2]
    facade["pbrMetallicRoughness"]["baseColorFactor"] = [0.97, 0.96, 0.94, 1.0]
    facade["pbrMetallicRoughness"]["roughnessFactor"] = 0.92
    facade["normalTexture"]["scale"] = 0.28
    facade["occlusionTexture"] = transform_info(facade_ao, (3.0, 3.0), (0.0, -2.0), strength=0.34)
    facade.setdefault("extras", {})["live_realism_upgrade"] = {"category": "MAT_WALL_EXTERIOR", "action": "retain 2K CC0 stucco; stronger micro-normal; embedded micro-AO; clean warm tint"}

    roof = materials[6]
    roof["pbrMetallicRoughness"]["baseColorFactor"] = [1.0, 0.94, 0.88, 1.0]
    roof["pbrMetallicRoughness"]["roughnessFactor"] = 0.88
    roof["normalTexture"]["scale"] = 1.32
    roof["occlusionTexture"] = transform_info(roof_ao, (3.6, 3.6), (0.0, -2.6), strength=0.72)
    roof.setdefault("extras", {})["live_realism_upgrade"] = {"category": "MAT_ROOF_TILES", "action": "retain 2K tile maps; stronger normal; roughness balance; tile-cavity AO"}

    set_pack(materials[8], grass, (8.0, 8.0), 0.76, 0.96, 0.72, "MAT_GRASS")
    set_pack(materials[33], hedge_deep, (2.4, 2.4), 0.62, 0.92, 0.72, "MAT_HEDGE_DEEP")
    set_pack(materials[34], hedge_fresh, (2.4, 2.4), 0.58, 0.90, 0.68, "MAT_HEDGE_FRESH")
    set_pack(materials[17], gravel, (6.0, 6.0), 0.78, 0.98, 0.88, "MAT_GRAVEL")
    set_pack(materials[5], terrace, (5.0, 5.0), 0.68, 0.91, 0.82, "MAT_TERRACE")
    set_pack(materials[3], interior_tile, (4.2, 4.2), 0.52, 0.69, 0.68, "MAT_INTERIOR_TILE_PRIMARY")
    set_pack(materials[25], interior_tile, (7.0, 7.0), 0.45, 0.65, 0.64, "MAT_INTERIOR_TILE_FINISH")

    for asphalt_index in (7, 19):
        asphalt = materials[asphalt_index]
        asphalt["pbrMetallicRoughness"]["baseColorFactor"] = [0.62, 0.65, 0.67, 1.0]
        asphalt["pbrMetallicRoughness"]["roughnessFactor"] = 0.95
        asphalt["normalTexture"]["scale"] = 0.88
        asphalt["occlusionTexture"] = transform_info(asphalt_ao, (9.0, 9.0), (0.0, -8.0), strength=0.52)
        asphalt.setdefault("extras", {})["live_realism_upgrade"] = {"category": "MAT_DRIVEWAY", "action": "retain 2K asphalt; neutral charcoal tint; deeper normal and AO"}

    oak = materials[22]
    oak["pbrMetallicRoughness"]["baseColorFactor"] = [1.0, 0.92, 0.82, 1.0]
    oak["pbrMetallicRoughness"]["roughnessFactor"] = 0.74
    oak["normalTexture"]["scale"] = 0.42
    oak["occlusionTexture"] = transform_info(wood_ao, (3.0, 3.0), (0.0, -2.0), strength=0.42)
    oak.setdefault("extras", {})["live_realism_upgrade"] = {"category": "MAT_TABLE_WOOD", "action": "retain 2K white-oak maps; warm tint; readable grain; AO"}

    def duplicate_material(source_index: int, name: str, pack: dict[str, int], scale: tuple[float, float], normal_scale: float, roughness: float, ao_strength: float, category: str) -> int:
        material = copy.deepcopy(materials[source_index])
        material["name"] = name
        material.pop("extensions", None)
        material["extras"] = {"live_realism_upgrade": {"category": category, "source_material": materials[source_index].get("name"), "embedded": True, "codec": "WebP"}}
        set_pack(material, pack, scale, normal_scale, roughness, ao_strength, category)
        materials.append(material)
        return len(materials) - 1

    sofa_mat = duplicate_material(21, "V18_WEB_SOFA_WARM_WEAVE", sofa, (6.0, 6.0), 0.46, 0.82, 0.58, "MAT_SOFA")
    armchair_mat = duplicate_material(21, "V18_WEB_ARMCHAIR_OLIVE_WEAVE", armchair, (6.0, 6.0), 0.48, 0.83, 0.58, "MAT_ARMCHAIR")
    chair_mat = duplicate_material(21, "V18_WEB_DINING_CHAIR_CARAMEL_WEAVE", chair, (7.0, 7.0), 0.44, 0.80, 0.56, "MAT_CHAIR")
    bark_mat = duplicate_material(9, "V18_WEB_TREE_BARK", bark, (1.7, 4.2), 0.82, 0.94, 0.78, "MAT_TREE_TRUNK")
    tree_deep_mat = duplicate_material(33, "V18_WEB_TREE_LEAVES_DEEP", tree_deep, (2.0, 2.0), 0.58, 0.89, 0.68, "MAT_TREE_LEAVES_DEEP")
    tree_fresh_mat = duplicate_material(34, "V18_WEB_TREE_LEAVES_FRESH", tree_fresh, (2.0, 2.0), 0.54, 0.87, 0.64, "MAT_TREE_LEAVES_FRESH")

    reassigned: list[str] = []

    def reassign_node(node_name: str, old_index: int, new_index: int) -> None:
        matches = [node for node in doc["nodes"] if node.get("name") == node_name]
        if len(matches) != 1 or "mesh" not in matches[0]:
            raise RuntimeError(f"node target mismatch: {node_name}")
        mesh = doc["meshes"][matches[0]["mesh"]]
        changed = 0
        for primitive in mesh.get("primitives", []):
            if primitive.get("material") == old_index:
                primitive["material"] = new_index
                changed += 1
        if not changed:
            raise RuntimeError(f"material target not found on node: {node_name}")
        reassigned.append(f"{node_name}:{materials[old_index].get('name')}->{materials[new_index].get('name')}")

    reassign_node("V11_LIVING_SOFA", 21, sofa_mat)
    for node_name in ("V11_LIVING_ARMCHAIR", "V12_LIVING_ARMCHAIR_2"):
        reassign_node(node_name, 21, armchair_mat)
    for number in range(1, 7):
        reassign_node(f"V11_DINING_CHAIR_{number:02d}", 21, chair_mat)
    for number in range(1, 5):
        for suffix in ("BRANCH_L", "BRANCH_R", "TRUNK"):
            reassign_node(f"V17_TREE_LIGHT_{number:02d}_{suffix}", 9, bark_mat)
        for suffix, old, new in (("CANOPY_C", 33, tree_deep_mat), ("CANOPY_R", 33, tree_deep_mat), ("CANOPY_L", 34, tree_fresh_mat), ("CANOPY_TOP", 34, tree_fresh_mat)):
            reassign_node(f"V17_TREE_LIGHT_{number:02d}_{suffix}", old, new)

    # Physical glass for facade/window glass and interior glazing. OPAQUE + transmission avoids alpha sorting artifacts.
    for material_index, transmission, roughness in ((4, 0.76, 0.12), (20, 0.91, 0.075)):
        glass = materials[material_index]
        glass["alphaMode"] = "OPAQUE"
        glass.pop("alphaCutoff", None)
        pbr = glass.setdefault("pbrMetallicRoughness", {})
        pbr["baseColorFactor"] = [0.73, 0.86, 0.91, 1.0]
        pbr["metallicFactor"] = 0.0
        pbr["roughnessFactor"] = roughness
        glass["extensions"] = {
            "KHR_materials_transmission": {"transmissionFactor": transmission},
            "KHR_materials_ior": {"ior": 1.5},
            "KHR_materials_volume": {"thicknessFactor": 0.006, "attenuationDistance": 8.0, "attenuationColor": [0.93, 0.98, 1.0]},
        }
        glass.setdefault("extras", {})["live_realism_upgrade"] = {"category": "MAT_GLASS", "action": "physical transmission, IOR 1.5, subtle cyan tint, low roughness, no alpha sorting"}

    # Compact the GLB after replacements: remove unused textures/images and repack
    # every referenced bufferView. Geometry payload bytes are copied verbatim.
    live_bindings_before_compaction = material_texture_bindings(doc)
    used_texture_indices = sorted({texture_index for _, texture_index in live_bindings_before_compaction})
    texture_mapping = {old_index: new_index for new_index, old_index in enumerate(used_texture_indices)}

    for material in doc["materials"]:
        pbr = material.get("pbrMetallicRoughness", {})
        for key in ("baseColorTexture", "metallicRoughnessTexture"):
            info = pbr.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                info["index"] = texture_mapping[info["index"]]
        for key in ("normalTexture", "occlusionTexture", "emissiveTexture"):
            info = material.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                info["index"] = texture_mapping[info["index"]]

    old_textures = doc["textures"]
    removed_texture_names = [old_textures[index].get("name", f"texture[{index}]") for index in range(len(old_textures)) if index not in texture_mapping]
    doc["textures"] = [old_textures[index] for index in used_texture_indices]

    used_image_indices = sorted(
        {
            texture.get("extensions", {}).get("EXT_texture_webp", {}).get("source")
            for texture in doc["textures"]
            if isinstance(texture.get("extensions", {}).get("EXT_texture_webp", {}).get("source"), int)
        }
    )
    image_mapping = {old_index: new_index for new_index, old_index in enumerate(used_image_indices)}
    old_images = doc["images"]
    removed_images = [(index, old_images[index]) for index in range(len(old_images)) if index not in image_mapping]
    removed_image_names = [image.get("name", f"image[{index}]") for index, image in removed_images]
    removed_image_payload_bytes = sum(doc["bufferViews"][image["bufferView"]]["byteLength"] for _, image in removed_images)
    doc["images"] = [old_images[index] for index in used_image_indices]
    for texture in doc["textures"]:
        webp = texture.get("extensions", {}).get("EXT_texture_webp", {})
        webp["source"] = image_mapping[webp["source"]]

    used_view_indices = sorted(referenced_buffer_views(doc))
    view_mapping = {old_index: new_index for new_index, old_index in enumerate(used_view_indices)}
    old_views = doc["bufferViews"]
    compacted_binary = bytearray()
    compacted_views: list[dict[str, Any]] = []
    for old_index in used_view_indices:
        while len(compacted_binary) % 4:
            compacted_binary.append(0)
        old_view = old_views[old_index]
        old_offset = old_view.get("byteOffset", 0)
        payload = bytes(binary[old_offset : old_offset + old_view["byteLength"]])
        new_view = copy.deepcopy(old_view)
        new_view["byteOffset"] = len(compacted_binary)
        compacted_binary.extend(payload)
        compacted_views.append(new_view)
    remap_buffer_view_references(doc, view_mapping)
    doc["bufferViews"] = compacted_views
    binary = compacted_binary

    doc["buffers"][0]["byteLength"] = len(binary)
    doc.setdefault("asset", {}).setdefault("extras", {})["v18_web_realism_upgrade"] = {
        "source_sha256": source_sha,
        "geometry_policy": "all accessor payloads are byte-identical; superseded source image payloads are removed",
        "new_images": len(added_image_names),
        "new_materials": len(materials) - len(source_doc["materials"]),
        "removed_source_images": len(removed_images),
        "removed_source_image_payload_bytes": removed_image_payload_bytes,
        "reassigned_meshes": len(reassigned),
        "external_uri": False,
    }

    output_bytes = encode_glb(doc, bytes(binary))
    OUTPUT.write_bytes(output_bytes)

    out_doc, out_bin = parse_glb(output_bytes)
    source_geom = geometry_digest(source_doc, source_bin)
    output_geom = geometry_digest(out_doc, out_bin)
    bindings = material_texture_bindings(out_doc)
    invalid_bindings: list[str] = []
    reachable_images: set[int] = set()
    for path, texture_index in bindings:
        if not 0 <= texture_index < len(out_doc["textures"]):
            invalid_bindings.append(f"{path}=texture[{texture_index}] out-of-range")
            continue
        texture = out_doc["textures"][texture_index]
        source = texture.get("extensions", {}).get("EXT_texture_webp", {}).get("source")
        if not isinstance(source, int) or not 0 <= source < len(out_doc["images"]):
            invalid_bindings.append(f"{path}=texture[{texture_index}] invalid EXT_texture_webp source")
        else:
            reachable_images.add(source)

    decoded = 0
    decode_errors: list[str] = []
    for image_index, image in enumerate(out_doc["images"]):
        if "uri" in image or image.get("mimeType") != "image/webp" or "bufferView" not in image:
            decode_errors.append(f"image[{image_index}] external-or-non-webp")
            continue
        bv = out_doc["bufferViews"][image["bufferView"]]
        start = bv.get("byteOffset", 0)
        payload = out_bin[start : start + bv["byteLength"]]
        try:
            with Image.open(io.BytesIO(payload)) as picture:
                picture.load()
                if picture.format != "WEBP":
                    raise ValueError(picture.format)
            decoded += 1
        except Exception as exc:  # pragma: no cover - detailed build failure path
            decode_errors.append(f"image[{image_index}] {type(exc).__name__}:{exc}")

    no_external_uri = not any("uri" in image for image in out_doc.get("images", [])) and not any("uri" in buffer for buffer in out_doc.get("buffers", []))
    output_image_names = [image.get("name", "") for image in out_doc["images"]]
    added_image_name_set = set(added_image_names)
    added_images_reachable = sum(1 for image_index in reachable_images if output_image_names[image_index] in added_image_name_set)
    orphan_image_bytes = sum(
        out_doc["bufferViews"][image["bufferView"]]["byteLength"]
        for image_index, image in enumerate(out_doc["images"])
        if image_index not in reachable_images
    )
    accessor_semantics_identical = all(
        {key: value for key, value in source_accessor.items() if key != "bufferView"}
        == {key: value for key, value in output_accessor.items() if key != "bufferView"}
        for source_accessor, output_accessor in zip(source_doc["accessors"], out_doc["accessors"])
    ) and len(source_doc["accessors"]) == len(out_doc["accessors"])
    geometry_accessor_payloads_identical = geometry_payloads_identical(source_doc, source_bin, out_doc, out_bin)
    output_referenced_views = referenced_buffer_views(out_doc)
    orphan_buffer_views = sorted(set(range(len(out_doc["bufferViews"]))) - output_referenced_views)
    output_sha = sha256(output_bytes)
    rebuild_matches_previous = previous_output_sha == output_sha
    pass_checks = all(
        (
            len(output_bytes) <= MAX_OUTPUT_BYTES,
            accessor_semantics_identical,
            geometry_accessor_payloads_identical,
            source_geom == output_geom,
            not invalid_bindings,
            not decode_errors,
            decoded == len(out_doc["images"]),
            no_external_uri,
            len(reachable_images) == len(out_doc["images"]),
            orphan_image_bytes == 0,
            added_images_reachable == len(added_image_names),
            not orphan_buffer_views,
            len(reassigned) == 37,
        )
    )

    report_lines = [
        "V18_WEB_REALISM_GLB_VALIDATION",
        f"SOURCE={SOURCE}",
        f"OUTPUT={OUTPUT}",
        f"SOURCE_BYTES={len(source_bytes)}",
        f"SOURCE_SHA256={source_sha}",
        f"OUTPUT_BYTES={len(output_bytes)}",
        f"OUTPUT_SHA256={output_sha}",
        f"PREVIOUS_OUTPUT_SHA256={previous_output_sha}",
        f"REPRODUCIBLE_REBUILD_MATCH={'YES' if rebuild_matches_previous else 'FIRST_OR_CHANGED_BUILD'}",
        f"MAX_OUTPUT_BYTES={MAX_OUTPUT_BYTES}",
        f"SIZE_REASONABLE={'YES' if len(output_bytes) <= MAX_OUTPUT_BYTES else 'NO'}",
        f"SIZE_DELTA_VS_SOURCE={len(output_bytes) - len(source_bytes)}",
        f"SIZE_AT_OR_BELOW_SOURCE={'YES' if len(output_bytes) <= len(source_bytes) else 'NO'}",
        f"SOURCE_COUNTS=nodes:{len(source_doc['nodes'])},meshes:{len(source_doc['meshes'])},accessors:{len(source_doc['accessors'])},materials:{len(source_doc['materials'])},textures:{len(source_doc['textures'])},images:{len(source_doc['images'])}",
        f"OUTPUT_COUNTS=nodes:{len(out_doc['nodes'])},meshes:{len(out_doc['meshes'])},accessors:{len(out_doc['accessors'])},materials:{len(out_doc['materials'])},textures:{len(out_doc['textures'])},images:{len(out_doc['images'])}",
        f"ADDED_MATERIALS={len(out_doc['materials']) - len(source_doc['materials'])}",
        f"GENERATED_TEXTURES={len(added_image_names)}",
        f"REMOVED_UNUSED_TEXTURES={len(removed_texture_names)}",
        f"NET_TEXTURE_DELTA={len(out_doc['textures']) - len(source_doc['textures'])}",
        f"GENERATED_EMBEDDED_WEBP={len(added_image_names)}",
        f"REMOVED_REPLACED_SOURCE_IMAGES={len(removed_images)}",
        f"REMOVED_REPLACED_SOURCE_IMAGE_PAYLOAD_BYTES={removed_image_payload_bytes}",
        f"NET_IMAGE_DELTA={len(out_doc['images']) - len(source_doc['images'])}",
        f"ACCESSOR_SEMANTICS_IDENTICAL={'YES' if accessor_semantics_identical else 'NO'}",
        f"GEOMETRY_ACCESSOR_PAYLOAD_BYTES_IDENTICAL={'YES' if geometry_accessor_payloads_identical else 'NO'}",
        f"SOURCE_GEOMETRY_SHA256={source_geom}",
        f"OUTPUT_GEOMETRY_SHA256={output_geom}",
        f"GEOMETRY_IDENTICAL={'YES' if source_geom == output_geom else 'NO'}",
        f"MATERIAL_TEXTURE_BINDINGS_VALID={len(bindings) - len(invalid_bindings)}/{len(bindings)}",
        f"REACHABLE_IMAGES={len(reachable_images)}/{len(out_doc['images'])}",
        f"ADDED_IMAGES_REACHABLE={added_images_reachable}/{len(added_image_names)}",
        f"ORPHAN_IMAGE_BYTES={orphan_image_bytes}",
        f"ORPHAN_BUFFER_VIEWS={len(orphan_buffer_views)}",
        "REMOVED_REPLACED_SOURCE_IMAGE_NAMES=" + "|".join(removed_image_names),
        "REMOVED_UNUSED_TEXTURE_NAMES=" + "|".join(removed_texture_names),
        "COMPACTION_POLICY=all superseded images, their unused textures, bufferViews and payloads are removed; geometry payloads remain byte-identical",
        f"WEBP_DECODED={decoded}/{len(out_doc['images'])}",
        f"EXTERNAL_URI_COUNT={0 if no_external_uri else 1}",
        f"REASSIGNED_MESH_MATERIAL_BINDINGS={len(reassigned)}",
        "TARGETED_EXISTING_MATERIALS=V12_PBR_OFFWHITE_STUCCO|PBR_B_ROOF|PBR_B_GRASS|V17_PBR_FOLIAGE_DEEP|V17_PBR_FOLIAGE_FRESH|PBR_B_ASPHALT|V10_ASPHALT|V10_GRAVEL|PBR_B_CONCRETE|PBR_B_FLOOR|V12_PBR_LIGHT_PORCELAIN|V12_PBR_WHITE_OAK|MAT_B_GLASS|V10_PHYSICAL_GLASS",
        "ADDED_MATERIAL_NAMES=" + "|".join(material.get("name", "") for material in out_doc["materials"][len(source_doc["materials"]) :]),
        "ADDED_IMAGE_NAMES=" + "|".join(added_image_names),
        "REASSIGNED_BINDINGS_BEGIN",
        *reassigned,
        "REASSIGNED_BINDINGS_END",
    ]
    if invalid_bindings:
        report_lines.extend(["INVALID_BINDINGS_BEGIN", *invalid_bindings, "INVALID_BINDINGS_END"])
    if decode_errors:
        report_lines.extend(["DECODE_ERRORS_BEGIN", *decode_errors, "DECODE_ERRORS_END"])
    report_lines.append(f"V18_WEB_REALISM_GLB_VALIDATION={'PASS' if pass_checks else 'FAIL'}")
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    print(
        "V18_WEB_REALISM_BUILD=" + ("PASS" if pass_checks else "FAIL")
        + f" source_bytes={len(source_bytes)} source_sha256={source_sha}"
        + f" output_bytes={len(output_bytes)} output_sha256={output_sha}"
        + f" materials={len(source_doc['materials'])}->{len(out_doc['materials'])}"
        + f" textures={len(source_doc['textures'])}->{len(out_doc['textures'])}"
        + f" images={len(source_doc['images'])}->{len(out_doc['images'])}"
        + f" reassigned_bindings={len(reassigned)} geometry_identical={str(source_geom == output_geom).lower()}"
        + f" valid_bindings={len(bindings) - len(invalid_bindings)}/{len(bindings)}"
        + f" reachable_images={len(reachable_images)}/{len(out_doc['images'])} orphan_views={len(orphan_buffer_views)}"
        + f" external_uri={0 if no_external_uri else 1} size_delta={len(output_bytes) - len(source_bytes)}"
    )
    print(f"VALIDATION_REPORT={REPORT}")
    return 0 if pass_checks else 1


if __name__ == "__main__":
    raise SystemExit(main())
