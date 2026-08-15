# Matériaux réellement chargés par les viewers V18

## Chaîne live vérifiée

- `shared/project-config.json` est la source de vérité : `version=V18`, `release=V18-LIVE-SYNC-3`, `model=./Chamagnieu_V18_REALISM_FINAL.glb`, SHA-256 attendu `79A0F908…D58C28`, 27 987 896 octets.
- `presentation/presentation.js` et `visite/visite.js` chargent la configuration, résolvent `config.model`, puis ajoutent `?release=v18-live-sync-3`. Les deux pages utilisent donc le même alias live.
- Après chargement, `tuneLiveModel()` conserve les maps du GLB, active l’anisotropie jusqu’à `min(8, capacité GPU)`, marque les matériaux à mettre à jour et règle `envMapIntensity` à 0,90 pour les noms GLASS/WINDOW/METAL, 0,55 sinon. **Aucune texture n’est remplacée par une image de galerie.**
- `setupLiveLighting()` applique sRGB, ACES Filmic, exposition **0,92**, une IBL PMREM générée depuis un ciel Canvas procédural, HemisphereLight **0,72**, AmbientLight **0,06**, DirectionalLight **2,4** et fill light **0,22**.
- Sur desktop : PCFSoftShadowMap et shadow map 2048. Sur mobile : ombres désactivées et pixel ratio plafonné à 1,1; les JPEG restent chargés, mais la profondeur perçue diminue.
- L’ajout PMREM/anisotropy corrige objectivement deux causes d’un rendu plat (aucune IBL et filtrage oblique par défaut). La PMREM reste néanmoins un gradient procédural 512×256, pas une HDRI photographique D5/Blender; elle améliore métaux/verres sans garantir une correspondance exacte aux images de galerie.

## Couverture matérielle

- **20/35 matériaux** ont au moins un slot texture; **15/35** reposent uniquement sur des facteurs/couleurs PBR.
- Matériaux texturés : **501/795 primitives (63.0%)** et **266 905/316 781 triangles (84.3%)**.
- Matériaux couleur/facteur seuls : **294 primitives** et **49 876 triangles**.
- Tous les **35 matériaux** sont `doubleSided=true`; cela réduit les trous par winding, mais peut rendre visibles des faces internes et ne remplace pas une épaisseur géométrique correcte.

## Toggle mobilier — preuve structurelle release 3 et preuve navigateur release 2

- Le classifieur final couvre les préfixes mobilier **V11 et V12** et propage `isFurnitureTree` du parent vers tous ses descendants. Le JSON glTF contient **167 nœuds nommés candidats mobilier**, totalisant **219 319 triangles**.
- Structure statique exacte : **165 nœuds mono-primitifs** deviennent chacun un `Mesh`; `V11_LIVING_ARMCHAIR` et `V12_LIVING_ARMCHAIR_2` ont chacun **2 primitives** et deviennent chacun un `Group` avec 2 enfants `Mesh`. Le runtime contient donc **165 + 2 + 2 = 169 meshes mobilier**.
- La propagation parent→enfants couvre les quatre enfants aux noms génériques `Cube639`, `Cube639_1`, `Cube100`, `Cube100_1`. Les deux fauteuils multi-primitives ne restent plus hors du toggle.

```text
FURNITURE_CLASSIFIER_STATIC_RESULT=PASS named_nodes=167 runtime_meshes=169 multi_primitive_nodes=[V11_LIVING_ARMCHAIR:2,V12_LIVING_ARMCHAIR_2:2] inherited_child_classification=true
```

- Le dernier test Chromium effectivement capturé porte sur `V18-LIVE-SYNC-2` : `/presentation/` et `/visite/` exposaient chacun 165 meshes directs, suivaient `true > false > true` et ne produisaient aucune erreur console. Ce test a précisément révélé les deux groupes multi-primitives non propagés.
- La release 3 corrige ce cas dans le code, passe la syntaxe des deux modules, et son parsing structurel compte 169 meshes couverts. Aucune preuve navigateur release 3 n'est attribuée à ce rapport.

```text
FURNITURE_TOGGLE_BROWSER_RESULT=PASS paths=2 runtime_meshes_each=165 state_sequence=true>false>true release=V18-LIVE-SYNC-2 console_errors=0
FURNITURE_RELEASE3_STATIC_RESULT=PASS named_nodes=167 runtime_meshes=169 multi_primitive_nodes=2 inherited_child_classification=true module_syntax=true
```

- Portée exacte release 3 : les **167 nœuds glTF nommés** produisent **169 meshes runtime**, que l’algorithme classe tous dans l’arbre mobilier. La séquence de clic réelle est prouvée sur les 165 meshes directs de release 2; la couverture des quatre enfants supplémentaires est prouvée structurellement par propagation parent→enfants.

## Tableau exhaustif des 35 matériaux

| # | Matériau | Primitives / triangles | Slots images | Mode / extensions | Exemples de nœuds |
|---:|---|---:|---|---|---|
| 0 | `AUDIT_OPENING_GREEN` | 1 / 92 | facteurs seulement | OPAQUE; — | `BLENDER_NORTH_REFERENCE` |
| 1 | `MAT_B_ALU` | 32 / 3 456 | facteurs seulement | OPAQUE; — | `FRAME_GF_W_BAY_1_REFERENCE_B`  `FRAME_GF_W_BAY_1_REFERENCE_L`  `FRAME_GF_W_BAY_1_REFERENCE_R` |
| 2 | `V12_PBR_OFFWHITE_STUCCO` | 62 / 3 720 | BC: t1→`white_stucco_diff_2k`; MR: t2→`white_stucco_rough_2k`; N: t0→`white_stucco_nor_gl_2k` | OPAQUE; — | `GF_EXT_EAST_00_DIRECT`  `GF_EXT_NORTH_00_DIRECT`  `GF_EXT_NORTH_01_DIRECT` |
| 3 | `PBR_B_FLOOR` | 17 / 220 | BC: t4→`floor_tiles_02_diff_2k`; MR: t5→`floor_tiles_02_rough_2k`; N: t3→`floor_tiles_02_nor_gl_2k` | OPAQUE; — | `GF_ROOM_CELLAR`  `GF_ROOM_ENTRY`  `GF_ROOM_LIVING` |
| 4 | `MAT_B_GLASS` | 16 / 192 | facteurs seulement | BLEND; KHR_materials_transmission | `GF_W_BAY_1_REFERENCE`  `GF_W_BAY_2_REFERENCE`  `GF_W_NORTH_1_REFERENCE_CORRECTED` |
| 5 | `PBR_B_CONCRETE` | 1 / 108 | BC: t7→`brushed_concrete_04_diff_2k`; MR: t8→`brushed_concrete_04_rough_2k`; N: t6→`brushed_concrete_04_nor_gl_2k` | OPAQUE; — | `GROUND_TERRACE_GARDEN` |
| 6 | `PBR_B_ROOF` | 234 / 43 446 | BC: t10→`clay_roof_tiles_02_diff_2k`; MR: t11→`clay_roof_tiles_02_rough_2k`; N: t9→`clay_roof_tiles_02_nor_gl_2k` | OPAQUE; — | `ROOF_FRONT_WING_AUDITED`  `ROOF_GARAGE_AUDITED`  `ROOF_MAIN_AUDITED` |
| 7 | `PBR_B_ASPHALT` | 1 / 24 | BC: t13→`asphalt_01_diff_2k`; MR: t14→`asphalt_01_rough_2k`; N: t12→`asphalt_01_nor_gl_2k` | OPAQUE; — | `SITE_ACCESS_AUDITED` |
| 8 | `PBR_B_GRASS` | 2 / 76 | BC: t16→`leafy_grass_diff_2k`; MR: t17→`leafy_grass_rough_2k`; N: t15→`leafy_grass_nor_gl_2k` | OPAQUE; — | `SITE_PARCEL_L6_AUDITED`  `V18_SITE_GROUND_VISIBLE` |
| 9 | `PBR_B_WOOD` | 37 / 3 852 | BC: t19→`american_walnut_veneer_diff_2k`; MR: t20→`american_walnut_veneer_rough_2k`; N: t18→`american_walnut_veneer_nor_gl_2k` | OPAQUE; — | `UF_D_BED1_LINTEL`  `UF_D_BED2_LINTEL`  `UF_D_BED3_LINTEL` |
| 10 | `V10_BRUSHED_CONCRETE` | 11 / 2 068 | BC: t22→`brushed_concrete_04_diff_2k`; MR: t23→`brushed_concrete_04_rough_2k`; N: t21→`brushed_concrete_04_nor_gl_2k` | OPAQUE; — | `V10_ACCESS_KERB_0`  `V10_ACCESS_KERB_1`  `V10_ENTRY_PAVER_00` |
| 11 | `V10_ANTHRACITE` | 77 / 11 228 | facteurs seulement | OPAQUE; — | `V10_DOWNPIPE_0`  `V10_DOWNPIPE_1`  `V10_DOWNPIPE_2` |
| 12 | `V10_RUBBER_GASKET` | 19 / 3 572 | facteurs seulement | OPAQUE; — | `V10_ENTRY_GASKET_L`  `V10_ENTRY_GASKET_R`  `V10_ENTRY_PANEL_JOINT_0` |
| 13 | `V10_BRUSHED_CHROME` | 35 / 6 044 | facteurs seulement | OPAQUE; — | `V10_ENTRY_HANDLE`  `V10_ENTRY_LOCK`  `V10_WINDOW_HANDLE` |
| 14 | `V10_ENTRY_WOOD` | 1 / 188 | BC: t25→`american_walnut_veneer_diff_2k`; MR: t26→`american_walnut_veneer_rough_2k`; N: t24→`american_walnut_veneer_nor_gl_2k` | OPAQUE; — | `V10_ENTRY_LEAF` |
| 15 | `V10_STUCCO_NEW_BUILD` | 7 / 1 316 | BC: t28→`white_stucco_diff_2k`; MR: t29→`white_stucco_rough_2k`; N: t27→`white_stucco_nor_gl_2k` | OPAQUE; — | `V10_ENTRY_REVEAL_L`  `V10_ENTRY_REVEAL_R`  `V10_ENTRY_REVEAL_T` |
| 16 | `V10_SILL_STONE` | 8 / 1 504 | facteurs seulement | OPAQUE; — | `V10_ENTRY_THRESHOLD`  `V10_GARAGE_THRESHOLD`  `V10_WINDOW_SILL_EXT` |
| 17 | `V10_GRAVEL` | 3 / 660 | BC: t31→`gravel_diff_2k`; MR: t32→`gravel_rough_2k`; N: t30→`gravel_nor_gl_2k` | OPAQUE; — | `V10_FACADE_DRAIN_MAIN`  `V10_FACADE_DRAIN_RIGHT`  `V10_FRONT_ACCESS_GRAVEL_BAND` |
| 18 | `V10_SOFFIT` | 10 / 1 880 | facteurs seulement | OPAQUE; — | `V10_FACADE_PLINTH_0`  `V10_FACADE_PLINTH_1`  `V10_FACADE_PLINTH_2` |
| 19 | `V10_ASPHALT` | 1 / 284 | BC: t34→`asphalt_01_diff_2k`; MR: t35→`asphalt_01_rough_2k`; N: t33→`asphalt_01_nor_gl_2k` | OPAQUE; — | `V10_FRONT_ACCESS_ASPHALT` |
| 20 | `V10_PHYSICAL_GLASS` | 5 / 940 | facteurs seulement | OPAQUE; KHR_materials_transmission  KHR_materials_ior | `V10_WINDOW_GLAZING`  `V11_KITCHEN_OVEN_GLASS`  `V11_LIVING_TV_SCREEN` |
| 21 | `V12_PBR_BEIGE_COTTON` | 34 / 146 458 | BC: t37→`cotton_jersey_diff_2k`; MR: t38→`cotton_jersey_rough_2k`; N: t36→`cotton_jersey_nor_gl_2k` | OPAQUE; — | `V11_BEDROOM1_BED_BASE`  `V11_BEDROOM1_BED_DUVET`  `V11_BEDROOM1_BED_MATTRESS` |
| 22 | `V12_PBR_WHITE_OAK` | 43 / 42 432 | BC: t40→`white_oak_veneer_diff_2k`; MR: t41→`white_oak_veneer_rough_2k`; N: t39→`white_oak_veneer_nor_gl_2k` | OPAQUE; — | `V11_BEDROOM1_BED_HEAD`  `V11_BEDROOM1_NIGHT_L`  `V11_BEDROOM1_NIGHT_R` |
| 23 | `MAT_B_WHITE` | 62 / 15 516 | facteurs seulement | OPAQUE; — | `V11_DOOR_GF_CELLAR_FRAME_L`  `V11_DOOR_GF_CELLAR_FRAME_R`  `V11_DOOR_GF_CELLAR_FRAME_T` |
| 24 | `V11_COUNTER_STONE` | 9 / 1 692 | facteurs seulement | OPAQUE; — | `V11_DOOR_GF_CELLAR_THRESHOLD`  `V11_DOOR_GF_WC_THRESHOLD`  `V11_DOOR_UF_BED1_THRESHOLD` |
| 25 | `V12_PBR_LIGHT_PORCELAIN` | 5 / 940 | BC: t43→`floor_tiles_02_diff_2k`; MR: t44→`floor_tiles_02_rough_2k`; N: t42→`floor_tiles_02_nor_gl_2k` | OPAQUE; — | `V11_GF_FINISH_TILE`  `V11_KITCHEN_BACKSPLASH`  `V11_UF_TILE_SDB_N` |
| 26 | `V12_WARM_WHITE_LACQUER` | 5 / 940 | facteurs seulement | OPAQUE; — | `V11_GF_WC_BASIN_BASE`  `V11_SDB_N_SHOWER_TRAY`  `V11_SDB_N_VANITY_BASE` |
| 27 | `V11_MIRROR` | 3 / 564 | facteurs seulement | OPAQUE; — | `V11_GF_WC_BASIN_MIRROR`  `V11_SDB_N_VANITY_MIRROR`  `V11_SDB_S_VANITY_MIRROR` |
| 28 | `V12_PBR_BRUSHED_CONCRETE` | 6 / 1 128 | BC: t46→`brushed_concrete_04_diff_2k`; MR: t47→`brushed_concrete_04_rough_2k`; N: t45→`brushed_concrete_04_nor_gl_2k` | OPAQUE; — | `V11_GF_WC_BASIN_TOP`  `V11_KITCHEN_ISLAND_TOP`  `V11_KITCHEN_RUN_LEFT_TOP` |
| 29 | `V11_APPLIANCE_BLACK` | 4 / 752 | facteurs seulement | OPAQUE; — | `V11_KITCHEN_COOKTOP`  `V11_KITCHEN_PENDANT_1`  `V11_KITCHEN_PENDANT_2` |
| 30 | `V12_KITCHEN_GREIGE` | 8 / 1 504 | facteurs seulement | OPAQUE; — | `V11_KITCHEN_ISLAND_BODY`  `V11_KITCHEN_OVEN_FRONT`  `V11_KITCHEN_RUN_LEFT_BODY` |
| 31 | `modern_coffee_table_01.001` | 1 / 4 504 | BC: t49→`modern_coffee_table_01_diff_1k`; N: t48→`modern_coffee_table_01_nor_gl_1k` | OPAQUE; — | `V11_LIVING_COFFEE_TABLE` |
| 32 | `potted_plant_04` | 1 / 8 929 | BC: t52→`potted_plant_04_diff_1k`; MR: t53→`potted_plant_04_arm_1k`; N: t51→`potted_plant_04_nor_gl_1k` | OPAQUE; — | `V11_LIVING_PLANT` |
| 33 | `V17_PBR_FOLIAGE_DEEP` | 20 / 3 600 | BC: t54→`v17_foliage_deep` | OPAQUE; — | `V17_HEDGE_LIGHT_01`  `V17_HEDGE_LIGHT_02`  `V17_HEDGE_LIGHT_04` |
| 34 | `V17_PBR_FOLIAGE_FRESH` | 14 / 2 952 | BC: t55→`v17_foliage_fresh` | OPAQUE; — | `V17_HEDGE_LIGHT_03`  `V17_HEDGE_LIGHT_06`  `V17_HEDGE_LIGHT_09` |

## Assets de mobilier à provenance explicite

| Nœud | Source déclarée | Triangles | Matériau(x) | Lecture |
|---|---|---:|---|---|
| `V11_DINING_CHAIR_01` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_DINING_CHAIR_02` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_DINING_CHAIR_03` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_DINING_CHAIR_04` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_DINING_CHAIR_05` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_DINING_CHAIR_06` | `Poly Haven CC0/dining_chair_02` | 22 013 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_LIVING_ARMCHAIR` | `Poly Haven CC0/modern_arm_chair_01` | 8 916 | `V12_PBR_WHITE_OAK`  `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_LIVING_COFFEE_TABLE` | `Poly Haven CC0/modern_coffee_table_01` | 4 504 | `modern_coffee_table_01.001` | asset détaillé/sourcé |
| `V11_LIVING_PLANT` | `Poly Haven CC0/potted_plant_04` | 8 929 | `potted_plant_04` | asset détaillé/sourcé |
| `V11_LIVING_SOFA` | `Poly Haven CC0/sofa_02` | 2 728 | `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |
| `V11_LIVING_TV_CONSOLE` | `Poly Haven CC0/modern_wooden_cabinet` | 24 976 | `V12_PBR_WHITE_OAK` | asset détaillé/sourcé |
| `V12_LIVING_ARMCHAIR_2` | `Poly Haven CC0/modern_arm_chair_01` | 8 916 | `V12_PBR_WHITE_OAK`  `V12_PBR_BEIGE_COTTON` | asset détaillé/sourcé |

- Total haute définition sourcé : **12 nœuds / 191 047 triangles**, soit **87,1 % des triangles du sous-ensemble mobilier** et 60,3 % du GLB complet. Sources déclarées : 6 × `Poly Haven CC0/dining_chair_02`, 2 × `modern_arm_chair_01`, puis 1 × `modern_coffee_table_01`, `potted_plant_04`, `sofa_02` et `modern_wooden_cabinet`.
- Mobilier procédural/non sourcé : **155 nœuds / 28 272 triangles**, soit 12,9 % des triangles du sous-ensemble mobilier. Il regroupe cuisine, lits, rangements, sanitaires, table V12 et bar stools construits majoritairement à partir de signatures répétées 44/60/68/76/188/300/960 triangles.
- Les 12 nœuds avec `asset_source` sont les candidats les plus solides à « mobilier réaliste » : provenance explicite, topologie nettement plus détaillée et matériaux PBR texturés. Les 155 autres ne sont pas nécessairement incorrects, mais leur répétition topologique justifie la qualification procédurale/placeholder-like.

## Géométrie procédurale / placeholder-like et végétation

- **495 nœuds ont exactement 188 triangles**, signature répétée des volumes arrondis/procéduraux. Cuisine V11 : **33 nœuds / 5 260 triangles**; mobilier de chambres V11 : **47 / 6 148**; table V12 : **5 / 668**; trois bar stools V12 : **21 / 2 268**. Ils possèdent des dimensions fonctionnelles et parfois un matériau PBR, mais leur topologie répétitive explique l’aspect « bloc » plus que l’absence de fichiers texture.
- Toitures principales : `ROOF_FRONT_WING_AUDITED`, `ROOF_GARAGE_AUDITED`, `ROOF_MAIN_AUDITED` ont chacune **14 vertices / 6 triangles**. Elles utilisent bien le set `PBR_B_ROOF` 1024² (base color + roughness + normal), mais le volume principal reste un plan de toiture très peu subdivisé; le relief des tuiles vient donc surtout de la normal map et des éléments de rive séparés.
- Sols : `SITE_ACCESS_AUDITED` **24 triangles** avec asphalte PBR, `SITE_PARCEL_L6_AUDITED` **64** avec gazon PBR, `GROUND_TERRACE_GARDEN` **108** avec béton PBR, `V18_SITE_GROUND_VISIBLE` **12** avec gazon PBR. Les maps existent, mais les surfaces sont géométriquement simples.
- Végétation extérieure : le GLB et `project-config.json` concordent sur **18 haies / 1 944 triangles** et **4 arbres composés de 28 nœuds** (16 canopées / 4 608 triangles, 8 branches / 288, 4 troncs / 208). Les canopées/haies utilisent deux JPEG 256² base-color-only, `OPAQUE`, sans alpha/normal/roughness; c’est une végétation stylisée low-poly, pas un asset botanique photoréaliste.
- La plante de salon est différente : asset `potted_plant_04`, **8 929 triangles**, avec base color + normal + ARM. Elle est techniquement bien plus détaillée que les arbres V17.

## Pourquoi les textures peuvent sembler absentes alors qu’elles sont présentes

1. **Le GLB contient bien les maps** : 37 images embarquées, 55 objets texture utilisés, UV sur 795/795 primitives. Un problème de chemin externe n’explique pas le rendu live.
2. **Les images de galerie ne sont pas les textures du GLB** : ce sont des rendus 2D séparés, avec éclairage/post-traitement déjà calculés.
3. **15 matériaux restent plats** : notamment alu, verre, anthracite, chrome, pierre de seuil, soffite, blanc, counter stone, lacquer, mirror, appliance black et kitchen greige. Ils ont uniquement couleur/metallic/roughness, donc aucun grain local.
4. **Éclairage live différent du moteur de rendu** : le viewer final possède maintenant une IBL PMREM et une ambiance réduite, mais son ciel est un gradient Canvas et non la HDRI/scène lumineuse D5/Blender; la correspondance reste donc approximative.
5. **Géométrie simplifiée** : toiture, sols, cuisine et mobilier procédural restent peu détaillés même avec de bonnes maps; une texture ne transforme pas une silhouette cubique en asset réaliste.
6. **Qualité mobile réduite** : ombres coupées et ratio de pixels limité; cela affecte la profondeur perçue, sans supprimer les JPEG embarqués.
7. **Correctifs runtime maintenant présents** : anisotropie, environnement PMREM, lumière ambiante abaissée et cache/version centralisé rendent les maps plus lisibles; ils ne changent toutefois ni la topologie low-poly ni les 15 matériaux couleur-seulement.

## Statut de réalisme

`REALISM_STATUS=PARTIAL`

- **Présent et fonctionnel :** GLB unique synchronisé, 37 images embarquées, 20 matériaux texturés, anisotropie 8 sur le GPU de test, IBL PMREM, ombres desktop, 12 assets détaillés sourcés, 4 arbres et 18 haies; séquence du toggle prouvée en release 2 et couverture des 169 meshes démontrée structurellement en release 3.
- **Encore partiel :** 15 matériaux couleur-seulement, 155 nœuds de mobilier procéduraux, 495 nœuds partageant la signature 188 triangles, trois pans principaux de toiture à 6 triangles chacun, feuillages 256² opaques base-color-only, environnement Canvas plutôt que HDRI. `environmentIntensity=0.55` est déclaré dans la configuration mais n’est pas appliqué à `scene.environmentIntensity` par `setupLiveLighting()`; l’intensité effective est pilotée ici par `material.envMapIntensity` (0,90/0,55).
- Les rendus Blender de galerie restent des références 2D distinctes; le viewer Web amélioré ne constitue pas une reproduction pixel-identique de Blender/D5.

## Contrôle de dérive documentaire

Les trois audits finaux doivent décrire exclusivement `V18-LIVE-SYNC-3`. Les valeurs live finales sont : exposition 0,92; hemisphere 0,72; ambient 0,06; directional 2,4; fill 0,22; `environmentIntensity=0.55` déclaré mais non consommé; envMapIntensity 0,90 pour verre/métal et 0,55 sinon.

```text
FINAL_AUDIT_TOKEN_SCAN_RESULT=PASS files=3 release_1_tokens=0 old_lighting_phrases=0 release=V18-LIVE-SYNC-3
```

## Limites

- « Placeholder » est ici une classification prudente fondée sur provenance, répétition topologique, complexité et slots PBR; elle ne déclare pas qu’un objet est inutilisable ni qu’un asset très polygonal est automatiquement beau.
- L’audit ne remplace pas une comparaison visuelle synchronisée (même caméra, même exposition, même GPU) entre Blender/D5 et le viewer Three.js.
- Les images JPEG intégrées ont été comptées et décodées, mais aucune analyse perceptuelle automatisée de leur contenu (contraste, répétition, gamut) n’a été utilisée pour classer leur qualité.
