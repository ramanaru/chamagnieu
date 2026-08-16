#!/usr/bin/env python3
"""Copy the accepted staging assets into the mandatory furniture hierarchy."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets_external" / "models"
FURNITURE = ROOT / "assets_external" / "furniture"
TARGETS = {
    "sofa": FURNITURE / "living" / "sofa",
    "table": FURNITURE / "dining" / "table",
    "chair": FURNITURE / "dining" / "chair",
    "bed": FURNITURE / "bedroom" / "bed",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> int:
    inventory = []
    for role, target in TARGETS.items():
        source_original = MODELS / role / "original" / "selected"
        source_optimized = MODELS / role / "optimized" / "selected" / f"{role}_web.glb"
        original = target / "original"
        optimized = target / "optimized"
        original.mkdir(parents=True, exist_ok=True)
        optimized.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source_original, original, dirs_exist_ok=True)
        web_target = optimized / f"{role}_web.glb"
        shutil.copy2(source_optimized, web_target)
        files = sorted([p for p in target.rglob("*") if p.is_file()])
        inventory.append(
            {
                "role": role,
                "root": target.relative_to(ROOT).as_posix(),
                "files": [
                    {
                        "path": p.relative_to(ROOT).as_posix(),
                        "bytes": p.stat().st_size,
                        "sha256": sha256(p),
                    }
                    for p in files
                ],
                "optimized_web_glb": web_target.relative_to(ROOT).as_posix(),
                "optimized_web_glb_sha256": sha256(web_target),
            }
        )
        print(
            f"FURNITURE_STAGE=PASS role={role} files={len(files)} "
            f"glb_sha256={sha256(web_target)}"
        )
    output = FURNITURE / "selected_furniture_inventory.json"
    output.write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FURNITURE_STAGE_RESULT=PASS assets=4/4 output={output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
