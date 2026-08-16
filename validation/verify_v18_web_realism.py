#!/usr/bin/env python3
"""Validation statique autonome de la livraison V18 Web Realism.

Le validateur ne modifie aucun fichier du viewer. Il contrôle la configuration,
les GLB réellement servis, les deux runtimes, les cinq pages publiques et les
rapports de preuve lorsqu'ils existent. Une base HTTP peut être ajoutée avec
``--base-url`` afin d'exiger des réponses 200 pour les ressources critiques.
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
from pathlib import Path
from typing import Any, Iterable


EXPECTED_RELEASE = "V18-WEB-REALISM-1"
EXPECTED_CACHE_KEY = "v18-web-realism-1"
EXPECTED_MODEL = "Chamagnieu_V18_WEB_REALISM_UPGRADED.glb"
EXPECTED_MODEL_BYTES = 22_687_292
EXPECTED_MODEL_SHA256 = "9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E"
EXPECTED_SOURCE_MODEL = "Chamagnieu_V18_REALISM_FINAL_WEBP.glb"
EXPECTED_SOURCE_SHA256 = "69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE"

EXPECTED_TREE = "assets/vegetation/island_tree_02_web.glb"
EXPECTED_TREE_BYTES = 4_268_472
EXPECTED_TREE_SHA256 = "845CD738030743A4592FDC10DB77A38E522E15C8901E6710C377C3D5C303CF76"
EXPECTED_HEDGE = "assets/vegetation/shrub_03_web.glb"
EXPECTED_HEDGE_BYTES = 675_924
EXPECTED_HEDGE_SHA256 = "C285AD37DDAA6014347AD1AD8A31311BAC46C384EE0D5F8C5D445186AA7960EE"

EXPECTED_MATERIALS = 41
EXPECTED_TEXTURES = 90
EXPECTED_IMAGES = 78
EXPECTED_BINDINGS = 95
EXPECTED_ACCESSORS = 2_454

MATERIAL_PLAN_FIELDS = (
    "name",
    "currently_visible_quality",
    "baseColorTexture",
    "normalTexture",
    "roughnessTexture",
    "metallicTexture",
    "aoTexture",
    "tiling",
    "problem",
    "action",
)
PRIORITY_ALIASES = (
    "MAT_WALL_EXTERIOR",
    "MAT_ROOF_TILES",
    "MAT_GRASS",
    "MAT_HEDGE",
    "MAT_TREE_LEAVES",
    "MAT_TREE_TRUNK",
    "MAT_DRIVEWAY",
    "MAT_GRAVEL",
    "MAT_TERRACE",
    "MAT_INTERIOR_TILE",
    "MAT_SOFA",
    "MAT_ARMCHAIR",
    "MAT_TABLE_WOOD",
    "MAT_CHAIR",
    "MAT_GLASS",
)
VISUAL_DEFECT_SECTIONS = (
    "FACADE",
    "ROOF",
    "GRASS",
    "HEDGES",
    "TREES",
    "DRIVEWAY",
    "INTERIOR_FLOOR",
    "SOFA",
    "CHAIRS",
    "TABLE",
    "GLASS",
    "LIGHTING",
    "OVERALL_REALISM",
)
VISUAL_DEFECT_FIELDS = (
    "CURRENT_PROBLEM",
    "CAUSE",
    "CORRECTION_APPLIED",
    "RESULT",
    "STATUS",
)
FINAL_REPORT_FIELDS = (
    "LIVE_VERSION",
    "LIVE_GLB_USED",
    "MATERIAL_UPGRADES",
    "ROOF",
    "FACADE",
    "GRASS",
    "HEDGES",
    "TREES",
    "EXTERIOR_GROUND",
    "INTERIOR_FLOOR",
    "FURNITURE_MATERIALS",
    "GLASS",
    "LIGHTING",
    "PERFORMANCE",
    "BEFORE_AFTER_SUMMARY",
    "FINAL_STATUS",
)
FINAL_VERDICTS = (
    "LIVE_WEB_REALISM_IMPROVED=YES",
    "TEXTURE_QUALITY_IMPROVED=YES",
    "GROUND_REALISM_IMPROVED=YES",
    "VEGETATION_REALISM_IMPROVED=YES",
    "INTERIOR_REALISM_IMPROVED=YES",
    "FINAL_STATUS=PASS",
)


class DuplicateKeyError(ValueError):
    pass


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest().upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def unique_object(pairs: Iterable[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json_unique(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object)


def parse_glb(payload: bytes) -> tuple[dict[str, Any], bytes]:
    if len(payload) < 28:
        raise ValueError("GLB shorter than minimum header/chunks")
    magic, version, declared = struct.unpack_from("<4sII", payload, 0)
    if magic != b"glTF" or version != 2 or declared != len(payload):
        raise ValueError(
            f"invalid GLB header magic={magic!r} version={version} declared={declared} actual={len(payload)}"
        )
    json_length, json_type = struct.unpack_from("<I4s", payload, 12)
    if json_type != b"JSON":
        raise ValueError("first GLB chunk is not JSON")
    json_start = 20
    json_end = json_start + json_length
    if json_end + 8 > len(payload):
        raise ValueError("truncated GLB JSON chunk")
    doc = json.loads(
        payload[json_start:json_end].decode("utf-8").rstrip(" \0"),
        object_pairs_hook=unique_object,
    )
    bin_length, bin_type = struct.unpack_from("<I4s", payload, json_end)
    if bin_type != b"BIN\0":
        raise ValueError("second GLB chunk is not BIN")
    bin_start = json_end + 8
    bin_end = bin_start + bin_length
    if bin_end != len(payload):
        raise ValueError(f"invalid BIN boundary end={bin_end} actual={len(payload)}")
    return doc, payload[bin_start:bin_end]


def geometry_digest(doc: dict[str, Any], binary: bytes) -> str:
    digest = hashlib.sha256()
    for accessor in doc.get("accessors", []):
        semantics = {key: value for key, value in accessor.items() if key != "bufferView"}
        digest.update(json.dumps(semantics, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        if "bufferView" not in accessor:
            continue
        view = doc["bufferViews"][accessor["bufferView"]]
        view_semantics = {key: value for key, value in view.items() if key not in ("byteOffset", "name")}
        digest.update(json.dumps(view_semantics, sort_keys=True, separators=(",", ":")).encode("utf-8"))
        start = view.get("byteOffset", 0)
        digest.update(binary[start : start + view["byteLength"]])
    return digest.hexdigest().upper()


def geometry_payloads_identical(
    source_doc: dict[str, Any],
    source_binary: bytes,
    output_doc: dict[str, Any],
    output_binary: bytes,
) -> bool:
    source_accessors = source_doc.get("accessors", [])
    output_accessors = output_doc.get("accessors", [])
    if len(source_accessors) != len(output_accessors):
        return False
    for source_accessor, output_accessor in zip(source_accessors, output_accessors):
        source_semantics = {key: value for key, value in source_accessor.items() if key != "bufferView"}
        output_semantics = {key: value for key, value in output_accessor.items() if key != "bufferView"}
        if source_semantics != output_semantics:
            return False
        if ("bufferView" in source_accessor) != ("bufferView" in output_accessor):
            return False
        if "bufferView" not in source_accessor:
            continue
        source_view = source_doc["bufferViews"][source_accessor["bufferView"]]
        output_view = output_doc["bufferViews"][output_accessor["bufferView"]]
        source_view_semantics = {
            key: value for key, value in source_view.items() if key not in ("byteOffset", "name")
        }
        output_view_semantics = {
            key: value for key, value in output_view.items() if key not in ("byteOffset", "name")
        }
        if source_view_semantics != output_view_semantics:
            return False
        source_start = source_view.get("byteOffset", 0)
        output_start = output_view.get("byteOffset", 0)
        if (
            source_binary[source_start : source_start + source_view["byteLength"]]
            != output_binary[output_start : output_start + output_view["byteLength"]]
        ):
            return False
    return True


def material_texture_bindings(doc: dict[str, Any]) -> list[tuple[str, int]]:
    bindings: list[tuple[str, int]] = []
    for material_index, material in enumerate(doc.get("materials", [])):
        pbr = material.get("pbrMetallicRoughness", {})
        for key in ("baseColorTexture", "metallicRoughnessTexture"):
            info = pbr.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                bindings.append((f"materials/{material_index}/pbrMetallicRoughness/{key}", info["index"]))
        for key in ("normalTexture", "occlusionTexture", "emissiveTexture"):
            info = material.get(key)
            if isinstance(info, dict) and isinstance(info.get("index"), int):
                bindings.append((f"materials/{material_index}/{key}", info["index"]))
    return bindings


def referenced_buffer_views(doc: dict[str, Any]) -> set[int]:
    references: set[int] = set()

    def walk(value: Any) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "bufferView" and isinstance(child, int):
                    references.add(child)
                else:
                    walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    for key, value in doc.items():
        if key != "bufferViews":
            walk(value)
    return references


def check_glb(root: Path) -> tuple[list[Check], dict[str, Any]]:
    checks: list[Check] = []
    facts: dict[str, Any] = {}
    model_path = root / "shared" / EXPECTED_MODEL
    if not model_path.is_file():
        return [Check("model_file", "FAIL", f"missing={model_path}")], facts

    model_payload = model_path.read_bytes()
    model_sha = sha256_bytes(model_payload)
    facts.update(model_bytes=len(model_payload), model_sha256=model_sha)
    checks.append(
        Check(
            "model_identity",
            "PASS" if len(model_payload) == EXPECTED_MODEL_BYTES and model_sha == EXPECTED_MODEL_SHA256 else "FAIL",
            f"bytes={len(model_payload)}/{EXPECTED_MODEL_BYTES} sha256={model_sha}/{EXPECTED_MODEL_SHA256}",
        )
    )

    try:
        doc, binary = parse_glb(model_payload)
    except Exception as exc:  # noqa: BLE001 - validator must report malformed deliverables
        checks.append(Check("model_glb_parse", "FAIL", f"{type(exc).__name__}: {exc}"))
        return checks, facts
    checks.append(Check("model_glb_parse", "PASS", "GLB_2.0 JSON+BIN chunks valid"))

    materials = doc.get("materials", [])
    textures = doc.get("textures", [])
    images = doc.get("images", [])
    accessors = doc.get("accessors", [])
    facts.update(
        materials=len(materials),
        textures=len(textures),
        images=len(images),
        accessors=len(accessors),
    )
    counts_ok = (
        len(materials) == EXPECTED_MATERIALS
        and len(textures) == EXPECTED_TEXTURES
        and len(images) == EXPECTED_IMAGES
        and len(accessors) == EXPECTED_ACCESSORS
    )
    checks.append(
        Check(
            "model_counts",
            "PASS" if counts_ok else "FAIL",
            f"materials={len(materials)}/{EXPECTED_MATERIALS} textures={len(textures)}/{EXPECTED_TEXTURES} "
            f"images={len(images)}/{EXPECTED_IMAGES} accessors={len(accessors)}/{EXPECTED_ACCESSORS}",
        )
    )

    bindings = material_texture_bindings(doc)
    invalid_bindings: list[str] = []
    reachable_images: set[int] = set()
    for binding_path, texture_index in bindings:
        if not 0 <= texture_index < len(textures):
            invalid_bindings.append(f"{binding_path}:texture[{texture_index}] out-of-range")
            continue
        webp = textures[texture_index].get("extensions", {}).get("EXT_texture_webp", {})
        image_index = webp.get("source")
        if not isinstance(image_index, int) or not 0 <= image_index < len(images):
            invalid_bindings.append(f"{binding_path}:texture[{texture_index}] invalid EXT_texture_webp.source")
            continue
        reachable_images.add(image_index)
    facts.update(bindings=len(bindings), reachable_images=len(reachable_images))
    binding_ok = len(bindings) == EXPECTED_BINDINGS and not invalid_bindings
    checks.append(
        Check(
            "material_texture_bindings",
            "PASS" if binding_ok else "FAIL",
            f"valid={len(bindings) - len(invalid_bindings)}/{len(bindings)} expected={EXPECTED_BINDINGS} "
            f"errors={'NONE' if not invalid_bindings else '|'.join(invalid_bindings[:5])}",
        )
    )

    image_errors: list[str] = []
    orphan_image_bytes = 0
    buffer_views = doc.get("bufferViews", [])
    for image_index, image in enumerate(images):
        if "uri" in image or image.get("mimeType") != "image/webp" or not isinstance(image.get("bufferView"), int):
            image_errors.append(f"image[{image_index}] external-or-non-webp")
            continue
        view_index = image["bufferView"]
        if not 0 <= view_index < len(buffer_views):
            image_errors.append(f"image[{image_index}] bufferView[{view_index}] out-of-range")
            continue
        view = buffer_views[view_index]
        start = view.get("byteOffset", 0)
        end = start + view.get("byteLength", 0)
        image_payload = binary[start:end]
        if end > len(binary) or len(image_payload) < 12:
            image_errors.append(f"image[{image_index}] truncated payload")
        elif not (image_payload[:4] == b"RIFF" and image_payload[8:12] == b"WEBP"):
            image_errors.append(f"image[{image_index}] invalid WebP signature")
        if image_index not in reachable_images:
            orphan_image_bytes += view.get("byteLength", 0)

    uri_locations: list[str] = []

    def find_uri(value: Any, location: str = "$") -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_location = f"{location}.{key}"
                if key == "uri":
                    uri_locations.append(child_location)
                find_uri(child, child_location)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                find_uri(child, f"{location}[{index}]")

    find_uri(doc)
    referenced_views = referenced_buffer_views(doc)
    orphan_views = sorted(set(range(len(buffer_views))) - referenced_views)
    facts.update(
        orphan_image_bytes=orphan_image_bytes,
        orphan_buffer_views=len(orphan_views),
        uri_count=len(uri_locations),
    )
    embedded_ok = (
        not image_errors
        and len(reachable_images) == EXPECTED_IMAGES
        and orphan_image_bytes == 0
        and not uri_locations
        and not orphan_views
    )
    checks.append(
        Check(
            "embedded_webp_integrity",
            "PASS" if embedded_ok else "FAIL",
            f"webp_valid={EXPECTED_IMAGES - len(image_errors)}/{EXPECTED_IMAGES} "
            f"reachable={len(reachable_images)}/{EXPECTED_IMAGES} uri={len(uri_locations)} "
            f"orphan_image_bytes={orphan_image_bytes} orphan_buffer_views={len(orphan_views)} "
            f"errors={'NONE' if not image_errors else '|'.join(image_errors[:5])}",
        )
    )

    source_path = root / "shared" / EXPECTED_SOURCE_MODEL
    if not source_path.is_file():
        checks.append(Check("geometry_unchanged", "SKIP", f"reference source missing={source_path}"))
    else:
        try:
            source_payload = source_path.read_bytes()
            source_sha = sha256_bytes(source_payload)
            source_doc, source_binary = parse_glb(source_payload)
            source_geometry = geometry_digest(source_doc, source_binary)
            output_geometry = geometry_digest(doc, binary)
            identical = geometry_payloads_identical(source_doc, source_binary, doc, binary)
            geometry_ok = (
                source_sha == EXPECTED_SOURCE_SHA256
                and len(source_doc.get("accessors", [])) == EXPECTED_ACCESSORS
                and identical
                and source_geometry == output_geometry
            )
            facts.update(
                source_model_sha256=source_sha,
                source_geometry_sha256=source_geometry,
                output_geometry_sha256=output_geometry,
            )
            checks.append(
                Check(
                    "geometry_unchanged",
                    "PASS" if geometry_ok else "FAIL",
                    f"source_sha256={source_sha}/{EXPECTED_SOURCE_SHA256} accessors={len(source_doc.get('accessors', []))} "
                    f"payloads_identical={str(identical).upper()} source_geometry_sha256={source_geometry} "
                    f"output_geometry_sha256={output_geometry}",
                )
            )
        except Exception as exc:  # noqa: BLE001
            checks.append(Check("geometry_unchanged", "FAIL", f"{type(exc).__name__}: {exc}"))
    return checks, facts


def check_config(root: Path) -> tuple[list[Check], dict[str, Any]]:
    path = root / "shared" / "project-config.json"
    facts: dict[str, Any] = {}
    try:
        config = load_json_unique(path)
    except Exception as exc:  # noqa: BLE001
        return [Check("central_config", "FAIL", f"{type(exc).__name__}: {exc}")], facts

    expected = {
        "version": "V18",
        "release": EXPECTED_RELEASE,
        "cacheKey": EXPECTED_CACHE_KEY,
        "model": f"./{EXPECTED_MODEL}",
        "modelSha256": EXPECTED_MODEL_SHA256,
        "modelBytes": EXPECTED_MODEL_BYTES,
        "viewerSource": "LIVE WEB VIEWER",
    }
    mismatches = [f"{key}={config.get(key)!r} expected={value!r}" for key, value in expected.items() if config.get(key) != value]
    materials = config.get("materials", {})
    profile = config.get("modelProfile", {})
    material_expected = {
        "codec": "WebP",
        "embeddedImageCount": EXPECTED_IMAGES,
        "pbrTextureBindings": EXPECTED_BINDINGS,
        "externalTextureCount": 0,
        "orphanImageBytes": 0,
    }
    profile_expected = {
        "geometryChanged": False,
        "geometryAccessorPayloadsIdentical": True,
        "materials": EXPECTED_MATERIALS,
        "textures": EXPECTED_TEXTURES,
        "embeddedImages": EXPECTED_IMAGES,
        "orphanBufferViews": 0,
    }
    mismatches.extend(
        f"materials.{key}={materials.get(key)!r} expected={value!r}"
        for key, value in material_expected.items()
        if materials.get(key) != value
    )
    mismatches.extend(
        f"modelProfile.{key}={profile.get(key)!r} expected={value!r}"
        for key, value in profile_expected.items()
        if profile.get(key) != value
    )
    assets = config.get("assets", {})
    asset_expected = {
        "treeModel": f"./{EXPECTED_TREE}",
        "treeModelBytes": EXPECTED_TREE_BYTES,
        "treeModelSha256": EXPECTED_TREE_SHA256,
        "hedgeModel": f"./{EXPECTED_HEDGE}",
        "hedgeModelBytes": EXPECTED_HEDGE_BYTES,
        "hedgeModelSha256": EXPECTED_HEDGE_SHA256,
    }
    mismatches.extend(
        f"assets.{key}={assets.get(key)!r} expected={value!r}"
        for key, value in asset_expected.items()
        if assets.get(key) != value
    )
    lighting = config.get("lighting", {})
    if lighting.get("pipeline") != "V18-WEB-REALISM-LIGHTING-R2":
        mismatches.append(f"lighting.pipeline={lighting.get('pipeline')!r}")
    facts.update(config=config)
    return [
        Check(
            "central_config",
            "PASS" if not mismatches else "FAIL",
            f"release={config.get('release')} cache={config.get('cacheKey')} model={config.get('model')} "
            f"mismatches={'NONE' if not mismatches else '|'.join(mismatches)}",
        )
    ], facts


def check_asset(path: Path, expected_bytes: int, expected_sha: str, label: str) -> Check:
    if not path.is_file():
        return Check(label, "FAIL", f"missing={path}")
    size = path.stat().st_size
    digest = sha256_file(path)
    glb_valid = False
    try:
        parse_glb(path.read_bytes())
        glb_valid = True
    except Exception:  # reported in detail below without a second parser pass
        glb_valid = False
    ok = size == expected_bytes and digest == expected_sha and glb_valid
    return Check(
        label,
        "PASS" if ok else "FAIL",
        f"bytes={size}/{expected_bytes} sha256={digest}/{expected_sha} glb2={str(glb_valid).upper()}",
    )


def check_runtime_integration(root: Path) -> list[Check]:
    expected_imports = (
        f"../shared/project-config.js?release={EXPECTED_CACHE_KEY}",
        f"../shared/live-realism.js?release={EXPECTED_CACHE_KEY}&pipeline=lighting-r2",
        f"../shared/live-vegetation.js?release={EXPECTED_CACHE_KEY}",
    )
    checks: list[Check] = []
    for relative in ("presentation/presentation.js", "visite/visite.js"):
        path = root / relative
        if not path.is_file():
            checks.append(Check(f"runtime_imports_{relative.replace('/', '_')}", "FAIL", f"missing={path}"))
            continue
        text = path.read_text(encoding="utf-8-sig")
        missing = [item for item in expected_imports if item not in text]
        required_runtime = (
            "setupLiveLighting",
            "tuneLiveModel",
            "installLiveVegetation",
            "await installLiveVegetation",
            "config.cacheKey",
        )
        missing.extend(item for item in required_runtime if item not in text)
        checks.append(
            Check(
                f"runtime_imports_{relative.replace('/', '_')}",
                "PASS" if not missing else "FAIL",
                f"versioned_imports=3/3 runtime_hooks=5/5 missing={'NONE' if not missing else '|'.join(missing)}",
            )
        )
    return checks


def check_pages(root: Path) -> Check:
    page_specs: dict[str, tuple[str, ...]] = {
        "index.html": (EXPECTED_RELEASE, EXPECTED_CACHE_KEY, EXPECTED_MODEL, "SOURCE = LIVE WEB VIEWER"),
        "presentation/index.html": (EXPECTED_CACHE_KEY, "SOURCE = LIVE WEB VIEWER", "presentation.js"),
        "visite/index.html": (EXPECTED_CACHE_KEY, "SOURCE = LIVE WEB VIEWER", "visite.js", "Commencer dehors"),
        "rapide/index.html": (EXPECTED_CACHE_KEY, "SOURCE = BLENDER", "page-version.js"),
        "gpt/index.html": (EXPECTED_CACHE_KEY, EXPECTED_MODEL, "SOURCE = LIVE WEB VIEWER", "page-version.js"),
    }
    passed: list[str] = []
    failed: list[str] = []
    for relative, needles in page_specs.items():
        path = root / relative
        if not path.is_file():
            failed.append(f"{relative}:missing")
            continue
        text = path.read_text(encoding="utf-8-sig")
        missing = [needle for needle in needles if needle not in text]
        if missing:
            failed.append(f"{relative}:missing({','.join(missing)})")
        else:
            passed.append(relative)
    return Check(
        "runtime_pages_coherence",
        "PASS" if len(passed) == len(page_specs) and not failed else "FAIL",
        f"pages={len(passed)}/{len(page_specs)} passed={','.join(passed) or 'NONE'} failed={'NONE' if not failed else '|'.join(failed)}",
    )


def check_house_pair(root: Path) -> Check:
    left_path = root / "house.json"
    right_path = root / "gpt" / "house.json"
    try:
        left_bytes = left_path.read_bytes()
        right_bytes = right_path.read_bytes()
        left = load_json_unique(left_path)
        right = load_json_unique(right_path)
        model = left.get("media", {}).get("model", {})
        vegetation = left.get("media", {}).get("vegetation", {})
        tree = vegetation.get("tree", {})
        hedge = vegetation.get("hedge", {})
        expected_fields = (
            left.get("release") == EXPECTED_RELEASE,
            model.get("repository_path") == f"shared/{EXPECTED_MODEL}",
            model.get("bytes") == EXPECTED_MODEL_BYTES,
            model.get("sha256") == EXPECTED_MODEL_SHA256,
            left.get("source_policy", {}).get("interactive") == "LIVE WEB VIEWER",
            tree.get("repository_path") == f"shared/{EXPECTED_TREE}",
            tree.get("bytes") == EXPECTED_TREE_BYTES,
            tree.get("sha256") == EXPECTED_TREE_SHA256,
            hedge.get("repository_path") == f"shared/{EXPECTED_HEDGE}",
            hedge.get("bytes") == EXPECTED_HEDGE_BYTES,
            hedge.get("sha256") == EXPECTED_HEDGE_SHA256,
        )
        identical = left_bytes == right_bytes and left == right
        ok = identical and all(expected_fields)
        return Check(
            "house_json_pair",
            "PASS" if ok else "FAIL",
            f"byte_identical={str(left_bytes == right_bytes).upper()} semantic_identical={str(left == right).upper()} "
            f"release={left.get('release')} model={model.get('repository_path')} sha256={model.get('sha256')} "
            f"tree_sha256={tree.get('sha256')} hedge_sha256={hedge.get('sha256')}",
        )
    except Exception as exc:  # noqa: BLE001
        return Check("house_json_pair", "FAIL", f"{type(exc).__name__}: {exc}")


def check_old_tokens(root: Path) -> Check:
    runtime_files = (
        "index.html",
        "house.json",
        "gpt/index.html",
        "gpt/house.json",
        "presentation/index.html",
        "presentation/presentation.js",
        "visite/index.html",
        "visite/visite.js",
        "rapide/index.html",
        "shared/project-config.json",
        "shared/project-config.js",
        "shared/page-version.js",
        "shared/live-realism.js",
        "shared/live-vegetation.js",
    )
    forbidden = re.compile(r"(?i)(?:v18[-_ ]live[-_ ]sync[-_ ]?[1-4]\b|\bv16\b|\bv16[-_])")
    hits: list[str] = []
    scanned = 0
    for relative in runtime_files:
        path = root / relative
        if not path.is_file():
            hits.append(f"{relative}:MISSING")
            continue
        scanned += 1
        for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            match = forbidden.search(line)
            if match:
                hits.append(f"{relative}:{line_number}:{match.group(0)}")
    return Check(
        "obsolete_active_tokens",
        "PASS" if not hits else "FAIL",
        f"runtime_files={scanned}/{len(runtime_files)} hits={'NONE' if not hits else '|'.join(hits)}",
    )


def check_material_and_lighting_reports(root: Path) -> list[Check]:
    checks: list[Check] = []
    plan_path = root / "analysis" / "live_material_upgrade_plan.md"
    if not plan_path.is_file():
        checks.append(Check("material_upgrade_plan", "FAIL", f"missing={plan_path}"))
    else:
        text = plan_path.read_text(encoding="utf-8-sig")
        missing_fields = [field for field in MATERIAL_PLAN_FIELDS if field not in text]
        missing_aliases = [alias for alias in PRIORITY_ALIASES if alias not in text]
        checks.append(
            Check(
                "material_upgrade_plan",
                "PASS" if not missing_fields and not missing_aliases else "FAIL",
                f"fields={len(MATERIAL_PLAN_FIELDS) - len(missing_fields)}/{len(MATERIAL_PLAN_FIELDS)} "
                f"priority_aliases={len(PRIORITY_ALIASES) - len(missing_aliases)}/{len(PRIORITY_ALIASES)} "
                f"missing={'NONE' if not (missing_fields or missing_aliases) else '|'.join(missing_fields + missing_aliases)}",
            )
        )

    lighting_path = root / "analysis" / "live_lighting_tuning.md"
    if not lighting_path.is_file():
        checks.append(Check("lighting_tuning_report", "FAIL", f"missing={lighting_path}"))
    else:
        text = lighting_path.read_text(encoding="utf-8-sig")
        required = (
            "SOURCE = LIVE WEB VIEWER",
            "V18-WEB-REALISM-LIGHTING-R2",
            "HDRI",
            "tone mapping",
            "exposition",
            "AmbientLight",
            "directionnel",
            "ombre",
            "environnement",
        )
        missing = [item for item in required if item.lower() not in text.lower()]
        checks.append(
            Check(
                "lighting_tuning_report",
                "PASS" if not missing else "FAIL",
                f"required_topics={len(required) - len(missing)}/{len(required)} missing={'NONE' if not missing else '|'.join(missing)}",
            )
        )
    return checks


def markdown_sections(text: str) -> dict[str, str]:
    matches = list(re.finditer(r"(?m)^#{1,6}\s+([^\r\n#]+?)\s*$", text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        title = re.sub(r"^\d+(?:[.)-]|\s)+\s*", "", title).strip().upper()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[title] = text[match.end() : end]
    return result


def check_optional_reports(root: Path) -> list[Check]:
    checks: list[Check] = []
    defects_path = root / "validation" / "live_visual_defects.md"
    if not defects_path.is_file():
        checks.append(Check("live_visual_defects_report", "SKIP", "report_not_present_yet"))
    else:
        text = defects_path.read_text(encoding="utf-8-sig")
        sections = markdown_sections(text)
        missing_sections = [section for section in VISUAL_DEFECT_SECTIONS if section not in sections]
        missing_fields: list[str] = []
        for section in VISUAL_DEFECT_SECTIONS:
            body = sections.get(section, "")
            for field in VISUAL_DEFECT_FIELDS:
                if not re.search(rf"(?<![A-Z0-9_]){re.escape(field)}(?![A-Z0-9_])", body, re.IGNORECASE):
                    missing_fields.append(f"{section}.{field}")
        checks.append(
            Check(
                "live_visual_defects_report",
                "PASS" if not missing_sections and not missing_fields else "FAIL",
                f"sections={len(VISUAL_DEFECT_SECTIONS) - len(missing_sections)}/{len(VISUAL_DEFECT_SECTIONS)} "
                f"fields={len(VISUAL_DEFECT_SECTIONS) * len(VISUAL_DEFECT_FIELDS) - len(missing_fields)}/"
                f"{len(VISUAL_DEFECT_SECTIONS) * len(VISUAL_DEFECT_FIELDS)} "
                f"missing={'NONE' if not (missing_sections or missing_fields) else '|'.join(missing_sections + missing_fields)}",
            )
        )

    final_path = root / "validation" / "V18_WEB_REALISM_FIX_REPORT.md"
    if not final_path.is_file():
        checks.append(Check("final_realism_report", "SKIP", "report_not_present_yet"))
    else:
        text = final_path.read_text(encoding="utf-8-sig")

        def field_present(field: str) -> bool:
            patterns = (
                rf"(?mi)^\s*(?:[-*]\s*)?(?:\*\*)?{re.escape(field)}(?:\*\*)?\s*[:=]",
                rf"(?mi)^\s*\|\s*{re.escape(field)}\s*\|",
                rf"(?mi)^#{{1,6}}\s+{re.escape(field)}\s*$",
            )
            return any(re.search(pattern, text) for pattern in patterns)

        missing_fields = [field for field in FINAL_REPORT_FIELDS if not field_present(field)]
        normalized_lines = {line.strip().replace(" ", "") for line in text.splitlines()}
        missing_verdicts = [line for line in FINAL_VERDICTS if line not in normalized_lines]
        checks.append(
            Check(
                "final_realism_report",
                "PASS" if not missing_fields and not missing_verdicts else "FAIL",
                f"fields={len(FINAL_REPORT_FIELDS) - len(missing_fields)}/{len(FINAL_REPORT_FIELDS)} "
                f"pass_verdicts={len(FINAL_VERDICTS) - len(missing_verdicts)}/{len(FINAL_VERDICTS)} "
                f"missing={'NONE' if not (missing_fields or missing_verdicts) else '|'.join(missing_fields + missing_verdicts)}",
            )
        )
    return checks


def check_http(base_url: str | None) -> Check:
    if not base_url:
        return Check("http_200", "SKIP", "--base-url not supplied")
    base_url = base_url.rstrip("/") + "/"
    paths = (
        "",
        "presentation/",
        "visite/",
        "rapide/",
        "gpt/",
        "house.json",
        "gpt/house.json",
        "shared/project-config.json",
        f"shared/{EXPECTED_MODEL}",
        f"shared/{EXPECTED_TREE}",
        f"shared/{EXPECTED_HEDGE}",
        "shared/live-realism.js",
        "shared/live-vegetation.js",
    )
    statuses: list[str] = []
    failures: list[str] = []
    for relative in paths:
        url = urllib.parse.urljoin(base_url, relative)
        request = urllib.request.Request(url, headers={"User-Agent": "Chamagnieu-V18-static-validator/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                status = int(response.status)
                response.read(1)
            statuses.append(f"/{relative}:{status}")
            if status != 200:
                failures.append(f"/{relative}:{status}")
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            statuses.append(f"/{relative}:ERROR")
            failures.append(f"/{relative}:{type(exc).__name__}:{exc}")
    return Check(
        "http_200",
        "PASS" if not failures else "FAIL",
        f"resources={len(paths) - len(failures)}/{len(paths)} statuses={','.join(statuses)} "
        f"failures={'NONE' if not failures else '|'.join(failures)}",
    )


def render(checks: list[Check], root: Path, base_url: str | None, facts: dict[str, Any]) -> str:
    passed = sum(check.status == "PASS" for check in checks)
    failed = sum(check.status == "FAIL" for check in checks)
    skipped = sum(check.status == "SKIP" for check in checks)
    required_total = passed + failed
    verdict = "PASS" if failed == 0 else "FAIL"
    lines = [
        "V18_WEB_REALISM_STATIC_VALIDATION",
        f"ROOT={root}",
        f"BASE_URL={base_url or 'NOT_SUPPLIED'}",
        f"EXPECTED_RELEASE={EXPECTED_RELEASE}",
        f"EXPECTED_MODEL={EXPECTED_MODEL}",
        f"EXPECTED_MODEL_BYTES={EXPECTED_MODEL_BYTES}",
        f"EXPECTED_MODEL_SHA256={EXPECTED_MODEL_SHA256}",
    ]
    for check in checks:
        lines.append(f"CHECK {check.name}={check.status} :: {check.detail}")
    if facts:
        for key in sorted(key for key in facts if key != "config"):
            lines.append(f"FACT {key}={facts[key]}")
    lines.extend(
        [
            f"CHECKS_PASS={passed}",
            f"CHECKS_FAIL={failed}",
            f"CHECKS_SKIP={skipped}",
            f"CHECKS_REQUIRED_TOTAL={required_total}",
            f"V18_WEB_REALISM_STATIC_VALIDATION={verdict}",
            f"V18_WEB_REALISM_STATIC_RESULT={verdict} checks={passed}/{required_total} skipped={skipped} "
            f"release={EXPECTED_RELEASE} model={EXPECTED_MODEL} "
            f"model_sha256={facts.get('model_sha256', 'UNKNOWN')} "
            f"materials={facts.get('materials', 'UNKNOWN')} textures={facts.get('textures', 'UNKNOWN')} "
            f"images={facts.get('images', 'UNKNOWN')} bindings={facts.get('bindings', 'UNKNOWN')} "
            f"uri={facts.get('uri_count', 'UNKNOWN')} orphan_image_bytes={facts.get('orphan_image_bytes', 'UNKNOWN')} "
            f"orphan_buffer_views={facts.get('orphan_buffer_views', 'UNKNOWN')}",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="racine du checkout Chamagnieu (défaut: parent de validation/)",
    )
    parser.add_argument(
        "--base-url",
        help="base HTTP optionnelle; exige HTTP 200 sur les pages, GLB, assets et runtimes critiques",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="écrit aussi la sortie littérale dans ce fichier (chemin relatif résolu depuis --root)",
    )
    args = parser.parse_args()
    root = args.root.expanduser().resolve()

    checks: list[Check] = []
    facts: dict[str, Any] = {}
    config_checks, config_facts = check_config(root)
    checks.extend(config_checks)
    facts.update(config_facts)
    glb_checks, glb_facts = check_glb(root)
    checks.extend(glb_checks)
    facts.update(glb_facts)
    checks.extend(
        (
            check_asset(root / "shared" / EXPECTED_TREE, EXPECTED_TREE_BYTES, EXPECTED_TREE_SHA256, "tree_asset"),
            check_asset(root / "shared" / EXPECTED_HEDGE, EXPECTED_HEDGE_BYTES, EXPECTED_HEDGE_SHA256, "hedge_asset"),
        )
    )
    checks.extend(check_runtime_integration(root))
    checks.append(check_pages(root))
    checks.append(check_house_pair(root))
    checks.append(check_old_tokens(root))
    checks.extend(check_material_and_lighting_reports(root))
    checks.extend(check_optional_reports(root))
    checks.append(check_http(args.base_url))

    output = render(checks, root, args.base_url, facts)
    sys.stdout.write(output)
    if args.output:
        output_path = args.output if args.output.is_absolute() else root / args.output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8", newline="\n")
    return 0 if all(check.status != "FAIL" for check in checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
