#!/usr/bin/env python3
"""Normalize and export the pinned furniture winners for the live Web viewer.

Run with Blender 5.2 LTS:
  blender --background --factory-startup --python validation/optimize_selected_furniture_assets.py

Every result is centred on X/Z (Three.js coordinates) and rests on Y=0 after
export.  Texture payloads are embedded and no Draco/Meshopt decoder is needed.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import bpy
from mathutils import Vector


ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "assets_external" / "models"
PREVIEWS = ROOT / "validation" / "asset_pilot_previews"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def reset() -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)


def import_asset(role: str, source: Path) -> None:
    if source.suffix.lower() in {".glb", ".gltf"}:
        bpy.ops.import_scene.gltf(
            filepath=str(source), import_pack_images=True, import_webp_texture=True
        )
        return
    if source.suffix.lower() == ".blend":
        with bpy.data.libraries.load(str(source), link=False) as (data_from, data_to):
            data_to.objects = list(data_from.objects)
        for obj in data_to.objects:
            if obj is not None and obj.name not in bpy.context.scene.objects:
                bpy.context.collection.objects.link(obj)
        return
    raise ValueError(f"{role}: unsupported source {source}")


def mesh_objects() -> list[bpy.types.Object]:
    return [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]


def bounds(objects: list[bpy.types.Object]) -> tuple[Vector, Vector]:
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    if not points:
        raise RuntimeError("no mesh bounds")
    return (
        Vector(tuple(min(p[i] for p in points) for i in range(3))),
        Vector(tuple(max(p[i] for p in points) for i in range(3))),
    )


def triangles(objects: list[bpy.types.Object]) -> int:
    total = 0
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        mesh.calc_loop_triangles()
        total += len(mesh.loop_triangles)
        evaluated.to_mesh_clear()
    return total


def high_vertex_centroid(objects: list[bpy.types.Object], lo: Vector, hi: Vector) -> list[float] | None:
    threshold = lo.z + (hi.z - lo.z) * 0.72
    points: list[Vector] = []
    depsgraph = bpy.context.evaluated_depsgraph_get()
    for obj in objects:
        evaluated = obj.evaluated_get(depsgraph)
        mesh = evaluated.to_mesh()
        matrix = obj.matrix_world
        points.extend(matrix @ vertex.co for vertex in mesh.vertices if (matrix @ vertex.co).z >= threshold)
        evaluated.to_mesh_clear()
    if not points:
        return None
    mean = sum(points, Vector()) / len(points)
    return [round(mean.x, 5), round(mean.y, 5), round(mean.z, 5)]


def add_preview_scene(lo: Vector, hi: Vector) -> None:
    size = hi - lo
    span = max(size.x, size.y, size.z, 0.5)
    center = (lo + hi) * 0.5
    bpy.ops.object.camera_add(location=(span * 1.42, -span * 1.65, span * 1.16))
    camera = bpy.context.object
    camera.rotation_euler = (center - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 54
    bpy.context.scene.camera = camera
    for location, energy, size_factor in (
        ((span * 1.1, -span * 0.8, span * 1.9), 850, 1.6),
        ((-span * 1.0, span * 0.4, span * 1.25), 480, 1.25),
    ):
        bpy.ops.object.light_add(type="AREA", location=location)
        light = bpy.context.object
        light.data.energy = energy
        light.data.size = span * size_factor
        light.rotation_euler = (center - light.location).to_track_quat("-Z", "Y").to_euler()
    bpy.ops.mesh.primitive_plane_add(size=span * 7, location=(0, 0, -0.006))
    floor = bpy.context.object
    floor.name = "AUDIT_PREVIEW_FLOOR"
    mat = bpy.data.materials.new("Audit neutral floor")
    mat.diffuse_color = (0.16, 0.17, 0.16, 1)
    mat.roughness = 0.82
    floor.data.materials.append(mat)


def render(role: str, lo: Vector, hi: Vector) -> Path:
    add_preview_scene(lo, hi)
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 800
    scene.render.resolution_y = 650
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    if scene.world is None:
        scene.world = bpy.data.worlds.new("Furniture preview world")
    scene.world.color = (0.028, 0.034, 0.031)
    scene.view_settings.look = "AgX - Medium High Contrast"
    PREVIEWS.mkdir(parents=True, exist_ok=True)
    target = PREVIEWS / f"furniture-selected-{role}.png"
    scene.render.filepath = str(target)
    bpy.ops.render.render(write_still=True)
    return target


def source_for(role: str) -> Path:
    selected = MODELS / role / "original" / "selected"
    if role == "table":
        matches = list(selected.glob("*_source.blend"))
    elif role == "chair":
        matches = list(selected.glob("*_1k.gltf"))
    else:
        matches = list(selected.glob("*.glb"))
    if len(matches) != 1:
        raise RuntimeError(f"{role}: expected one selected source, got {len(matches)}")
    return matches[0]


def optimize(role: str) -> dict:
    reset()
    source = source_for(role)
    import_asset(role, source)
    objects = mesh_objects()
    if not objects:
        raise RuntimeError(f"{role}: source imported without a mesh")

    # The selected table source has no extra floor meshes, but the explicit
    # guard prevents a hidden preview plane from expanding the metric bounds.
    if role == "table":
        asset_like = [obj for obj in objects if not any(x in obj.name.lower() for x in ("floor", "ground", "plane"))]
        if asset_like:
            for obj in objects:
                if obj not in asset_like:
                    bpy.data.objects.remove(obj, do_unlink=True)
            objects = asset_like

    lo, hi = bounds(objects)
    original_dimensions = hi - lo
    direction_centroid = high_vertex_centroid(objects, lo, hi)
    roots = [obj for obj in bpy.context.scene.objects if obj.parent is None]
    pivot = bpy.data.objects.new(f"PILOT_FURNITURE_{role.upper()}_CC0", None)
    bpy.context.collection.objects.link(pivot)
    for obj in roots:
        if obj == pivot or obj.type in {"CAMERA", "LIGHT"}:
            continue
        matrix = obj.matrix_world.copy()
        obj.parent = pivot
        obj.matrix_world = matrix
    pivot.location = (-((lo.x + hi.x) * 0.5), -((lo.y + hi.y) * 0.5), -lo.z)
    pivot["asset_role"] = role
    pivot["asset_license"] = "CC0-1.0"
    pivot["source_sha256"] = digest(source)
    bpy.context.view_layer.update()

    normalized = mesh_objects()
    normalized_lo, normalized_hi = bounds(normalized)
    tri_count = triangles(normalized)
    materials = sorted(
        {
            slot.material.name
            for obj in normalized
            for slot in obj.material_slots
            if slot.material
        }
    )
    images = sorted(
        {
            image.name
            for material in bpy.data.materials
            if material.use_nodes and material.node_tree
            for node in material.node_tree.nodes
            if node.type == "TEX_IMAGE" and (image := node.image) is not None
        }
    )

    target = MODELS / role / "optimized" / "selected" / f"{role}_web.glb"
    target.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=str(target),
        export_format="GLB",
        export_yup=True,
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
        export_apply=True,
        export_unused_images=False,
        export_unused_textures=False,
    )
    preview = render(role, normalized_lo, normalized_hi)
    return {
        "role": role,
        "source": source.relative_to(ROOT).as_posix(),
        "source_bytes": source.stat().st_size,
        "source_sha256": digest(source),
        "optimized": target.relative_to(ROOT).as_posix(),
        "optimized_bytes": target.stat().st_size,
        "optimized_sha256": digest(target),
        "dimensions_m_blender_xyz": [round(x, 5) for x in original_dimensions],
        "dimensions_m_three_xzy": [
            round(original_dimensions.x, 5),
            round(original_dimensions.z, 5),
            round(original_dimensions.y, 5),
        ],
        "normalized_bounds_blender": {
            "min": [round(x, 5) for x in normalized_lo],
            "max": [round(x, 5) for x in normalized_hi],
        },
        "high_vertex_centroid_blender_before_normalization": direction_centroid,
        "triangles": tri_count,
        "mesh_objects": len(normalized),
        "materials": materials,
        "embedded_texture_sources": images,
        "preview": preview.relative_to(ROOT).as_posix(),
        "decoder_dependencies": [],
        "source_textures_preserved": True,
    }


def main() -> int:
    records = []
    for role in ("sofa", "table", "chair", "bed"):
        record = optimize(role)
        records.append(record)
        print(
            f"SELECTED_FURNITURE_OPTIMIZE=PASS role={role} "
            f"dimensions_three_m={record['dimensions_m_three_xzy']} "
            f"triangles={record['triangles']} bytes={record['optimized_bytes']} "
            f"sha256={record['optimized_sha256']}"
        )
    target = MODELS / "selected_furniture_optimization.json"
    target.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SELECTED_FURNITURE_OPTIMIZE_RESULT=PASS assets=4/4 output={target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
