"""Validate the V18 live vegetation runtime and optimized GLB assets."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import struct
import subprocess
from pathlib import Path

from PIL import Image


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def read_glb(path: Path) -> tuple[dict, bytes]:
    data = path.read_bytes()
    magic, version, total_length = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF" or version != 2 or total_length != len(data):
        raise ValueError(f"Invalid GLB header: {path}")
    json_length, json_type = struct.unpack_from("<II", data, 12)
    if json_type != 0x4E4F534A:
        raise ValueError(f"Missing JSON chunk: {path}")
    document = json.loads(data[20 : 20 + json_length].decode("utf-8"))
    bin_header = 20 + json_length
    bin_length, bin_type = struct.unpack_from("<II", data, bin_header)
    if bin_type != 0x004E4942:
        raise ValueError(f"Missing BIN chunk: {path}")
    binary = data[bin_header + 8 : bin_header + 8 + bin_length]
    return document, binary


def glb_metrics(path: Path) -> dict[str, object]:
    document, binary = read_glb(path)
    triangles = 0
    primitives = 0
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            primitives += 1
            accessor = document["accessors"][primitive["indices"]]
            if primitive.get("mode", 4) == 4:
                triangles += accessor["count"] // 3
    images = []
    for image in document.get("images", []):
        view = document["bufferViews"][image["bufferView"]]
        start = view.get("byteOffset", 0)
        payload = binary[start : start + view["byteLength"]]
        with Image.open(io.BytesIO(payload)) as bitmap:
            images.append(
                {
                    "name": image.get("name", ""),
                    "mime": image.get("mimeType", ""),
                    "width": bitmap.width,
                    "height": bitmap.height,
                    "bytes": len(payload),
                }
            )
    return {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "triangles": triangles,
        "meshes": len(document.get("meshes", [])),
        "primitives": primitives,
        "materials": [material.get("name", "") for material in document.get("materials", [])],
        "textures": len(document.get("textures", [])),
        "images": images,
    }


def source_provenance(manifest_path: Path, source_models: Path, asset_id: str) -> dict[str, object]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    entry = next(asset for asset in manifest["assets"] if asset["id"] == asset_id)
    mismatches = []
    for item in entry["files"]:
        marker = f"assets/models/{asset_id}/"
        relative = item["path"].replace("\\", "/").split(marker, 1)[1]
        path = source_models / asset_id / relative
        actual = {"bytes": path.stat().st_size, "sha256": sha256(path)}
        if actual["bytes"] != item["bytes"] or actual["sha256"] != item["sha256"]:
            mismatches.append({"path": str(path), "expected": item, "actual": actual})
    return {
        "license": entry["license"],
        "source_url": entry["source_url"],
        "files": len(entry["files"]),
        "mismatches": mismatches,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--source-models", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = args.root.resolve()
    module = root / "shared" / "live-vegetation.js"
    outputs = {
        "shrub_03": root / "shared" / "assets" / "vegetation" / "shrub_03_web.glb",
        "island_tree_02": root / "shared" / "assets" / "vegetation" / "island_tree_02_web.glb",
    }
    metrics = {asset_id: glb_metrics(path) for asset_id, path in outputs.items()}
    provenance = {
        asset_id: source_provenance(args.manifest, args.source_models, asset_id)
        for asset_id in outputs
    }
    syntax = subprocess.run(
        ["node", "--check", str(module)],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    source_build = json.loads((root / "validation" / "vegetation-build-report.json").read_text(encoding="utf-8"))
    build_assets = {asset["asset_id"]: asset for asset in source_build["assets"]}
    module_text = module.read_text(encoding="utf-8")
    checks = {
        "syntax_exit_zero": syntax.returncode == 0,
        "module_exports_installer": "export async function installLiveVegetation" in module_text,
        "module_has_constrained_fallback": "original-low-poly-constrained" in module_text,
        "module_masks_after_success": "hideOriginals" in module_text and "status === 'fulfilled'" in module_text,
        "module_exposes_metrics": all(token in module_text for token in ("displayedTriangles", "drawCalls", "loadMs")),
        "module_uses_two_rows_three_tiles": all(
            token in module_text
            for token in ("segment.userData.rowCount = 2", "const tilesPerRow = 3", "hedgeCloneInstances")
        ),
        "module_uses_shrub_alpha_008": "family === 'hedge' ? 0.08" in module_text,
        "module_uses_dense_hedge_scale": all(
            token in module_text
            for token in ("size.y * 1.28", "shortSide * 0.82")
        ),
        "shrub_size_under_1mb": metrics["shrub_03"]["bytes"] < 1_000_000,
        "shrub_one_draw_primitive": metrics["shrub_03"]["primitives"] == 1,
        "shrub_triangles_expected": 8_000 <= metrics["shrub_03"]["triangles"] <= 8_500,
        "tree_size_under_5mb": metrics["island_tree_02"]["bytes"] < 5_000_000,
        "tree_triangles_web_budget": 35_000 <= metrics["island_tree_02"]["triangles"] <= 50_000,
        "embedded_images_512_or_less": all(
            max(image["width"], image["height"]) <= 512
            for asset in metrics.values()
            for image in asset["images"]
        ),
        "source_manifest_hashes_match": all(not item["mismatches"] for item in provenance.values()),
        "build_source_preserved": all(asset["source_preserved"] for asset in build_assets.values()),
        "output_hashes_match_build": all(
            metrics[asset_id]["sha256"] == build_assets[asset_id]["output_sha256"]
            for asset_id in metrics
        ),
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    lines = [
        f"VEGETATION_ASSET_VALIDATION={status}",
        "LICENSE_POLICY=Poly Haven CC0 1.0; source files read-only; derived Web GLBs preserve attribution evidence",
    ]
    for asset_id in ("shrub_03", "island_tree_02"):
        item = metrics[asset_id]
        source = provenance[asset_id]
        image_summary = ",".join(
            f"{image['name']}:{image['width']}x{image['height']}:{image['mime']}:{image['bytes']}B"
            for image in item["images"]
        )
        lines.extend(
            [
                f"ASSET={asset_id}",
                f"SOURCE_URL={source['source_url']}",
                f"LICENSE={source['license']}",
                f"SOURCE_FILES_VERIFIED={source['files']}",
                f"OUTPUT={outputs[asset_id].resolve()}",
                f"OUTPUT_BYTES={item['bytes']}",
                f"OUTPUT_SHA256={item['sha256']}",
                f"TRIANGLES={item['triangles']}",
                f"MESHES={item['meshes']}",
                f"PRIMITIVES_DRAW_CALLS_PER_INSTANCE={item['primitives']}",
                f"MATERIALS={','.join(item['materials'])}",
                f"TEXTURES={item['textures']}",
                f"IMAGES={image_summary}",
            ]
        )
    lines.extend(
        [
            f"MODULE={module.resolve()}",
            f"MODULE_BYTES={module.stat().st_size}",
            f"MODULE_SHA256={sha256(module)}",
            "MODULE_API=await installLiveVegetation({scene,house,renderer,mobile,cacheKey})",
            "DESKTOP_POLICY=4 shared-geometry tree clones + 18 hedge segments x 2 staggered rows x 3 shared-geometry shrub tiles = 108 shrub clones; hide originals per family only after asset success",
            "MOBILE_POLICY=modern phones receive the same optimized vegetation; save-data or deviceMemory below 4 GB keeps original low-poly vegetation and downloads no optional GLB",
            "FALLBACK_POLICY=independent tree/hedge Promise results; failed family remains visible from the base house GLB",
            "SYNTAX_COMMAND=node --check shared/live-vegetation.js",
            f"SYNTAX_LITERAL_OUTPUT={(syntax.stdout + syntax.stderr).strip() or '<empty>'}",
            f"SYNTAX_EXIT_STATUS={syntax.returncode}",
        ]
    )
    for name, passed in checks.items():
        lines.append(f"CHECK_{name.upper()}={'PASS' if passed else 'FAIL'}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0])
    print(
        "VEGETATION_RUNTIME_BUDGET="
        f"desktop_trees={metrics['island_tree_02']['triangles'] * 4}tris/"
        f"{metrics['island_tree_02']['primitives'] * 4}draws "
        f"desktop_hedges={metrics['shrub_03']['triangles'] * 108}tris/"
        f"{metrics['shrub_03']['primitives'] * 108}draws"
    )
    if status != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
