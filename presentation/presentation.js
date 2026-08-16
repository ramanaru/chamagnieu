import * as THREE from '../shared/vendor/three.module.js';
import { OrbitControls } from '../shared/vendor/addons/controls/OrbitControls.js';
import { GLTFLoader } from '../shared/vendor/addons/loaders/GLTFLoader.js';
import { loadProjectConfig, applyProjectVersion, resolveProjectAsset } from '../shared/project-config.js?release=v18-asset-pilot-1';
import { setupLiveLighting, tuneLiveModel } from '../shared/live-realism.js?release=v18-asset-pilot-1&pipeline=lighting-r2';
import { installLiveVegetation } from '../shared/live-vegetation.js?release=v18-asset-pilot-1';
import { installLiveFurniturePilot } from '../shared/live-furniture-pilot.js?release=v18-asset-pilot-1';
import { installLiveMaterialPilot } from '../shared/live-materials-pilot.js?release=v18-asset-pilot-1';

const config = await loadProjectConfig();
applyProjectVersion(config);
const scene = new THREE.Scene();
scene.background = new THREE.Color(0xb8c5bb);
scene.fog = new THREE.Fog(0xb8c5bb, 56, 125);
const camera = new THREE.PerspectiveCamera(52, innerWidth / innerHeight, .018, 260);
const mobile = matchMedia('(pointer:coarse)').matches;
const renderer = new THREE.WebGLRenderer({ antialias: !mobile, powerPreference: 'high-performance' });
// Render one physical pixel per CSS pixel on high-DPI screens. This keeps the
// complete asset pilot responsive on phones and integrated browsers without
// changing geometry, PBR maps or the antialiased output.
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.0));
renderer.setSize(innerWidth, innerHeight);
document.body.prepend(renderer.domElement);
setupLiveLighting(THREE, scene, renderer, config, mobile);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = .06;
controls.minDistance = .35;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI * .98;

const views = {
  front: { p: [1.941, 4.4, -15.173], t: [-1.436, 2.655, -.663], label: 'Façade et toiture — vraie scène Web V18' },
  axon: { p: [22.008, 21.5, -10.53], t: [-.75, 2.1, -4.5], label: 'Vue générale — modèle Web V18 complet' },
  garden: { p: [15.0, 9.6, -24.0], t: [-3.0, 2.45, -7.0], label: 'Jardin — 4 arbres réalistes, pelouse et maison' },
  hedges: { p: [9.0, 4.2, -18.5], t: [-1.0, 1.0, -11.2], label: 'Haies — 18 segments feuillus CC0 instanciés sur GPU' },
  kitchen: { p: [-5.875, 1.82, 4.353], t: [-3.439, .92, 2.852], label: 'Cuisine — mobilier réellement contenu dans le GLB Web' },
  living: { p: [-7.465, 1.58, 5.190], t: [-5.459, .92, 8.133], label: 'Séjour — matériaux intégrés au GLB Web' },
  dining: { p: [-7.465, 1.58, 5.190], t: [-4.80, .86, 6.45], label: 'Salle à manger — table et six chaises CC0 à échelle réelle' },
  bed: { p: [-7.834, 4.30, 7.915], t: [-7.724, 3.60, 9.534], fov: 74, label: 'Chambre — lit CC0 redimensionné et placé sur le plan' },
  floor: { p: [-7.465, 1.65, 5.190], t: [-5.459, .12, 8.133], label: 'Sol intérieur — carrelage, joints, relief et mobilier du séjour' },
  ground: { p: [9.5, 8.2, -10.5], t: [-2.4, .15, -5.4], label: 'Sols extérieurs — pelouse, enrobé et gravier intégrés' },
  upper: { p: [-7.834, 4.30, 7.915], t: [-7.724, 3.60, 9.534], label: 'Étage — chambre, cloisons, portes et mobilier du GLB Web' }
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
function setView(key) {
  const view = views[key];
  camera.fov = view.fov || 52;
  camera.updateProjectionMatrix();
  camera.position.fromArray(view.p);
  controls.target.fromArray(view.t);
  controls.update();
  status.textContent = `${view.label} · SOURCE = ${config.viewerSource}`;
  document.querySelectorAll('[data-view]').forEach(button => button.classList.toggle('active', button.dataset.view === key));
  window.__lastView = key;
}
window.__setView = setView;
window.__viewerCamera = camera;
window.__viewerControls = controls;
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

new GLTFLoader().load(modelUrl.href, async gltf => {
  house = gltf.scene;
  classifyFurniture(house);
  window.__liveMaterialAudit = tuneLiveModel(renderer, house, mobile, config);
  scene.add(house);
  loading.textContent = `Installation des assets CC0 à échelle réelle · ${config.version}…`;
  const [materialPilot, furniturePilot, vegetation] = await Promise.all([
    installLiveMaterialPilot({ THREE, house, renderer, mobile, cacheKey: config.cacheKey }),
    installLiveFurniturePilot({ scene, house, renderer, cacheKey: config.cacheKey }),
    installLiveVegetation({ scene, house, renderer, mobile, cacheKey: config.cacheKey })
  ]);
  window.__assetPilotMaterialAudit = materialPilot;
  window.__assetPilotFurnitureAudit = furniturePilot;
  window.__liveVegetationAudit = vegetation;
  // Lighting and the architectural scene are static. Render the 2048 px
  // shadow map once after all pilot assets are installed instead of rebuilding
  // it on every frame; the visual result stays identical and navigation gains
  // substantial GPU headroom.
  renderer.shadowMap.autoUpdate = false;
  renderer.shadowMap.needsUpdate = true;
  document.documentElement.dataset.viewerShadowMode = 'static-once-after-assets';
  furnitureMeshCount = 0;
  classifyFurniture(house);
  loading.classList.add('hide');
  setView('front');
  window.__viewerReady = true;
document.documentElement.dataset.viewerReady = 'true';
document.documentElement.dataset.viewerMeshes = String(window.__liveMaterialAudit.meshes);
document.documentElement.dataset.viewerMaterials = String(window.__liveMaterialAudit.uniqueMaterials);
document.documentElement.dataset.viewerTextures = String(window.__liveMaterialAudit.uniqueTextures);
document.documentElement.dataset.viewerFurnitureMeshes = String(furnitureMeshCount);
document.documentElement.dataset.viewerFurnitureVisible = 'true';
document.documentElement.dataset.viewerVegetation = window.__liveVegetationAudit.status;
document.documentElement.dataset.viewerAssetPilot = furniturePilot.status === 'accepted' && materialPilot.status === 'applied' ? 'accepted' : 'partial-fallback';
document.documentElement.dataset.viewerAssetPilotFamilies = String(furniturePilot.acceptedFamilies || 0);
document.documentElement.dataset.viewerAssetPilotInstances = String(furniturePilot.instanceCount || 0);
document.documentElement.dataset.viewerAssetPilotFurnitureErrors = String(furniturePilot.errors?.length || 0);
document.documentElement.dataset.viewerAssetPilotMaterialErrors = String(materialPilot.errors?.length || 0);
document.documentElement.dataset.viewerAssetPilotMaterialMatches = String(materialPilot.matchedMaterials || 0);
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

document.querySelectorAll('[data-view]').forEach(button => button.onclick = () => setView(button.dataset.view));
document.querySelector('#furniture').onclick = event => {
  furnitureVisible = !furnitureVisible;
  house?.traverse(object => { if (object.userData.isFurnitureTree) object.visible = furnitureVisible; });
  event.currentTarget.textContent = furnitureVisible ? 'Masquer les meubles' : 'Afficher les meubles';
  document.documentElement.dataset.viewerFurnitureVisible = String(furnitureVisible);
};
addEventListener('resize', () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});
renderer.setAnimationLoop(() => { controls.update(); renderer.render(scene, camera); });
