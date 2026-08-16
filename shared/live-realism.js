function makeSkyTexture(THREE) {
  const canvas = document.createElement('canvas');
  canvas.width = 512; canvas.height = 256;
  const context = canvas.getContext('2d');
  const sky = context.createLinearGradient(0, 0, 0, canvas.height);
  sky.addColorStop(0, '#83a8c5');
  sky.addColorStop(0.43, '#c7d8dc');
  sky.addColorStop(0.58, '#eee2c9');
  sky.addColorStop(1, '#6d7358');
  context.fillStyle = sky; context.fillRect(0, 0, canvas.width, canvas.height);
  const glow = context.createRadialGradient(390, 72, 2, 390, 72, 72);
  glow.addColorStop(0, 'rgba(255,246,214,1)');
  glow.addColorStop(0.12, 'rgba(255,226,164,.88)');
  glow.addColorStop(1, 'rgba(255,226,164,0)');
  context.fillStyle = glow; context.fillRect(300, 0, 212, 150);
  const texture = new THREE.CanvasTexture(canvas);
  texture.mapping = THREE.EquirectangularReflectionMapping;
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
}

export function setupLiveLighting(THREE, scene, renderer, config, mobile) {
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = config.lighting.exposure;
  renderer.shadowMap.enabled = !mobile;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;

  const skyTexture = makeSkyTexture(THREE);
  const pmrem = new THREE.PMREMGenerator(renderer);
  pmrem.compileEquirectangularShader();
  const environmentTarget = pmrem.fromEquirectangular(skyTexture);
  scene.environment = environmentTarget.texture;
  scene.environmentIntensity = config.lighting.environmentIntensity;
  skyTexture.dispose();
  pmrem.dispose();

  const hemi = new THREE.HemisphereLight(0xeaf4ff, 0x4e4737, config.lighting.hemisphereIntensity);
  const ambient = new THREE.AmbientLight(0xfff2df, config.lighting.ambientIntensity);
  const sun = new THREE.DirectionalLight(0xffdfae, config.lighting.directionalIntensity);
  sun.position.set(-18, 28, -10);
  sun.castShadow = !mobile;
  sun.shadow.mapSize.set(mobile ? 1024 : 2048, mobile ? 1024 : 2048);
  sun.shadow.camera.near = .5; sun.shadow.camera.far = 95;
  sun.shadow.camera.left = -30; sun.shadow.camera.right = 30;
  sun.shadow.camera.top = 30; sun.shadow.camera.bottom = -30;
  sun.shadow.bias = -.00012; sun.shadow.normalBias = .018;
  const fill = new THREE.DirectionalLight(0xa9c8e8, config.lighting.fillIntensity);
  fill.position.set(18, 12, 18);
  scene.add(hemi, ambient, sun, fill);
  return { environmentTarget, hemi, ambient, sun, fill };
}

export function tuneLiveModel(renderer, root, mobile, config) {
  const maxAnisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy());
  const textureSlots = ['map','normalMap','roughnessMap','metalnessMap','aoMap','emissiveMap','alphaMap'];
  const materials = new Set();
  const textures = new Set();
  let meshes = 0, texturedMaterials = 0;
  root.traverse(object => {
    if (!object.isMesh) return;
    meshes += 1;
    object.castShadow = !mobile;
    object.receiveShadow = !mobile;
    const list = Array.isArray(object.material) ? object.material : [object.material];
    list.filter(Boolean).forEach(material => {
      materials.add(material);
      let textured = false;
      textureSlots.forEach(slot => {
        const texture = material[slot];
        if (!texture) return;
        textured = true; textures.add(texture);
        texture.anisotropy = maxAnisotropy;
        texture.needsUpdate = true;
      });
      if (textured) texturedMaterials += 1;
      if ('envMapIntensity' in material) {
        const reflective = /GLASS|WINDOW|METAL|ALU|CHROME|ANTHRACITE|MIRROR|APPLIANCE_BLACK/i.test(material.name);
        material.envMapIntensity = reflective ? 1.15 : .8;
      }
      material.needsUpdate = true;
    });
  });
  return {
    meshes,
    uniqueMaterials: materials.size,
    uniqueTextures: textures.size,
    texturedMaterialBindings: texturedMaterials,
    anisotropy: maxAnisotropy,
    environment: 'procedural PMREM IBL',
    environmentIntensity: config.lighting.environmentIntensity,
    shadows: mobile ? 'disabled-mobile' : 'PCFSoft-2048'
  };
}
