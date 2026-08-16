# Pilote végétation — gate visuel, intégration Web et repli

**Date :** 2026-08-16
**Verdict : `PASS`**
**Périmètre :** `shared/live-vegetation.js`, assets végétation externes et harness de validation seulement. Les pages, la configuration projet, l'architecture et le GLB de la maison n'ont pas été modifiés.

## Décision arbre : conserver le Poly Haven actuel

Le gate Blender rejette honnêtement **Decorative Urban Tree** : la source importée est un arbre d'hiver sans feuilles. Sa silhouette ne correspond pas au jardin vert fourni; l'export Web fait **123 949 triangles** et **7 032 388 octets**, au-dessus des gates pilote de 45 k triangles et 5 Mo. Score post-import : **29/60**.

Le live conserve **Poly Haven Island Tree 02**, CC0, avec feuillage d'été et écorce photogrammétrique. Copie optimisée : `assets_external/vegetation/trees/island_tree_02/optimized/island_tree_02_web.glb`, **4 268 472 octets**, SHA-256 `845CD738030743A4592FDC10DB77A38E522E15C8901E6710C377C3D5C303CF76`, **47 000 triangles**, dimensions runtime **[4.20032, 3.40825, 4.06767] m**. Score maintenu : **48/60**. Les originaux glTF/bin/textures sont préservés sous `assets_external/vegetation/trees/island_tree_02/original/`.

## Décision haie : accepter le Shrub BlenderKit CC0

La haie pilote utilise `assets_external/vegetation/hedges/blenderkit_shrub/optimized/hedge_web.glb` : **1292892 octets**, SHA-256 `552369C1C70CE040EC8971DA0F235D24ECB9CB915B9320B1ABCB4EA0C423B7C2`, dimensions **[1.2546, 1.2522, 0.7617] m**, **20994 triangles** et 2 matériaux PBR.

Optimisation appliquée sans toucher l'original : branches de 8 576 à **3 944 triangles**; LOD déterministe conservant **72,0017 %** des cartes de feuilles et leurs UV/alpha, soit **17 050 triangles** de feuillage. Le rendu Blender reste dense. Score post-import : **51/60**.

## Runtime exact

- **18 segments architecturaux = 18 instances** du buisson complet; aucune modification de l'implantation.
- **2 batches GPU `InstancedMesh`** au lieu de 108 clones Object3D.
- Arbres : 4 instances actuelles conservées.
- Total affiché : **565892 triangles**, **14 draw calls**, 38 objets fallback masqués seulement après chargement réussi.
- Baseline : 1082996 triangles / 120 draw calls / 108 clones de haie.
- Gain : **47.748 %** de triangles, **88.333 %** de draw calls et **83.333 %** de clones de haie en moins.
- Harness Chromium/WebGL2 : **PASS**, chargement 475 ms, soumission main-thread **456.27 FPS** (>30), 0 erreur console, 0 requête échouée et 0 réponse HTTP >=400 sur le chemin primaire. Cette mesure est explicitement une mesure de soumission; le validateur du viewer complet porte le gate FPS GPU/wall-clock.

## Replis prouvés

- Téléphone non contraint : `enhanced-mobile`, 18 instances, 565892 triangles, 14 draw calls, 2 requêtes GLB.
- Téléphone contraint (`deviceMemory=2`) : `mobile-fallback`, 0 asset optionnel téléchargé, 0 remplacement et les low-poly d'origine restent visibles.
- Échec primaire forcé (`missing-primary-hedge.glb` = HTTP 404) : `shared/assets/vegetation/shrub_03_web.glb` répond HTTP 200 et est réellement chargé avec `source=retained-fallback`; l'ancien chemin 108 clones / 1 082 996 triangles reste intact.

## Preuves visuelles séparées

- Blender — haie optimisée : `validation/asset_pilot_previews/hedge-optimized-preview.png`
- Blender — arbre candidat rejeté : `validation/asset_pilot_previews/tree-optimized-preview.png`
- Navigateur WebGL2 — 4 arbres actuels + 18 haies instanciées : `validation/vegetation-runtime-harness.png`
- JSON machine exact : `validation/pilot_vegetation_integration.json`
- JSON de test navigateur : `validation/vegetation-runtime-validation.json`

## Licences

Les deux assets live et le repli sont CC0. Sources officielles : [Poly Haven](https://polyhaven.com/license), [BlenderKit](https://www.blenderkit.com/docs/licenses/). Le candidat arbre rejeté reste archivé avec sa source et son export pour audit; il n'est pas chargé par le viewer.
