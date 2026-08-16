# Pilote matériaux PBR — façade White Stucco + pelouse Grass005

## Décision du pilote

Le pilote retient uniquement deux sources officielles sous licence CC0 :

| Usage | Source retenue | Score documentaire | Licence | Décision |
|---|---|---:|---|---|
| Façade | [Poly Haven — White Stucco](https://polyhaven.com/a/white_stucco) (`white_stucco`) | 56/60 | [CC0 1.0](https://polyhaven.com/license) | Conserver la bonne source existante, mais remplacer le câblage incomplet/ancien par un triplet local couleur + normal OpenGL + ARM et corriger le tiling. |
| Pelouse | [ambientCG — Grass 005](https://ambientcg.com/a/Grass005) (`Grass005`) | 55/60 | [CC0 1.0 Universal](https://docs.ambientcg.com/license/) | Remplacer `leafy_grass`, trop beige et chargé en feuilles/brindilles, par une pelouse courte et verte. |

Le téléchargement est effectué au build avec un User-Agent dédié. Le viewer ne hotlinke aucun fournisseur : il ne charge que les dérivés locaux sous `assets_external/`.

## Arborescence livrée

```text
assets_external/materials/
├── facade/white_stucco/
│   ├── original/
│   │   ├── white_stucco_diff_2k.jpg
│   │   ├── white_stucco_nor_gl_2k.jpg
│   │   ├── white_stucco_arm_2k.jpg
│   │   ├── white_stucco_info.json
│   │   └── white_stucco_files.json
│   └── optimized/
│       ├── white_stucco_color_1k.webp
│       ├── white_stucco_normal_gl_1k.webp
│       ├── white_stucco_arm_1k.webp
│       └── white_stucco_ao_1k.webp
└── exterior/grass005/
    ├── original/
    │   ├── Grass005_2K-JPG.zip
    │   └── Grass005_metadata.json
    └── optimized/
        ├── Grass005_color_1k.webp
        ├── Grass005_normal_gl_1k.webp
        ├── Grass005_arm_1k.webp
        └── Grass005_ao_1k.webp
```

Le ZIP officiel `Grass005_2K-JPG.zip` est conservé intact et son CRC est validé. Il contient les cartes Color, NormalGL, NormalDX, Roughness, AmbientOcclusion, Displacement et les descripteurs de matériau. L'extraction intermédiaire est supprimée après optimisation pour éviter de publier une duplication d'environ 39 Mio ; l'original officiel reste intégralement disponible dans `/original`.

## Optimisation mesurée

### White Stucco

- Source physique publiée : **1,998 × 1,998 m**.
- Originaux Web utiles : **7 742 799 octets** (diffuse, normal OpenGL, ARM en 2K).
- Charge runtime : **489 958 octets** (couleur, normal et ARM en WebP 1K).
- Réduction de la charge runtime : **93,67 %**.
- Un AO 1K séparé est également livré pour l'inspection ; le runtime lit directement le canal R du pack ARM et évite donc une quatrième requête.

### Grass005

- L'API v3 officielle publie les dimensions à zéro : aucune dimension physique fiable n'est revendiquée.
- Cartes sources utilisées dans le ZIP : **24 986 179 octets** (Color, NormalGL, Roughness, AO).
- Charge runtime : **1 558 326 octets** (couleur, normal et ARM en WebP 1K).
- Réduction de la charge runtime : **93,76 %**.
- Le pack ARM est généré localement : **R=AO, G=roughness, B=metalness=0**.

Les dimensions, octets et SHA-256 de chaque fichier figurent dans `validation/pilot_material_asset_build.json` et `validation/pilot_material_integration_validation.json`.

## Câblage runtime

Module : `shared/live-materials-pilot.js`

API :

```js
await installLiveMaterialPilot({ THREE, house, renderer, mobile, cacheKey });
```

Le module vise exactement :

- `V12_PBR_OFFWHITE_STUCCO` : repeat `3 × 3`, offset `0 / -2`, normalScale `0,42` ;
- `V10_STUCCO_NEW_BUILD` : repeat `6 × 6`, offset `0 / -5`, normalScale `0,32` ;
- `PBR_B_GRASS` : repeat `8 × 8`, offset `0 / 0`, normalScale `0,72`.

Ces repeats reprennent les transformations physiques déjà autorisées dans le GLB V18 au lieu d'appliquer un scale arbitraire. Pour Grass005, le repeat 8 conserve l'échelle visuelle de la pelouse existante puisque le fournisseur ne publie pas de dimension exploitable.

Règles de textures :

- baseColor : `SRGBColorSpace` ;
- normal OpenGL et ARM : `NoColorSpace` ;
- textures appliquées à un GLB : `flipY=false` ;
- `RepeatWrapping`, mipmaps et anisotropie bornée à 8 ;
- `aoMap`, `roughnessMap` et `metalnessMap` partagent le même pack ARM ;
- aucune géométrie, ouverture, toiture, mur ou cote architecturale n'est modifiée.

Le module expose `window.__assetPilotMaterialAudit` et `data-viewer-material-pilot`. Il ne remplace une catégorie que lorsque ses trois cartes sont chargées. Si une carte façade échoue, les bindings façade intégrés au GLB restent intacts ; la même règle s'applique indépendamment à la pelouse.

## Validation WebGL réelle

Harness indépendant : `validation/material-pilot-harness.html`

Résultat littéral observé dans le navigateur après un chargement propre :

```text
V18-ASSET-PILOT-MATERIALS-1
status=applied
materials=3/3
facade=2
grass=1
errors=0
```

- `data-material-harness-ready=true`
- `data-viewer-material-pilot=applied`
- GLB principal : HTTP 200
- 6 cartes runtime : HTTP 200
- console : **0 warning, 0 error** sur le chargement propre
- capture LIVE WEB VIEWER : `validation/material-pilot-live-harness.png`

La capture montre que la façade conserve sa géométrie V18 et reçoit un grain d'enduit fin, tandis que le matériau `PBR_B_GRASS` reçoit la pelouse Grass005 sans ajouter de maillage ni de draw call.

## Tests reproductibles

```text
COMMAND: python .\validation\build_pilot_material_assets.py
EXIT: 0
RESULT: status=PASS; facade_original_bytes=7742799; facade_optimized_bytes=578960; grass_archive_bytes=39523019; grass_optimized_bytes=2192974

COMMAND: node --check .\shared\live-materials-pilot.js
EXIT: 0
RESULT: [sortie vide]

COMMAND: python -m py_compile .\validation\build_pilot_material_assets.py
EXIT: 0
RESULT: [sortie vide]
```

## Intégration dans les deux viewers

Le module est prêt à être importé par `presentation/presentation.js` et `visite/visite.js`. L'appel doit intervenir après `tuneLiveModel(...)` et avant d'annoncer le viewer prêt, afin que l'audit public corresponde aux bindings effectivement visibles. Les pages et `project-config` restent volontairement inchangés dans ce sous-lot, conformément au périmètre d'intégration partagé.
