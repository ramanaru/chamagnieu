#!/usr/bin/env python3
"""Autonomous static/HTTP release gate for the Chamagnieu V18 asset pilot.

The validator deliberately uses only the Python standard library.  It checks
the repository payload that the two real Web viewers consume; it does not
accept a Blender preview, a successful build alone, or unreferenced downloads
as proof of integration.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EXPECTED_RELEASE = "V18-ASSET-PILOT-1"
EXPECTED_CACHE_KEY = "v18-asset-pilot-1"
EXPECTED_MODEL = "Chamagnieu_V18_WEB_REALISM_UPGRADED.glb"
EXPECTED_MODEL_BYTES = 22_687_292
EXPECTED_MODEL_SHA256 = "9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E"
MANIFEST_REQUIRED_FIELDS = (
    "name",
    "category",
    "source",
    "url",
    "author",
    "license",
    "download_date",
    "original_file",
    "original_size",
    "optimized_file",
    "optimized_size",
    "polygons_before",
    "polygons_after",
    "textures",
    "where_used",
)


@dataclass
class GlbInfo:
    bytes: int
    sha256: str
    triangles: int
    meshes: int
    materials: int
    images: int
    external_uris: list[str]
    draco: bool


class Gate:
    def __init__(self) -> None:
        self.lines: list[str] = []
        self.failures: list[str] = []
        self.passes = 0

    def check(self, condition: bool, code: str, detail: str) -> bool:
        status = "PASS" if condition else "FAIL"
        self.lines.append(f"CHECK {code}={status} :: {detail}")
        if condition:
            self.passes += 1
        else:
            self.failures.append(f"{code}: {detail}")
        return condition

    def note(self, code: str, detail: str) -> None:
        self.lines.append(f"INFO {code} :: {detail}")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def glb_info(path: Path) -> GlbInfo:
    raw = path.read_bytes()
    if len(raw) < 20 or raw[:4] != b"glTF":
        raise ValueError("not a binary glTF (GLB) file")
    version, declared_length = struct.unpack_from("<II", raw, 4)
    if version != 2 or declared_length != len(raw):
        raise ValueError(
            f"invalid GLB header version={version} declared={declared_length} actual={len(raw)}"
        )
    offset = 12
    document: dict[str, Any] | None = None
    while offset + 8 <= len(raw):
        chunk_length, chunk_type = struct.unpack_from("<II", raw, offset)
        offset += 8
        payload = raw[offset : offset + chunk_length]
        offset += chunk_length
        if chunk_type == 0x4E4F534A:
            document = json.loads(payload.rstrip(b" \t\r\n\0").decode("utf-8"))
            break
    if document is None:
        raise ValueError("GLB JSON chunk is missing")

    external_uris: list[str] = []
    for record in list(document.get("buffers", [])) + list(document.get("images", [])):
        uri = record.get("uri") if isinstance(record, dict) else None
        if uri and not str(uri).startswith("data:"):
            external_uris.append(str(uri))

    used_extensions = set(document.get("extensionsUsed", [])) | set(
        document.get("extensionsRequired", [])
    )
    draco = "KHR_draco_mesh_compression" in used_extensions
    accessors = document.get("accessors", [])
    triangles = 0
    for mesh in document.get("meshes", []):
        for primitive in mesh.get("primitives", []):
            if "KHR_draco_mesh_compression" in primitive.get("extensions", {}):
                draco = True
            if "indices" in primitive:
                count = int(accessors[int(primitive["indices"])].get("count", 0))
            else:
                position_accessor = primitive.get("attributes", {}).get("POSITION")
                count = (
                    int(accessors[int(position_accessor)].get("count", 0))
                    if position_accessor is not None
                    else 0
                )
            mode = int(primitive.get("mode", 4))
            if mode == 4:  # TRIANGLES
                triangles += count // 3
            elif mode in (5, 6):  # TRIANGLE_STRIP / TRIANGLE_FAN
                triangles += max(0, count - 2)

    return GlbInfo(
        bytes=len(raw),
        sha256=hashlib.sha256(raw).hexdigest().upper(),
        triangles=triangles,
        meshes=len(document.get("meshes", [])),
        materials=len(document.get("materials", [])),
        images=len(document.get("images", [])),
        external_uris=external_uris,
        draco=draco,
    )


def resolve_config_path(root: Path, config_path_value: str) -> Path:
    # project-config paths are resolved from shared/project-config.json.
    return (root / "shared" / config_path_value).resolve()


def url_for_repo_path(base_url: str, repo_path: str) -> str:
    quoted = "/".join(urllib.parse.quote(part) for part in Path(repo_path).as_posix().split("/"))
    return base_url.rstrip("/") + "/" + quoted


def http_status(url: str, timeout: float) -> tuple[int | None, int | None, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": "Chamagnieu-asset-pilot-validator/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            return int(response.status), len(body), None
    except urllib.error.HTTPError as exc:
        return int(exc.code), None, str(exc)
    except Exception as exc:  # pragma: no cover - exercised when the local server is down
        return None, None, f"{type(exc).__name__}: {exc}"


def nested(data: dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root (default: parent of validation/)",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8902")
    parser.add_argument("--http-timeout", type=float, default=8.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="result path (default: validation/asset-pilot-static-validation.txt)",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    output = (args.output or root / "validation" / "asset-pilot-static-validation.txt").resolve()
    gate = Gate()
    started = datetime.now(timezone.utc).isoformat()

    config_path = root / "shared" / "project-config.json"
    config: dict[str, Any] = {}
    try:
        config = load_json(config_path)
        gate.check(True, "CONFIG_JSON", f"parsed={config_path.relative_to(root).as_posix()}")
    except Exception as exc:
        gate.check(False, "CONFIG_JSON", f"{config_path}: {type(exc).__name__}: {exc}")

    gate.check(config.get("version") == "V18", "CONFIG_VERSION", f"observed={config.get('version')!r}; expected='V18'")
    gate.check(config.get("release") == EXPECTED_RELEASE, "CONFIG_RELEASE", f"observed={config.get('release')!r}; expected={EXPECTED_RELEASE!r}")
    gate.check(config.get("cacheKey") == EXPECTED_CACHE_KEY, "CONFIG_CACHE_KEY", f"observed={config.get('cacheKey')!r}; expected={EXPECTED_CACHE_KEY!r}")
    gate.check(config.get("viewerSource") == "LIVE WEB VIEWER", "CONFIG_VIEWER_SOURCE", f"observed={config.get('viewerSource')!r}")

    model_value = str(config.get("model", ""))
    model_path = resolve_config_path(root, model_value) if model_value else root / "__missing_model__"
    model_exists = model_path.is_file()
    gate.check(model_exists and model_path.name == EXPECTED_MODEL, "MAIN_MODEL_PATH", f"observed={model_path}; expected_name={EXPECTED_MODEL}")
    if model_exists:
        model_bytes = model_path.stat().st_size
        model_sha = sha256_file(model_path)
        gate.check(model_bytes == EXPECTED_MODEL_BYTES == config.get("modelBytes"), "MAIN_MODEL_BYTES_UNCHANGED", f"observed={model_bytes}; config={config.get('modelBytes')}; baseline={EXPECTED_MODEL_BYTES}")
        gate.check(model_sha == EXPECTED_MODEL_SHA256 == str(config.get("modelSha256", "")).upper(), "MAIN_MODEL_HASH_UNCHANGED", f"observed={model_sha}; config={config.get('modelSha256')}; baseline={EXPECTED_MODEL_SHA256}")

    asset_pilot = config.get("assetPilot", {}) if isinstance(config.get("assetPilot"), dict) else {}
    gate.check(asset_pilot.get("architectureChanged") is False, "ARCHITECTURE_UNCHANGED", f"assetPilot.architectureChanged={asset_pilot.get('architectureChanged')!r}")
    gate.check(asset_pilot.get("visualisationOnly") is True and asset_pilot.get("contractual") is False, "VISUALISATION_ONLY", f"visualisationOnly={asset_pilot.get('visualisationOnly')!r}; contractual={asset_pilot.get('contractual')!r}")

    module_names = (
        "shared/live-furniture-pilot.js",
        "shared/live-materials-pilot.js",
        "shared/live-vegetation.js",
    )
    page_names = ("presentation/presentation.js", "visite/visite.js")
    expected_installers = (
        "installLiveFurniturePilot",
        "installLiveMaterialPilot",
        "installLiveVegetation",
    )
    for module_name in module_names:
        gate.check((root / module_name).is_file(), "MODULE_EXISTS_" + Path(module_name).stem.upper().replace("-", "_"), module_name)
    for page_name in page_names:
        page = root / page_name
        text = page.read_text(encoding="utf-8") if page.is_file() else ""
        for installer in expected_installers:
            gate.check(installer in text, f"PAGE_{Path(page_name).parent.name.upper()}_{installer.upper()}", f"{page_name} imports/calls {installer}")
        gate.check("Promise.all" in text, f"PAGE_{Path(page_name).parent.name.upper()}_PARALLEL_LOAD", f"{page_name} uses Promise.all for the three pilot families")
        gate.check("static-once-after-assets" in text, f"PAGE_{Path(page_name).parent.name.upper()}_STATIC_SHADOW", f"{page_name} records static post-load shadows")

    required_dirs = (
        "assets_external/furniture/living",
        "assets_external/furniture/dining",
        "assets_external/furniture/kitchen",
        "assets_external/furniture/bedroom",
        "assets_external/furniture/bathroom",
        "assets_external/vegetation/trees",
        "assets_external/vegetation/hedges",
        "assets_external/vegetation/grass",
        "assets_external/vegetation/indoor_plants",
        "assets_external/materials/facade",
        "assets_external/materials/roof",
        "assets_external/materials/floor",
        "assets_external/materials/exterior",
        "assets_external/materials/vegetation",
        "assets_external/hdri",
    )
    missing_dirs = [path for path in required_dirs if not (root / path).is_dir()]
    gate.check(not missing_dirs, "REQUIRED_DIRECTORY_HIERARCHY", f"required={len(required_dirs)}; missing={missing_dirs}")

    mandatory_files = (
        "assets_external/ASSET_MANIFEST.json",
        "assets_external/ASSET_LICENSES.md",
        "analysis/asset_scale_validation.md",
        "validation/ASSET_REALISM_INTEGRATION_REPORT.md",
    )
    for mandatory in mandatory_files:
        path = root / mandatory
        gate.check(path.is_file() and path.stat().st_size > 0, "MANDATORY_" + path.stem.upper().replace("-", "_"), f"{mandatory}; exists={path.is_file()}; bytes={path.stat().st_size if path.exists() else 0}")

    # The eight required pilot categories are tied to exact files actually used by runtime.
    furniture_assets = nested(asset_pilot, "furniture", "assets", default={}) or {}
    selected: dict[str, dict[str, Any]] = {}
    for role in ("sofa", "table", "chair", "bed"):
        record = furniture_assets.get(role, {}) if isinstance(furniture_assets, dict) else {}
        configured = str(record.get("path", ""))
        selected[role] = {
            "path": resolve_config_path(root, configured) if configured else root / f"__missing_{role}__",
            "configured": record,
        }
    selected["tree"] = {
        "path": root / "assets_external/vegetation/trees/island_tree_02/optimized/island_tree_02_web.glb",
        "configured": {
            "bytes": nested(config, "assets", "treeModelBytes"),
            "sha256": nested(config, "assets", "treeModelSha256"),
        },
    }
    selected["hedge"] = {
        "path": resolve_config_path(root, str(nested(config, "assets", "hedgeModel", default=""))),
        "configured": {
            "bytes": nested(config, "assets", "hedgeModelBytes"),
            "sha256": nested(config, "assets", "hedgeModelSha256"),
        },
    }

    furniture_report_path = root / "validation/pilot_furniture_integration.json"
    vegetation_report_path = root / "validation/pilot_vegetation_integration.json"
    furniture_report = load_json(furniture_report_path) if furniture_report_path.is_file() else {}
    vegetation_report = load_json(vegetation_report_path) if vegetation_report_path.is_file() else {}
    reported_triangles: dict[str, int | None] = {}
    for record in furniture_report.get("assets", []) if isinstance(furniture_report, dict) else []:
        reported_triangles[str(record.get("role"))] = record.get("trianglesPerSource")
    reported_triangles["tree"] = nested(vegetation_report, "tree_selection", "accepted", "runtime_triangles_per_instance")
    reported_triangles["hedge"] = nested(vegetation_report, "hedge_selection", "accepted", "triangles_per_instance")

    parsed_glbs: dict[str, GlbInfo] = {}
    for role, item in selected.items():
        path = Path(item["path"])
        exists = path.is_file()
        gate.check(exists, f"ASSET_{role.upper()}_EXISTS", f"{path.relative_to(root).as_posix() if path.is_absolute() and root in path.parents else path}")
        if not exists:
            continue
        try:
            info = glb_info(path)
            parsed_glbs[role] = info
        except Exception as exc:
            gate.check(False, f"ASSET_{role.upper()}_GLB_PARSE", f"{type(exc).__name__}: {exc}")
            continue
        expected = item["configured"]
        gate.check(info.bytes == expected.get("bytes"), f"ASSET_{role.upper()}_BYTES", f"observed={info.bytes}; configured={expected.get('bytes')}")
        gate.check(info.sha256 == str(expected.get("sha256", "")).upper(), f"ASSET_{role.upper()}_SHA256", f"observed={info.sha256}; configured={expected.get('sha256')}")
        expected_triangles = reported_triangles.get(role)
        gate.check(isinstance(expected_triangles, int) and info.triangles == expected_triangles, f"ASSET_{role.upper()}_TRIANGLES", f"GLB={info.triangles}; report={expected_triangles}; meshes={info.meshes}")
        gate.check(not info.external_uris, f"ASSET_{role.upper()}_NO_EXTERNAL_URI", f"external_uris={info.external_uris}")
        gate.check(not info.draco, f"ASSET_{role.upper()}_NO_DRACO", f"draco={info.draco}; decoder-free Web GLB required")
        gate.note(f"ASSET_{role.upper()}_PROFILE", f"bytes={info.bytes}; sha256={info.sha256}; triangles={info.triangles}; meshes={info.meshes}; materials={info.materials}; images={info.images}")

    material_module = root / "shared/live-materials-pilot.js"
    material_text = material_module.read_text(encoding="utf-8") if material_module.is_file() else ""
    texture_relatives = sorted(set(re.findall(r"['\"](\.\./assets_external/[^'\"]+\.webp)['\"]", material_text, re.IGNORECASE)))
    texture_repo_paths = [Path("shared", relative).resolve().relative_to(root).as_posix() for relative in texture_relatives]
    gate.check(len(texture_repo_paths) == 6, "PBR_TEXTURE_RUNTIME_COUNT", f"runtime_webp_maps={len(texture_repo_paths)}; paths={texture_repo_paths}")
    gate.check(any("white_stucco" in path.lower() for path in texture_repo_paths), "CATEGORY_FACADE_PBR", "White Stucco maps referenced by runtime")
    gate.check(any("grass005" in path.lower() for path in texture_repo_paths), "CATEGORY_GRASS_PBR", "Grass005 maps referenced by runtime")
    expected_texture_bytes = nested(config, "materials", "externalTextureBytes")
    actual_texture_bytes = sum((root / path).stat().st_size for path in texture_repo_paths if (root / path).is_file())
    gate.check(actual_texture_bytes == expected_texture_bytes, "PBR_TEXTURE_BYTES", f"observed={actual_texture_bytes}; configured={expected_texture_bytes}")

    for repo_path in texture_repo_paths:
        local_path = root / repo_path
        gate.check(local_path.is_file(), "TEXTURE_FILE_" + local_path.stem.upper(), f"{repo_path}; bytes={local_path.stat().st_size if local_path.exists() else 0}")
        url = url_for_repo_path(args.base_url, repo_path)
        status, body_bytes, error = http_status(url, args.http_timeout)
        expected_bytes = local_path.stat().st_size if local_path.is_file() else None
        gate.check(status == 200 and body_bytes == expected_bytes, "TEXTURE_HTTP_" + local_path.stem.upper(), f"url={url}; status={status}; response_bytes={body_bytes}; local_bytes={expected_bytes}; error={error}")

    integrated_categories = set(parsed_glbs) | ({"facade_pbr", "grass_pbr"} if len(texture_repo_paths) == 6 else set())
    expected_categories = {"sofa", "table", "chair", "bed", "tree", "hedge", "facade_pbr", "grass_pbr"}
    gate.check(integrated_categories == expected_categories, "EIGHT_PILOT_CATEGORIES", f"observed={sorted(integrated_categories)}; expected={sorted(expected_categories)}")

    # Validate the exact 15-field per-resource contract from mission section 24.
    # Extra audit fields remain allowed, but these names must exist directly on
    # every one of the eight resource records (not hidden in nested aliases).
    manifest_path = root / "assets_external/ASSET_MANIFEST.json"
    if manifest_path.is_file():
        try:
            manifest = load_json(manifest_path)
            manifest_text = json.dumps(manifest, ensure_ascii=False).lower()
            gate.check(True, "MANIFEST_JSON_PARSE", f"parsed={manifest_path.relative_to(root).as_posix()}")
            manifest_assets = manifest.get("assets", []) if isinstance(manifest, dict) else []
            gate.check(isinstance(manifest_assets, list) and len(manifest_assets) == 8, "MANIFEST_ASSET_COUNT", f"observed={len(manifest_assets) if isinstance(manifest_assets, list) else 'not-a-list'}; expected=8")
            manifest_categories = {
                str(record.get("category"))
                for record in manifest_assets
                if isinstance(record, dict) and "category" in record
            }
            gate.check(manifest_categories == expected_categories, "MANIFEST_EIGHT_CATEGORIES_EXACT", f"observed={sorted(manifest_categories)}; expected={sorted(expected_categories)}")

            for index, record in enumerate(manifest_assets):
                if not isinstance(record, dict):
                    gate.check(False, f"MANIFEST_ENTRY_{index}_OBJECT", f"observed_type={type(record).__name__}")
                    continue
                category = str(record.get("category", f"index_{index}"))
                code_category = re.sub(r"[^A-Z0-9]+", "_", category.upper()).strip("_")
                for field in MANIFEST_REQUIRED_FIELDS:
                    gate.check(
                        field in record,
                        f"MANIFEST_{code_category}_FIELD_{field.upper()}",
                        f"entry={index}; category={category}; exact_top_level_field={field!r}",
                    )

                text_fields = ("name", "category", "source", "url", "author", "license", "download_date", "original_file", "optimized_file")
                gate.check(all(isinstance(record.get(field), str) and record[field].strip() for field in text_fields), f"MANIFEST_{code_category}_TEXT_VALUES", f"all required text fields are non-empty strings")
                gate.check(str(record.get("url", "")).startswith("https://"), f"MANIFEST_{code_category}_HTTPS_SOURCE", f"url={record.get('url')!r}")
                gate.check(bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(record.get("download_date", "")))), f"MANIFEST_{code_category}_DOWNLOAD_DATE", f"download_date={record.get('download_date')!r}; expected=YYYY-MM-DD")
                gate.check("cc0" in str(record.get("license", "")).lower(), f"MANIFEST_{code_category}_CC0", f"license={record.get('license')!r}")

                original_rel = str(record.get("original_file", ""))
                optimized_rel = str(record.get("optimized_file", ""))
                original_path = root / original_rel
                optimized_path = root / optimized_rel
                original_size = record.get("original_size")
                optimized_size = record.get("optimized_size")
                gate.check(original_path.is_file() and "/original/" in "/" + Path(original_rel).as_posix(), f"MANIFEST_{code_category}_ORIGINAL_FILE", f"path={original_rel}; exists={original_path.is_file()}")
                gate.check(optimized_path.is_file() and "/optimized/" in "/" + Path(optimized_rel).as_posix(), f"MANIFEST_{code_category}_OPTIMIZED_FILE", f"path={optimized_rel}; exists={optimized_path.is_file()}")
                gate.check(isinstance(original_size, int) and original_path.is_file() and original_path.stat().st_size == original_size, f"MANIFEST_{code_category}_ORIGINAL_SIZE", f"manifest={original_size}; disk={original_path.stat().st_size if original_path.is_file() else None}")
                gate.check(isinstance(optimized_size, int) and optimized_path.is_file() and optimized_path.stat().st_size == optimized_size, f"MANIFEST_{code_category}_OPTIMIZED_SIZE", f"manifest={optimized_size}; disk={optimized_path.stat().st_size if optimized_path.is_file() else None}")
                gate.check(original_path.resolve() != optimized_path.resolve(), f"MANIFEST_{code_category}_ORIGINAL_PRESERVED", f"original={original_rel}; optimized={optimized_rel}")
                gate.check(isinstance(record.get("textures"), dict) and bool(record["textures"]), f"MANIFEST_{code_category}_TEXTURES", f"type={type(record.get('textures')).__name__}; entries={len(record.get('textures', {})) if isinstance(record.get('textures'), dict) else 0}")
                gate.check(isinstance(record.get("where_used"), list) and bool(record["where_used"]), f"MANIFEST_{code_category}_WHERE_USED", f"where_used={record.get('where_used')!r}")

                if category in parsed_glbs:
                    before = record.get("polygons_before")
                    after = record.get("polygons_after")
                    gate.check(isinstance(before, int) and before > 0, f"MANIFEST_{code_category}_POLYGONS_BEFORE", f"polygons_before={before}")
                    gate.check(isinstance(after, int) and after == parsed_glbs[category].triangles, f"MANIFEST_{code_category}_POLYGONS_AFTER", f"manifest={after}; parsed_glb={parsed_glbs[category].triangles}")
                else:
                    gate.check(record.get("polygons_before") is None and record.get("polygons_after") is None, f"MANIFEST_{code_category}_POLYGONS_NOT_APPLICABLE", f"non-geometry PBR resource uses null polygon counts")

            gate.check("sha256" in manifest_text and "triang" in manifest_text and "score" in manifest_text, "MANIFEST_INTEGRITY_FIELDS", "contains sha256, triangle and score evidence")
        except Exception as exc:
            gate.check(False, "MANIFEST_JSON_PARSE", f"{type(exc).__name__}: {exc}")

    licenses_path = root / "assets_external/ASSET_LICENSES.md"
    if licenses_path.is_file():
        license_text = licenses_path.read_text(encoding="utf-8").lower()
        gate.check("cc0" in license_text and "poly haven" in license_text and "blenderkit" in license_text and "ambientcg" in license_text, "LICENSE_LEDGER_PROVIDERS", "CC0 + Poly Haven + BlenderKit + ambientCG are documented")
        gate.check("https://" in license_text, "LICENSE_LEDGER_URLS", "direct source/license URLs documented")

    scale_path = root / "analysis/asset_scale_validation.md"
    if scale_path.is_file():
        scale_text = scale_path.read_text(encoding="utf-8").lower()
        scale_tokens = ("sofa", "table", "chair", "bed", "tree", "hedge", "mètre")
        gate.check(all(token in scale_text for token in scale_tokens), "SCALE_REPORT_CATEGORIES", f"required_tokens={scale_tokens}")

    final_report_path = root / "validation/ASSET_REALISM_INTEGRATION_REPORT.md"
    if final_report_path.is_file():
        final_text = final_report_path.read_text(encoding="utf-8").lower()
        gate.check("live web viewer" in final_text and "blender" in final_text, "FINAL_REPORT_SOURCE_SEPARATION", "contains LIVE WEB VIEWER and BLENDER source labels")
        gate.check("30 fps" in final_text or ">=30" in final_text or "≥30" in final_text, "FINAL_REPORT_FPS_GATE", "contains explicit 30 FPS target evidence")
        gate.check("architecture" in final_text and "inchang" in final_text, "FINAL_REPORT_ARCHITECTURE", "architecture unchanged is explicit")

    # When either copy is changed, both machine-readable house records must stay
    # byte-identical and name the current release.  Existing legacy mesh names in
    # the GLB (V11_/V12_) are data identifiers, not active release/cache tokens.
    house = root / "house.json"
    gpt_house = root / "gpt/house.json"
    if house.is_file() or gpt_house.is_file():
        paired = house.is_file() and gpt_house.is_file()
        gate.check(paired, "HOUSE_PAIR_EXISTS", f"house={house.is_file()}; gpt_house={gpt_house.is_file()}")
        if paired:
            same = house.read_bytes() == gpt_house.read_bytes()
            gate.check(same, "HOUSE_PAIR_IDENTICAL", f"house_sha256={sha256_file(house)}; gpt_house_sha256={sha256_file(gpt_house)}")
            try:
                house_json = load_json(house)
                gate.check(house_json.get("release") == EXPECTED_RELEASE, "HOUSE_RELEASE_CURRENT", f"observed={house_json.get('release')!r}; expected={EXPECTED_RELEASE!r}")
            except Exception as exc:
                gate.check(False, "HOUSE_JSON_PARSE", f"{type(exc).__name__}: {exc}")

    active_runtime_files = (
        "shared/project-config.json",
        "presentation/index.html",
        "presentation/presentation.js",
        "visite/index.html",
        "visite/visite.js",
    )
    active_release_values: list[str] = []
    for name in active_runtime_files:
        text = (root / name).read_text(encoding="utf-8")
        active_release_values.extend(re.findall(r"(?:release=|\"cacheKey\"\s*:\s*\")([^\"'&?\s<>]+)", text, re.IGNORECASE))
    stale_active = sorted({value for value in active_release_values if value.lower() != EXPECTED_CACHE_KEY.lower()})
    gate.check(not stale_active, "NO_STALE_ACTIVE_RELEASE_TOKEN", f"active_release_values={sorted(set(active_release_values))}; stale={stale_active}; legacy GLB node prefixes intentionally excluded")

    # Existing component reports are part of the static release gate.
    component_reports = (
        ("validation/pilot_furniture_integration.json", "result", "PASS"),
        ("validation/pilot_material_integration_validation.json", "status", "PASS"),
        ("validation/pilot_vegetation_integration.json", "result", "PASS"),
        ("validation/vegetation-runtime-validation.json", "result", "PASS"),
    )
    for report_name, key, expected in component_reports:
        path = root / report_name
        try:
            value = load_json(path).get(key)
            gate.check(value == expected, "COMPONENT_" + path.stem.upper().replace("-", "_"), f"{report_name}: {key}={value!r}")
        except Exception as exc:
            gate.check(False, "COMPONENT_" + path.stem.upper().replace("-", "_"), f"{report_name}: {type(exc).__name__}: {exc}")

    result = "PASS" if not gate.failures else "FAIL"
    summary = [
        f"ASSET_PILOT_STATIC_VALIDATION={result}",
        f"GENERATED_AT_UTC={started}",
        f"ROOT={root}",
        f"BASE_URL={args.base_url}",
        f"EXPECTED_RELEASE={EXPECTED_RELEASE}",
        f"EXPECTED_MODEL_SHA256={EXPECTED_MODEL_SHA256}",
        f"CHECKS_TOTAL={gate.passes + len(gate.failures)}",
        f"CHECKS_PASS={gate.passes}",
        f"CHECKS_FAIL={len(gate.failures)}",
        "",
        *gate.lines,
        "",
        "FAILURES:",
        *(gate.failures if gate.failures else ["NONE"]),
        "",
        f"FINAL_RESULT={result}",
        f"EXIT_STATUS={0 if result == 'PASS' else 1}",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(summary) + "\n", encoding="utf-8", newline="\n")
    print(f"ASSET_PILOT_STATIC_VALIDATION={result} checks={gate.passes + len(gate.failures)} pass={gate.passes} fail={len(gate.failures)}")
    for failure in gate.failures:
        print(f"FAIL {failure}")
    print(f"OUTPUT={output}")
    return 0 if result == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
