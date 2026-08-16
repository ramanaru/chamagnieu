import * as THREE from './vendor/three.module.js';
import { GLTFLoader } from './vendor/addons/loaders/GLTFLoader.js';

const DEFAULT_TREE_URL = new URL('./assets/vegetation/island_tree_02_web.glb', import.meta.url);
const DEFAULT_HEDGE_URL = new URL('../assets_external/vegetation/hedges/blenderkit_shrub/optimized/hedge_web.glb', import.meta.url);
const DEFAULT_HEDGE_FALLBACK_URL = new URL('./assets/vegetation/shrub_03_web.glb', import.meta.url);
const ENHANCED_GROUP_NAME = 'V18_WEB_REALISM_VEGETATION';
const TREE_PATTERN = /^V17_TREE_LIGHT_(\d{2})_(?:BRANCH_[LR]|CANOPY_(?:C|L|R|TOP)|TRUNK)$/i;
const HEDGE_PATTERN = /^V17_HEDGE_LIGHT_\d{2}$/i;

function now() {
  return globalThis.performance?.now?.() ?? Date.now();
}

function cacheBustedUrl(input, cacheKey) {
  const url = new URL(input, globalThis.document?.baseURI || import.meta.url);
  if (cacheKey) url.searchParams.set('release', cacheKey);
  return url.href;
}

function loadGlb(url, timeoutMs) {
  return new Promise((resolve, reject) => {
    let settled = false;
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      reject(new Error(`vegetation-timeout:${timeoutMs}`));
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

function tuneTemplate(root, renderer, family) {
  const maxAnisotropy = renderer?.capabilities?.getMaxAnisotropy?.() || 1;
  const anisotropy = Math.min(8, maxAnisotropy);
  const seenMaterials = new Set();
  root.traverse(object => {
    if (!object.isMesh) return;
    object.castShadow = true;
    object.receiveShadow = true;
    object.frustumCulled = true;
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of materials) {
      if (!material || seenMaterials.has(material.uuid)) continue;
      seenMaterials.add(material.uuid);
      material.side = THREE.DoubleSide;
      material.metalness = 0;
      material.roughness = Math.max(material.roughness ?? 0.75, family === 'hedge' ? 0.82 : 0.72);
      material.transparent = false;
      material.depthWrite = true;
      if (/leaf|leaves|shrub/i.test(material.name)) {
        // Keep the small leaf cards visible after the source shrub is scaled to
        // hedge dimensions.  A low deterministic cutout threshold gives the
        // two staggered rows a dense silhouette without alpha blending.
        material.alphaTest = family === 'hedge' ? 0.24 : Math.max(material.alphaTest || 0, 0.32);
        material.color.multiply(new THREE.Color(family === 'hedge' ? 0x7d9a70 : 0x91aa84));
      }
      if (/branch|island_tree_02$/i.test(material.name)) {
        material.color.multiply(new THREE.Color(0xb79f82));
      }
      for (const key of ['map', 'normalMap', 'roughnessMap', 'aoMap']) {
        const texture = material[key];
        if (!texture) continue;
        texture.anisotropy = anisotropy;
        texture.needsUpdate = true;
      }
      material.needsUpdate = true;
    }
  });
}

function templateMetrics(root) {
  let triangles = 0;
  let drawCalls = 0;
  let meshes = 0;
  const geometries = new Set();
  const materials = new Set();
  root.traverse(object => {
    if (!object.isMesh) return;
    meshes += 1;
    drawCalls += Array.isArray(object.material) ? object.material.length : 1;
    const geometry = object.geometry;
    if (!geometries.has(geometry.uuid)) {
      geometries.add(geometry.uuid);
      const count = geometry.index?.count ?? geometry.attributes.position?.count ?? 0;
      triangles += Math.floor(count / 3);
    }
    const list = Array.isArray(object.material) ? object.material : [object.material];
    for (const material of list) if (material) materials.add(material.uuid);
  });
  return { triangles, drawCalls, meshes, uniqueGeometries: geometries.size, uniqueMaterials: materials.size };
}

function normalizedTemplate(source) {
  const wrapper = new THREE.Group();
  wrapper.add(source);
  source.updateWorldMatrix(true, true);
  const box = new THREE.Box3().setFromObject(source);
  const size = box.getSize(new THREE.Vector3());
  const center = box.getCenter(new THREE.Vector3());
  source.position.x -= center.x;
  source.position.y -= box.min.y;
  source.position.z -= center.z;
  source.updateWorldMatrix(true, true);
  wrapper.userData.sourceSize = size.toArray();
  return { wrapper, size };
}

function findOriginalVegetation(house) {
  const treeFamilies = new Map();
  const hedges = [];
  house.updateWorldMatrix(true, true);
  house.traverse(object => {
    const treeMatch = TREE_PATTERN.exec(object.name);
    if (treeMatch) {
      const family = treeFamilies.get(treeMatch[1]) || [];
      family.push(object);
      treeFamilies.set(treeMatch[1], family);
    } else if (HEDGE_PATTERN.test(object.name)) {
      hedges.push(object);
    }
  });
  return { treeFamilies, hedges };
}

function familyBox(objects) {
  const box = new THREE.Box3();
  for (const object of objects) box.union(new THREE.Box3().setFromObject(object));
  return box;
}

function hideOriginals(objects, reason) {
  for (const object of objects) {
    object.visible = false;
    object.userData.hiddenByLiveVegetation = reason;
  }
}

function installTrees(parent, house, template, sourceSize, families) {
  const allOriginals = [];
  let instances = 0;
  for (const [familyId, objects] of [...families.entries()].sort(([a], [b]) => a.localeCompare(b))) {
    const trunk = objects.find(object => /_TRUNK$/i.test(object.name));
    if (!trunk) continue;
    const oldBox = familyBox(objects);
    const oldSize = oldBox.getSize(new THREE.Vector3());
    const oldCenter = oldBox.getCenter(new THREE.Vector3());
    const trunkPosition = trunk.getWorldPosition(new THREE.Vector3());
    const scale = oldSize.y / Math.max(0.001, sourceSize.y);
    const clone = template.clone(true);
    clone.name = `V18_REAL_TREE_${familyId}`;
    clone.scale.setScalar(scale);
    clone.rotation.y = Number(familyId) * 0.73 + 0.17;
    clone.position.set(
      trunkPosition.x,
      oldBox.min.y,
      trunkPosition.z
    );
    clone.userData.liveVegetationFamily = familyId;
    clone.userData.replaces = objects.map(object => object.name);
    parent.add(clone);
    allOriginals.push(...objects);
    instances += 1;
  }
  if (instances) hideOriginals(allOriginals, 'V18_REAL_TREE');
  return { instances, originalsHidden: instances ? allOriginals.length : 0 };
}

function installLegacyHedges(parent, template, sourceSize, hedges) {
  let instances = 0;
  let cloneInstances = 0;
  const installed = [];
  for (const [index, hedge] of hedges.entries()) {
    const box = new THREE.Box3().setFromObject(hedge);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const alongX = size.x >= size.z;
    const longSide = Math.max(size.x, size.z);
    const shortSide = Math.min(size.x, size.z);
    const segment = new THREE.Group();
    const segmentId = String(index + 1).padStart(2, '0');
    segment.name = `V18_REAL_HEDGE_${segmentId}`;
    segment.position.set(center.x, box.min.y, center.z);
    segment.rotation.y = alongX ? 0 : Math.PI / 2;
    segment.userData.replaces = hedge.name;
    segment.userData.rowCount = 2;

    // Three shorter shrub clumps per row retain the leaf density of the source
    // asset. Stretching one clump over the complete segment made the hedge
    // read as sparse branches rather than a continuous, newly planted hedge.
    const tilesPerRow = 3;
    const tileSpan = longSide / tilesPerRow;
    for (let rowIndex = 0; rowIndex < 2; rowIndex += 1) {
      for (let tileIndex = 0; tileIndex < tilesPerRow; tileIndex += 1) {
        const seed = (index + 1) * 17 + (rowIndex + 1) * 29 + (tileIndex + 1) * 43;
        const lengthVariation = 1 + ((seed % 7) - 3) * 0.008;
        const heightVariation = 1 + (((seed * 3) % 5) - 2) * 0.012;
        const yawVariation = (((seed * 5) % 7) - 3) * 0.010;
        const longitudinalShift = (((seed * 11) % 5) - 2) * tileSpan * 0.018;
        const tile = template.clone(true);
        tile.name = `V18_REAL_HEDGE_${segmentId}_ROW_${rowIndex === 0 ? 'A' : 'B'}_TILE_${tileIndex + 1}`;
        tile.position.set(
          -longSide * 0.5 + tileSpan * (tileIndex + 0.5) + longitudinalShift,
          rowIndex * size.y * 0.015,
          (rowIndex === 0 ? -1 : 1) * shortSide * 0.20
        );
        tile.rotation.y = yawVariation;
        tile.scale.set(
          tileSpan * 1.28 * lengthVariation / Math.max(0.001, sourceSize.x),
          size.y * 1.28 * heightVariation / Math.max(0.001, sourceSize.y),
          shortSide * 0.82 / Math.max(0.001, sourceSize.z)
        );
        tile.userData.liveVegetationRow = rowIndex;
        tile.userData.liveVegetationTile = tileIndex;
        segment.add(tile);
        cloneInstances += 1;
      }
    }
    parent.add(segment);
    installed.push(hedge);
    instances += 1;
  }
  if (instances) hideOriginals(installed, 'V18_REAL_HEDGE');
  return { instances, cloneInstances, originalsHidden: instances ? installed.length : 0 };
}

function relativeMeshRecords(template) {
  template.updateWorldMatrix(true, true);
  const inverse = template.matrixWorld.clone().invert();
  const records = [];
  template.traverse(object => {
    if (!object.isMesh) return;
    records.push({
      source: object,
      matrix: inverse.clone().multiply(object.matrixWorld)
    });
  });
  return records;
}

/**
 * Install one full, dense CC0 shrub per architectural hedge segment.
 *
 * The 18 transformations are rendered through one InstancedMesh per source
 * mesh/material instead of 108 cloned Object3D trees.  This keeps the real
 * segment bounds and leaf silhouettes while reducing the hedge path to two GPU
 * batches for the optimized two-mesh asset.
 */
function installInstancedHedges(parent, template, sourceSize, hedges) {
  const records = relativeMeshRecords(template);
  const placements = [];
  for (const [index, hedge] of hedges.entries()) {
    const box = new THREE.Box3().setFromObject(hedge);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    const alongX = size.x >= size.z;
    const longSide = Math.max(size.x, size.z);
    const shortSide = Math.min(size.x, size.z);
    const seed = (index + 1) * 97;
    const lengthVariation = 1 + ((seed % 7) - 3) * 0.006;
    const heightVariation = 1 + (((seed * 3) % 5) - 2) * 0.012;
    const yawVariation = (((seed * 5) % 7) - 3) * 0.008;
    const position = new THREE.Vector3(center.x, box.min.y, center.z);
    const rotation = new THREE.Quaternion().setFromAxisAngle(
      new THREE.Vector3(0, 1, 0),
      (alongX ? 0 : Math.PI / 2) + yawVariation
    );
    const scale = new THREE.Vector3(
      longSide * lengthVariation / Math.max(0.001, sourceSize.x),
      size.y * 1.04 * heightVariation / Math.max(0.001, sourceSize.y),
      shortSide * 0.98 / Math.max(0.001, sourceSize.z)
    );
    placements.push(new THREE.Matrix4().compose(position, rotation, scale));
  }

  for (const [meshIndex, record] of records.entries()) {
    const batch = new THREE.InstancedMesh(
      record.source.geometry,
      record.source.material,
      placements.length
    );
    batch.name = `V18_PILOT_REAL_HEDGE_GPU_BATCH_${String(meshIndex + 1).padStart(2, '0')}`;
    const sourceLabel = `${record.source.name} ${Array.isArray(record.source.material)
      ? record.source.material.map(material => material?.name || '').join(' ')
      : record.source.material?.name || ''}`;
    batch.castShadow = !/leaf|leaves/i.test(sourceLabel);
    batch.receiveShadow = true;
    batch.frustumCulled = true;
    batch.instanceMatrix.setUsage(THREE.StaticDrawUsage);
    for (let index = 0; index < placements.length; index += 1) {
      batch.setMatrixAt(index, placements[index].clone().multiply(record.matrix));
    }
    batch.instanceMatrix.needsUpdate = true;
    batch.computeBoundingSphere?.();
    batch.userData.liveVegetationFamily = 'hedge';
    batch.userData.logicalSegments = hedges.map(hedge => hedge.name);
    batch.userData.gpuInstanced = true;
    batch.userData.shadowPolicy = batch.castShadow ? 'cast-and-receive' : 'receive-only-leaf-lod';
    parent.add(batch);
  }
  if (records.length && hedges.length) hideOriginals(hedges, 'V18_PILOT_REAL_HEDGE_GPU');
  return {
    instances: hedges.length,
    cloneInstances: hedges.length,
    gpuBatchCount: records.length,
    gpuInstancing: records.length > 0,
    originalsHidden: records.length ? hedges.length : 0
  };
}

function publicError(error) {
  const message = error?.message || String(error);
  return message.replace(/https?:\/\/[^\s)]+/g, '<asset-url>');
}

/**
 * Replace V17 low-poly vegetation only after a real enhanced asset is loaded.
 * Modern phones use the same optimized assets; data-saving or low-memory
 * devices keep the originals and download no optional GLB. Failures are
 * isolated per family, so the house never loses all vegetation.
 */
export async function installLiveVegetation({
  scene,
  house,
  renderer,
  mobile = false,
  cacheKey = '',
  treeUrl = DEFAULT_TREE_URL,
  hedgeUrl = DEFAULT_HEDGE_URL,
  hedgeFallbackUrl = DEFAULT_HEDGE_FALLBACK_URL,
  timeoutMs = 15_000
} = {}) {
  if (!scene || !house) throw new TypeError('installLiveVegetation requires scene and house');
  const existing = scene.getObjectByName(ENHANCED_GROUP_NAME);
  if (existing?.userData.audit) return existing.userData.audit;

  const startedAt = now();
  const coarsePointer = globalThis.matchMedia?.('(pointer:coarse)')?.matches || false;
  const deviceMemory = Number(globalThis.navigator?.deviceMemory || 0);
  const saveData = Boolean(globalThis.navigator?.connection?.saveData);
  const constrainedDevice = Boolean(saveData || (deviceMemory > 0 && deviceMemory < 4));
  const originals = findOriginalVegetation(house);
  const audit = {
    status: constrainedDevice ? 'mobile-fallback' : 'loading',
    mode: constrainedDevice ? 'original-low-poly-constrained' : (mobile || coarsePointer ? 'enhanced-mobile' : 'enhanced-desktop'),
    mobile: Boolean(mobile || coarsePointer),
    deviceMemoryGb: deviceMemory || null,
    saveData,
    originalTreeFamilies: originals.treeFamilies.size,
    originalHedges: originals.hedges.length,
    treeInstances: 0,
    hedgeInstances: 0,
    hedgeCloneInstances: 0,
    hedgeGpuBatches: 0,
    hedgeGpuInstancing: false,
    originalsHidden: 0,
    displayedTriangles: 0,
    drawCalls: 0,
    loadMs: 0,
    assets: {
      tree: {
        requested: false,
        loaded: false,
        error: null,
        decision: 'ACCEPT_RETAIN_CURRENT_POLY_HAVEN',
        rejectedPilot: 'BlenderKit Decorative Urban Tree',
        rejectionReason: 'winter leafless silhouette; 123949 triangles; 7032388 bytes'
      },
      hedge: {
        requested: false,
        loaded: false,
        error: null,
        decision: 'ACCEPT_BLENDERKIT_SHRUB_CC0',
        fallbackAsset: 'Poly Haven shrub_03_web.glb'
      }
    },
    fallbackUsed: constrainedDevice,
    performanceBudget: {
      baselineDisplayedTriangles: 1_082_996,
      baselineDrawCalls: 120,
      baselineHedgeClones: 108,
      targetFpsMinimum: 30
    }
  };
  globalThis.__liveVegetationAudit = audit;
  if (globalThis.document?.documentElement) {
    document.documentElement.dataset.viewerVegetation = audit.status;
  }
  if (constrainedDevice) {
    audit.loadMs = Math.round(now() - startedAt);
    return audit;
  }

  const enhanced = new THREE.Group();
  enhanced.name = ENHANCED_GROUP_NAME;
  enhanced.userData.audit = audit;
  scene.add(enhanced);
  const urls = {
    tree: cacheBustedUrl(treeUrl, cacheKey),
    hedge: cacheBustedUrl(hedgeUrl, cacheKey),
    hedgeFallback: cacheBustedUrl(hedgeFallbackUrl, cacheKey)
  };
  audit.assets.tree = { ...audit.assets.tree, requested: true, loaded: false, url: urls.tree, error: null };
  audit.assets.hedge = {
    ...audit.assets.hedge,
    requested: true,
    loaded: false,
    url: urls.hedge,
    fallbackUrl: urls.hedgeFallback,
    fallbackRequested: false,
    fallbackLoaded: false,
    error: null
  };

  const [treeResult, hedgeResult] = await Promise.allSettled([
    loadGlb(urls.tree, timeoutMs),
    loadGlb(urls.hedge, timeoutMs)
  ]);

  if (treeResult.status === 'fulfilled') {
    tuneTemplate(treeResult.value, renderer, 'tree');
    const metrics = templateMetrics(treeResult.value);
    const { wrapper, size } = normalizedTemplate(treeResult.value);
    const installed = installTrees(enhanced, house, wrapper, size, originals.treeFamilies);
    audit.treeInstances = installed.instances;
    audit.originalsHidden += installed.originalsHidden;
    audit.displayedTriangles += metrics.triangles * installed.instances;
    audit.drawCalls += metrics.drawCalls * installed.instances;
    audit.assets.tree = {
      ...audit.assets.tree,
      loaded: true,
      dimensionsM: size.toArray().map(value => Number(value.toFixed(5))),
      ...metrics
    };
  } else {
    audit.assets.tree.error = publicError(treeResult.reason);
    audit.fallbackUsed = true;
  }

  let acceptedHedge = hedgeResult.status === 'fulfilled' ? hedgeResult.value : null;
  let hedgeSource = 'pilot-primary';
  if (!acceptedHedge) {
    audit.assets.hedge.error = publicError(hedgeResult.reason);
    audit.assets.hedge.fallbackRequested = true;
    try {
      acceptedHedge = await loadGlb(urls.hedgeFallback, timeoutMs);
      hedgeSource = 'retained-fallback';
      audit.assets.hedge.fallbackLoaded = true;
      audit.fallbackUsed = true;
    } catch (error) {
      audit.assets.hedge.fallbackError = publicError(error);
    }
  }

  if (acceptedHedge) {
    tuneTemplate(acceptedHedge, renderer, 'hedge');
    const metrics = templateMetrics(acceptedHedge);
    const { wrapper, size } = normalizedTemplate(acceptedHedge);
    const installed = hedgeSource === 'pilot-primary'
      ? installInstancedHedges(enhanced, wrapper, size, originals.hedges)
      : installLegacyHedges(enhanced, wrapper, size, originals.hedges);
    audit.hedgeInstances = installed.instances;
    audit.hedgeCloneInstances = installed.cloneInstances;
    audit.hedgeGpuBatches = installed.gpuBatchCount || 0;
    audit.hedgeGpuInstancing = Boolean(installed.gpuInstancing);
    audit.originalsHidden += installed.originalsHidden;
    audit.displayedTriangles += metrics.triangles * installed.cloneInstances;
    audit.drawCalls += hedgeSource === 'pilot-primary'
      ? metrics.drawCalls
      : metrics.drawCalls * installed.cloneInstances;
    audit.assets.hedge = {
      ...audit.assets.hedge,
      loaded: true,
      source: hedgeSource,
      dimensionsM: size.toArray().map(value => Number(value.toFixed(5))),
      ...metrics
    };
  } else {
    audit.fallbackUsed = true;
  }

  const loadedFamilies = Number(audit.assets.tree.loaded) + Number(audit.assets.hedge.loaded);
  audit.status = loadedFamilies === 2 ? 'enhanced' : loadedFamilies === 1 ? 'partial-fallback' : 'original-fallback';
  audit.loadMs = Math.round(now() - startedAt);
  if (globalThis.document?.documentElement) {
    document.documentElement.dataset.viewerVegetation = audit.status;
    document.documentElement.dataset.viewerVegetationTriangles = String(audit.displayedTriangles);
    document.documentElement.dataset.viewerVegetationDrawCalls = String(audit.drawCalls);
    document.documentElement.dataset.viewerVegetationHedgeClones = String(audit.hedgeCloneInstances);
    document.documentElement.dataset.viewerVegetationHedgeGpuBatches = String(audit.hedgeGpuBatches);
    document.documentElement.dataset.viewerVegetationGpuInstancing = String(audit.hedgeGpuInstancing);
    document.documentElement.dataset.viewerVegetationLoadMs = String(audit.loadMs);
  }
  return audit;
}
