# Pilote mobilier CC0 — intégration métrique et Web

## Verdict

**PASS — 4/4 familles sélectionnées acceptées visuellement et techniquement.** Le pilote charge 1 canapé, 1 table, 6 chaises et 3 lits depuis `assets_external/furniture/`, sans Draco/Meshopt. Les anciens nœuds de la famille correspondante ne sont masqués **qu'après** le chargement et l'instanciation réussis. `HOUSE_REFERENCE_ORIGIN`, le GLB architectural et les pages/config du viewer restent inchangés.

Racine testée : `C:\Users\jonat\Documents\Codex\2026-08-16\chamagnieu-v18-assets-pilot`

## Gagnants et budget réel

| Rôle | Asset CC0 / score | Dimensions source X×H×P | Dimensions placées X×H×P | Triangles / draw calls source | Instances | Budget instancié | GLB Web final (octets, SHA-256) | Verdict visuel |
|---|---|---:|---:|---:|---:|---:|---|---|
| Canapé | BlenderKit Leather Sofa, **50/60**, réalisme 8/10 | 2,8725×1,0054×1,0117 m | 2,4416×0,8546×0,8599 m | 60 384 / 1 | 1 | 60 384 / 1 | `assets_external/furniture/living/sofa/optimized/sofa_web.glb` — 2 577 832 — `A1321C8B14FFC4170CECA330B581441ADE66B64CA87FF89D772E385367D21B3D` | **PASS** : trois assises et coussins lisibles; réduction uniforme 0,85 pour éviter un canapé surdimensionné. |
| Table | BlenderKit Wooden table with metalic legs, **51/60**, réalisme 8/10 | 2,0000×0,7500×0,9000 m | 1,8000×0,7500×0,9000 m | 3 500 / 6 | 1 | 3 500 / 6 | `assets_external/furniture/dining/table/optimized/table_web.glb` — 3 544 464 — `A8BCD84ADADC29F9DC26EEFA068FA393823E2599493BCADB62797986D89F67B0` | **PASS** : plateau bois PBR et piétement métal fin; largeur alignée sur la table planifiée. |
| Chaise | Poly Haven Dining Chair 02, **54/60**, réalisme 9/10 | 0,4336×0,9734×0,5764 m | 0,4076×0,9150×0,5418 m | 22 013 / 1 | 6 | 132 078 / 6 | `assets_external/furniture/dining/chair/optimized/chair_web.glb` — 920 384 — `6E5CC754877D49AF17EA2431693E29B07DEEA0A6B14163B1F23EF933E1FAAC71` | **PASS** : cuir capitonné/bois visibles; les six rotations pointent vers le centre de la table et ne se croisent pas. |
| Lit | BlenderKit Master bed, **48/60**, réalisme 8/10 | 1,7622×1,0604×2,2266 m | chambre 1 : 1,6001×0,9543×2,0000 m; chambres 2/3 : 1,4000×0,9543×2,0000 m | 8 566 / 3 | 3 | 25 698 / 9 | `assets_external/furniture/bedroom/bed/optimized/bed_web.glb` — 350 248 — `AC6B3C975A1EE98F1288A5567D4C5F89C8A9973AF7D4CF3EAB88AC79AF205637` | **PASS** : cadre bois et tête textile lisibles; trois formats alignés sur les dimensions V12, sans traversée de mur observée. |

**Total ajouté dans la scène : 11 instances, 221 660 triangles, 22 draw calls.** Les géométries et matériaux des clones restent partagés; les 6 chaises et 3 lits ne dupliquent pas leurs buffers GPU.

## Originaux préservés et optimisation

- Canapé original : `assets_external/furniture/living/sofa/original/sofa_4faac4b8-cc88-4ff2-b7fd-a7edf46d3518_library.glb`, 731 828 octets, SHA-256 `ACFAB778384BB6D6D5EB4AFE809A6A010017BFBA184EA35CCFF965E91150B7A2`.
- Table téléchargée : `assets_external/furniture/dining/table/original/table_bdff957c-a9e9-4827-b6c9-602b264a4fbf_1k_download.blend.zst`, 1 599 907 octets, SHA-256 `4D1F439387C0D5B04CDBBA919B7C9C21F2E7ED1BA3C6B9074938D61D8417DEEC`; source Blender décompressée : SHA-256 `CB6B19157399A87DBDAA9E9C8F92A05B5DA8E9D3A652FD85D8D8BA39B06A2F8C`.
- Chaise : le bundle glTF 1K officiel complet est conservé sous `assets_external/furniture/dining/chair/original/` (gltf, bin, diffuse, normal OpenGL et ARM); chaque taille/MD5 a été contrôlé contre l'API Poly Haven.
- Lit original conservé : `assets_external/furniture/bedroom/bed/original/bed_d493c69a-5c64-40bf-a7a6-a4e745bfbea8_library.glb`, 133 244 octets, SHA-256 `3BEFAF428A7AAE55C6C2C2277DAD340599E3C7D95A63462A2EE9E2770975395E`.
- Les exportations GLB finales embarquent les textures source, reposent sur Y=0, sont centrées X/Z et ont `decoderDependencies: []`. Les sources de staging sous `assets_external/models/` restent également disponibles.

L'inventaire exhaustif avec chemin, octets et SHA-256 de **chaque** original/optimisé est dans `assets_external/furniture/selected_furniture_inventory.json`.

## Runtime transactionnel

`shared/live-furniture-pilot.js` exporte `installLiveFurniturePilot({ scene, house, renderer, cacheKey })` et :

1. charge séparément les quatre GLB depuis l'arborescence `assets_external/furniture/`;
2. règle ombres, anisotropie et classification `userData.isFurnitureTree`;
3. instancie à l'échelle métrique dans le repère enfant `HOUSE_REFERENCE_ORIGIN`;
4. masque uniquement la famille d'origine dont le remplacement est complet;
5. conserve automatiquement le fallback d'une famille si son chargement échoue;
6. expose `window.__assetPilotFurnitureAudit` avec URL, métriques, placements et noms masqués.

Comptes de fallback validés : canapé 1, table 5, chaises 6, lits 30. `architectureChanged=false`.

## Commandes réellement exécutées

```powershell
python validation\download_selected_furniture_assets.py
```

Résultat littéral : `SELECTED_FURNITURE_DOWNLOAD_RESULT=PASS assets=4/4`.

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background --factory-startup --python validation\optimize_selected_furniture_assets.py
```

Résultat littéral : `SELECTED_FURNITURE_OPTIMIZE_RESULT=PASS assets=4/4`.

```powershell
python validation\stage_selected_furniture.py
```

Résultat littéral : `FURNITURE_STAGE_RESULT=PASS assets=4/4`.

```powershell
node --check shared\live-furniture-pilot.js
python -m py_compile validation\download_selected_furniture_assets.py validation\optimize_selected_furniture_assets.py validation\stage_selected_furniture.py
```

Résultat littéral : `STATIC_FURNITURE_PILOT=PASS`.

```powershell
$env:NODE_PATH='C:\Users\jonat\AppData\Local\MangaDownloaderRuntime\node_modules'
node validation\run_furniture_pilot_browser.cjs
```

Résultat littéral : `FURNITURE_BROWSER_RESULT=PASS families=4/4 triangles=221660 drawCalls=22`.

## Validation navigateur et images rouvertes

Le test automatisé `validation/pilot_furniture_browser.json` donne :

- `viewsReady=true`;
- `acceptedFourFamilies=true`;
- `architectureUnchanged=true`;
- `fallbackCounts=true`;
- `zeroConsoleErrors=true`;
- `zeroFailedRequests=true`.

Captures du **GLB principal réellement chargé** avec le module :

- séjour/table/chaises/canapé : `validation/browser/playwright-furniture-main-living.png`, SHA-256 `C9A501CED5DE9B730773521091EB74D33AAEA64708FB03B89B660F4AFEA0A73A`;
- étage/lit dans la chambre : `validation/browser/playwright-furniture-main-upper.png`, SHA-256 `9F9447B1CCFC6EC4A154FC5C292290CC8839F64B46CF6B3913D7922F01EEF8FE`;
- harness métrique automatisé : `validation/browser/playwright-furniture-main-fixture.png`, SHA-256 `A60C461434DD7D19FB17D2B4F3F5B5E24617DC0D55D8632C3638501C75967080`.

Les quatre previews Blender séparées sont `validation/asset_pilot_previews/furniture-selected-{sofa,table,chair,bed}.png`. Elles ont été rouvertes et inspectées avant l'acceptation finale.

## Fichier de preuve machine

`validation/pilot_furniture_integration.json` agrège les licences, scores, dimensions, échelles, hashes, budgets et captures. Verdict final : **PASS**.
