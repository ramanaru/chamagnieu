# Audit final courant de synchronisation — V18-LIVE-SYNC-3

> **État audité :** worktree final courant après correction live-sync. Cette section décrit la release `V18-LIVE-SYNC-3`. La section historique pré-correction est conservée intégralement plus bas et ne doit pas être confondue avec l'état actuel.

## A. Verdict final statique actuel

1. Les cinq pages `/`, `/presentation/`, `/visite/`, `/rapide/` et `/gpt/` lisent désormais la même configuration `shared/project-config.json`.
2. La configuration centrale annonce `version=V18`, `release=V18-LIVE-SYNC-3`, `cacheKey=v18-live-sync-3` et `model=./Chamagnieu_V18_REALISM_FINAL.glb`.
3. Les deux viewers WebGL résolvent le modèle actif vers `/shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3`; aucun chemin GLB n'est plus codé en dur dans leurs loaders.
4. Le fichier actif est byte-for-byte identique au meilleur GLB V18 audité : `27 987 896` octets, SHA-256 `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28`.
5. L'ancien nom `Chamagnieu_V18_ROOF_GROUND_REALISM.glb` reste présent comme copie identique, mais il n'est plus le modèle sélectionné par la configuration runtime.
6. Toutes les pages affichent V18; l'ancien titre V16 de `/rapide/` est corrigé. Aucune page actuelle n'affiche `Chamagnieu V11`.
7. Les sources visuelles sont maintenant explicites : `/presentation/` et `/visite/` portent `SOURCE = LIVE WEB VIEWER`; `/` et `/rapide/` étiquettent les WebP `SOURCE = BLENDER`; `/gpt/` explique les deux sources.
8. `/gpt/` n'est plus une redirection; c'est une page stable qui lit la configuration centrale et fournit les liens vers la page publique, `house.json` et les rapports.
9. L'éclairage live est centralisé dans `shared/live-realism.js` avec environnement PMREM procédural, ACES, exposition réduite, ombres desktop 2048 et anisotropie jusqu'à 8.
10. Le filtre mobilier reconnaît les préfixes V11 et V12 sur `167/167` nœuds glTF nommés. La propagation d’appartenance à leurs enfants couvre `169` meshes runtime Three.js après expansion des deux nœuds à deux primitives, contre seulement `30/167` nœuds nommés dans la baseline.

## B. Tableau final demandé par page

| Page | Version affichée / source | GLB chargé | JSON chargé | Textures / images chargées | Scripts chargés | Source matériaux | Source mobilier | Source végétation | Cache actuel |
|---|---|---|---|---|---|---|---|---|---|
| `/` | Fallback HTML `V18`, puis `V18` et `V18-LIVE-SYNC-3` appliqués depuis config. Galerie marquée `SOURCE = BLENDER` | **Aucun GLB runtime.** L'URL du GLB dans JSON-LD est documentaire | `shared/project-config.json` via `page-version.js`, fetch `{cache:'no-store'}`. `house.json` est seulement lié | Deux WebP Blender `images/v18-facade-roof-ground.webp` et `v18-jardin-textures.webp` | `shared/page-version.js?release=v18-live-sync-3` → `project-config.js` | Non applicable au HTML; les visuels sont des rendus Blender | Visible uniquement dans les WebP Blender | Visible uniquement dans les WebP Blender | Entrée JS versionnée; config no-store; HTML et deux images racine sans query |
| `/presentation/` | `V18` depuis config; badge `SOURCE = LIVE WEB VIEWER`; release exposée dans `dataset` et `window.__viewerRelease` | **Oui** : config `./Chamagnieu_V18_REALISM_FINAL.glb` résolue sous `/shared/`, query `?release=v18-live-sync-3` | `shared/project-config.json` no-store. `house.json` non fetché | 37 JPEG embarqués dans le GLB + CanvasTexture 512×256 convertie en environnement PMREM; `preview.webp` uniquement pendant chargement | Three r179, `OrbitControls`, `GLTFLoader`, `presentation.js`, `project-config.js`, `live-realism.js` | 35 matériaux du GLB Blender; 20 albedos, 18 normales, 17 MR; tuning anisotropie/envMap au runtime | Géométrie V11/V12 embarquée; 167 nœuds glTF nommés et 169 meshes runtime couverts après propagation aux enfants | 4 arbres légers + 18 haies V17 embarqués; textures feuillage 256 px | HTML appelle JS/CSS avec release; config no-store; GLB reçoit la query centrale release. Helpers transitifs sans query propre |
| `/visite/` | `V18` depuis config; badge `SOURCE = LIVE WEB VIEWER`; départ extérieur conservé | **Oui** : exactement le même URL/config/hash que `/presentation/` | `shared/project-config.json` no-store. `house.json` non fetché | Même jeu de 37 JPEG intégrés + même environnement PMREM; `preview.webp` au chargement | Three r179, `PointerLockControls`, `GLTFLoader`, `visite.js`, `project-config.js`, `live-realism.js` | Identique à `/presentation/` | Identique à `/presentation/`; 167 nœuds glTF nommés donnent 169 meshes runtime masquables; bouton Masquer/Afficher | Identique à `/presentation/`; aucune végétation externe | Même politique que `/presentation/` |
| `/rapide/` | Titre et H1 `V18`; version appliquée depuis config; avertissement `SOURCE = BLENDER` | **Aucun** | `shared/project-config.json` no-store via `page-version.js` | Neuf WebP statiques Blender, tous avec `?release=v18-live-sync-3` | `shared/page-version.js?release=v18-live-sync-3` → `project-config.js` | Matériaux du rendu Blender seulement; aucune matière live | Mobilier visible uniquement dans les images Blender | Végétation visible uniquement dans les images Blender; la page précise que le modèle Web reste low-poly | Images et entry JS versionnées; config no-store |
| `/gpt/` | Titre/H1 `V18` puis config; explique `LIVE WEB VIEWER` vs `BLENDER` | **Aucun chargement GLB.** Le nom actif est affiché textuellement | `shared/project-config.json` no-store via `page-version.js`; `house.json` est un lien | Aucune image/texture runtime sur cette page | `shared/page-version.js?release=v18-live-sync-3` → `project-config.js` | Décrit les sources, sans créer de matériaux | Aucun mobilier rendu | Aucune végétation rendue | Entry JS versionnée; config no-store |

## C. Chemin d'exécution final réel

```text
shared/project-config.json
  version = V18
  release = V18-LIVE-SYNC-3
  cacheKey = v18-live-sync-3
  model = ./Chamagnieu_V18_REALISM_FINAL.glb

/presentation/ ou /visite/
  -> script d'entrée ?release=v18-live-sync-3
  -> loadProjectConfig()
  -> fetch /shared/project-config.json avec cache:no-store
  -> resolveProjectAsset(config.model)
  -> /shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3
  -> GLTFLoader.load()
  -> tuneLiveModel()
  -> scène Three.js
```

Les variables runtime exposent en plus :

```text
window.__viewerVersion = V18
window.__viewerRelease = V18-LIVE-SYNC-3
window.__viewerModelUrl = .../Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3
window.__viewerSource = LIVE WEB VIEWER
window.__liveMaterialAudit = compteurs du modèle réellement chargé
```

## D. Cohérence JSON et documentation publique

| Fichier | Version / release | Modèle | Statut |
|---|---|---|---|
| `shared/project-config.json` | `V18` / `V18-LIVE-SYNC-3` | `./Chamagnieu_V18_REALISM_FINAL.glb` | Source de vérité runtime |
| `house.json` | `V18` / `V18-LIVE-SYNC-3` | `shared/Chamagnieu_V18_REALISM_FINAL.glb` | Cohérent; lien descriptif, non fetché par viewers |
| `gpt/house.json` | Identique byte-for-byte à `house.json` | Même chemin/hash | Cohérent |
| `README.md` | `V18-LIVE-SYNC-3` | Lien `Chamagnieu_V18_REALISM_FINAL.glb` | Synchronisé |
| `llms.txt` | `V18-LIVE-SYNC-3` | Lien et SHA actifs | Synchronisé |
| JSON-LD de `/` | V18 REALISM FINAL | URL brute du nouveau nom | Synchronisé |

`houseData` est déclaré dans la configuration, mais aucun script runtime ne fetch encore `house.json`. La version et le modèle proviennent bien de `project-config.json`; `house.json` reste un manifeste public parallèle cohérent.

`presentationImages` est également déclaré dans la config, mais `/` et `/rapide/` gardent leurs chemins d'images dans le HTML. Cette duplication n'affecte pas le GLB actif, mais elle demeure une dette de centralisation mineure.

## E. Modèles présents et rôle final

| Fichier | Taille | SHA-256 | Rôle |
|---|---:|---|---|
| `shared/Chamagnieu_V18_REALISM_FINAL.glb` | 27 987 896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | **Actif via config** |
| `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb` | 27 987 896 | même SHA | Copie historique byte-identique, non sélectionnée par le runtime |

Il n'existe aucun `.gltf`, aucun GLB V11, aucun modèle lite et aucun fallback géométrique. Le changement de nom ne change pas le contenu visuel du modèle; les améliorations live viennent de la configuration unique, des corrections de sélection mobilier, de l'éclairage et du tuning runtime.

## F. Textures et matériaux finaux

Le contenu du GLB actif est identique à la baseline :

- 37 images JPEG embarquées, 0 texture externe;
- 56 objets texture glTF, dont une entrée sans source mais inutilisée;
- 35 matériaux;
- 20 `baseColorTexture`, 18 `normalTexture`, 17 `metallicRoughnessTexture`;
- 0 `occlusionTexture`, 0 `emissiveTexture`;
- 15 matériaux sans texture;
- cartes clés toiture/asphalte/herbe/gravier à 1024;
- cartes secondaires surtout à 512;
- deux cartes de feuillage à 256.

`live-realism.js` ajoute désormais :

- anisotropie jusqu'à 8 sur les textures utilisées;
- `envMapIntensity` à `.9` pour verre/fenêtre/métal, `.55` pour les autres matériaux compatibles;
- ACES Filmic, exposition `.92`;
- environnement PMREM généré depuis une CanvasTexture procédurale 512×256;
- ombres PCFSoft 2048 desktop;
- HemisphereLight `.72`, AmbientLight `.06`, soleil `2.4`, fill `.22`.

Ce tuning améliore la lecture PBR, mais ne transforme pas la végétation légère ou les matériaux sans cartes en assets D5 haute fidélité.

## G. Mobilier final

Les préfixes V11 auparavant omis ont été ajoutés aux deux scripts. Le filtre final couvre :

- cuisine V11;
- chaises/salle à manger V11 et table V12;
- séjour V11/V12;
- chambres V11/V12;
- dressing, sanitaires, WC, buanderie et placard d'entrée;
- tabourets V12.

Résultat statique sur le GLB : `167` nœuds glTF nommés correspondent au filtre. Deux d’entre eux — `V11_LIVING_ARMCHAIR` et `V12_LIVING_ARMCHAIR_2` — possèdent chacun deux primitives. `GLTFLoader` les développe en enfants meshes; la propagation de `isFurnitureTree` couvre donc `169` meshes runtime Three.js. La commande de visibilité agit sur ces 169 meshes, au lieu des seuls 30 nœuds V12 reconnus dans la baseline.

## H. Végétation finale

La synchronisation n'a pas remplacé les assets :

- 18 haies V17;
- quatre arbres `V17_TREE_LIGHT`, 7 meshes par arbre;
- 1 276 triangles par arbre;
- deux cartes de feuillage 256×256.

La page `/rapide/` indique désormais explicitement que ses arbres sont un rendu Blender de référence et que la végétation du modèle Web reste volontairement low-poly. Il n'y a plus de confusion de source, mais il n'y a pas non plus de nouveaux arbres D5 dans le GLB actif.

## I. Cache final

### Mesures présentes

- `project-config.json` est fetché avec `{ cache: 'no-store' }`;
- scripts d'entrée, CSS et WebP de galerie portent `?release=v18-live-sync-3`;
- le GLB reçoit dynamiquement `?release=v18-live-sync-3` depuis `config.cacheKey`;
- le GLB actif possède un nom final distinct;
- aucun service worker, CacheStorage, Workbox ou manifest PWA.

### Risque résiduel mineur

`project-config.js` et `live-realism.js` sont des imports transitifs sans query propre. Le script d'entrée est versionné et la configuration JSON est no-store, mais un cache HTTP particulièrement agressif peut encore réutiliser ces helpers à URL stable. Ce point n'affecte pas le choix final du modèle tant que `project-config.js` courant est servi, mais une query/import map centralisée sur les helpers serait plus hermétique.

Les deux images racine de `/` n'ont pas de query; elles restent des rendus Blender statiques et non les textures live.

## J. Références V11 à V18 dans l'état final

- **V11 :** présent dans le code uniquement comme préfixes de sélection mobilier et dans 416 nodes du GLB; jamais utilisé comme version affichée.
- **V12 :** préfixes mobilier/matériaux et 30 nodes du GLB.
- **V13 à V16 :** uniquement dans l'historique `scenes[0].extras` du GLB.
- **V17 :** noms des arbres/haies/matériaux de végétation et deux assets de galerie historiques inutilisés.
- **V18 :** version d'application, release, nom actif du GLB, UI, manifests et derniers meshes/metadata.

Le relevé exhaustif, avec lignes source et pointeurs JSON du GLB, se trouve dans `audit/version-references.txt`, section `FINAL CURRENT`.

## K. Verdict final statique

```text
FINAL_RELEASE=V18-LIVE-SYNC-3
FINAL_ALL_FIVE_PAGES_USE_CENTRAL_CONFIG=YES
FINAL_ALL_PAGE_LABELS_V18=YES
FINAL_ACTIVE_GLB=shared/Chamagnieu_V18_REALISM_FINAL.glb
FINAL_ACTIVE_GLB_HASH_MATCHES_CONFIG=YES
FINAL_PRESENTATION_AND_VISIT_USE_SAME_GLB=YES
FINAL_GLB_TEXTURES_EMBEDDED=YES
FINAL_EXTERNAL_TEXTURE_COUNT=0
FINAL_MATERIAL_RUNTIME_TUNING=YES
FINAL_PROCEDURAL_PMREM_IBL=YES
FINAL_FURNITURE_FILTER_COVERS_AUDITED_SET=YES (167/167 NAMED_GLTF_NODES; 169 RUNTIME_MESHES)
FINAL_VEGETATION_HIGH_FIDELITY_D5=NO
FINAL_GALLERY_SOURCE_LABEL=BLENDER
FINAL_VIEWER_SOURCE_LABEL=LIVE WEB VIEWER
FINAL_HOUSE_JSON_RUNTIME_FETCH=NO
FINAL_SERVICE_WORKER=NONE
FINAL_STATIC_VERSION_SYNC_STATUS=PASS
FINAL_REALISM_MATCH_TO_BLENDER=PARTIAL_BY_DESIGN
PUBLIC_BROWSER_NETWORK_STATUS=OUTSIDE_THIS_STATIC_REPORT
```

## L. Limite du présent audit

Cette section prouve la cohérence du worktree final actuel. Elle ne remplace pas la vérification navigateur/public : le test final doit confirmer que GitHub Pages sert ces mêmes octets, que le canvas charge le GLB final, qu'aucune erreur console/réseau n'apparaît et que les captures sont étiquetées `SOURCE = LIVE WEB VIEWER`.

---

# BASELINE HISTORIQUE PRÉ-CORRECTION — SECTION PRÉSERVÉE

La section suivante est le rapport initial sur le commit `145caaad9822a1381e931bbd87dfa3d0f1d62edb`. Les chemins GLB directs, le titre V16 de `/rapide/`, l'absence d'IBL et le filtre mobilier incomplet qui y sont décrits sont des constats historiques désormais corrigés dans la section finale ci-dessus.

# Audit statique de synchronisation des versions — snapshot initial V18

> **Nature de ce document :** première version factuelle, établie avant toute correction du viewer. Ce rapport décrit le code et le GLB présents lors du snapshot initial. Il ne constitue pas encore la preuve réseau/navigateur du déploiement public.

> **Snapshot de référence :** commit Git `145caaad9822a1381e931bbd87dfa3d0f1d62edb`. Des corrections live-sync ont commencé en parallèle dans le worktree après la collecte; elles sont volontairement exclues de ce rapport initial et devront faire l'objet d'un second scan final.

## 1. Verdict immédiat

1. **Les deux seules pages qui chargent réellement une scène 3D sont `/presentation/` et `/visite/`.** Elles pointent toutes deux, en dur, vers `../shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a` (`presentation/presentation.js:22`, `visite/visite.js:13`).
2. **Il n'existe qu'un seul fichier `.glb` et aucun `.gltf` dans le snapshot.** Aucun GLB V11, lite, presentation, viewer ou fallback n'est présent.
3. **Le GLB chargé est bien nommé V18 et son hash correspond au manifeste :** `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28`, `27 987 896` octets.
4. **Le texte `Chamagnieu V11` n'est affiché par aucune page actuelle.** V11 est néanmoins massivement présent dans les noms internes du GLB (mobilier, portes, toiture, escalier). Si le navigateur affiche réellement `Chamagnieu V11`, cette chaîne vient d'un autre déploiement/build ou d'un document HTML/JS obsolète servi au navigateur, pas des pages auditées ici.
5. **Une incohérence visible existe dans le code actuel :** le `<title>` de `/rapide/` dit encore `Chamagnieu V16 — Galerie instantanée`, tandis que son `<h1>` annonce V18 (`rapide/index.html:2` et `:4`).
6. **Les textures majeures ne sont pas absentes du GLB : elles sont embarquées.** Le GLB contient 37 images JPEG intégrées et aucune URI de texture externe. Il ne peut donc pas y avoir de 404 individuel sur ces textures; seul le téléchargement/décodage du GLB entier peut échouer.
7. **Le rendu live est techniquement différent des images statiques.** Les pages d'accueil et galerie affichent des WebP pré-rendus; elles ne rendent pas le GLB. Le viewer Three.js utilise un éclairage simplifié sans HDRI/IBL, sans `scene.environment`, sans occlusion texturée et avec ombres désactivées sur mobile. Cette différence explique un rendu plus plat même lorsque les textures sont bien chargées.
8. **Le modèle Web est explicitement allégé.** Les métadonnées du GLB indiquent en V13 `web::no_draco+reduced_vegetation` et `23` objets mobiles lourds retirés. La V17 réintroduit seulement `4_light_trees+18_hedges`; la V18 conserve ces arbres qualifiés `light`.

## 2. Périmètre et méthode

- Racine auditée : `C:\Users\jonat\Documents\Codex\2026-08-14\files-mentioned-by-the-user-c\outputs\Chamagnieu_3D_V18_LIVE_SYNC`
- Sources lues : HTML, JavaScript, CSS, JSON, Markdown, `llms.txt`, `robots.txt`, `sitemap.xml`, script serveur.
- GLB inspecté via son chunk JSON glTF 2.0, pas par une recherche de chaînes binaires.
- Vendor Three.js et faux positifs binaires exclus des occurrences de versions.
- Inventaire exhaustif des références : `audit/version-references.txt`.
- Ce snapshot statique doit ensuite être confronté au réseau/console du site public.

## 3. Matrice page par page

| Page | Nature réelle | Version affichée | GLB réellement chargé | JSON réellement chargé | Scripts / runtime | Images / textures visibles | Cache possible |
|---|---|---|---|---|---|---|---|
| `/` | Page HTML statique, pas un viewer | `V18`, badge `V18-GITHUB-1` | **Aucun**. Le GLB apparaît seulement dans le JSON-LD sous forme d'URL documentaire | **Aucun fetch**. `house.json` est seulement un lien | Aucun JS d'application; uniquement JSON-LD inline | Deux WebP : `images/v18-facade-roof-ground.webp`, `images/v18-jardin-textures.webp` | HTML et images sans query de version |
| `/presentation/` | Viewer WebGL orbital | `V18` partout | `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a` | Aucun | Three.js r179, `OrbitControls`, `GLTFLoader`, `presentation.js?v=18a` | Les 37 images embarquées du GLB; `shared/preview.webp` seulement pendant le chargement | CSS, JS et GLB utilisent `?v=18a` |
| `/visite/` | Viewer WebGL première personne | `V18` partout | `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a` | Aucun | Three.js r179, `PointerLockControls`, `GLTFLoader`, `visite.js?v=18a` | Les 37 images embarquées du GLB; `shared/preview.webp` seulement pendant le chargement | CSS, JS et GLB utilisent `?v=18a` |
| `/rapide/` | Galerie d'images, **pas de 3D live** | `<title>` **V16**, `<h1>` V18 | **Aucun** | Aucun | Aucun JS | 9 WebP. Les 2 premières sont nommées V18; les 7 intérieures sont non versionnées | Images demandées avec `?v=18a`, HTML sans query imposée |
| `/gpt/` | Redirection HTML | Aucune version visible durablement | **Aucun** | Aucun | `<meta http-equiv="refresh" content="0;url=../">` | Aucune; redirige vers `/` | Redirection/HTML sans query |
| `/house.json` | Donnée statique | `V18-GITHUB-1` | URL brute descriptive seulement | C'est le document lui-même | Aucun | Deux URLs d'images et une URL GLB documentaires | Sans query |
| `/gpt/house.json` | Copie statique | `V18-GITHUB-1` | URL brute descriptive seulement | C'est le document lui-même | Aucun | Identique à `/house.json` | Sans query |

### Point essentiel

`house.json` n'est la source de vérité d'aucun viewer. Ni `presentation.js`, ni `visite.js`, ni `/rapide/`, ni `/gpt/` ne le chargent. Le nom du modèle, la query `18a` et les libellés V18 sont dupliqués et codés en dur.

## 4. Ce qui charge le GLB et ce qui est seulement galerie/rendu

### Charge réellement le GLB

- `presentation/presentation.js:22`
  - `new GLTFLoader()`
  - `loader.load('../shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb?v=18a', ...)`
  - scène affichée en Three.js avec `OrbitControls`.
- `visite/visite.js:13`
  - `new GLTFLoader()`
  - même URL GLB.
  - scène affichée en Three.js avec `PointerLockControls`.

### Ne charge pas le GLB

- `/` : deux images WebP statiques; l'URL GLB du JSON-LD n'est pas exécutée.
- `/rapide/` : neuf images WebP statiques; le bouton « Ouvrir la 3D » navigue vers `/presentation/`.
- `/gpt/` : simple redirection vers `/`.
- `house.json`, `gpt/house.json`, `README.md`, `llms.txt` : liens documentaires uniquement.
- `shared/preview.webp` : arrière-plan du masque de chargement, pas une capture live et pas une texture de la maison.

**Conséquence :** une belle image visible sur `/` ou `/rapide/` ne prouve pas que le viewer Three.js produit le même rendu.

## 5. Inventaire réel du GLB utilisé

| Champ | Valeur |
|---|---|
| Fichier | `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb` |
| Taille | `27 987 896` octets |
| SHA-256 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` |
| Format | GLB glTF 2.0 |
| Générateur | `Khronos glTF Blender I/O v5.2.39` |
| Chunk JSON | `754 700` octets |
| Chunk BIN | `27 233 168` octets |
| Nodes | `794` |
| Meshes | `793` |
| Somme des sommets par accessor | `377 701` |
| Triangles | `316 781` |
| Materials | `35` |
| Textures glTF | `56` |
| Images intégrées | `37` JPEG |
| Textures externes | `0` |
| Animations | `1` (`modern_wooden_cabinet_body`, non jouée par le viewer) |
| Caméras dans le GLB | `0` |
| Lumières dans le GLB | `0` |
| Extensions utilisées | `KHR_materials_transmission`, `KHR_materials_ior`, `KHR_texture_transform` |
| Draco | Non. Pas de `KHR_draco_mesh_compression`; `DRACOLoader` vendor n'est pas configuré |
| KTX2/Basis | Non |

Une entrée texture glTF (`textures[50]`) n'a pas de `source`, mais elle est **inutilisée par tous les matériaux**. Les 37 images sont toutes référencées par au moins une autre entrée texture.

## 6. Versions internes du GLB : V11 ne veut pas dire que le fichier chargé est V11

Le GLB V18 est un assemblage cumulatif. Ses noms de nodes contiennent :

| Préfixe interne | Nombre de nodes | Rôle observé |
|---|---:|---|
| V10 | 165 | façade, fenêtres, porte d'entrée, garage, descentes, tuiles de rive, gouttières, sols d'accès |
| V11 | 416 | mobilier principal, cuisine, portes, escalier, sanitaires, tuiles de faîtage/arêtiers |
| V12 | 30 | tabourets, table salle à manger, fauteuil supplémentaire, plaids |
| V17 | 46 | 18 haies + 4 arbres composés de 7 meshes chacun |
| V18 | 1 node nommé | sol visible ajouté; d'autres meshes toiture/site portent V18 dans leur nom de mesh |

Les scènes `extras` enregistrent en plus les étapes V12 à V18. Elles contiennent donc des références V13, V14, V15 et V16 même lorsqu'aucun node n'a ces préfixes.

### Traçabilité déclarée dans `scenes[0].extras`

- V12 : `furniture::metric_relayout; materials::6_PBR_sets; exterior::CC0_vegetation`
- V13 : `dining::6_chairs_facing_table; kitchen::backsplash_attached_to_wall; web::no_draco+reduced_vegetation`; `23` objets mobiles lourds retirés.
- V14 : retrait de `18` liaisons `TEXCOORD` invalides; départ extérieur; fallback détaillé.
- V15 : conversion/diffusion en JPEG 512 sans dépendance WebP.
- V16 : retrait d'une référence de texture dont la source manquait.
- V17 : `20` UV restaurés; matériaux toiture/herbe/asphalte/gravier/sol intérieur; `4_light_trees+18_hedges+outdoor_dining`.
- V18 : `29` nodes de table extérieure supprimés; trois toitures reprises; UV toiture; trois sols extérieurs repris; textures PBR clés à 1024; quatre arbres légers et dix-huit haies conservés.

Le terme **V11 visible dans un inspecteur de scène** correspond donc aux noms historiques des composants. Le fichier conteneur chargé et les derniers correctifs de toiture/sol sont bien V18. En revanche, les composants de mobilier n'ont pas été renommés vers V18.

## 7. Audit des textures et matériaux live

### Images embarquées

- 37 JPEG intégrés dans le chunk BIN; aucune `uri` externe.
- 12 images de surfaces clés sont réellement `1024 × 1024` : toiture, asphalte, pelouse et gravier (diffuse, normal, roughness).
- 23 images sont `512 × 512`.
- 2 images de feuillage V17 sont seulement `256 × 256`.
- Plusieurs noms de sources contiennent `_2k` ou `_1k`, mais les images réellement embarquées sont redimensionnées à 512 ou 1024.

### Couverture matériaux

- 35 matériaux au total.
- 20 ont une `baseColorTexture`.
- 18 ont une `normalTexture`.
- 17 ont une `metallicRoughnessTexture`.
- 0 ont une `occlusionTexture`.
- 0 ont une `emissiveTexture`.
- 15 sont entièrement basés sur des facteurs/couleurs sans texture : aluminium, verre, anthracite, joints, chrome, pierre de seuil, sous-face, blanc, pierre de plan de travail, laque, miroir, électroménager noir, greige de cuisine, etc.

### Sources déclarées

Les métadonnées attribuent explicitement à Poly Haven CC0 les ensembles V12 `white_stucco`, `floor_tiles_02`, `white_oak_veneer`, `brushed_concrete_04`, `cotton_jersey`. Les autres noms embarqués incluent notamment `clay_roof_tiles_02`, `asphalt_01`, `leafy_grass`, `gravel`, `american_walnut_veneer`, `modern_coffee_table_01`, `potted_plant_04` et deux cartes de feuillage V17. Le snapshot ne contient pas de fichier de licence détaillant individuellement ces derniers assets; leur présence dans le GLB est cependant vérifiée.

### Conclusion texture-path

Aucun chemin relatif de texture n'est utilisé au runtime. Les textures ne sont ni dans un dossier local oublié, ni demandées séparément à GitHub Pages. Si le GLB atteint `HTTP 200` et se décode, ses images embarquées sont disponibles au loader. Le diagnostic « textures absentes » doit donc distinguer :

- **texture réellement manquante** (non observée statiquement pour les 55 entrées utilisées),
- **matériau volontairement sans texture** (15 matériaux),
- **texture faible résolution** (256/512),
- **PBR visuellement aplati par l'éclairage live**.

## 8. Source du mobilier live

Le mobilier n'est pas chargé depuis des fichiers externes. Il est incorporé dans le même GLB :

- 137 meshes de mobilier à préfixe V11 : environ `176 387` sommets et `206 567` triangles;
- 30 meshes complémentaires à préfixe V12 : environ `13 092` sommets et `12 752` triangles;
- exemples : cuisine, six chaises, canapé, fauteuils, TV, lits, chevets, dressings, sanitaires, buanderie;
- deux matériaux/assets nommés `modern_coffee_table_01` et `potted_plant_04` sont également embarqués.

Il n'existe pas dans ce site un second catalogue de meubles « beaux rendus » chargé seulement pour la galerie. Toutefois, les WebP intérieurs ne contiennent aucune métadonnée prouvant qu'ils ont été générés par ce GLB exact. La correspondance doit être vérifiée visuellement et non supposée.

### Défaut fonctionnel du bouton « Masquer les meubles »

Les deux scripts détectent presque exclusivement des préfixes `V12_*`, alors que l'essentiel du mobilier du GLB est `V11_*` :

- nodes de mobilier larges identifiés : `167`;
- nodes effectivement marqués par le prédicat actuel : `30`;
- nodes V11 manqués par le bouton : `137`.

Le bouton ne masque donc pas la cuisine, les lits, le canapé, les six chaises V11, les sanitaires et la majorité du mobilier. Ce défaut est identique dans `presentation.js:20` et `visite.js:11`.

## 9. Source de la végétation live

La végétation est également incorporée au GLB, pas générée au runtime :

- `18` haies V17 : `1 728` sommets, `1 944` triangles;
- `4` arbres V17, chacun divisé en 7 meshes : `882` sommets et `1 276` triangles par arbre;
- total arbres : `3 528` sommets, `5 104` triangles;
- feuillage : deux textures JPEG `256 × 256`, `V17_PBR_FOLIAGE_DEEP` et `V17_PBR_FOLIAGE_FRESH`.

Les noms `V17_TREE_LIGHT_*`, la résolution 256 et la métadonnée V13 `reduced_vegetation` prouvent qu'il s'agit d'un set Web léger, pas d'arbres D5/Blender haute fidélité. Les métadonnées déclarent une double filière de réalisme (`REALISM_DUAL_PIPELINES`) et un pipeline `B_D5_READY`; le viewer Three.js ne charge aucun asset D5.

## 10. Éclairage live réellement appliqué

### `/presentation/`

- `HemisphereLight` intensité `2.8`;
- `AmbientLight` intensité `1.35`;
- `DirectionalLight` intensité `2.8`;
- ACES Filmic, exposition `1.22`;
- fond et brouillard unis;
- ombres PCF soft sur desktop, shadow map `1024`;
- mobile : antialiasing désactivé, ombres désactivées, pixel ratio limité à `1.1`.

### `/visite/`

- `HemisphereLight` intensité `2.9`;
- `AmbientLight` intensité `1.45`;
- `DirectionalLight` intensité `2.8`;
- ACES Filmic, exposition `1.24`;
- mêmes restrictions mobile.

### Manques confirmés

- aucune HDRI;
- aucune IBL / `scene.environment`;
- aucun `PMREMGenerator`;
- aucune light probe;
- aucune lumière embarquée dans le GLB;
- aucune occlusion texturée;
- `RGBELoader.js` existe dans vendor mais n'est importé par aucun viewer.

La somme très élevée de lumière hémisphérique + ambiante + directionnelle remplit fortement les ombres. Sans environnement, les matériaux physiques (verre, métal, chrome) manquent de réflexions; sans AO, les contacts mobilier/sol paraissent faibles. Le résultat est nécessairement plus plat qu'un rendu Blender Eevee/D5 même avec les mêmes albedos et normales.

## 11. Galerie et provenance des images

- `images/v18-facade-roof-ground.webp` est byte-identique à `shared/gallery/v18-facade-roof-ground.webp`.
- `images/v18-jardin-textures.webp` est byte-identique à `shared/gallery/v18-jardin-textures.webp`.
- Deux fichiers V17 restent présents mais ne sont référencés par aucune page : `v17-facade-textures.webp`, `v17-jardin-textures.webp`.
- Les sept images intérieures de `/rapide/` ont des noms non versionnés (`cuisine.webp`, `salon.webp`, etc.) tout en étant décrites comme V18.
- Les WebP n'ont pas de métadonnée de provenance moteur/version exploitable.
- Le GLB déclare `render_engine_truth=BLENDER_EEVEE_D5_IMPORT_PREVIEW`, `realism_branch=REALISM_DUAL_PIPELINES`, `pipeline=B_D5_READY` et un UUID D5. Le viewer Web n'interprète aucune de ces métadonnées.

**Verdict de provenance :** les deux images nommées V18 sont des rendus de contrôle statiques; les sept images intérieures sont statiques et non versionnées. Aucune n'est une capture automatiquement produite par la page live au moment de l'ouverture.

## 12. Cache et risque d'ancienne V11

### Éléments absents

- aucun service worker;
- aucun appel `navigator.serviceWorker.register`;
- aucune utilisation de `CacheStorage` (`caches.*`);
- aucun manifest PWA/cache;
- aucun fallback vers un GLB V11;
- aucun fichier `house.glb` générique réutilisé.

### Éléments présents

- `?v=18a` sur CSS, JS, GLB et images de `/rapide/`;
- nom de modèle versionné V18;
- HTML de route, images racine et JSON sans query imposée;
- `serve.ps1` utilise `python -m http.server`, sans politique Cache-Control personnalisée.

Le code actuel ne peut pas produire le titre V11. Une V11 vue publiquement doit donc être recherchée dans : ancien HTML mis en cache, ancien déploiement GitHub Pages, autre URL/domaine, onglet non rechargé ou version antérieure du repository. La preuve finale nécessite l'URL effective, les en-têtes HTTP et les ressources réellement téléchargées dans Network.

## 13. Défauts de synchronisation statiques classés

### Critiques pour la vérité affichée

1. Pas de configuration centrale : version, modèle et query sont dupliqués.
2. `house.json` n'est pas consommé par les viewers.
3. `/rapide/` mélange V16 dans le titre et V18 dans la page.
4. Galerie statique présentée à côté du viewer sans étiquette de moteur/source.

### Importants pour le réalisme

5. Aucun HDRI/IBL/environment map dans Three.js.
6. Ombres et antialiasing supprimés sur mobile; pixel ratio très limité.
7. Végétation explicitement allégée et feuillage à 256 px.
8. 15 matériaux sans aucune texture; aucune AO/emissive.
9. Texture source annoncée 2k mais livraison 512/1024.
10. Le bouton de visibilité mobilier manque 137 nodes V11.

### Hygiène / dette

11. Deux images V17 inutilisées restent publiées.
12. Un objet texture glTF sans source reste dans le GLB, même s'il est inutilisé.
13. L'animation embarquée n'est jamais jouée.
14. Les dossiers vendor contiennent Draco/RGBE, mais aucun des deux n'est configuré; leur présence ne signifie pas que le live les utilise.

## 14. Hypothèse causale consolidée

Le mauvais rendu observé n'est pas expliqué par un viewer actuel chargeant un fichier V11 différent : les deux loaders visent le seul GLB V18. La différence visible vient principalement de la combinaison suivante :

1. les images de présentation sont des WebP statiques issues d'une filière de rendu séparée;
2. la scène Web conserve des composants historiques V10/V11/V12 et une végétation V17 légère;
3. la V13 a retiré 23 objets lourds et réduit la végétation pour le mobile;
4. les cartes sont compressées à 256/512/1024;
5. Three.js n'a ni HDRI, ni IBL, ni AO, ni éclairage intérieur comparable à Blender/D5;
6. sur mobile, les ombres et l'antialiasing sont coupés;
7. les libellés et assets ne proviennent pas d'une source de vérité unique.

## 15. État provisoire et vérifications restantes

```text
STATIC_CODE_POINTS_TO_V18=YES
STATIC_ONLY_ONE_GLB=YES
STATIC_GLB_HASH_MATCHES_HOUSE_JSON=YES
GLB_TEXTURES_EMBEDDED=YES
GLB_EXTERNAL_TEXTURE_PATHS=NONE
CURRENT_SOURCE_DISPLAYS_V11=NO
CURRENT_SOURCE_HAS_V11_COMPONENT_NAMES=YES
RAPIDE_TITLE_VERSION_SYNC=FAIL (V16 vs V18)
HOUSE_JSON_IS_RUNTIME_SOURCE_OF_TRUTH=NO
GALLERY_IS_LIVE_WEB_VIEWER=NO
LIVE_LIGHTING_MATCHES_BLENDER_D5=NO
LIVE_VEGETATION_IS_HIGH_FIDELITY_D5=NO
LIVE_FURNITURE_TOGGLE_COMPLETE=NO
PUBLIC_RUNTIME_VERIFIED_IN_THIS_STATIC_REPORT=NO
PRESENTATION_IMAGES_MATCH_LIVE_GLTF=NOT_PROVEN
STATIC_SYNC_STATUS=PARTIAL
```

### Étape de preuve suivante

Ouvrir réellement le déploiement public avec cache désactivé, enregistrer l'URL finale de chaque requête, le statut et la taille du GLB, vérifier `window.__viewerVersion`, capturer façade/jardin/intérieur depuis le canvas WebGL, et étiqueter chaque preuve `SOURCE = LIVE WEB VIEWER`. C'est la seule manière de transformer ce verdict statique en verdict live.
