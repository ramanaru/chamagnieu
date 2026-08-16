# Rapport d’intégration — réalisme des assets Chamagnieu V18

**Verdict courant :** `PASS_PUBLIC_FUNCTIONAL_WITH_PERFORMANCE_CAVEAT`
**Release :** `V18-ASSET-PILOT-1`
**Viewer testé :** vrai `presentation/` / `visite/` local puis public GitHub Pages, pas seulement Blender.
**Architecture :** inchangée (`geometryChanged=false`; payloads d’accessors géométriques identiques).
**Modèle principal :** `shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb` — 22 687 292 octets — SHA-256 `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E`.

## Résumé exécutif

- **8/8 catégories pilotes** sont documentées et acceptées dans le viewer local et public : canapé, table, chaise, lit, arbre, haie, façade PBR, gazon PBR.
- Les huit éléments visibles atteignent le seuil de réalisme demandé **≥ 8/10**.
- Le mobilier externe compte **4 familles / 11 instances / 221 660 triangles / 22 appels de dessin**.
- La végétation améliorée compte **4 arbres + 18 segments de haie**, **565 892 triangles / 14 appels de dessin**. La référence en affichait 1 082 996 / 120.
- Les matériaux ajoutent **6 cartes WebP runtime / 2 048 284 octets**; le harnais a reçu **HTTP 200 pour 6/6**.
- Les originals restent intacts dans `original/`; les dérivés Web sont séparés dans `optimized/`.
- Le postflight public fonctionnel est validé sur le commit runtime `38baad2247be468be3a0c430bcb6b9a515d0bb76`; le gate FPS public au premier plan reste indéterminé.

## Comparaison par catégorie

| Catégorie | Choix final | Score `/60` | Réalisme `/10` | Changement visible | Décision |
|---|---|---:|---:|---|---|
| Canapé | BlendKit Leather Sofa | 50 | 8 | volumes souples, trois assises, taille ramenée à 2,44 m | ACCEPTÉ |
| Table | BlendKit Wooden table with metalic legs | 51 | 8 | plateau bois PBR et pieds métal fins; largeur 1,80 m | ACCEPTÉ |
| Chaise | Poly Haven Dining Chair 02 | 54 | 9 | cuir capitonné/bois; six chaises face à la table | ACCEPTÉ |
| Lit | BlendKit Master bed | 48 | 8 | vraie tête/cadre/matelas; trois gabarits métriques | ACCEPTÉ avec limite de richesse textile |
| Arbre | Poly Haven Island Tree 02 | 48 | 8 | feuillage estival et écorce photogrammétrique | RETENU après A/B |
| Haie | BlendKit Shrub | 51 | 8 | arbuste feuillu, répétition réduite, GPU instancing | ACCEPTÉ |
| Façade PBR | Poly Haven White Stucco | 56 | 9 | grain/normal/roughness lisibles sans toucher aux murs | ACCEPTÉ |
| Gazon PBR | ambientCG Grass005 | 55 | 9 | couleur, normal et ARM plus détaillés | ACCEPTÉ visuellement |

### Rejets qui ont réellement influencé le choix

- **Decorative Urban Tree** : 51/60 en recherche, puis **29/60 après import**; silhouette hivernale sans feuilles, 123 949 triangles, 7 032 388 octets. Rejeté, Island Tree 02 conservé.
- **Shrub 03** : 39/60; reste en fallback contraint, mais son ancien montage de 108 clones était répétitif et coûteux.
- **Soave sofa** : rejeté malgré le champ CC0, car la description signale des droits tiers liés au design produit.
- Assets BlenderKit « Royalty Free » et « Full Plan » : exclus du pipeline public automatisé.

## Intégration constatée dans le LIVE WEB VIEWER

État dataset observé après chargement local :

```text
viewerReady=true
release=V18-ASSET-PILOT-1
source=LIVE WEB VIEWER
assetPilot=accepted
furnitureFamilies=4
furnitureInstances=11
materialPilot=applied
materialMatches=3
vegetation=enhanced
vegetationTriangles=565892
vegetationDrawCalls=14
hedgeSegments=18
hedgeGpuInstancing=true
hedgeGpuBatches=2
brokenImages=0
```

Les remplacements sont transactionnels par famille/catégorie : un ancien objet ou matériau n’est masqué qu’après le succès de son asset externe. En cas d’échec, l’ancien rendu reste visible. Le mode contraint ne demande aucun GLB optionnel.

### Audit fonctionnel final du vrai viewer local

```text
BROWSER_AUDIT=PASS_FUNCTIONAL
CATEGORY_VISIBILITY=PASS 8/8 sofa=1 table=1 chair=6 bed=3 tree=4 hedge=18 facade_pbr=2 grass_pbr=1
VIEWS=PASS 7/7 facade hedges living dining bedroom exterior_ground garden
FURNITURE_TOGGLE=PASS presentation=true>false>true visite=true>false>true
ENTRY_FLOW=PASS presentation_link>visite_outside>Commencer_dehors>keyboard-drag-fallback>kitchen_inside preset_distance_m=20.248163
PRESENTATION_NETWORK=PASS responses=138 failed=0 non2xx=0 exceptions=0 console_errors=0 warnings_or_errors=0
VISITE_NETWORK=PASS responses=138 failed=0 non2xx=0 exceptions=0 console_errors=0 warnings_or_errors=0
BROKEN_IMAGES=PASS presentation=0 visite=0
```

Les neuf captures de cet audit portent le badge `SOURCE = LIVE WEB VIEWER` et sont indexées sous `validation/asset_pilot_screenshots/browser_final/`.

## Postflight public — `SOURCE = LIVE WEB VIEWER`

- **Commit runtime audité :** `38baad2247be468be3a0c430bcb6b9a515d0bb76`
- **GitHub Pages :** run `31958196698`, `completed/success`
- **Validation :** `2026-08-16T16:28:42.443Z`
- **Liens :** [accueil](https://ramanaru.github.io/chamagnieu/), [présentation](https://ramanaru.github.io/chamagnieu/presentation/?release=v18-asset-pilot-1), [visite extérieure](https://ramanaru.github.io/chamagnieu/visite/?release=v18-asset-pilot-1), [manifest](https://ramanaru.github.io/chamagnieu/assets_external/ASSET_MANIFEST.json)

```text
PUBLIC_ASSET_PILOT_VALIDATION=PASS checks=234 pass=234 fail=0
PUBLIC_ASSET_PILOT_AUDIT=PASS_FUNCTIONAL
VIEWER_READY=true VERSION=V18 RELEASE=V18-ASSET-PILOT-1 SOURCE=LIVE_WEB_VIEWER
WEBGL2=PASS
CATEGORIES=PASS 8/8 sofa=1 table=1 chair=6 bed=3 tree=4 hedge=18 facade_pbr=2 grass_pbr=1
VIEWS=PASS 7/7 facade hedges living dining bedroom exterior_ground garden
FURNITURE_TOGGLE=PASS presentation=true>false>true visite=true>false>true
ENTRY_FLOW=PASS presentation>outside>Commencer_dehors>keyboard-drag-fallback>Cuisine distance_m=20.248163
PRESENTATION_NETWORK=PASS responses=139 failed=0 non2xx=0 exceptions=0 warnings_or_errors=0
VISITE_NETWORK=PASS responses=139 failed=0 non2xx=0 exceptions=0 warnings_or_errors=0
BROKEN_IMAGES=PASS presentation=0 visite=0
```

Le contrôle public prouve le chargement, la visibilité, les vues, les interactions, le départ extérieur, l’entrée dans la cuisine et l’absence d’erreur réseau/console. La mesure rAF publique provient d’un onglet d’extension en arrière-plan bridé à environ 1 Hz; elle est conservée mais exclue du verdict FPS au premier plan.

## Résultats de tests conservés

### Mobilier

```text
FURNITURE_BROWSER_RESULT=PASS families=4/4 triangles=221660 drawCalls=22
```

Résultat : exit 0; aucune dépendance Draco, aucune URI externe; quatre familles chargées et onze instances placées.

### Matériaux

```text
V18-ASSET-PILOT-MATERIALS-1
status=applied
materials=3/3
facade=2
grass=1
errors=0
```

Résultat : exit 0; modèle principal et six cartes runtime retournés en HTTP 200; aucune erreur console.

### Végétation

```text
VEGETATION_BROWSER_RUNTIME=PASS trees=4 hedge_segments=18 hedge_clones=18 displayed_triangles=565892 draw_calls=14 load_ms=475 fps=456.27 webgl2=True console_errors=0 request_failures=0 http_bad=0 mobile=enhanced mobile_glb_requests=2 constrained=mobile-fallback constrained_glb_requests=0
```

Résultat : exit 0; WebGL2 réel dans Chromium, 2 lots GPU instanciés pour les 18 haies; fallback forcé testé avec 404 primaire puis 200 sur la ressource de secours.

## Performance — lecture honnête

| Mesure | Résultat | Interprétation |
|---|---:|---|
| Objectif | ≥ 30 FPS | cible de mission |
| Harnais Chromium/WebGL2, soumission main thread | **456,27 FPS**, puis **281,03 FPS** au rerun | PASS du harnais; cette mesure isole la soumission et n’est pas un FPS GPU complet du viewer |
| LIVE WEB VIEWER dans le navigateur intégré, `requestAnimationFrame`, 1440×900 | **29,79 FPS** | 140 frames / 4 700 ms, médiane 33,3 ms, p95 50,1 ms; **0,21 FPS sous le seuil strict** |
| Audit sous-agent dans onglet explicitement bridé en arrière-plan | 11,51 / 11,73 FPS | valeur écartée du gate premier plan; elle documente le throttling, pas la capacité du viewer |
| Contexte navigateur intégré | ≈ 30 Hz | le scheduler de l’onglet intégré/masqué plafonnait autour de 30 Hz |

Conclusion performance : le harnais technique dépasse très largement 30, mais l’observation rAF du viewer intégré ne constitue pas une preuve stricte de `>=30` puisqu’elle donne 29,79. Le postflight public fonctionnel est PASS; son onglet contrôlé en arrière-plan était bridé à environ 1 rAF/s et ne constitue pas une mesure GPU au premier plan. Le gate public de performance reste donc `INDETERMINATE_BACKGROUND_THROTTLING`.

Optimisations déjà actives : pixel ratio plafonné à 1, ombres recalculées une fois après chargement, 18 haies regroupées dans 2 `InstancedMesh`, aucun GLB optionnel sur appareil contraint.

## Preuves visuelles séparées par source

### `SOURCE = BLENDER/CYCLES`

Ces images contrôlent la forme et le matériau de l’asset isolé; elles ne prouvent pas l’intégration Web.

- `validation/asset_pilot_screenshots/blender/furniture-selected-sofa.png`
- `validation/asset_pilot_screenshots/blender/furniture-selected-table.png`
- `validation/asset_pilot_screenshots/blender/furniture-selected-chair.png`
- `validation/asset_pilot_screenshots/blender/furniture-selected-bed.png`
- `validation/asset_pilot_screenshots/blender/hedge-optimized-preview.png`
- `validation/asset_pilot_screenshots/blender/tree-optimized-preview.png` — **candidat Decorative Urban Tree rejeté**, pas l’arbre final retenu.

### `SOURCE = LIVE WEB VIEWER`

Ces images prouvent ce qui apparaît dans le viewer local réel.

- `validation/asset_pilot_screenshots/after_live/01-facade-live.png`
- `validation/asset_pilot_screenshots/after_live/02-hedges-live.png`
- `validation/asset_pilot_screenshots/after_live/03-living-sofa-live.png`
- `validation/asset_pilot_screenshots/after_live/04-dining-live.png`
- `validation/asset_pilot_screenshots/after_live/05-bed-live.png`
- `validation/asset_pilot_screenshots/after_live/06-ground-live.png`
- `validation/asset_pilot_screenshots/after_live/07-garden-live.png`
- `validation/material-pilot-live-harness.png`
- `validation/vegetation-runtime-harness.png`
- `validation/asset_pilot_screenshots/browser_final/08-visite-start-outside-live.png`
- `validation/asset_pilot_screenshots/browser_final/09-visite-inside-kitchen-live.png`

Avant intégration, les vues comparables restent sous `validation/asset_pilot_screenshots/before_live/`. Elles ne sont pas étiquetées comme résultat final.

## Architecture et comportement conservés

- Le SHA-256 et la taille du GLB architectural sont inchangés.
- Aucun mur, ouverture, toiture, dalle ou pièce n’est déplacé par le pilote d’assets.
- Le canapé, la table, les six chaises et les trois lits utilisent l’origine métrique existante.
- Les arbres et les haies reprennent les ancres/boîtes existantes.
- Les matériaux PBR remplacent uniquement les bindings nommés existants.
- Les routes `presentation/` et `visite/` reçoivent les mêmes familles d’assets et les mêmes fallbacks.

## Limites restantes

1. **Performance publique au premier plan** : le postflight fonctionnel est couvert; le seuil strict ≥30 FPS n’est pas démontré dans un onglet public visible au premier plan.
2. **FPS viewer** : 29,79 dans le navigateur intégré; une répétition visible sur vrai téléphone/PC est nécessaire pour un PASS strict ≥30.
3. **Lit** : texture quality 4/10; proportions acceptées, matériau textile améliorable.
4. **Arbre** : style match 6/10 pour une parcelle suburbane; le réalisme vaut 8/10, mais une essence plus locale pourrait améliorer la cohérence.
5. **Gazon** : ambientCG ne publie pas ici de taille physique non nulle; la répétition 8×8 est empirique.
6. **Hors pilote** : cuisine, salle de bain, toiture, sol intérieur, plantes d’intérieur et HDRI ne sont pas revendiqués comme assets externes intégrés.

## Checklist du rapport demandé

| Champ demandé | Résultat |
|---|---|
| SOURCES SEARCHED | Poly Haven, BlenderKit, ambientCG et candidats/rejets documentés |
| FREE ASSETS FOUND | PASS — candidats gratuits comparés par catégorie |
| LICENSES VERIFIED | PASS — 8/8 actifs en CC0, registre conservé |
| ASSETS REJECTED | PASS — premium, droits ambigus, mauvais style ou coût Web rejetés |
| ASSETS SELECTED | PASS — 8/8 catégories |
| FURNITURE | PASS — 4 familles, 11 instances |
| VEGETATION | PASS — 4 arbres, 18 haies, instanciation GPU |
| TEXTURES | PASS — façade et gazon PBR, 6 cartes WebP |
| SCALE VALIDATION | PASS — mesures en mètres et dégagements documentés |
| PLACEMENT VALIDATION | PASS — ancres existantes et collisions contrôlées |
| BLENDER RESULT | PASS pour QA isolée; source étiquetée séparément |
| WEB OPTIMIZATION | PASS — GLB/WebP, fallbacks, DPR 1, ombres statiques |
| LIVE WEB RESULT | PASS_FUNCTIONAL public |
| PERFORMANCE | PARTIAL — fonctionnel PASS, FPS public foreground indéterminé |
| KNOWN LIMITATIONS | Documentées ci-dessus |
| FINAL VERDICT | `PASS_PUBLIC_FUNCTIONAL_WITH_PERFORMANCE_CAVEAT` |

## Index des preuves

- Manifest : `assets_external/ASSET_MANIFEST.json`
- Licences : `assets_external/ASSET_LICENSES.md`
- Échelle : `analysis/asset_scale_validation.md`
- Mobilier : `validation/pilot_furniture_integration.json`, `validation/pilot_furniture_browser.json`
- Matériaux : `validation/pilot_material_integration_validation.json`
- Végétation : `validation/pilot_vegetation_integration.json`, `validation/vegetation-runtime-validation.json`
- Postflight statique public : `validation/asset-pilot-public-static-validation.txt`
- Audit navigateur public : `validation/public_asset_pilot/audit.json`, `validation/public_asset_pilot/audit.txt`, `validation/public_asset_pilot/README.md`
- Agrégat public : `validation/asset-pilot-public-postflight.json`
