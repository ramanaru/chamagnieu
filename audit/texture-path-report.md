# Rapport des chemins et contenus de textures — GLB V18

## Conclusion principale

- Le GLB live `Chamagnieu_V18_REALISM_FINAL.glb` et l’alias `Chamagnieu_V18_ROOF_GROUND_REALISM.glb` sont byte-identiques; les résultats ci-dessous s’appliquent aux deux. `project-config.json` confirme `externalTextureCount: 0`. Configuration runtime vérifiée : `release=V18-LIVE-SYNC-3`, `cacheKey=v18-live-sync-3`.

- **37/37 images de matériau sont embarquées dans le BIN du GLB via `bufferView`**; aucune image glTF n’a de champ `uri` et il n’existe donc **aucun chemin externe de texture à casser ou à servir en 404**.
- Les 37 images embarquées totalisent **2 818 542 octets (10.07% du GLB)**. Elles sont toutes des JPEG RGB.
- Résolutions : **12 × 1024²**, **23 × 512²**, **2 × 256²**.
- **55/56 objets texture** sont réellement référencés par des matériaux; `textures[50]` n’a ni `source` ni référence de matériau. C’est un objet mort, pas une référence runtime invalide.
- **37/37 images** sont utilisées. Toutes les **795 primitives** ont `TEXCOORD_0`; l’hypothèse « textures absentes à cause d’UV manquantes » n’est pas soutenue par ce GLB.
- `KHR_texture_transform` est requis : un loader qui ne le supporte pas conserverait les images mais avec une échelle/orientation UV erronée. Le `GLTFLoader` Three.js livré dans le worktree supporte cette extension.

## Images embarquées

| i | Nom interne | Résolution | Octets | SHA-256 court | Objet(s) texture |
|---:|---|---:|---:|---|---|
| 0 | `white_stucco_nor_gl_2k` | 512x512 | 12 903 | `a207f9960ce1b1af` | `0 27` |
| 1 | `white_stucco_diff_2k` | 512x512 | 6 046 | `5232b5e695efdcd9` | `1 28` |
| 2 | `white_stucco_rough_2k` | 512x512 | 2 548 | `4ad7339b9c643774` | `2 29` |
| 3 | `floor_tiles_02_nor_gl_2k` | 512x512 | 7 174 | `1577873bf45d8ced` | `3 42` |
| 4 | `floor_tiles_02_diff_2k` | 512x512 | 20 708 | `85de3cb89b647f80` | `4 43` |
| 5 | `floor_tiles_02_rough_2k` | 512x512 | 21 295 | `a096f4c0bc2184a8` | `5 44` |
| 6 | `brushed_concrete_04_nor_gl_2k` | 512x512 | 42 600 | `0144582232971458` | `6 21 45` |
| 7 | `brushed_concrete_04_diff_2k` | 512x512 | 30 028 | `8e261c633b628a6a` | `7 22 46` |
| 8 | `brushed_concrete_04_rough_2k` | 512x512 | 6 023 | `199145e67c23c056` | `8 23 47` |
| 9 | `clay_roof_tiles_02_nor_gl_2k` | 1024x1024 | 228 353 | `fd3d1ab00d802cf3` | `9` |
| 10 | `clay_roof_tiles_02_diff_2k` | 1024x1024 | 207 755 | `9502307fcd37fc10` | `10` |
| 11 | `clay_roof_tiles_02_rough_2k` | 1024x1024 | 38 061 | `410ecf3e8d6aee2d` | `11` |
| 12 | `asphalt_01_nor_gl_2k` | 1024x1024 | 310 248 | `70df03088ac8ed71` | `12 33` |
| 13 | `asphalt_01_diff_2k` | 1024x1024 | 153 146 | `9fcaa1ac8af9640d` | `13 34` |
| 14 | `asphalt_01_rough_2k` | 1024x1024 | 9 703 | `6fcc9484b8585943` | `14 35` |
| 15 | `leafy_grass_nor_gl_2k` | 1024x1024 | 420 868 | `0ec8f3e81a54821d` | `15` |
| 16 | `leafy_grass_diff_2k` | 1024x1024 | 317 207 | `7a578aa344ea7765` | `16` |
| 17 | `leafy_grass_rough_2k` | 1024x1024 | 36 745 | `69e238ae6d6cde70` | `17` |
| 18 | `american_walnut_veneer_nor_gl_2k` | 512x512 | 4 589 | `c5cac9489e32048f` | `18 24` |
| 19 | `american_walnut_veneer_diff_2k` | 512x512 | 17 354 | `64120ac69ee8d223` | `19 25` |
| 20 | `american_walnut_veneer_rough_2k` | 512x512 | 21 580 | `e97fda2c69d0b19f` | `20 26` |
| 21 | `gravel_nor_gl_2k` | 1024x1024 | 459 912 | `f7faae5e88930158` | `30` |
| 22 | `gravel_diff_2k` | 1024x1024 | 219 000 | `c05cec2e982f60ad` | `31` |
| 23 | `gravel_rough_2k` | 1024x1024 | 27 346 | `094c2bb004487945` | `32` |
| 24 | `cotton_jersey_nor_gl_2k` | 512x512 | 2 939 | `ea1c4d0a0fc404f4` | `36` |
| 25 | `cotton_jersey_diff_2k` | 512x512 | 5 118 | `12963d734036f587` | `37` |
| 26 | `cotton_jersey_rough_2k` | 512x512 | 14 427 | `2971701b47ee6fc6` | `38` |
| 27 | `white_oak_veneer_nor_gl_2k` | 512x512 | 9 632 | `c7f9ca6082052ce7` | `39` |
| 28 | `white_oak_veneer_diff_2k` | 512x512 | 19 124 | `11460ae4b7a2aaf1` | `40` |
| 29 | `white_oak_veneer_rough_2k` | 512x512 | 8 926 | `16628ab8f1ef1873` | `41` |
| 30 | `modern_coffee_table_01_nor_gl_1k` | 512x512 | 5 644 | `3a8a7642e80609a1` | `48` |
| 31 | `modern_coffee_table_01_diff_1k` | 512x512 | 15 246 | `c95ddba2c8c6c0a0` | `49` |
| 32 | `potted_plant_04_nor_gl_1k` | 512x512 | 45 157 | `76fef641f14af96d` | `51` |
| 33 | `potted_plant_04_diff_1k` | 512x512 | 36 667 | `c9731673dae7154e` | `52` |
| 34 | `potted_plant_04_arm_1k` | 512x512 | 23 605 | `35ad7645df41409e` | `53` |
| 35 | `v17_foliage_deep` | 256x256 | 5 169 | `c3c854235854d645` | `54` |
| 36 | `v17_foliage_fresh` | 256x256 | 5 696 | `93b8e0df8d07e1d3` | `55` |

> Les suffixes historiques `_2k` et `_1k` dans les noms ne décrivent plus toujours la résolution livrée : la plupart des `_2k` intérieurs sont réellement en 512²; seuls toit, asphalte, gazon et gravier sont en 1024². Les deux feuillages V17 ne font que 256².

## Résolution des slots matériaux vers les images

| Matériau | Base color | Metallic/Roughness | Normal | Autres |
|---|---|---|---|---|
| 2 `V12_PBR_OFFWHITE_STUCCO` | t1→i1 `white_stucco_diff_2k`; UV scale=[3, 3], offset=[0, -2] | t2→i2 `white_stucco_rough_2k`; UV scale=[3, 3], offset=[0, -2] | t0→i0 `white_stucco_nor_gl_2k`; UV scale=[3, 3], offset=[0, -2]; strength=0.1599999964237213 | — |
| 3 `PBR_B_FLOOR` | t4→i4 `floor_tiles_02_diff_2k`; UV scale=[4.199999809265137, 4.199999809265137], offset=[0, -3.1999998092651367] | t5→i5 `floor_tiles_02_rough_2k`; UV scale=[4.199999809265137, 4.199999809265137], offset=[0, -3.1999998092651367] | t3→i3 `floor_tiles_02_nor_gl_2k`; UV scale=[4.199999809265137, 4.199999809265137], offset=[0, -3.1999998092651367]; strength=0.550000011920929 | — |
| 5 `PBR_B_CONCRETE` | t7→i7 `brushed_concrete_04_diff_2k`; UV scale=[5, 5], offset=[0, -4] | t8→i8 `brushed_concrete_04_rough_2k`; UV scale=[5, 5], offset=[0, -4] | t6→i6 `brushed_concrete_04_nor_gl_2k`; UV scale=[5, 5], offset=[0, -4]; strength=0.6000000238418579 | — |
| 6 `PBR_B_ROOF` | t10→i10 `clay_roof_tiles_02_diff_2k`; UV scale=[3.5999999046325684, 3.5999999046325684], offset=[0, -2.5999999046325684] | t11→i11 `clay_roof_tiles_02_rough_2k`; UV scale=[3.5999999046325684, 3.5999999046325684], offset=[0, -2.5999999046325684] | t9→i9 `clay_roof_tiles_02_nor_gl_2k`; UV scale=[3.5999999046325684, 3.5999999046325684], offset=[0, -2.5999999046325684]; strength=1.149999976158142 | — |
| 7 `PBR_B_ASPHALT` | t13→i13 `asphalt_01_diff_2k`; UV scale=[9, 9], offset=[0, -8] | t14→i14 `asphalt_01_rough_2k`; UV scale=[9, 9], offset=[0, -8] | t12→i12 `asphalt_01_nor_gl_2k`; UV scale=[9, 9], offset=[0, -8]; strength=0.8500000238418579 | — |
| 8 `PBR_B_GRASS` | t16→i16 `leafy_grass_diff_2k`; UV scale=[8, 8], offset=[0, -7] | t17→i17 `leafy_grass_rough_2k`; UV scale=[8, 8], offset=[0, -7] | t15→i15 `leafy_grass_nor_gl_2k`; UV scale=[8, 8], offset=[0, -7]; strength=0.800000011920929 | — |
| 9 `PBR_B_WOOD` | t19→i19 `american_walnut_veneer_diff_2k`; UV scale=[2, 5], offset=[0, -4] | t20→i20 `american_walnut_veneer_rough_2k`; UV scale=[2, 5], offset=[0, -4] | t18→i18 `american_walnut_veneer_nor_gl_2k`; UV scale=[2, 5], offset=[0, -4]; strength=0.5799999833106995 | — |
| 10 `V10_BRUSHED_CONCRETE` | t22→i7 `brushed_concrete_04_diff_2k`; UV scale=[5, 5], offset=[0, -4] | t23→i8 `brushed_concrete_04_rough_2k`; UV scale=[5, 5], offset=[0, -4] | t21→i6 `brushed_concrete_04_nor_gl_2k`; UV scale=[5, 5], offset=[0, -4]; strength=0.36000001430511475 | — |
| 14 `V10_ENTRY_WOOD` | t25→i19 `american_walnut_veneer_diff_2k`; UV scale=[7, 7], offset=[0, -6] | t26→i20 `american_walnut_veneer_rough_2k`; UV scale=[7, 7], offset=[0, -6] | t24→i18 `american_walnut_veneer_nor_gl_2k`; UV scale=[7, 7], offset=[0, -6]; strength=0.2800000011920929 | — |
| 15 `V10_STUCCO_NEW_BUILD` | t28→i1 `white_stucco_diff_2k`; UV scale=[6, 6], offset=[0, -5] | t29→i2 `white_stucco_rough_2k`; UV scale=[6, 6], offset=[0, -5] | t27→i0 `white_stucco_nor_gl_2k`; UV scale=[6, 6], offset=[0, -5]; strength=0.23999999463558197 | — |
| 17 `V10_GRAVEL` | t31→i22 `gravel_diff_2k`; UV scale=[6, 6], offset=[0, -5] | t32→i23 `gravel_rough_2k`; UV scale=[6, 6], offset=[0, -5] | t30→i21 `gravel_nor_gl_2k`; UV scale=[6, 6], offset=[0, -5]; strength=0.5 | — |
| 19 `V10_ASPHALT` | t34→i13 `asphalt_01_diff_2k`; UV scale=[5, 5], offset=[0, -4] | t35→i14 `asphalt_01_rough_2k`; UV scale=[5, 5], offset=[0, -4] | t33→i12 `asphalt_01_nor_gl_2k`; UV scale=[5, 5], offset=[0, -4]; strength=0.4000000059604645 | — |
| 21 `V12_PBR_BEIGE_COTTON` | t37→i25 `cotton_jersey_diff_2k`; UV scale=[7, 7], offset=[0, -6] | t38→i26 `cotton_jersey_rough_2k`; UV scale=[7, 7], offset=[0, -6] | t36→i24 `cotton_jersey_nor_gl_2k`; UV scale=[7, 7], offset=[0, -6]; strength=0.3499999940395355 | — |
| 22 `V12_PBR_WHITE_OAK` | t40→i28 `white_oak_veneer_diff_2k`; UV scale=[3, 3], offset=[0, -2] | t41→i29 `white_oak_veneer_rough_2k`; UV scale=[3, 3], offset=[0, -2] | t39→i27 `white_oak_veneer_nor_gl_2k`; UV scale=[3, 3], offset=[0, -2]; strength=0.25999999046325684 | — |
| 25 `V12_PBR_LIGHT_PORCELAIN` | t43→i4 `floor_tiles_02_diff_2k`; UV scale=[9, 9], offset=[0, -8] | t44→i5 `floor_tiles_02_rough_2k`; UV scale=[9, 9], offset=[0, -8] | t42→i3 `floor_tiles_02_nor_gl_2k`; UV scale=[9, 9], offset=[0, -8]; strength=0.2199999988079071 | — |
| 28 `V12_PBR_BRUSHED_CONCRETE` | t46→i7 `brushed_concrete_04_diff_2k`; UV scale=[4, 4], offset=[0, -3] | t47→i8 `brushed_concrete_04_rough_2k`; UV scale=[4, 4], offset=[0, -3] | t45→i6 `brushed_concrete_04_nor_gl_2k`; UV scale=[4, 4], offset=[0, -3]; strength=0.18000000715255737 | — |
| 31 `modern_coffee_table_01.001` | t49→i31 `modern_coffee_table_01_diff_1k` | — | t48→i30 `modern_coffee_table_01_nor_gl_1k` | — |
| 32 `potted_plant_04` | t52→i33 `potted_plant_04_diff_1k` | t53→i34 `potted_plant_04_arm_1k` | t51→i32 `potted_plant_04_nor_gl_1k` | — |
| 33 `V17_PBR_FOLIAGE_DEEP` | t54→i35 `v17_foliage_deep` | — | — | — |
| 34 `V17_PBR_FOLIAGE_FRESH` | t55→i36 `v17_foliage_fresh` | — | — | — |

## Sampler et canaux absents

- Sampler unique : `magFilter=9729` (LINEAR), `minFilter=9987` (LINEAR_MIPMAP_LINEAR); `wrapS`/`wrapT` omis, donc valeur glTF par défaut REPEAT.
- Aucun matériau n’utilise `occlusionTexture` ni `emissiveTexture`. Les sets appelés PBR sont essentiellement base color + roughness/metallic + normal; le coffee table n’a que base color + normal; les feuillages n’ont que base color.
- Les JPEG sont avec pertes et sans alpha. Les matériaux de feuillage V17 sont `OPAQUE`; les arbres/haies ne peuvent donc pas obtenir des silhouettes de feuilles par cutout alpha à partir de ces deux images.

## Images WebP du site ≠ textures 3D

- Le worktree contient **14 WebP autonomes** (`images/`, `shared/gallery/`, `shared/preview.webp`). Ils ne sont pas référencés par le JSON du GLB.
- `shared/preview.webp` sert uniquement au fond de chargement CSS. Les fichiers `shared/gallery/*.webp` et `images/*.webp` sont des rendus raster présentés par la galerie/README.
- Par conséquent, les « belles images » de galerie ne constituent pas des maps appliquées à la maison interactive. Leur éclairage, post-traitement et ombres déjà calculés ne sont pas transférés au viewer en chargeant le GLB. Le nouveau viewer ajoute une IBL PMREM procédurale, mais elle ne recrée pas exactement le moteur ni le décor lumineux des rendus de galerie.

## Limites

- Cette analyse prouve l’intégration binaire, les dimensions et les liaisons glTF. Elle ne mesure pas la fidélité colorimétrique de chaque JPEG ni la qualité visuelle finale sous tous les GPU.
- La présence d’UV sur chaque primitive ne garantit pas une bonne densité texel, l’absence d’étirement ou une orientation artistique correcte; une inspection rendue est requise pour cela.
