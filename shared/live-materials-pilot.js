const PILOT_ID = 'V18-ASSET-PILOT-MATERIALS-1';

const FILES = {
  facade: {
    color: '../assets_external/materials/facade/white_stucco/optimized/white_stucco_color_1k.webp',
    normal: '../assets_external/materials/facade/white_stucco/optimized/white_stucco_normal_gl_1k.webp',
    arm: '../assets_external/materials/facade/white_stucco/optimized/white_stucco_arm_1k.webp'
  },
  grass: {
    color: '../assets_external/materials/exterior/grass005/optimized/Grass005_color_1k.webp',
    normal: '../assets_external/materials/exterior/grass005/optimized/Grass005_normal_gl_1k.webp',
    arm: '../assets_external/materials/exterior/grass005/optimized/Grass005_arm_1k.webp'
  }
};

const PROFILES = {
  V12_PBR_OFFWHITE_STUCCO: {
    category: 'facade', repeat: [3, 3], offset: [0, -2], normalScale: .42,
    aoIntensity: .48, roughness: .92, metalness: 0, color: [.985, .98, .965], envMapIntensity: .38
  },
  V10_STUCCO_NEW_BUILD: {
    category: 'facade', repeat: [6, 6], offset: [0, -5], normalScale: .32,
    aoIntensity: .44, roughness: .93, metalness: 0, color: [.985, .98, .965], envMapIntensity: .36
  },
  PBR_B_GRASS: {
    category: 'grass', repeat: [8, 8], offset: [0, 0], normalScale: .72,
    aoIntensity: .68, roughness: .98, metalness: 0, color: [.96, 1, .96], envMapIntensity: .25
  }
};

const PAYLOAD_BYTES = {
  facade: 489958,
  grass: 1558326,
  total: 2048284
};

function urlWithRelease(relative, cacheKey) {
  const url = new URL(relative, import.meta.url);
  if (cacheKey) url.searchParams.set('release', cacheKey);
  return url.href;
}

async function loadBundle(THREE, loader, category, cacheKey, audit) {
  const entries = Object.entries(FILES[category]);
  try {
    const textures = await Promise.all(entries.map(async ([role, relative]) => {
      const url = urlWithRelease(relative, cacheKey);
      const texture = await loader.loadAsync(url);
      texture.name = `${PILOT_ID}-${category}-${role}-source`;
      audit.network.push({
        category,
        role,
        url: new URL(url).pathname,
        status: 'loaded',
        dimensions: [texture.image?.naturalWidth || texture.image?.width || null, texture.image?.naturalHeight || texture.image?.height || null]
      });
      return [role, texture];
    }));
    audit.categories[category].loadStatus = 'loaded';
    return Object.fromEntries(textures);
  } catch (error) {
    audit.categories[category].loadStatus = 'fallback-preserved';
    audit.errors.push({ category, message: error?.message || String(error) });
    return null;
  }
}

function cloneTexture(THREE, source, profile, role, renderer, materialName) {
  const texture = source.clone();
  texture.name = `${PILOT_ID}-${materialName}-${role}`;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(...profile.repeat);
  texture.offset.set(...profile.offset);
  texture.rotation = 0;
  texture.flipY = false;
  texture.colorSpace = role === 'color' ? THREE.SRGBColorSpace : THREE.NoColorSpace;
  texture.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
  texture.generateMipmaps = true;
  texture.needsUpdate = true;
  texture.userData = {
    ...texture.userData,
    assetPilot: PILOT_ID,
    role,
    source: source.name
  };
  return texture;
}

function applyBundle(THREE, renderer, material, profile, bundle) {
  const color = cloneTexture(THREE, bundle.color, profile, 'color', renderer, material.name);
  const normal = cloneTexture(THREE, bundle.normal, profile, 'normal', renderer, material.name);
  const arm = cloneTexture(THREE, bundle.arm, profile, 'arm', renderer, material.name);

  // Three samples the packed ARM texture as AO=R, roughness=G, metalness=B.
  // Reusing one texture also avoids a fourth network request and GPU upload.
  material.map = color;
  material.normalMap = normal;
  material.aoMap = arm;
  material.roughnessMap = arm;
  material.metalnessMap = arm;
  material.normalScale?.set(profile.normalScale, profile.normalScale);
  material.aoMapIntensity = profile.aoIntensity;
  material.roughness = profile.roughness;
  material.metalness = profile.metalness;
  if ('envMapIntensity' in material) material.envMapIntensity = profile.envMapIntensity;
  material.color?.setRGB(...profile.color);
  material.dithering = true;
  material.needsUpdate = true;
  material.userData = {
    ...material.userData,
    assetPilot: PILOT_ID,
    assetCategory: profile.category,
    sourceLicense: 'CC0 1.0',
    pbrWiring: 'baseColor + OpenGL normal + packed ARM',
    tiling: profile.repeat.slice()
  };
  return { color, normal, arm };
}

/**
 * Apply the locally cached CC0 material pilot after the house GLB is loaded.
 * A category is mutated only after all three required maps load successfully;
 * otherwise the corresponding embedded GLB material remains untouched.
 */
export async function installLiveMaterialPilot({ THREE, house, renderer, mobile = false, cacheKey = '' }) {
  const audit = {
    pilot: PILOT_ID,
    status: 'loading',
    sources: {
      facade: { provider: 'Poly Haven', asset: 'White Stucco', assetId: 'white_stucco', license: 'CC0 1.0' },
      grass: { provider: 'ambientCG', asset: 'Grass 005', assetId: 'Grass005', license: 'CC0 1.0 Universal' }
    },
    payloadBytes: PAYLOAD_BYTES,
    categories: {
      facade: { loadStatus: 'pending', matchedMaterials: 0, appliedMaterials: 0 },
      grass: { loadStatus: 'pending', matchedMaterials: 0, appliedMaterials: 0 }
    },
    materialDetails: [],
    network: [],
    errors: [],
    fallbackRule: 'embedded GLB binding preserved category-by-category if any required optimized map fails',
    mobile: Boolean(mobile)
  };
  window.__assetPilotMaterialAudit = audit;
  document.documentElement.dataset.viewerMaterialPilot = 'loading';

  const loader = new THREE.TextureLoader();
  const [facade, grass] = await Promise.all([
    loadBundle(THREE, loader, 'facade', cacheKey, audit),
    loadBundle(THREE, loader, 'grass', cacheKey, audit)
  ]);
  const bundles = { facade, grass };
  const seen = new Set();

  house.traverse(object => {
    if (!object.isMesh) return;
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    materials.filter(Boolean).forEach(material => {
      if (seen.has(material)) return;
      seen.add(material);
      const profile = PROFILES[material.name];
      if (!profile) return;
      const category = audit.categories[profile.category];
      category.matchedMaterials += 1;
      const bundle = bundles[profile.category];
      if (!bundle) {
        audit.materialDetails.push({ material: material.name, category: profile.category, action: 'fallback-preserved' });
        return;
      }
      const textures = applyBundle(THREE, renderer, material, profile, bundle);
      category.appliedMaterials += 1;
      audit.materialDetails.push({
        material: material.name,
        category: profile.category,
        action: 'pilot-applied',
        repeat: profile.repeat.slice(),
        offset: profile.offset.slice(),
        normalScale: profile.normalScale,
        aoIntensity: profile.aoIntensity,
        maps: Object.values(textures).map(texture => texture.name)
      });
    });
  });

  const applied = Object.values(audit.categories).reduce((sum, category) => sum + category.appliedMaterials, 0);
  const matched = Object.values(audit.categories).reduce((sum, category) => sum + category.matchedMaterials, 0);
  const loadedCategories = Object.values(audit.categories).filter(category => category.loadStatus === 'loaded').length;
  audit.status = applied > 0 && loadedCategories === 2 ? 'applied' : applied > 0 ? 'partial' : 'fallback';
  audit.appliedMaterials = applied;
  audit.matchedMaterials = matched;
  audit.completedAt = new Date().toISOString();
  window.__assetPilotMaterialAudit = audit;
  document.documentElement.dataset.viewerMaterialPilot = audit.status;
  return audit;
}

export const LIVE_MATERIAL_PILOT_ID = PILOT_ID;
