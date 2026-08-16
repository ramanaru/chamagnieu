#!/usr/bin/env python3
"""Re-audit reproductible de la livraison Web Chamagnieu V18.

Ce script ne rend pas la scène. Il vérifie les octets locaux et publics, la
configuration centrale, les routes, les références runtime et la structure
glTF binaire. La preuve visuelle/console reste produite séparément par un vrai
navigateur.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXPECTED_VERSION = "V18"
EXPECTED_RELEASE = "V18-LIVE-SYNC-4"
EXPECTED_MODEL = "Chamagnieu_V18_REALISM_FINAL_WEBP.glb"
EXPECTED_MODEL_SHA256 = (
    "69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE"
)
PAGES = ("", "presentation/", "visite/", "rapide/", "gpt/")
RUNTIME_FILES = (
    "shared/project-config.json",
    "shared/project-config.js",
    "shared/page-version.js",
    "shared/live-realism.js",
    "presentation/presentation.js",
    "visite/visite.js",
    "house.json",
    "gpt/house.json",
)
FURNITURE_PREFIXES = (
    "V11_KITCHEN", "V11_DINING", "V11_LIVING", "V11_BEDROOM",
    "V11_DRESSING", "V11_SDB", "V11_GF_WC", "V11_UF_WC",
    "V11_LAUNDRY", "V11_ENTRY_CLOSET", "V12_KITCHEN", "V12_DINING",
    "V12_LIVING", "V12_BEDROOM", "V12_DRESSING", "V12_SDB",
    "V12_GF_WC", "V12_UF_WC_TOILET", "V12_LAUNDRY",
    "V12_ENTRY_CLOSET", "V12_BARSTOOL", "V12_DINING_TABLE",
)
TEXTURE_SLOTS = (
    "baseColorTexture",
    "metallicRoughnessTexture",
    "normalTexture",
    "occlusionTexture",
    "emissiveTexture",
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def read_glb(path: Path) -> tuple[dict[str, Any], bytes]:
    raw = path.read_bytes()
    if len(raw) < 20 or raw[:4] != b"glTF":
        raise ValueError(f"GLB invalide: {path}")
    version, declared_length = struct.unpack_from("<II", raw, 4)
    if version != 2 or declared_length != len(raw):
        raise ValueError(
            f"En-tête GLB incohérent: version={version} "
            f"declared={declared_length} actual={len(raw)}"
        )
    offset = 12
    chunks: dict[bytes, bytes] = {}
    while offset < len(raw):
        chunk_length, chunk_type = struct.unpack_from("<I4s", raw, offset)
        offset += 8
        chunks[chunk_type] = raw[offset : offset + chunk_length]
        offset += chunk_length
    document = json.loads(chunks[b"JSON"].rstrip(b" \x00").decode("utf-8"))
    return document, chunks.get(b"BIN\x00", b"")


def material_textures(material: dict[str, Any]) -> dict[str, int | None]:
    pbr = material.get("pbrMetallicRoughness", {})
    values: dict[str, int | None] = {
        "baseColorTexture": (pbr.get("baseColorTexture") or {}).get("index"),
        "metallicRoughnessTexture": (
            pbr.get("metallicRoughnessTexture") or {}
        ).get("index"),
        "normalTexture": (material.get("normalTexture") or {}).get("index"),
        "occlusionTexture": (
            material.get("occlusionTexture") or {}
        ).get("index"),
        "emissiveTexture": (material.get("emissiveTexture") or {}).get("index"),
    }
    return values


def node_prefix(name: str) -> str:
    upper = name.upper()
    for version in ("V18", "V17", "V16", "V15", "V14", "V13", "V12", "V11", "V10"):
        if upper.startswith(version + "_"):
            return version
    return "OTHER"


def glb_audit(path: Path) -> dict[str, Any]:
    doc, binary = read_glb(path)
    meshes = doc.get("meshes", [])
    nodes = doc.get("nodes", [])
    materials = doc.get("materials", [])
    textures = doc.get("textures", [])
    images = doc.get("images", [])
    primitives = [primitive for mesh in meshes for primitive in mesh.get("primitives", [])]
    external_images = [image for image in images if image.get("uri")]
    embedded_images = [image for image in images if "bufferView" in image]
    used_textures: set[int] = set()
    material_rows = []
    for index, material in enumerate(materials):
        slots = material_textures(material)
        used_textures.update(value for value in slots.values() if value is not None)
        material_rows.append(
            {
                "index": index,
                "name": material.get("name", f"material_{index}"),
                **slots,
            }
        )
    texture_to_materials: dict[int, list[str]] = defaultdict(list)
    for row in material_rows:
        for slot in TEXTURE_SLOTS:
            value = row[slot]
            if value is not None:
                texture_to_materials[int(value)].append(f"{row['name']}:{slot}")
    image_rows = []
    buffer_views = doc.get("bufferViews", [])
    for index, image in enumerate(images):
        view_index = image.get("bufferView")
        byte_length = None
        digest = None
        if view_index is not None:
            view = buffer_views[view_index]
            start = view.get("byteOffset", 0)
            end = start + view["byteLength"]
            payload = binary[start:end]
            byte_length = len(payload)
            digest = sha256(payload)
        image_rows.append(
            {
                "index": index,
                "name": image.get("name", f"image_{index}"),
                "mimeType": image.get("mimeType"),
                "embedded": view_index is not None,
                "bufferView": view_index,
                "uri": image.get("uri"),
                "bytes": byte_length,
                "sha256": digest,
            }
        )
    prefix_counts = Counter(node_prefix(node.get("name", "")) for node in nodes)
    furniture_nodes = []
    furniture_runtime_meshes = 0
    for index, node in enumerate(nodes):
        name = node.get("name", "")
        if not name.upper().startswith(FURNITURE_PREFIXES):
            continue
        furniture_nodes.append({"index": index, "name": name, "mesh": node.get("mesh")})
        if node.get("mesh") is not None:
            furniture_runtime_meshes += len(meshes[node["mesh"]].get("primitives", []))
    return {
        "path": str(path),
        "bytes": path.stat().st_size,
        "sha256": sha256(path.read_bytes()),
        "asset": doc.get("asset", {}),
        "nodes": len(nodes),
        "meshes": len(meshes),
        "primitives": len(primitives),
        "materials": len(materials),
        "textures": len(textures),
        "usedTextures": len(used_textures),
        "images": len(images),
        "embeddedImages": len(embedded_images),
        "externalImages": len(external_images),
        "externalImageUris": [image.get("uri") for image in external_images],
        "materialRows": material_rows,
        "imageRows": image_rows,
        "textureToMaterials": dict(sorted(texture_to_materials.items())),
        "nodeVersionPrefixes": dict(sorted(prefix_counts.items())),
        "furnitureNodes": len(furniture_nodes),
        "furnitureRuntimeMeshes": furniture_runtime_meshes,
        "extensionsUsed": doc.get("extensionsUsed", []),
        "extensionsRequired": doc.get("extensionsRequired", []),
    }


def http_get(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "Chamagnieu-V18-Reaudit/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
            return {
                "url": url,
                "status": response.status,
                "bytes": len(body),
                "sha256": sha256(body),
                "contentType": response.headers.get("Content-Type"),
                "cacheControl": response.headers.get("Cache-Control"),
                "etag": response.headers.get("ETag"),
            }
    except urllib.error.HTTPError as error:
        return {"url": url, "status": error.code, "bytes": 0, "error": str(error)}


def http_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "Chamagnieu-V18-Reaudit/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def static_audit(root: Path, base_url: str) -> dict[str, Any]:
    config = json.loads((root / "shared" / "project-config.json").read_text(encoding="utf-8"))
    model_path = root / "shared" / Path(config["model"]).name
    glb = glb_audit(model_path)
    runtime_text = "\n".join(
        (root / relative).read_text(encoding="utf-8")
        for relative in RUNTIME_FILES
    )
    source_text = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for suffix in ("*.html", "*.js", "*.json")
        for path in root.rglob(suffix)
        if not ({"audit", "validation", "vendor"} & set(path.relative_to(root).parts))
    )
    tracked_models = sorted(
        str(path.relative_to(root)).replace("\\", "/")
        for pattern in ("*.glb", "*.gltf")
        for path in root.rglob(pattern)
        if ".git" not in path.parts
    )
    public_urls = [base_url.rstrip("/") + "/" + page for page in PAGES]
    public_urls += [
        base_url.rstrip("/") + "/" + relative
        for relative in RUNTIME_FILES
    ]
    public_urls.append(
        base_url.rstrip("/")
        + "/shared/"
        + model_path.name
        + "?release="
        + config["cacheKey"]
    )
    http = [http_get(url) for url in public_urls]
    public_config_url = base_url.rstrip("/") + "/shared/project-config.json"
    public_config = http_json(public_config_url)
    public_model_http = next(
        row for row in http if "/shared/" + model_path.name + "?release=" in row["url"]
    )
    result = {
        "config": config,
        "model": glb,
        "trackedModels": tracked_models,
        "runtimeHardcodedLegacyModelRefs": runtime_text.count(
            "Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a"
        ),
        "runtimeDisplayedV11": "Chamagnieu V11" in runtime_text,
        "serviceWorkerRegistrations": source_text.lower().count("serviceworker.register"),
        "publicConfig": public_config,
        "publicConfigMatchesLocal": public_config == config,
        "publicModelMatchesLocal": (
            public_model_http.get("bytes") == glb["bytes"]
            and public_model_http.get("sha256") == glb["sha256"]
        ),
        "houseJsonIdentical": (
            (root / "house.json").read_bytes() == (root / "gpt" / "house.json").read_bytes()
        ),
        "http": http,
    }
    failures = []
    if config.get("version") != EXPECTED_VERSION:
        failures.append("version")
    if config.get("release") != EXPECTED_RELEASE:
        failures.append("release")
    if model_path.name != EXPECTED_MODEL:
        failures.append("model-name")
    if glb["sha256"] != EXPECTED_MODEL_SHA256:
        failures.append("model-sha256")
    if glb["externalImages"]:
        failures.append("external-images")
    if result["runtimeHardcodedLegacyModelRefs"]:
        failures.append("legacy-model-ref")
    if result["runtimeDisplayedV11"]:
        failures.append("displayed-v11")
    if any(row.get("status") != 200 for row in http):
        failures.append("http")
    if not result["publicConfigMatchesLocal"]:
        failures.append("public-config-drift")
    if not result["publicModelMatchesLocal"]:
        failures.append("public-model-drift")
    result["failures"] = failures
    result["status"] = "PASS" if not failures else "FAIL"
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()
    result = static_audit(args.root.resolve(), args.base_url)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    model = result["model"]
    print(
        f"V18_REAUDIT_STATIC_RESULT={result['status']} "
        f"pages={len(PAGES)} http_200={sum(row['status'] == 200 for row in result['http'])}/{len(result['http'])} "
        f"version={result['config']['version']} release={result['config']['release']} "
        f"model={Path(model['path']).name} model_bytes={model['bytes']} "
        f"glb_sha256={model['sha256']} nodes={model['nodes']} meshes={model['meshes']} "
        f"primitives={model['primitives']} materials={model['materials']} "
        f"textures={model['textures']} used_textures={model['usedTextures']} "
        f"images={model['images']} embedded_images={model['embeddedImages']} "
        f"external_images={model['externalImages']} furniture_nodes={model['furnitureNodes']} "
        f"furniture_runtime_meshes={model['furnitureRuntimeMeshes']} "
        f"displayed_v11={str(result['runtimeDisplayedV11']).lower()} "
        f"legacy_model_refs={result['runtimeHardcodedLegacyModelRefs']} "
        f"service_worker_registrations={result['serviceWorkerRegistrations']} "
        f"public_config_match={str(result['publicConfigMatchesLocal']).lower()} "
        f"public_model_match={str(result['publicModelMatchesLocal']).lower()} "
        f"failures={len(result['failures'])}"
    )
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
