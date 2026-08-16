const PIPELINE_ID = 'V18-WEB-REALISM-LIGHTING-R2';

const clamp = (value, minimum, maximum) => Math.max(minimum, Math.min(maximum, value));
const rounded = value => Math.round(value * 1000) / 1000;

function makeSkyTexture(THREE, mobile) {
  const canvas = document.createElement('canvas');
  canvas.width = mobile ? 512 : 1024;
  canvas.height = canvas.width / 2;
  const context = canvas.getContext('2d');

  // A deterministic, warm late-morning sky gives the PBR materials readable
  // reflections without downloading an HDRI or adding another network failure.
  const sky = context.createLinearGradient(0, 0, 0, canvas.height);
  sky.addColorStop(0, '#557b9b');
  sky.addColorStop(0.34, '#8fb1c2');
  sky.addColorStop(0.55, '#d5d9ce');
  sky.addColorStop(0.64, '#e5cda4');
  sky.addColorStop(1, '#4b513d');
  context.fillStyle = sky;
  context.fillRect(0, 0, canvas.width, canvas.height);

  const sunX = canvas.width * .72;
  const sunY = canvas.height * .22;
  const sunRadius = canvas.height * .3;
  const glow = context.createRadialGradient(sunX, sunY, 1, sunX, sunY, sunRadius);
  glow.addColorStop(0, 'rgba(255,250,224,1)');
  glow.addColorStop(.08, 'rgba(255,228,170,.96)');
  glow.addColorStop(.38, 'rgba(247,190,113,.24)');
  glow.addColorStop(1, 'rgba(247,190,113,0)');
  context.fillStyle = glow;
  context.fillRect(sunX - sunRadius, 0, sunRadius * 2, sunY + sunRadius);

  // Broad cloud bands break the old flat green-grey background. Their fixed
  // positions keep screenshots and runtime audits reproducible.
  const clouds = [
    [.12, .24, .20, .035, .12], [.35, .18, .16, .028, .08],
    [.57, .31, .22, .04, .1], [.84, .17, .14, .026, .08]
  ];
  clouds.forEach(([x, y, width, height, alpha]) => {
    const cloud = context.createRadialGradient(
      canvas.width * x, canvas.height * y, 0,
      canvas.width * x, canvas.height * y, canvas.width * width
    );
    cloud.addColorStop(0, `rgba(255,250,238,${alpha})`);
    cloud.addColorStop(.38, `rgba(247,244,234,${alpha * .72})`);
    cloud.addColorStop(1, 'rgba(245,242,232,0)');
    context.save();
    context.scale(1, height / width * 4.4);
    context.fillStyle = cloud;
    context.fillRect(0, 0, canvas.width, canvas.height * width / height / 4.4);
    context.restore();
  });

  const texture = new THREE.CanvasTexture(canvas);
  texture.name = `${PIPELINE_ID}-PROCEDURAL-SKY`;
  texture.mapping = THREE.EquirectangularReflectionMapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}

function materialProfile(name = '') {
  const upper = name.toUpperCase();
  // The upgraded GLB carries authored albedo for these six materials. Keep
  // their colour identity instead of letting the legacy generic expressions
  // collapse sofa, armchair, chairs and trees to one brown/green tint.
  if (/V18_WEB_SOFA_WARM_WEAVE/.test(upper)) return { family: 'sofa-warm-weave', env: .36, roughness: .82, normal: .88, preserveAlbedo: true };
  if (/V18_WEB_ARMCHAIR_OLIVE_WEAVE/.test(upper)) return { family: 'armchair-olive-weave', env: .30, roughness: .83, normal: .90, preserveAlbedo: true };
  if (/V18_WEB_DINING_CHAIR_CARAMEL_WEAVE/.test(upper)) return { family: 'chair-caramel-weave', env: .34, roughness: .80, normal: .88, preserveAlbedo: true };
  if (/V18_WEB_TREE_BARK/.test(upper)) return { family: 'tree-bark', env: .22, roughness: .94, normal: 1.04, preserveAlbedo: true };
  if (/V18_WEB_TREE_LEAVES_DEEP/.test(upper)) return { family: 'tree-leaves-deep', env: .20, roughness: .89, normal: .92, preserveAlbedo: true };
  if (/V18_WEB_TREE_LEAVES_FRESH/.test(upper)) return { family: 'tree-leaves-fresh', env: .22, roughness: .87, normal: .92, preserveAlbedo: true };
  if (/V12_PBR_BEIGE_COTTON/.test(upper)) return { family: 'bedding-cream', env: .30, roughness: .90, normal: .76, tint: [.88, .82, .72] };
  if (/PHYSICAL_GLASS|MAT_B_GLASS|\bGLASS\b|WINDOW/.test(upper)) return { family: 'glass', env: 1.75, roughness: .12 };
  if (/MIRROR/.test(upper)) return { family: 'mirror', env: 2.05, roughness: .06, metalness: .82 };
  if (/ALU|CHROME|ANTHRACITE|APPLIANCE_BLACK|METAL/.test(upper)) return { family: 'metal', env: 1.45 };
  if (/ROOF/.test(upper)) return { family: 'roof', env: .62, roughness: .78, normal: 1.18, tint: [.93, .76, .58] };
  if (/FOLIAGE_DEEP/.test(upper)) return { family: 'foliage-deep', env: .22, roughness: .86, tint: [.40, .62, .26] };
  if (/FOLIAGE_FRESH/.test(upper)) return { family: 'foliage-fresh', env: .24, roughness: .84, tint: [.55, .75, .31] };
  if (/POTTED_PLANT/.test(upper)) return { family: 'foliage-detail', env: .26, roughness: .82, normal: .88, tint: [.68, .82, .46] };
  if (/GRASS/.test(upper)) return { family: 'grass', env: .25, roughness: .94, normal: 1.05, tint: [.72, .88, .44] };
  if (/GRAVEL/.test(upper)) return { family: 'gravel', env: .34, roughness: .90, normal: 1.12, tint: [.70, .62, .50] };
  if (/ASPHALT/.test(upper)) return { family: 'asphalt', env: .26, roughness: .92, normal: 1.02, tint: [.34, .37, .40] };
  if (/FLOOR|PORCELAIN|TILE/.test(upper)) return { family: 'interior-floor', env: .68, roughness: .62, normal: .74, tint: [.82, .76, .65] };
  if (/STUCCO|OFFWHITE/.test(upper)) return { family: 'facade', env: .34, roughness: .88, normal: .55, tint: [.90, .86, .76] };
  if (/CONCRETE/.test(upper)) return { family: 'concrete', env: .40, roughness: .82, normal: .78, tint: [.72, .70, .65] };
  if (/COTTON|SOFA|ARMCHAIR|CHAIR/.test(upper)) return { family: 'legacy-upholstery', env: .34, roughness: .87, normal: .90, tint: [.65, .54, .42] };
  if (/WHITE_OAK|ENTRY_WOOD|PBR_B_WOOD|COFFEE_TABLE|TABLE_WOOD/.test(upper)) return { family: 'wood', env: .48, roughness: .66, normal: .80, tint: [.70, .51, .31] };
  if (/LACQUER|KITCHEN_GREIGE/.test(upper)) return { family: 'cabinetry', env: .74, roughness: .34, tint: [.58, .50, .40] };
  if (/COUNTER_STONE|SILL_STONE/.test(upper)) return { family: 'stone', env: .72, roughness: .40, tint: [.62, .56, .47] };
  return { family: 'standard', env: .62 };
}

function tuneMaterial(material, profile) {
  const changes = [];
  if (profile.preserveAlbedo) changes.push('albedo=preserved-from-GLB');
  if (profile.tint && material.color) {
    material.color.setRGB(...profile.tint);
    changes.push(`tint=${profile.tint.join('/')}`);
  }
  if (profile.roughness !== undefined && 'roughness' in material) {
    material.roughness = profile.roughness;
    changes.push(`roughness=${profile.roughness}`);
  }
  if (profile.metalness !== undefined && 'metalness' in material) {
    material.metalness = profile.metalness;
    changes.push(`metalness=${profile.metalness}`);
  }
  if (profile.normal !== undefined && material.normalScale?.set) {
    const ySign = Math.sign(material.normalScale.y) || 1;
    material.normalScale.set(profile.normal, profile.normal * ySign);
    changes.push(`normalScale=${profile.normal}`);
  }
  if ('envMapIntensity' in material) {
    material.envMapIntensity = profile.env;
    changes.push(`envMapIntensity=${profile.env}`);
  }

  if (profile.family === 'glass') {
    const thinBlendGlass = /MAT_B_GLASS/i.test(material.name);
    material.color?.setRGB(.16, .27, .33);
    material.roughness = thinBlendGlass ? .16 : .11;
    material.metalness = 0;
    if ('transmission' in material) material.transmission = thinBlendGlass ? .68 : .88;
    if ('ior' in material) material.ior = 1.48;
    if ('thickness' in material) material.thickness = thinBlendGlass ? .025 : .06;
    if ('attenuationDistance' in material) material.attenuationDistance = 4.5;
    if (thinBlendGlass) {
      material.transparent = true;
      material.opacity = .42;
      material.depthWrite = false;
    }
    changes.push(`glass=${thinBlendGlass ? 'thin-visible' : 'physical-transmission'}`);
  }

  material.dithering = true;
  material.needsUpdate = true;
  return changes;
}

export function setupLiveLighting(THREE, scene, renderer, config, mobile) {
  const configured = config.lighting || {};
  const exposure = rounded(clamp(Number(configured.exposure ?? .865), .82, .90));
  const environmentIntensity = rounded(clamp(Number(configured.environmentIntensity ?? .765), .68, .82));
  const hemisphereIntensity = rounded(clamp(Number(configured.hemisphereIntensity ?? .518), .42, .56));
  const ambientIntensity = rounded(clamp(Number(configured.ambientIntensity ?? .03), .02, .04));
  const sunIntensity = rounded(clamp(Number(configured.directionalIntensity ?? 2.76), 2.45, 2.85));
  const fillIntensity = rounded(clamp(Number(configured.fillIntensity ?? .158), .12, .18));
  const rimIntensity = mobile ? .20 : rounded(clamp(Number(configured.rimIntensity ?? .28), .20, .34));

  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = exposure;
  renderer.shadowMap.enabled = !mobile;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.shadowMap.autoUpdate = true;

  const skyTexture = makeSkyTexture(THREE, mobile);
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();
  const environmentTarget = pmrem.fromEquirectangular(skyTexture);
  environmentTarget.texture.name = `${PIPELINE_ID}-PMREM`;
  scene.environment = environmentTarget.texture;
  scene.environmentIntensity = environmentIntensity;
  scene.background = skyTexture;
  scene.backgroundIntensity = .82;
  scene.fog = new THREE.Fog(
    0xaebcb7,
    mobile ? 66 : Number(configured.fogNear ?? 78),
    mobile ? 142 : Number(configured.fogFar ?? 172)
  );
  if (scene.environmentRotation) scene.environmentRotation.y = -.36;
  if (scene.backgroundRotation) scene.backgroundRotation.y = -.36;
  pmrem.dispose();

  const hemi = new THREE.HemisphereLight(0xdcecff, 0x302c22, hemisphereIntensity);
  const ambient = new THREE.AmbientLight(0xffe8cf, ambientIntensity);
  const sun = new THREE.DirectionalLight(0xffd5a6, sunIntensity);
  sun.position.set(-22, 31, -16);
  sun.castShadow = !mobile;
  sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  sun.shadow.camera.near = .5;
  sun.shadow.camera.far = 105;
  sun.shadow.camera.left = -32;
  sun.shadow.camera.right = 32;
  sun.shadow.camera.top = 32;
  sun.shadow.camera.bottom = -32;
  sun.shadow.bias = -.00010;
  sun.shadow.normalBias = .014;
  sun.shadow.radius = 2;

  const fill = new THREE.DirectionalLight(0x92b9d8, fillIntensity);
  fill.position.set(20, 13, 20);
  const rim = new THREE.DirectionalLight(0xffead0, rimIntensity);
  rim.position.set(12, 18, -24);
  scene.add(hemi, ambient, sun, fill, rim);

  const audit = {
    pipeline: PIPELINE_ID,
    colorSpace: 'SRGBColorSpace',
    toneMapping: 'ACESFilmicToneMapping',
    configuredExposure: configured.exposure,
    appliedExposure: exposure,
    environment: 'deterministic procedural sky + PMREM IBL',
    configuredEnvironmentIntensity: configured.environmentIntensity,
    appliedEnvironmentIntensity: environmentIntensity,
    background: 'equirectangular procedural sky',
    fog: { color: '#aebcb7', near: scene.fog.near, far: scene.fog.far },
    lights: {
      hemisphere: hemisphereIntensity,
      ambient: ambientIntensity,
      sun: sunIntensity,
      fill: fillIntensity,
      rim: rimIntensity
    },
    shadows: mobile ? 'disabled-mobile' : 'PCFSoft-2048',
    mobile
  };
  window.__liveLightingAudit = audit;
  document.documentElement.dataset.liveLighting = PIPELINE_ID;
  return { environmentTarget, skyTexture, hemi, ambient, sun, fill, rim, audit };
}

export function tuneLiveModel(renderer, root, mobile, config) {
  const maxAnisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
  const textureSlots = ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap', 'emissiveMap', 'alphaMap'];
  const materials = new Set();
  const textures = new Set();
  const familyCounts = {};
  const materialDetails = [];
  let meshes = 0;
  let texturedMaterialBindings = 0;

  root.traverse(object => {
    if (!object.isMesh) return;
    meshes += 1;
    object.castShadow = !mobile;
    object.receiveShadow = !mobile;
    const list = Array.isArray(object.material) ? object.material : [object.material];
    let glassOnly = list.length > 0;

    list.filter(Boolean).forEach(material => {
      const firstUse = !materials.has(material);
      materials.add(material);
      let textured = false;
      textureSlots.forEach(slot => {
        const texture = material[slot];
        if (!texture) return;
        textured = true;
        textures.add(texture);
        texture.anisotropy = maxAnisotropy;
        texture.needsUpdate = true;
      });
      if (textured) texturedMaterialBindings += 1;

      const profile = materialProfile(material.name);
      glassOnly &&= profile.family === 'glass';
      if (!firstUse) return;
      const changes = tuneMaterial(material, profile);
      familyCounts[profile.family] = (familyCounts[profile.family] || 0) + 1;
      materialDetails.push({
        name: material.name || '(unnamed)',
        family: profile.family,
        textured,
        envMapIntensity: 'envMapIntensity' in material ? material.envMapIntensity : null,
        roughness: 'roughness' in material ? rounded(material.roughness) : null,
        metalness: 'metalness' in material ? rounded(material.metalness) : null,
        changes
      });
    });

    // Transparent panes should receive reflections but must not cast opaque
    // rectangles across the facade and the interior floor.
    if (glassOnly) {
      object.castShadow = false;
      object.receiveShadow = false;
    }
  });

  materialDetails.sort((a, b) => a.name.localeCompare(b.name));
  return {
    pipeline: PIPELINE_ID,
    meshes,
    uniqueMaterials: materials.size,
    uniqueTextures: textures.size,
    texturedMaterialBindings,
    tunedMaterials: materialDetails.length,
    familyCounts: Object.fromEntries(Object.entries(familyCounts).sort(([a], [b]) => a.localeCompare(b))),
    materials: materialDetails,
    anisotropy: maxAnisotropy,
    environment: 'deterministic procedural sky + PMREM IBL',
    environmentIntensity: window.__liveLightingAudit?.appliedEnvironmentIntensity ?? config.lighting.environmentIntensity,
    exposure: window.__liveLightingAudit?.appliedExposure ?? config.lighting.exposure,
    shadows: mobile ? 'disabled-mobile' : 'PCFSoft-2048'
  };
}
