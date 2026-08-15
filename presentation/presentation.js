import * as THREE from '../shared/vendor/three.module.js';
import {OrbitControls} from '../shared/vendor/addons/controls/OrbitControls.js';
import {GLTFLoader} from '../shared/vendor/addons/loaders/GLTFLoader.js';

const scene=new THREE.Scene();scene.background=new THREE.Color(0xbec9bd);scene.fog=new THREE.Fog(0xbec9bd,48,115);
const camera=new THREE.PerspectiveCamera(52,innerWidth/innerHeight,.018,260);
const mobile=matchMedia('(pointer:coarse)').matches;const renderer=new THREE.WebGLRenderer({antialias:!mobile,powerPreference:'high-performance'});renderer.setPixelRatio(Math.min(devicePixelRatio,mobile?1.1:1.6));renderer.setSize(innerWidth,innerHeight);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.22;renderer.shadowMap.enabled=!mobile;renderer.shadowMap.type=THREE.PCFSoftShadowMap;document.body.prepend(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.06;controls.minDistance=.35;controls.maxDistance=80;controls.maxPolarAngle=Math.PI*.98;
scene.add(new THREE.HemisphereLight(0xf5f7ff,0x5d5545,2.8));scene.add(new THREE.AmbientLight(0xfff1dc,1.35));const sun=new THREE.DirectionalLight(0xffe4bd,2.8);sun.position.set(-18,28,-10);sun.castShadow=!mobile;sun.shadow.mapSize.set(mobile?512:1024,mobile?512:1024);sun.shadow.camera.near=.5;sun.shadow.camera.far=95;sun.shadow.camera.left=-30;sun.shadow.camera.right=30;sun.shadow.camera.top=30;sun.shadow.camera.bottom=-30;scene.add(sun);
const views={
 front:{p:[1.941,4.4,-15.173],t:[-1.436,2.655,-.663],label:'Façade et toiture en tuiles PBR restaurées'},
 axon:{p:[22.008,21.5,-10.53],t:[-.75,2.1,-4.5],label:'Vue générale V18 avec terrain extérieur texturé'},
 garden:{p:[-12.5,5.3,-17.2],t:[-4.2,3.7,-11.86],label:'Jardin V18 · arbres, haies, pelouse et terrasse restaurés'},
 kitchen:{p:[-5.875,1.82,4.353],t:[-3.439,.92,2.852],label:'Cuisine replacée dans la zone sud du RDC'},
 living:{p:[-7.465,1.58,5.190],t:[-5.459,.92,8.133],label:'Séjour et mobilier PBR à échelle réelle'},
 ground:{p:[9.5,8.2,-10.5],t:[-2.4,.15,-5.4],label:'Sol extérieur V18 · pelouse, enrobé et gravier PBR'},
 upper:{p:[-7.650,4.12,5.740],t:[-5.819,3.62,4.689],label:'Palier, cloisons et portes de l’étage'}
};
let house,furnitureVisible=true;const status=document.querySelector('#status'),loading=document.querySelector('#loading');
function isFurniture(name){const n=name.toUpperCase();return ['V12_KITCHEN','V12_DINING','V12_LIVING','V12_BEDROOM','V12_DRESSING','V12_SDB','V12_GF_WC','V12_UF_WC_TOILET','V12_LAUNDRY','V12_ENTRY_CLOSET','V12_BARSTOOL','V12_DINING_TABLE','V12_LIVING','V12_HEDGE','V12_TREE','V12_OUTDOOR'].some(p=>n.startsWith(p))}
function setView(key){const v=views[key];camera.position.fromArray(v.p);controls.target.fromArray(v.t);controls.update();status.textContent=v.label;document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===key))}
const loader=new GLTFLoader();loader.load('../shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a',g=>{house=g.scene;house.traverse(o=>{if(o.isMesh){o.castShadow=!mobile;o.receiveShadow=!mobile;o.userData.isFurniture=isFurniture(o.name)}});scene.add(house);loading.classList.add('hide');setView('front');window.__viewerReady=true;window.__viewerVersion='V18'},p=>{if(p.total){const pc=Math.round(100*p.loaded/p.total);status.textContent=`Téléchargement ${pc} %`;loading.textContent=`Ouverture rapide ${pc} %`}},e=>{window.__viewerFailed=true;window.__viewerError=e?.message||String(e);loading.innerHTML='<div><strong>Erreur V18</strong><small id="errdetail"></small><button id="retry3d">Réessayer</button> <a href="../rapide/">Galerie</a></div>';document.querySelector('#errdetail').textContent=window.__viewerError;document.querySelector('#retry3d').onclick=()=>location.reload();status.textContent='Erreur : '+window.__viewerError;console.error(e)});setTimeout(()=>{if(!window.__viewerReady&&!window.__viewerFailed)loading.innerHTML='Toujours en cours… <a href="../rapide/">Voir la galerie instantanée</a>'},12000);
document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>setView(b.dataset.view));document.querySelector('#furniture').onclick=e=>{furnitureVisible=!furnitureVisible;house?.traverse(o=>{if(o.userData.isFurniture)o.visible=furnitureVisible});e.currentTarget.textContent=furnitureVisible?'Masquer les meubles':'Afficher les meubles'};
addEventListener('resize',()=>{camera.aspect=innerWidth/innerHeight;camera.updateProjectionMatrix();renderer.setSize(innerWidth,innerHeight)});renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera)});

