"""Build lightweight CC0 Poly Haven vegetation assets for the V18 Web viewer.

Run with Blender 5.x, for example:
  blender --background --python validation/build_v18_web_vegetation.py -- \
    --source-root C:/.../assets/models \
    --output-dir shared/assets/vegetation

The script never writes into ``source-root``.  It records source digests before
and after conversion, downsizes embedded images in Blender memory, decimates
the very dense tree by material, and emits self-contained GLB files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import bpy


TREE_TARGETS = {
    "island_tree_02": 5_000,
    "island_tree_02_leaves": 30_000,
    "island_tree_02_branches": 12_000,
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def file_inventory(root: Path) -> dict[str, dict[str, object]]:
    return {
        str(path.relative_to(root)).replace("\\", "/"): {
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def triangle_count(mesh: bpy.types.Mesh) -> int:
    return sum(max(0, len(poly.vertices) - 2) for poly in mesh.polygons)


def scene_metrics() -> dict[str, object]:
    objects = []
    total_triangles = 0
    for obj in sorted(bpy.context.scene.objects, key=lambda item: item.name):
        if obj.type != "MESH":
            continue
        triangles = triangle_count(obj.data)
        total_triangles += triangles
        used_materials = sorted(
            {
                obj.data.materials[poly.material_index].name
                for poly in obj.data.polygons
                if poly.material_index < len(obj.data.materials)
                and obj.data.materials[poly.material_index]
            }
        )
        objects.append(
            {
                "name": obj.name,
                "triangles": triangles,
                "vertices": len(obj.data.vertices),
                "materials": used_materials,
                "dimensions_m": [round(float(value), 5) for value in obj.dimensions],
            }
        )
    return {"triangles": total_triangles, "mesh_objects": objects}


def load_asset(path: Path) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    result = bpy.ops.import_scene.gltf(filepath=str(path))
    if "FINISHED" not in result:
        raise RuntimeError(f"glTF import failed: {path}")


def split_tree_by_material() -> None:
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if len(mesh_objects) != 1:
        raise RuntimeError(f"Expected one source tree mesh, found {len(mesh_objects)}")
    obj = mesh_objects[0]
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.separate(type="MATERIAL")
    bpy.ops.object.mode_set(mode="OBJECT")


def join_shrub_meshes() -> None:
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if not mesh_objects:
        raise RuntimeError("The shrub asset contains no mesh")
    material = next(
        (slot.material for obj in mesh_objects for slot in obj.material_slots if slot.material),
        None,
    )
    bpy.ops.object.select_all(action="DESELECT")
    for obj in mesh_objects:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_objects[0]
    bpy.ops.object.join()
    joined = bpy.context.view_layer.objects.active
    for poly in joined.data.polygons:
        poly.material_index = 0
    joined.data.materials.clear()
    if material:
        joined.data.materials.append(material)
    joined.name = "WEB_shrub_03"
    joined.data.name = "WEB_shrub_03_mesh"


def semantic_material_name(obj: bpy.types.Object) -> str:
    names = {
        obj.data.materials[poly.material_index].name
        for poly in obj.data.polygons
        if poly.material_index < len(obj.data.materials)
        and obj.data.materials[poly.material_index]
    }
    if len(names) != 1:
        raise RuntimeError(f"Could not identify a unique material for {obj.name}: {names}")
    return next(iter(names))


def decimate_tree() -> list[dict[str, object]]:
    report = []
    for obj in [item for item in bpy.context.scene.objects if item.type == "MESH"]:
        material_name = semantic_material_name(obj)
        before = triangle_count(obj.data)
        target = TREE_TARGETS[material_name]
        ratio = min(1.0, target / max(1, before))
        if ratio < 0.999:
            bpy.ops.object.select_all(action="DESELECT")
            obj.select_set(True)
            bpy.context.view_layer.objects.active = obj
            modifier = obj.modifiers.new(name="WEB_DECIMATE", type="DECIMATE")
            modifier.decimate_type = "COLLAPSE"
            modifier.ratio = ratio
            modifier.use_collapse_triangulate = True
            bpy.ops.object.modifier_apply(modifier=modifier.name)
        after = triangle_count(obj.data)
        obj.name = f"WEB_{material_name}"
        obj.data.name = f"WEB_{material_name}_mesh"
        report.append(
            {
                "material": material_name,
                "triangles_before": before,
                "triangles_after": after,
                "target": target,
                "ratio": round(ratio, 8),
            }
        )
    return sorted(report, key=lambda item: item["material"])


def resize_images(max_size: int) -> list[dict[str, object]]:
    report = []
    for image in sorted(bpy.data.images, key=lambda item: item.name):
        if image.source != "FILE":
            continue
        if not image.has_data:
            image.reload()
        before = [int(image.size[0]), int(image.size[1])]
        largest = max(before)
        if largest > max_size:
            factor = max_size / largest
            width = max(1, int(round(before[0] * factor)))
            height = max(1, int(round(before[1] * factor)))
            image.scale(width, height)
        image.pack()
        after = [int(image.size[0]), int(image.size[1])]
        report.append({"name": image.name, "before_px": before, "after_px": after})
    return report


def configure_materials() -> None:
    for material in bpy.data.materials:
        material.diffuse_color[3] = 1.0
        if "leaves" in material.name.lower() or "shrub" in material.name.lower():
            if hasattr(material, "surface_render_method"):
                material.surface_render_method = "DITHERED"
            if hasattr(material, "use_transparency_overlap"):
                material.use_transparency_overlap = False


def export_glb(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action="SELECT")
    result = bpy.ops.export_scene.gltf(
        filepath=str(path),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_image_format="JPEG",
        export_image_quality=78,
        export_materials="EXPORT",
        export_cameras=False,
        export_lights=False,
        export_extras=True,
    )
    if "FINISHED" not in result or not path.is_file():
        raise RuntimeError(f"GLB export failed: {path}")


def build_one(source_root: Path, output_dir: Path, asset_id: str) -> dict[str, object]:
    source_dir = source_root / asset_id
    source_gltf = source_dir / f"{asset_id}_1k.gltf"
    before_hashes = file_inventory(source_dir)
    load_asset(source_gltf)
    source_metrics = scene_metrics()
    decimation = []
    if asset_id == "island_tree_02":
        split_tree_by_material()
        decimation = decimate_tree()
    else:
        join_shrub_meshes()
    images = resize_images(max_size=512)
    configure_materials()
    output_path = output_dir / f"{asset_id}_web.glb"
    export_glb(output_path)
    output_metrics = scene_metrics()
    after_hashes = file_inventory(source_dir)
    if before_hashes != after_hashes:
        raise RuntimeError(f"Source asset changed during conversion: {asset_id}")
    return {
        "asset_id": asset_id,
        "source_gltf": str(source_gltf),
        "source_preserved": True,
        "source_inventory": before_hashes,
        "source_metrics": source_metrics,
        "decimation": decimation,
        "images": images,
        "output": str(output_path),
        "output_bytes": output_path.stat().st_size,
        "output_sha256": sha256(output_path),
        "output_metrics": output_metrics,
    }


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args(argv)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "builder": "Blender " + bpy.app.version_string,
        "texture_max_px": 512,
        "assets": [
            build_one(args.source_root, args.output_dir, "shrub_03"),
            build_one(args.source_root, args.output_dir, "island_tree_02"),
        ],
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("VEGETATION_BUILD_RESULT=PASS")
    for asset in result["assets"]:
        print(
            "VEGETATION_ASSET="
            f"{asset['asset_id']} bytes={asset['output_bytes']} "
            f"triangles={asset['output_metrics']['triangles']} "
            f"sha256={asset['output_sha256']}"
        )


if __name__ == "__main__":
    main()
