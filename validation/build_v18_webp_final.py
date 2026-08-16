#!/usr/bin/env python3
"""Build the corrected high-resolution V18 WebP GLB without touching its source.

The V18 WebP master contains one invalid material binding: material 31 points
to texture 50, whose EXT_texture_webp source is absent.  This builder removes
only that binding, keeps the binary payload byte-for-byte, and verifies that
every texture binding that remains resolves to an embedded image.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


EXPECTED_SOURCE_SHA256 = "97F842001CC77E65637271172D09A81043FFFDF3235591DCB1AFF0BA96D67DA0"
EXPECTED_INVALID_TEXTURE = 50
EXPECTED_REMOVED_PATH = "/materials/31/pbrMetallicRoughness/metallicRoughnessTexture"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def parse_glb(data: bytes) -> tuple[dict, bytes, int, int]:
    if len(data) < 28:
        raise ValueError("GLB trop court")
    magic, version, total_length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total_length != len(data):
        raise ValueError("entête GLB invalide")
    json_length, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise ValueError("chunk JSON absent")
    json_start, json_end = 20, 20 + json_length
    doc = json.loads(data[json_start:json_end].decode("utf-8").rstrip(" \t\r\n\0"))
    bin_length, bin_type = struct.unpack_from("<II", data, json_end)
    if bin_type != 0x004E4942:
        raise ValueError("chunk BIN absent")
    binary = data[json_end + 8 : json_end + 8 + bin_length]
    if len(binary) != bin_length:
        raise ValueError("chunk BIN tronqué")
    return doc, binary, magic, version


def texture_source(texture: dict) -> int | None:
    direct = texture.get("source")
    if isinstance(direct, int):
        return direct
    webp = texture.get("extensions", {}).get("EXT_texture_webp", {})
    source = webp.get("source")
    return source if isinstance(source, int) else None


def texture_bindings(value, path=""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}/{key}"
            if isinstance(child, dict) and isinstance(child.get("index"), int) and "texture" in key.lower():
                yield child_path, child["index"]
            yield from texture_bindings(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from texture_bindings(child, f"{path}/{index}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-source-sha", default=EXPECTED_SOURCE_SHA256)
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    source_bytes = source.read_bytes()
    source_sha = sha256(source_bytes)
    if source_sha != args.allow_source_sha.upper():
        raise SystemExit(f"V18_WEBP_BUILD=FAIL reason=source_sha actual={source_sha}")

    doc, binary, magic, version = parse_glb(source_bytes)
    images = doc.get("images", [])
    textures = doc.get("textures", [])
    invalid_textures = {
        index
        for index, texture in enumerate(textures)
        if (texture_source(texture) is None or not 0 <= texture_source(texture) < len(images))
    }
    if invalid_textures != {EXPECTED_INVALID_TEXTURE}:
        raise SystemExit(f"V18_WEBP_BUILD=FAIL reason=invalid_textures actual={sorted(invalid_textures)}")

    removed: list[str] = []

    def repair(value, path="") -> None:
        if isinstance(value, dict):
            for key, child in list(value.items()):
                child_path = f"{path}/{key}"
                if (
                    isinstance(child, dict)
                    and isinstance(child.get("index"), int)
                    and child["index"] in invalid_textures
                    and "texture" in key.lower()
                ):
                    del value[key]
                    removed.append(child_path)
                else:
                    repair(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                repair(child, f"{path}/{index}")

    repair(doc.get("materials", []), "/materials")
    if removed != [EXPECTED_REMOVED_PATH]:
        raise SystemExit(f"V18_WEBP_BUILD=FAIL reason=removed_paths actual={removed}")

    bad_bindings = []
    for path, index in texture_bindings(doc.get("materials", []), "/materials"):
        if not 0 <= index < len(textures) or texture_source(textures[index]) is None:
            bad_bindings.append(f"{path}:{index}")
    if bad_bindings:
        raise SystemExit(f"V18_WEBP_BUILD=FAIL reason=remaining_bad_bindings actual={bad_bindings}")

    embedded_images = sum(
        isinstance(image.get("bufferView"), int) and not image.get("uri")
        for image in images
    )
    if embedded_images != len(images) or any(image.get("mimeType") != "image/webp" for image in images):
        raise SystemExit("V18_WEBP_BUILD=FAIL reason=images_not_embedded_webp")

    # Preserve the source BIN chunk exactly. Only the JSON chunk is rebuilt.
    doc["buffers"][0]["byteLength"] = len(binary)
    json_bytes = json.dumps(doc, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    json_bytes += b" " * ((-len(json_bytes)) % 4)
    binary_padded = binary + b"\0" * ((-len(binary)) % 4)
    total_length = 12 + 8 + len(json_bytes) + 8 + len(binary_padded)
    result = bytearray(struct.pack("<4sII", magic, version, total_length))
    result += struct.pack("<II", len(json_bytes), 0x4E4F534A) + json_bytes
    result += struct.pack("<II", len(binary_padded), 0x004E4942) + binary_padded

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(result)

    output_doc, output_binary, _, _ = parse_glb(bytes(result))
    if output_binary != binary:
        raise SystemExit("V18_WEBP_BUILD=FAIL reason=bin_changed")
    if output_doc.get("meshes") != doc.get("meshes") or output_doc.get("accessors") != doc.get("accessors"):
        raise SystemExit("V18_WEBP_BUILD=FAIL reason=geometry_json_changed")

    output_sha = sha256(result)
    print(
        "V18_WEBP_BUILD=PASS "
        f"source_bytes={len(source_bytes)} source_sha256={source_sha} "
        f"output_bytes={len(result)} output_sha256={output_sha} "
        f"bin_bytes={len(binary)} bin_identical=true images={len(images)} "
        f"embedded_webp={embedded_images} textures={len(textures)} "
        f"removed={EXPECTED_REMOVED_PATH} remaining_bad_bindings=0",
        flush=True,
    )


if __name__ == "__main__":
    main()
