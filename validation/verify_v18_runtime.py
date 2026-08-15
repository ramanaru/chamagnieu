#!/usr/bin/env python3
"""Validate the single-source V18 runtime locally or through its public URL."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import urllib.parse
import urllib.request
from pathlib import Path


EXPECTED_SHA = "79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28"
EXPECTED_MODEL = "Chamagnieu_V18_REALISM_FINAL.glb"
PAGES = ["", "presentation/", "visite/", "rapide/", "gpt/"]
TEXT_RESOURCES = [
    "shared/project-config.json",
    "shared/project-config.js",
    "shared/page-version.js",
    "shared/live-realism.js",
    "presentation/presentation.js",
    "visite/visite.js",
    "house.json",
    "gpt/house.json",
]
FURNITURE_PREFIXES = (
    "V11_KITCHEN", "V11_DINING", "V11_LIVING", "V11_BEDROOM", "V11_DRESSING",
    "V11_SDB", "V11_GF_WC", "V11_UF_WC", "V11_LAUNDRY", "V11_ENTRY_CLOSET",
    "V12_KITCHEN", "V12_DINING", "V12_LIVING", "V12_BEDROOM", "V12_DRESSING",
    "V12_SDB", "V12_GF_WC", "V12_UF_WC_TOILET", "V12_LAUNDRY", "V12_ENTRY_CLOSET",
    "V12_BARSTOOL", "V12_DINING_TABLE",
)


def fail(reason: str) -> None:
    print(f"V18_RUNTIME_VALIDATION=FAIL reason={reason}")
    raise SystemExit(1)


def get(base: str, relative: str) -> tuple[int, bytes, str]:
    url = urllib.parse.urljoin(base.rstrip("/") + "/", relative)
    request = urllib.request.Request(url, headers={"User-Agent": "Chamagnieu-V18-Audit/1.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.status, response.read(), response.geturl()


def parse_glb(data: bytes) -> dict:
    if len(data) < 20:
        fail("glb_too_short")
    magic, version, total_length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total_length != len(data):
        fail("glb_header")
    json_length, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        fail("glb_json_chunk")
    return json.loads(data[20 : 20 + json_length].decode("utf-8").rstrip(" \t\r\n\0"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    config_path = root / "shared" / "project-config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    if config.get("version") != "V18" or config.get("release") != "V18-LIVE-SYNC-3":
        fail("config_version")
    if Path(config.get("model", "")).name != EXPECTED_MODEL:
        fail("config_model")
    if config.get("modelSha256") != EXPECTED_SHA:
        fail("config_hash")

    runtime_text = "\n".join(
        (root / relative).read_text(encoding="utf-8", errors="replace")
        for relative in [
            "index.html",
            "presentation/index.html",
            "presentation/presentation.js",
            "visite/index.html",
            "visite/visite.js",
            "rapide/index.html",
            "gpt/index.html",
            "house.json",
            "gpt/house.json",
            "shared/project-config.json",
        ]
    )
    if "Chamagnieu V16" in runtime_text or "?v=18a" in runtime_text:
        fail("stale_runtime_token")
    if runtime_text.count("Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a"):
        fail("hardcoded_old_model")

    http_ok = 0
    for page in PAGES:
        status, body, _ = get(args.base_url, page)
        if status != 200 or not body:
            fail("page_http_" + (page or "root"))
        http_ok += 1

    for resource in TEXT_RESOURCES:
        status, body, _ = get(args.base_url, resource)
        if status != 200 or not body:
            fail("resource_http_" + resource.replace("/", "_"))
        http_ok += 1

    model_relative = "shared/" + EXPECTED_MODEL + "?release=" + config["cacheKey"]
    status, model_bytes, _ = get(args.base_url, model_relative)
    if status != 200:
        fail("model_http")
    http_ok += 1
    digest = hashlib.sha256(model_bytes).hexdigest().upper()
    if digest != EXPECTED_SHA or len(model_bytes) != config["modelBytes"]:
        fail("model_integrity")

    gltf = parse_glb(model_bytes)
    images = gltf.get("images", [])
    embedded = sum(1 for image in images if "bufferView" in image and "uri" not in image)
    external = sum(1 for image in images if "uri" in image)
    if embedded != 37 or external != 0:
        fail("texture_delivery")
    if len(gltf.get("materials", [])) != 35 or len(gltf.get("textures", [])) != 56:
        fail("gltf_counts")

    furniture_nodes = []
    for node in gltf.get("nodes", []):
        name = node.get("name", "").upper()
        if "mesh" in node and name.startswith(FURNITURE_PREFIXES):
            primitive_count = len(gltf["meshes"][node["mesh"]].get("primitives", []))
            furniture_nodes.append((node.get("name", ""), primitive_count))
    furniture_meshes = sum(primitives for _, primitives in furniture_nodes)
    if len(furniture_nodes) != 167 or furniture_meshes != 169:
        fail("furniture_coverage")
    for relative in ("presentation/presentation.js", "visite/visite.js"):
        script = (root / relative).read_text(encoding="utf-8")
        if "object.parent?.userData.isFurnitureTree" not in script:
            fail("furniture_tree_propagation_" + relative.replace("/", "_"))

    print(
        "V18_RUNTIME_VALIDATION=PASS"
        f" pages={len(PAGES)} http_200={http_ok}"
        f" version={config['version']} release={config['release']}"
        f" model={EXPECTED_MODEL} model_bytes={len(model_bytes)}"
        f" glb_sha256={digest} materials={len(gltf.get('materials', []))}"
        f" textures={len(gltf.get('textures', []))} images={len(images)}"
        f" embedded_images={embedded} external_images={external}"
        f" furniture_nodes={len(furniture_nodes)} furniture_runtime_meshes={furniture_meshes}"
    )


if __name__ == "__main__":
    main()
