#!/usr/bin/env python3
"""Blender-side normalization and Web export for the four pilot models.

Run with Blender, not the system Python:
  blender --background --factory-startup --python validation/optimize_pilot_model_assets.py

The library GLBs use Draco compression.  The live viewer deliberately has no
Draco decoder, so this script imports them once, normalizes the origin to the
floor/centre, and exports embedded WebP GLBs without decoder-dependent geometry
extensions.  Source files under ``original`` are never modified.
"""

from __future__ import annotations

import hashlib
import json
import math
import pathlib

import bpy
from mathutils import Vector


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets_external" / "models"
PREVIEWS = ROOT / "validation" / "asset_pilot_previews"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def scene_reset() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name != "Collection":
            bpy.data.collections.remove(collection)


def mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def world_bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points: list[Vector] = []
    for obj in objects:
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
    hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
    return lo, hi


def triangle_count(objects: list[bpy.types.Object]) -> int:
    total = 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        evaluated.to_mesh_clear()
    return total


def add_preview_camera(lo: Vector, hi: Vector) -> None:
    size = hi - lo
    center = (lo + hi) * 0.5
    span = max(size.x, size.y, size.z, 0.5)
    bpy.ops.object.camera_add(location=(span * 1.55, -span * 1.8, span * 1.25))
    camera = bpy.context.object
    camera.name = "AUDIT_PREVIEW_CAMERA"
    direction = center - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 52
    bpy.context.scene.camera = camera

    bpy.ops.object.light_add(type="AREA", location=(span * 1.2, -span * 0.7, span * 2.0))
    key = bpy.context.object
    key.data.energy = 900
    key.data.shape = "DISK"
    key.data.size = span * 1.8
    direction = center - key.location
    key.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    bpy.ops.object.light_add(type="AREA", location=(-span * 1.1, span * 0.5, span * 1.2))
    fill = bpy.context.object
    fill.data.energy = 520
    fill.data.size = span * 1.3
    direction = center - fill.location
    fill.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    bpy.ops.mesh.primitive_plane_add(size=span * 8, location=(0, 0, -0.006))
    floor = bpy.context.object
    floor.name = "AUDIT_PREVIEW_FLOOR"
    material = bpy.data.materials.new("Audit floor")
    material.diffuse_color = (0.14, 0.15, 0.14, 1.0)
    floor.data.materials.append(material)


def render_preview(role: str, lo: Vector, hi: Vector) -> pathlib.Path:
    add_preview_camera(lo, hi)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 720
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.world.color = (0.035, 0.042, 0.038)
    scene.view_settings.look = "AgX - Medium High Contrast"
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    path = PREVIEWS / f"{role}-optimized-preview.png"
    scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)
    return path


def optimize(role: str, source: pathlib.Path) -> dict:
    scene_reset()
    bpy.ops.import_scene.gltf(filepath=str(source), import_pack_images=True, import_webp_texture=True)
    objects = mesh_objects()
    if not objects:
        raise RuntimeError(f"{role}: no mesh imported")

    lo, hi = world_bounds(objects)
    original_dimensions = hi - lo
    roots = [obj for obj in bpy.context.scene.objects if obj.parent is None]
    pivot = bpy.data.objects.new(f"PILOT_{role.upper()}_CC0", None)
    bpy.context.collection.objects.link(pivot)
    for obj in roots:
        if obj == pivot:
            continue
        matrix = obj.matrix_world.copy()
        obj.parent = pivot
        obj.matrix_world = matrix
    pivot.location = (-((lo.x + hi.x) * 0.5), -((lo.y + hi.y) * 0.5), -lo.z)
    pivot["asset_role"] = role
    pivot["asset_license"] = "CC0-1.0"
    pivot["asset_library"] = "BlenderKit"
    pivot["source_file_sha256"] = sha256(source)
    bpy.context.view_layer.update()

    normalized_objects = mesh_objects()
    normalized_lo, normalized_hi = world_bounds(normalized_objects)
    triangles = triangle_count(normalized_objects)
    materials = sorted({slot.material.name for obj in normalized_objects for slot in obj.material_slots if slot.material})

    optimized = source.parents[1] / "optimized" / f"{role}_web.glb"
    optimized.parent.mkdir(parents=True, exist_ok=True)
    # Preview helpers are created after export so they cannot leak into the GLB.
    bpy.ops.export_scene.gltf(
        filepath=str(optimized),
        export_format="GLB",
        export_yup=True,
        # AUTO preserves the source WebP/JPEG/PNG payloads and avoids Blender's
        # WebP writer rejecting valid one-channel roughness/sheen images.
        export_image_format="AUTO",
        export_image_quality=82,
        export_image_add_webp=False,
        export_draco_mesh_compression_enable=False,
        export_meshopt_compression_enable=False,
        export_use_gltfpack=False,
        export_animations=False,
        export_cameras=False,
        export_lights=False,
        export_extras=True,
        export_unused_images=False,
        export_unused_textures=False,
        export_apply=True,
    )
    preview = render_preview(role, normalized_lo, normalized_hi)

    return {
        "role": role,
        "source": source.relative_to(ROOT).as_posix(),
        "source_bytes": source.stat().st_size,
        "source_sha256": sha256(source),
        "optimized": optimized.relative_to(ROOT).as_posix(),
        "optimized_bytes": optimized.stat().st_size,
        "optimized_sha256": sha256(optimized),
        "dimensions_m": [round(v, 4) for v in original_dimensions],
        "normalized_bounds_m": {
            "min": [round(v, 5) for v in normalized_lo],
            "max": [round(v, 5) for v in normalized_hi],
        },
        "triangles": triangles,
        "mesh_objects": len(normalized_objects),
        "materials": materials,
        "preview": preview.relative_to(ROOT).as_posix(),
        "decoder_dependencies_removed": ["KHR_draco_mesh_compression"],
        "texture_codec": "source-preserving WebP/JPEG/PNG",
    }


def main() -> None:
    records = []
    for role in ("sofa", "table", "chair", "bed"):
        sources = list((MODELS / role / "original").glob("*.glb"))
        if len(sources) != 1:
            raise RuntimeError(f"{role}: expected exactly one source GLB, got {len(sources)}")
        record = optimize(role, sources[0])
        records.append(record)
        print(
            f"MODEL_OPTIMIZE=PASS role={role} dimensions_m={record['dimensions_m']} "
            f"triangles={record['triangles']} bytes={record['optimized_bytes']} "
            f"sha256={record['optimized_sha256']}"
        )
    output = MODELS / "pilot_model_optimization.json"
    output.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"MODEL_OPTIMIZE_RESULT=PASS assets={len(records)}/4 output={output}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        traceback.print_exc()
        raise SystemExit(1)
