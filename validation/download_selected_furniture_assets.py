#!/usr/bin/env python3
"""Acquire the four pinned CC0 furniture winners without altering prior sources.

The exact library payloads are retained in ``original/selected``.  BlenderKit
files are resolved through the official anonymous download API and the Poly
Haven chair is reconstructed from the official 1K glTF bundle manifest.
"""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import urllib.parse
import urllib.request
import uuid


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets_external" / "models"
CANDIDATES = ROOT / "analysis" / "pilot_furniture_candidates.json"
UA = "ChamagnieuAssetPilot/1.0 (CC0 selected furniture acquisition)"


def request(url: str):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers={"User-Agent": UA}), timeout=240
    )


def get_json(url: str) -> dict:
    with request(url) as response:
        return json.load(response)


def get_bytes(url: str) -> bytes:
    with request(url) as response:
        return response.read()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def md5(payload: bytes) -> str:
    return hashlib.md5(payload).hexdigest()


def decompress_blend(payload: bytes) -> tuple[bytes, str, str]:
    if payload.startswith(b"\x28\xb5\x2f\xfd"):
        sys.path.insert(0, str(Path(os.environ.get("TEMP", ".")) / "chamagnieu-pydeps"))
        import zstandard  # type: ignore

        with zstandard.ZstdDecompressor().stream_reader(
            io.BytesIO(payload), read_across_frames=True
        ) as reader:
            blend = reader.read()
        return blend, "zstd-concatenated", ".zst"
    if payload.startswith(b"\x1f\x8b"):
        return gzip.decompress(payload), "gzip", ".gz"
    return payload, "none", ""


def candidate(asset_id: str) -> dict:
    data = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    for entries in data["categories"].values():
        for entry in entries:
            if entry.get("asset_base_id") == asset_id or entry.get("asset_id") == asset_id:
                return entry
    raise KeyError(asset_id)


def acquire_blenderkit(
    role: str, asset_base_id: str, download_id: int, expected_name: str, kind: str
) -> dict:
    selected = MODELS / role / "original" / "selected"
    selected.mkdir(parents=True, exist_ok=True)
    search_url = (
        "https://www.blenderkit.com/api/v1/search/?"
        + urllib.parse.urlencode({"query": f"asset_base_id:{asset_base_id}"})
    )
    search = get_json(search_url)
    matches = [x for x in search.get("results", []) if x.get("assetBaseId") == asset_base_id]
    if len(matches) != 1:
        raise RuntimeError(f"{role}: official API returned {len(matches)} matches")
    asset = matches[0]
    if (
        asset.get("name") != expected_name
        or asset.get("license") != "cc_zero"
        or not asset.get("isFree")
        or not asset.get("canDownload")
    ):
        raise RuntimeError(f"{role}: pinned free CC0 identity gate failed")

    scene_uuid = str(uuid.uuid4())
    download_api = (
        f"https://www.blenderkit.com/api/v1/downloads/{download_id}/?"
        + urllib.parse.urlencode({"scene_uuid": scene_uuid})
    )
    response = get_json(download_api)
    payload = get_bytes(response["filePath"])
    if kind == "glb":
        if payload[:4] != b"glTF":
            raise RuntimeError(f"{role}: selected payload is not GLB")
        source = selected / f"{role}_{asset_base_id}_library.glb"
        source.write_bytes(payload)
        source_records = [
            {
                "path": source.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "sha256": sha256(payload),
                "transport_compression": "library-glb",
            }
        ]
    elif kind == "blend":
        blend, compression, suffix = decompress_blend(payload)
        if blend[:7] != b"BLENDER":
            raise RuntimeError(f"{role}: decompressed payload is not BLENDER")
        raw = selected / f"{role}_{asset_base_id}_1k_download.blend{suffix}"
        source = selected / f"{role}_{asset_base_id}_1k_source.blend"
        raw.write_bytes(payload)
        source.write_bytes(blend)
        source_records = [
            {
                "path": raw.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "sha256": sha256(payload),
                "transport_compression": compression,
            },
            {
                "path": source.relative_to(ROOT).as_posix(),
                "bytes": len(blend),
                "sha256": sha256(blend),
                "transport_compression": "decompressed-source",
            },
        ]
    else:
        raise ValueError(kind)

    record = {
        "role": role,
        "name": asset["name"],
        "asset_base_id": asset_base_id,
        "asset_version_id": asset.get("id"),
        "author": asset.get("author", {}).get("fullName"),
        "source": "BlenderKit",
        "license": "CC0-1.0",
        "source_page_url": f"https://www.blenderkit.com/asset-gallery-detail/{asset_base_id}/",
        "official_search_api": search_url,
        "download_api": download_api,
        "download_id": download_id,
        "library_file_type": response.get("fileType"),
        "original_files": source_records,
    }
    (selected / "library_metadata.json").write_text(
        json.dumps({"asset": asset, "acquisition": record}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return record


def acquire_polyhaven_chair() -> dict:
    role = "chair"
    asset_id = "dining_chair_02"
    selected = MODELS / role / "original" / "selected"
    textures = selected / "textures"
    textures.mkdir(parents=True, exist_ok=True)
    files_api = f"https://api.polyhaven.com/files/{asset_id}"
    metadata_api = "https://api.polyhaven.com/assets?t=models"
    files = get_json(files_api)
    metadata = get_json(metadata_api).get(asset_id)
    if not metadata or metadata.get("type") != 2:
        raise RuntimeError("chair: Poly Haven metadata identity gate failed")
    root = files["gltf"]["1k"]["gltf"]
    bundle = [(f"{asset_id}_1k.gltf", root)] + list(root["include"].items())
    records = []
    for relative, info in bundle:
        payload = get_bytes(info["url"])
        if len(payload) != info["size"] or md5(payload) != info["md5"]:
            raise RuntimeError(f"chair: size/MD5 gate failed for {relative}")
        target = selected / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        records.append(
            {
                "path": target.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "md5": md5(payload),
                "sha256": sha256(payload),
            }
        )
    record = {
        "role": role,
        "name": metadata["name"],
        "asset_id": asset_id,
        "author": metadata.get("authors", {}).get("James Ray Cock", "James Ray Cock"),
        "source": "Poly Haven",
        "license": "CC0-1.0",
        "source_page_url": f"https://polyhaven.com/a/{asset_id}",
        "official_metadata_api": metadata_api,
        "official_files_api": files_api,
        "original_files": records,
    }
    (selected / "library_metadata.json").write_text(
        json.dumps({"asset": metadata, "file_manifest": root, "acquisition": record}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return record


def retain_existing_bed() -> dict:
    role = "bed"
    source_root = MODELS / role / "original"
    selected = source_root / "selected"
    selected.mkdir(parents=True, exist_ok=True)
    source = next(source_root.glob("bed_*.glb"))
    target = selected / source.name
    shutil.copy2(source, target)
    metadata_source = source_root / "library_metadata.json"
    if metadata_source.exists():
        shutil.copy2(metadata_source, selected / "library_metadata.json")
    payload = target.read_bytes()
    metadata = json.loads((selected / "library_metadata.json").read_text(encoding="utf-8"))
    acquisition = metadata.get("acquisition", {})
    return {
        "role": role,
        "name": "Master bed",
        "asset_base_id": "3a845132-df64-4f02-8da6-44229fe774e4",
        "asset_version_id": acquisition.get("asset_id", "d493c69a-5c64-40bf-a7a6-a4e745bfbea8"),
        "author": acquisition.get("author"),
        "source": "BlenderKit",
        "license": "CC0-1.0",
        "source_page_url": "https://www.blenderkit.com/asset-gallery-detail/3a845132-df64-4f02-8da6-44229fe774e4/",
        "decision": "RETAIN_EXISTING_SELECTED_SOURCE",
        "original_files": [
            {
                "path": target.relative_to(ROOT).as_posix(),
                "bytes": len(payload),
                "sha256": sha256(payload),
            }
        ],
    }


def main() -> int:
    # Verify the research file still points to the exact four requested winners.
    expected = {
        "sofa": ("4faac4b8-cc88-4ff2-b7fd-a7edf46d3518", "Leather Sofa"),
        "table": ("bdff957c-a9e9-4827-b6c9-602b264a4fbf", "Wooden table with metalic legs"),
        "chair": ("dining_chair_02", "Dining Chair 02"),
        "bed": ("3a845132-df64-4f02-8da6-44229fe774e4", "Master bed"),
    }
    for asset_id, name in expected.values():
        entry = candidate(asset_id)
        if entry["name"] != name or entry["license_code"] != "cc_zero" or not entry["free"]:
            raise RuntimeError(f"research gate changed for {asset_id}")

    records = [
        acquire_blenderkit(
            "sofa", expected["sofa"][0], 766602, expected["sofa"][1], "glb"
        ),
        acquire_blenderkit(
            "table", expected["table"][0], 220504, expected["table"][1], "blend"
        ),
        acquire_polyhaven_chair(),
        retain_existing_bed(),
    ]
    output = MODELS / "selected_furniture_downloads.json"
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    for record in records:
        files = record["original_files"]
        print(
            f"SELECTED_FURNITURE_DOWNLOAD=PASS role={record['role']} "
            f"name={record['name']!r} license=CC0 files={len(files)} "
            f"bytes={sum(x['bytes'] for x in files)}"
        )
    print(f"SELECTED_FURNITURE_DOWNLOAD_RESULT=PASS assets={len(records)}/4 output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
