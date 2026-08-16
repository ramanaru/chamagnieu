#!/usr/bin/env python3
"""Download the exact, pinned CC0 pilot furniture assets from BlenderKit.

The script stores the library response and the untouched library-provided GLB in
each asset's ``original`` directory.  It intentionally does not overwrite an
existing original unless its checksum differs, so the acquisition is auditable.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
import sys
import urllib.parse
import urllib.request
import uuid


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "assets_external" / "models"
USER_AGENT = "ChamagnieuAssetPilot/1.0 (CC0 asset audit)"

ASSETS = {
    "sofa": {
        "id": "d4eaa6c1-866a-431e-a30c-4c582f2070ad",
        "download_id": 764183,
        "expected_name": "Cotton Mini Sofa",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/d4eaa6c1-866a-431e-a30c-4c582f2070ad/",
    },
    "table": {
        "id": "6c105d2e-e4a3-4e6e-a91a-c47d6e0326a1",
        "download_id": 998820,
        "expected_name": "Jiechen Table",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/6c105d2e-e4a3-4e6e-a91a-c47d6e0326a1/",
    },
    "chair": {
        "id": "d4302197-f279-4df8-82a1-5849fea19483",
        "download_id": 745827,
        "expected_name": "Carl-hansen-son CHAIR 29",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/d4302197-f279-4df8-82a1-5849fea19483/",
    },
    "bed": {
        "id": "d493c69a-5c64-40bf-a7a6-a4e745bfbea8",
        "download_id": 531158,
        "expected_name": "Master bed",
        "source_url": "https://www.blenderkit.com/asset-gallery-detail/d493c69a-5c64-40bf-a7a6-a4e745bfbea8/",
    },
}


def request_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def download(url: str, target: pathlib.Path) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = response.read()
    target.write_bytes(payload)
    return payload


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def main() -> int:
    scene_uuid = str(uuid.uuid4())
    results: list[dict] = []
    for role, spec in ASSETS.items():
        original = BASE / role / "original"
        optimized = BASE / role / "optimized"
        original.mkdir(parents=True, exist_ok=True)
        optimized.mkdir(parents=True, exist_ok=True)

        api_url = f"https://www.blenderkit.com/api/v1/assets/{spec['id']}/"
        metadata = request_json(api_url)
        if metadata.get("name") != spec["expected_name"]:
            raise RuntimeError(
                f"{role}: expected {spec['expected_name']!r}, got {metadata.get('name')!r}"
            )
        if metadata.get("license") != "cc_zero" or not metadata.get("isFree"):
            raise RuntimeError(f"{role}: asset is not an explicit free CC0 asset")

        download_api = (
            f"https://www.blenderkit.com/api/v1/downloads/{spec['download_id']}/?"
            + urllib.parse.urlencode({"scene_uuid": scene_uuid})
        )
        download_response = request_json(download_api)
        file_url = download_response["filePath"]
        filename = f"{role}_{spec['id']}_library.glb"
        target = original / filename
        payload = download(file_url, target)
        if payload[:4] != b"glTF":
            raise RuntimeError(f"{role}: downloaded file is not a GLB")

        record = {
            "role": role,
            "asset_id": spec["id"],
            "name": metadata["name"],
            "author": metadata.get("author", {}).get("fullName"),
            "license": metadata["license"],
            "is_free": metadata["isFree"],
            "verification_status": metadata.get("verificationStatus"),
            "source_url": spec["source_url"],
            "api_url": api_url,
            "download_api": download_api,
            "library_file_type": download_response.get("fileType"),
            "library_file_uuid": download_response.get("uuid"),
            "local_file": target.relative_to(ROOT).as_posix(),
            "bytes": len(payload),
            "sha256": sha256(payload),
            "dict_parameters": metadata.get("dictParameters", {}),
        }
        (original / "library_metadata.json").write_text(
            json.dumps({"asset": metadata, "acquisition": record}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        results.append(record)
        print(
            f"MODEL_DOWNLOAD=PASS role={role} name={metadata['name']!r} "
            f"bytes={len(payload)} sha256={record['sha256']} license=CC0"
        )

    (BASE / "pilot_model_downloads.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"MODEL_DOWNLOAD_RESULT=PASS assets={len(results)}/{len(ASSETS)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
