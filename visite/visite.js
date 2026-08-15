import * as THREE from '../shared/vendor/three.module.js';
import { PointerLockControls } from '../shared/vendor/addons/controls/PointerLockControls.js';
import { GLTFLoader } from '../shared/vendor/addons/loaders/GLTFLoader.js';
import { loadProjectConfig, applyProjectVersion, resolveProjectAsset } from '../shared/project-config.js';
import { setupLiveLighting, tuneLiveModel } from '../shared/live-realism.js';

const config = await loadProjectConfig();
applyProjectVersion(config);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xb8c5bb);
scene.fog = new THREE.Fog(0xb8c5bb, 58, 125);
const camera = new THREE.PerspectiveCamera(67, innerWidth / innerHeight, .018, 230);
const mobile = matchMedia('(pointer:coarse)').matches;
const renderer = new THREE.WebGLRenderer({ antialias: !mobile, powerPreference: 'high-performance' });
renderer.setPixelRatio(Math.min(devicePixelRatio, mobile ? 1.1 : 1.6));
renderer.setSize(innerWidth, innerHeight);
document.body.prepend(renderer.domElement);
setupLiveLighting(THREE, scene, renderer, config, mobile);
const controls = new PointerLockControls(camera, document.body);

const presets = {
  outside: { p: [-5.359, 1.65, -.537], t: [-4.684, 1.40, 1.378], label: 'Départ extérieur — avancez vers la porte pour entrer' },
  garden: { p: [-12.5, 1.65, -17.2], t: [-4.2, 1.45, -11.86], label: 'Jardin — 4 arbres, 18 haies et sols du GLB Web' },
  kitchen: { p: [-5.829, 1.65, 3.525], t: [-3.487, 1.20, 2.836], label: 'Cuisine au sud du séjour' },
  living: { p: [-7.037, 1.65, 5.862], t: [-5.749, 1.20, 8.616], label: 'Séjour du RDC' },
  stairs: { p: [-5.321, 1.65, 2.957], t: [-7.161, 1.30, 4.976], label: 'Escalier 16 marches' },
  upper: { p: [-7.321, 4.30, 5.450], t: [-5.832, 3.80, 4.790], label: 'Palier de l’étage' },
  bed1: { p: [-7.834, 4.30, 7.915], t: [-7.724, 3.60, 9.534], label: 'Chambre 1' },
  bed2: { p: [-5.390, 4.30, 5.044], t: [-4.099, 3.60, 6.850], label: 'Chambre 2' },
  bed3: { p: [-4.689, 4.30, 2.959], t: [-3.142, 3.60, 4.007], label: 'Chambre 3' },
  bathN: { p: [-6.420, 4.30, 11.239], t: [-4.997, 3.60, 11.085], label: 'Salle de bains nord' },
  bathS: { p: [-6.264, 4.30, 1.057], t: [-5.349, 3.60, 1.787], label: 'Salle de bains sud' }
};
let house;
let furnitureVisible = true;
let furnitureMeshCount = 0;
const status = document.querySelector('#status');
const loading = document.querySelector('#loading');
const furniturePrefixes = ['V11_KITCHEN','V11_DINING','V11_LIVING','V11_BEDROOM','V11_DRESSING','V11_SDB','V11_GF_WC','V11_UF_WC','V11_LAUNDRY','V11_ENTRY_CLOSET','V12_KITCHEN','V12_DINING','V12_LIVING','V12_BEDROOM','V12_DRESSING','V12_SDB','V12_GF_WC','V12_UF_WC_TOILET','V12_LAUNDRY','V12_ENTRY_CLOSET','V12_BARSTOOL','V12_DINING_TABLE'];
function isFurniture(name) { const upper = name.toUpperCase(); return furniturePrefixes.some(prefix => upper.startsWith(prefix)); }
function classifyFurniture(root) {
  root.traverse(object => {
    const inherited = Boolean(object.parent?.userData.isFurnitureTree);
    object.userData.isFurnitureTree = inherited || isFurniture(object.name);
    if (object.isMesh && object.userData.isFurnitureTree) furnitureMeshCount += 1;
  });
}
function preset(key) {
  const view = presets[key];
  camera.position.fromArray(view.p);
  camera.lookAt(new THREE.Vector3().fromArray(view.t));
  status.textContent = `${view.label} · SOURCE = ${config.viewerSource}`;
  window.__lastPreset = key;
}
window.__setPreset = preset;
preset('outside');
const modelUrl = new URL(resolveProjectAsset(config.model));
modelUrl.searchParams.set('release', config.cacheKey);
window.__viewerVersion = config.version;
window.__viewerRelease = config.release;
window.__viewerModelUrl = modelUrl.href;
window.__viewerSource = config.viewerSource;
document.documentElement.dataset.viewerVersion = config.version;
document.documentElement.dataset.viewerRelease = config.release;
document.documentElement.dataset.viewerModel = modelUrl.pathname.split('/').pop();
document.documentElement.dataset.viewerSource = config.viewerSource;
document.documentElement.dataset.viewerReady = 'loading';

new GLTFLoader().load(modelUrl.href, gltf => {
  house = gltf.scene;
  classifyFurniture(house);
  window.__liveMaterialAudit = tuneLiveModel(renderer, house, mobile);
  scene.add(house);
  loading.classList.add('hide');
  preset('outside');
  window.__viewerReady = true;
document.documentElement.dataset.viewerReady = 'true';
document.documentElement.dataset.viewerMeshes = String(window.__liveMaterialAudit.meshes);
document.documentElement.dataset.viewerMaterials = String(window.__liveMaterialAudit.uniqueMaterials);
document.documentElement.dataset.viewerTextures = String(window.__liveMaterialAudit.uniqueTextures);
document.documentElement.dataset.viewerFurnitureMeshes = String(furnitureMeshCount);
document.documentElement.dataset.viewerFurnitureVisible = 'true';
}, progress => {
  if (progress.total) {
    const percent = Math.round(100 * progress.loaded / progress.total);
    status.textContent = `Téléchargement ${percent} % · ${config.version}`;
    loading.textContent = `Ouverture du modèle ${config.version} — ${percent} %`;
  }
}, error => {
  window.__viewerFailed = true;
  document.documentElement.dataset.viewerReady = 'failed';
  window.__viewerError = error?.message || String(error);
  loading.innerHTML = `<div><strong>Erreur ${config.version}</strong><small id="errdetail"></small><button id="retry3d">Réessayer</button> <a href="../rapide/">Galerie sourcée</a></div>`;
  document.querySelector('#errdetail').textContent = window.__viewerError;
  document.querySelector('#retry3d').onclick = () => location.reload();
  status.textContent = `Erreur : ${window.__viewerError}`;
  console.error('[V18 GLTFLoader]', error);
});
setTimeout(() => {
  if (!window.__viewerReady && !window.__viewerFailed) loading.innerHTML = 'Toujours en cours… <a href="../rapide/">Voir la galerie sourcée</a>';
}, 20000);

document.querySelector('#start').onclick = () => {
  preset('outside');
  if (!mobile) controls.lock();
  else status.textContent = `Départ extérieur · utilisez ▲ pour entrer · SOURCE = ${config.viewerSource}`;
};
document.querySelectorAll('[data-preset]').forEach(button => button.onclick = () => preset(button.dataset.preset));
document.querySelector('#furniture').onclick = event => {
  furnitureVisible = !furnitureVisible;
  house?.traverse(object => { if (object.userData.isFurnitureTree) object.visible = furnitureVisible; });
  event.currentTarget.textContent = furnitureVisible ? 'Masquer les meubles' : 'Afficher les meubles';
  document.documentElement.dataset.viewerFurnitureVisible = String(furnitureVisible);
};
const keys = {};
addEventListener('keydown', event => keys[event.code] = true);
addEventListener('keyup', event => keys[event.code] = false);
const clock = new THREE.Clock();
function move() {
  const delta = Math.min(clock.getDelta(), .05);
  const speed = (keys.ShiftLeft || keys.ShiftRight ? 6 : 2.6) * delta;
  if (keys.KeyW || keys.KeyZ || keys.ArrowUp || keys.TouchForward) controls.moveForward(speed);
  if (keys.KeyS || keys.ArrowDown || keys.TouchBack) controls.moveForward(-speed);
  if (keys.KeyA || keys.KeyQ || keys.ArrowLeft || keys.TouchLeft) controls.moveRight(-speed);
  if (keys.KeyD || keys.ArrowRight || keys.TouchRight) controls.moveRight(speed);
  if (keys.KeyE) camera.position.y += speed;
  if (keys.KeyC) camera.position.y -= speed;
}
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
renderer.setAnimationLoop(() => { if (controls.isLocked) move(); else clock.getDelta(); renderer.render(scene, camera); });

if (mobile) {
  document.querySelector('#start').textContent = 'Commencer dehors';
  const pad = document.createElement('div');
  pad.className = 'mobile-pad';
  pad.innerHTML = '<button data-m="f">▲</button><button data-m="l">◀</button><button data-m="r">▶</button><button data-m="b">▼</button><span>Glissez sur l’image pour regarder</span>';
  document.body.append(pad);
  const map = { f: 'TouchForward', b: 'TouchBack', l: 'TouchLeft', r: 'TouchRight' };
  pad.querySelectorAll('button').forEach(button => {
    const key = map[button.dataset.m];
    button.addEventListener('pointerdown', event => { event.preventDefault(); keys[key] = true; });
    ['pointerup','pointercancel','pointerleave'].forEach(name => button.addEventListener(name, () => keys[key] = false));
  });
  let last = null;
  renderer.domElement.addEventListener('pointerdown', event => { last = [event.clientX, event.clientY]; renderer.domElement.setPointerCapture(event.pointerId); });
  renderer.domElement.addEventListener('pointermove', event => {
    if (!last) return;
    const dx = event.clientX - last[0], dy = event.clientY - last[1];
    last = [event.clientX, event.clientY];
    const euler = new THREE.Euler().setFromQuaternion(camera.quaternion, 'YXZ');
    euler.y -= dx * .004;
    euler.x = Math.max(-1.45, Math.min(1.45, euler.x - dy * .004));
    camera.quaternion.setFromEuler(euler);
  });
  renderer.domElement.addEventListener('pointerup', () => last = null);
}
