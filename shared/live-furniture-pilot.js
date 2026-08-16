import * as THREE from './vendor/three.module.js';
import { GLTFLoader } from './vendor/addons/loaders/GLTFLoader.js';

const PILOT_GROUP_NAME = 'V18_ASSET_PILOT_FURNITURE';
const SOURCE_URLS = {
  sofa: new URL('../assets_external/furniture/living/sofa/optimized/sofa_web.glb', import.meta.url),
  table: new URL('../assets_external/furniture/dining/table/optimized/table_web.glb', import.meta.url),
  chair: new URL('../assets_external/furniture/dining/chair/optimized/chair_web.glb', import.meta.url),
  bed: new URL('../assets_external/furniture/bedroom/bed/optimized/bed_web.glb', import.meta.url)
};

// The metric placements use the plan-locked local coordinates of
// HOUSE_REFERENCE_ORIGIN.  Objects stay children of that same reference root,
// so the architecture's surveyed world rotation is preserved exactly.
const PLACEMENTS = {
  sofa: [
    { name: 'PILOT_LIVING_SOFA_3_SEAT', position: [2.5, 0.02, -9.78], yaw: 0, scale: [0.85, 0.85, 0.85], targetDimensionsM: [2.4416, 0.8546, 0.8599] }
  ],
  table: [
    { name: 'PILOT_DINING_TABLE', position: [2.5, 0.02, -7.18], yaw: 0, scale: [0.9, 1, 1], targetDimensionsM: [1.8, 0.75, 0.9] }
  ],
  chair: [
    { name: 'PILOT_DINING_CHAIR_01', position: [2.02, 0.02, -6.46], yaw: Math.PI, scale: [0.94, 0.94, 0.94] },
    { name: 'PILOT_DINING_CHAIR_02', position: [2.98, 0.02, -6.46], yaw: Math.PI, scale: [0.94, 0.94, 0.94] },
    { name: 'PILOT_DINING_CHAIR_03', position: [2.02, 0.02, -7.9], yaw: 0, scale: [0.94, 0.94, 0.94] },
    { name: 'PILOT_DINING_CHAIR_04', position: [2.98, 0.02, -7.9], yaw: 0, scale: [0.94, 0.94, 0.94] },
    { name: 'PILOT_DINING_CHAIR_05', position: [1.25, 0.02, -7.18], yaw: Math.PI / 2, scale: [0.94, 0.94, 0.94] },
    { name: 'PILOT_DINING_CHAIR_06', position: [3.75, 0.02, -7.18], yaw: -Math.PI / 2, scale: [0.94, 0.94, 0.94] }
  ],
  bed: [
    { name: 'PILOT_BEDROOM1_BED', position: [4.95, 2.69, -11.65], yaw: 0, scale: [0.908, 0.9, 0.898], targetDimensionsM: [1.6001, 0.9543, 2.0] },
    { name: 'PILOT_BEDROOM2_BED', position: [1.7, 2.69, -8.15], yaw: 0, scale: [0.7945, 0.9, 0.898], targetDimensionsM: [1.4, 0.9543, 2.0] },
    { name: 'PILOT_BEDROOM3_BED', position: [1.7, 2.69, -5.25], yaw: 0, scale: [0.7945, 0.9, 0.898], targetDimensionsM: [1.4, 0.9543, 2.0] }
  ]
};

const FALLBACK_MATCHERS = {
  sofa: name => name.toUpperCase().startsWith('V11_LIVING_SOFA'),
  table: name => name.toUpperCase().startsWith('V12_DINING_TABLE'),
  chair: name => name.toUpperCase().startsWith('V11_DINING_CHAIR_'),
  bed: name => /^V11_BEDROOM[123]_BED_/i.test(name)
};

function now() {
  return globalThis.performance?.now?.() ?? Date.now();
}

function cacheBustedUrl(input, cacheKey) {
  const url = new URL(input, globalThis.document?.baseURI || import.meta.url);
  if (cacheKey) url.searchParams.set('release', cacheKey);
  return url.href;
}

function loadGlb(url, timeoutMs = 20000) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      reject(new Error(`furniture-timeout:${timeoutMs}`));
    }, timeoutMs);
    new GLTFLoader().load(
      url,
      gltf => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        resolve(gltf.scene);
      },
      undefined,
      error => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        reject(error instanceof Error ? error : new Error(String(error)));
      }
    );
  });
}

function templateMetrics(root) {
  let triangles = 0;
  let meshes = 0;
  let drawCalls = 0;
  const geometries = new Set();
  const materials = new Set();
  const textures = new Set();
  root.traverse(object => {
    if (!object.isMesh) return;
    meshes += 1;
    const assigned = Array.isArray(object.material) ? object.material : [object.material];
    drawCalls += assigned.length;
    if (!geometries.has(object.geometry.uuid)) {
      geometries.add(object.geometry.uuid);
      const count = object.geometry.index?.count ?? object.geometry.attributes.position?.count ?? 0;
      triangles += Math.floor(count / 3);
    }
    for (const material of assigned) {
      if (!material) continue;
      materials.add(material.uuid);
      for (const key of ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap']) {
        if (material[key]?.uuid) textures.add(material[key].uuid);
      }
    }
  });
  root.updateMatrixWorld(true);
  const size = new THREE.Box3().setFromObject(root).getSize(new THREE.Vector3());
  return {
    meshes,
    triangles,
    drawCalls,
    materials: materials.size,
    textures: textures.size,
    dimensionsM: [size.x, size.y, size.z].map(value => Number(value.toFixed(5)))
  };
}

function tuneTemplate(root, renderer, role) {
  const maxAnisotropy = renderer?.capabilities?.getMaxAnisotropy?.() || 1;
  const anisotropy = Math.min(8, maxAnisotropy);
  const seenMaterials = new Set();
  root.traverse(object => {
    object.userData.isFurnitureTree = true;
    object.userData.assetPilotRole = role;
    if (!object.isMesh) return;
    object.castShadow = true;
    object.receiveShadow = true;
    object.frustumCulled = true;
    const assigned = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of assigned) {
      if (!material || seenMaterials.has(material.uuid)) continue;
      seenMaterials.add(material.uuid);
      material.roughness = Math.max(material.roughness ?? 0.55, role === 'table' ? 0.38 : 0.48);
      for (const key of ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap']) {
        const texture = material[key];
        if (!texture) continue;
        texture.anisotropy = anisotropy;
        texture.needsUpdate = true;
      }
      material.needsUpdate = true;
    }
  });
}

function restorePreviouslyHiddenFallbacks(house) {
  house.traverse(object => {
    if (!object.userData.assetPilotFurnitureFallbackHidden) return;
    object.visible = object.userData.assetPilotFurnitureFallbackWasVisible !== false;
    delete object.userData.assetPilotFurnitureFallbackHidden;
    delete object.userData.assetPilotFurnitureFallbackWasVisible;
  });
}

function hideFallbackFamily(house, role) {
  const names = [];
  const matches = FALLBACK_MATCHERS[role];
  house.traverse(object => {
    if (!matches(object.name || '')) return;
    object.userData.assetPilotFurnitureFallbackWasVisible = object.visible;
    object.userData.assetPilotFurnitureFallbackHidden = true;
    object.visible = false;
    names.push(object.name);
  });
  return names.sort();
}

function instantiateFamily(template, role) {
  const group = new THREE.Group();
  group.name = `PILOT_FURNITURE_${role.toUpperCase()}_FAMILY`;
  group.userData.isFurnitureTree = true;
  group.userData.assetPilotRole = role;
  const placements = [];
  for (const placement of PLACEMENTS[role]) {
    const instance = template.clone(true);
    instance.name = placement.name;
    instance.position.fromArray(placement.position);
    instance.rotation.y = placement.yaw;
    instance.scale.fromArray(placement.scale);
    instance.userData.isFurnitureTree = true;
    instance.userData.assetPilotRole = role;
    instance.traverse(object => {
      object.userData.isFurnitureTree = true;
      object.userData.assetPilotRole = role;
    });
    group.add(instance);
    placements.push({
      name: placement.name,
      position: [...placement.position],
      yawRadians: Number(placement.yaw.toFixed(6)),
      scale: [...placement.scale],
      targetDimensionsM: placement.targetDimensionsM || null
    });
  }
  return { group, placements };
}

/**
 * Load four accepted CC0 families and replace only each successfully loaded
 * fallback family.  A failed request leaves that role's original furniture
 * visible, so network errors never create an empty room.
 */
export async function installLiveFurniturePilot({ scene, house, renderer, cacheKey, timeoutMs = 30000 }) {
  if (!scene || !house) throw new Error('furniture-pilot-missing-scene-or-house');
  const started = now();
  const anchor = house.getObjectByName('HOUSE_REFERENCE_ORIGIN') || house;
  restorePreviouslyHiddenFallbacks(house);
  const previous = anchor.getObjectByName(PILOT_GROUP_NAME);
  if (previous?.parent) previous.parent.remove(previous);

  const pilot = new THREE.Group();
  pilot.name = PILOT_GROUP_NAME;
  pilot.userData.isFurnitureTree = true;
  pilot.userData.assetPilot = true;
  // Attach the empty transaction container first. Each accepted family then
  // becomes visible in the same synchronous step that hides its fallback.
  anchor.add(pilot);
  const audit = {
    version: 'V18_ASSET_FURNITURE_PILOT_1',
    status: 'loading',
    architectureChanged: false,
    anchor: anchor.name || 'GLTF_SCENE',
    fallbackPolicy: 'replace-per-family-only-after-success',
    families: {},
    acceptedFamilies: 0,
    rejectedFamilies: 0,
    instanceCount: 0,
    elapsedMs: null
  };
  globalThis.__assetPilotFurnitureAudit = audit;

  const roles = ['sofa', 'table', 'chair', 'bed'];
  const settled = await Promise.allSettled(
    roles.map(async role => {
      const url = cacheBustedUrl(SOURCE_URLS[role], cacheKey);
      const loadedAt = now();
      const template = await loadGlb(url, timeoutMs);
      tuneTemplate(template, renderer, role);
      const metrics = templateMetrics(template);
      const replacement = instantiateFamily(template, role);
      // The replacement hierarchy is complete before the corresponding source
      // nodes are hidden.  This is the transactional visual handover.
      pilot.add(replacement.group);
      const hiddenFallbackNodes = hideFallbackFamily(house, role);
      audit.families[role] = {
        status: 'accepted-live',
        url,
        loadMs: Number((now() - loadedAt).toFixed(2)),
        sourceMetrics: metrics,
        hiddenFallbackNodes,
        placements: replacement.placements,
        instances: replacement.placements.length
      };
      return role;
    })
  );

  for (let i = 0; i < settled.length; i += 1) {
    const result = settled[i];
    const role = roles[i];
    if (result.status === 'fulfilled') continue;
    audit.families[role] = {
      status: 'rejected-live-fallback-retained',
      url: cacheBustedUrl(SOURCE_URLS[role], cacheKey),
      error: result.reason?.message || String(result.reason),
      instances: 0,
      hiddenFallbackNodes: []
    };
  }
  const accepted = Object.values(audit.families).filter(family => family.status === 'accepted-live');
  audit.acceptedFamilies = accepted.length;
  audit.rejectedFamilies = roles.length - accepted.length;
  audit.instanceCount = accepted.reduce((sum, family) => sum + family.instances, 0);
  audit.status = accepted.length === roles.length ? 'accepted' : accepted.length ? 'partial-fallback' : 'fallback';
  audit.elapsedMs = Number((now() - started).toFixed(2));
  globalThis.__assetPilotFurnitureAudit = audit;
  return audit;
}

export { PLACEMENTS as FURNITURE_PILOT_PLACEMENTS };
