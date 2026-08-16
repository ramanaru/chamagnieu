#!/usr/bin/env python3
"""Download the pinned 1K CC0 vegetation source blends from BlenderKit."""

from __future__ import annotations

import hashlib
import gzip
import io
import json
import pathlib
import sys
import os
import urllib.parse
import urllib.request
import uuid

sys.path.insert(0, str(pathlib.Path(os.environ.get("TEMP", ".")) / "chamagnieu-pydeps"))
import zstandard


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "assets_external" / "vegetation"
UA = "ChamagnieuAssetPilot/1.0 (CC0 asset audit)"

ASSETS = {
    "tree": {
        "version_id": "8775e08b-6ac7-4af3-86ad-9f3d56d65afd",
        "asset_base_id": "c8af7417-b4d3-4cff-8a7a-b0afdb5a577f",
        "download_id": 652232,
        "name": "Decorative Urban Tree",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/c8af7417-b4d3-4cff-8a7a-b0afdb5a577f/",
    },
    "hedge": {
        "version_id": "32002ed3-1b0b-40d9-835d-a36bc16d5b51",
        "asset_base_id": "2810ce15-1076-44e6-9b95-90487f8d5dc5",
        "download_id": 30090,
        "name": "Shrub",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/2810ce15-1076-44e6-9b95-90487f8d5dc5/",
    },
}


def get_json(url: str) -> dict:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60) as response:
        return json.load(response)


def get_bytes(url: str) -> bytes:
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=240) as response:
        return response.read()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:
    scene_uuid = str(uuid.uuid4())
    records = []
    for role, spec in ASSETS.items():
        directory = BASE / role / "original"
        (BASE / role / "optimized").mkdir(parents=True, exist_ok=True)
        directory.mkdir(parents=True, exist_ok=True)
        api_url = f"https://www.blenderkit.com/api/v1/assets/{spec['version_id']}/"
        metadata = get_json(api_url)
        if metadata.get("name") != spec["name"] or metadata.get("license") != "cc_zero" or not metadata.get("isFree"):
            raise RuntimeError(f"{role}: pinned CC0 metadata gate failed")
        download_api = (
            f"https://www.blenderkit.com/api/v1/downloads/{spec['download_id']}/?"
            + urllib.parse.urlencode({"scene_uuid": scene_uuid})
        )
        response = get_json(download_api)
        payload = get_bytes(response["filePath"])
        if payload.startswith(b"\x28\xb5\x2f\xfd"):
            # Blender's zstd-compressed .blend consists of concatenated frames.
            with zstandard.ZstdDecompressor().stream_reader(
                io.BytesIO(payload), read_across_frames=True
            ) as reader:
                blend_payload = reader.read()
            compression = "zstd-concatenated"
            raw_suffix = ".zst"
        elif payload.startswith(b"\x1f\x8b"):
            blend_payload = gzip.decompress(payload)
            compression = "gzip"
            raw_suffix = ".gz"
        else:
            blend_payload = payload
            compression = "none"
            raw_suffix = ""
        if blend_payload[:7] != b"BLENDER":
            raise RuntimeError(f"{role}: decompressed source is not a Blender file")
        target = directory / f"{role}_{spec['asset_base_id']}_1k_source.blend"
        raw_target = directory / f"{role}_{spec['asset_base_id']}_1k_download.blend{raw_suffix}"
        raw_target.write_bytes(payload)
        target.write_bytes(blend_payload)
        record = {
            "role": role,
            "name": metadata["name"],
            "asset_base_id": spec["asset_base_id"],
            "version_id": spec["version_id"],
            "author": metadata.get("author", {}).get("fullName"),
            "license": metadata["license"],
            "is_free": metadata["isFree"],
            "source_url": spec["source_url"],
            "api_url": api_url,
            "download_api": download_api,
            "library_file_type": response.get("fileType"),
            "downloaded_original_file": raw_target.relative_to(ROOT).as_posix(),
            "downloaded_original_bytes": len(payload),
            "downloaded_original_sha256": digest(payload),
            "decompressed_source_file": target.relative_to(ROOT).as_posix(),
            "decompressed_source_bytes": len(blend_payload),
            "decompressed_source_sha256": digest(blend_payload),
            "transport_compression": compression,
        }
        (directory / "library_metadata.json").write_text(
            json.dumps({"asset": metadata, "acquisition": record}, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        records.append(record)
        print(f"VEGETATION_DOWNLOAD=PASS role={role} name={metadata['name']!r} downloaded_bytes={len(payload)} downloaded_sha256={record['downloaded_original_sha256']} blend_bytes={len(blend_payload)} blend_sha256={record['decompressed_source_sha256']} license=CC0")
    (BASE / "pilot_vegetation_downloads.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print("VEGETATION_DOWNLOAD_RESULT=PASS assets=2/2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
