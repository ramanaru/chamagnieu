"""Verify that the public V18 Web Realism assets match this checkout byte-for-byte."""

from __future__ import annotations

import hashlib
import subprocess
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://ramanaru.github.io/chamagnieu/"
ASSETS = (
    "shared/project-config.json",
    "shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb",
    "shared/assets/vegetation/island_tree_02_web.glb",
    "shared/assets/vegetation/shrub_03_web.glb",
    "shared/live-realism.js",
    "shared/live-vegetation.js",
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def main() -> None:
    lines = ["PUBLIC_ASSET_HASH_VALIDATION", f"BASE_URL={BASE_URL}"]
    failures = []
    for relative in ASSETS:
        # GitHub Pages publishes the Git blob (LF for text), not Windows' CRLF
        # working-tree representation. Compare with the exact tracked blob.
        local = subprocess.check_output(
            ["git", "show", f"HEAD:{relative}"], cwd=ROOT
        )
        request = urllib.request.Request(
            f"{BASE_URL}{relative}?proof=v18-web-realism-1",
            headers={"Cache-Control": "no-cache", "User-Agent": "ChamagnieuVerifier/1.0"},
        )
        with urllib.request.urlopen(request, timeout=90) as response:
            public = response.read()
            status = response.status
        matches = status == 200 and public == local
        if not matches:
            failures.append(relative)
        lines.append(
            " ".join(
                (
                    f"ASSET={relative}",
                    f"HTTP={status}",
                    f"PUBLIC_BYTES={len(public)}",
                    f"GIT_BLOB_BYTES={len(local)}",
                    f"PUBLIC_SHA256={digest(public)}",
                    f"GIT_BLOB_SHA256={digest(local)}",
                    f"MATCH={'PASS' if matches else 'FAIL'}",
                )
            )
        )
    lines.append(
        f"PUBLIC_ASSET_HASH_RESULT={'PASS' if not failures else 'FAIL'} "
        f"assets={len(ASSETS) - len(failures)}/{len(ASSETS)}"
    )
    output = ROOT / "validation" / "public-asset-hashes.txt"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
