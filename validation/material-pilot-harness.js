import * as THREE from '../shared/vendor/three.module.js';
import { OrbitControls } from '../shared/vendor/addons/controls/OrbitControls.js';
import { GLTFLoader } from '../shared/vendor/addons/loaders/GLTFLoader.js';
import { installLiveMaterialPilot } from '../shared/live-materials-pilot.js?test=1';

const output = document.querySelector('#audit');
const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.35));
renderer.setSize(innerWidth, innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = .9;
document.body.prepend(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xabbab1);
scene.add(new THREE.HemisphereLight(0xe8f2ff, 0x494134, 1.8));
const sun = new THREE.DirectionalLight(0xffdfbc, 3.2);
sun.position.set(-18, 26, -14);
scene.add(sun);

const camera = new THREE.PerspectiveCamera(52, innerWidth / innerHeight, .02, 220);
camera.position.set(9.5, 8.2, -10.5);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(-2.4, .15, -5.4);
controls.enableDamping = true;

window.__materialHarness = { ready: false, status: 'loading' };
try {
  const modelUrl = new URL('../shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb?material-pilot-harness=1', import.meta.url);
  const gltf = await new GLTFLoader().loadAsync(modelUrl.href);
  scene.add(gltf.scene);
  const audit = await installLiveMaterialPilot({ THREE, house: gltf.scene, renderer, cacheKey: 'material-pilot-harness-1' });
  const targetMaterials = [];
  const seen = new Set();
  gltf.scene.traverse(object => {
    if (!object.isMesh) return;
    const materials = Array.isArray(object.material) ? object.material : [object.material];
    materials.filter(Boolean).forEach(material => {
      if (seen.has(material) || !material.userData?.assetPilot) return;
      seen.add(material);
      targetMaterials.push({
        name: material.name,
        maps: ['map','normalMap','aoMap','roughnessMap','metalnessMap'].filter(slot => Boolean(material[slot])),
        repeat: material.map?.repeat.toArray(),
        colorSpace: material.map?.colorSpace,
        normalColorSpace: material.normalMap?.colorSpace
      });
    });
  });
  window.__materialHarness = { ready: true, status: audit.status, audit, targetMaterials };
  document.documentElement.dataset.materialHarnessReady = 'true';
  output.textContent = `${audit.pilot}\nstatus=${audit.status}\nmaterials=${audit.appliedMaterials}/${audit.matchedMaterials}\nfacade=${audit.categories.facade.appliedMaterials}\ngrass=${audit.categories.grass.appliedMaterials}\nerrors=${audit.errors.length}`;
} catch (error) {
  window.__materialHarness = { ready: false, status: 'failed', error: error?.message || String(error) };
  document.documentElement.dataset.materialHarnessReady = 'failed';
  output.textContent = `ÉCHEC\n${window.__materialHarness.error}`;
  console.error(error);
}

addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
renderer.setAnimationLoop(() => {
  controls.update();
  renderer.render(scene, camera);
});
