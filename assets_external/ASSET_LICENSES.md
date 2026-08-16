# Registre des licences — pilote d’assets réalistes Chamagnieu V18

**État du registre :** `LIVE_VALIDATED_LOCAL`
**Release documentée :** `V18-ASSET-PILOT-1`
**Périmètre :** huit catégories obligatoires — canapé, table, chaise, lit, arbre, haie, façade PBR et gazon PBR.
**Usage :** visualisation Web du logement; aucune modification de l’architecture contractuelle.

Le détail fichier par fichier (chemin, octets et SHA-256) est conservé dans `assets_external/ASSET_MANIFEST.json`. Les crédits ci-dessous sont conservés même lorsque CC0 ne les impose pas.

## Règle de sélection appliquée

- Sources retenues : **Poly Haven CC0**, **BlenderKit uniquement lorsque l’API officielle indique `cc_zero`**, **ambientCG CC0**.
- Sources écartées : offre premium/Full Plan, asset « Royalty Free » dont le GLB public serait extractible, licence ou droits tiers ambigus.
- Les fichiers sources restent sous `original/`; les dérivés Web restent sous `optimized/`.
- Aucun asset payant, copié illicitement ou à licence indéterminée n’est intégré.

Pages officielles de référence :

- Poly Haven : https://polyhaven.com/license
- BlenderKit : https://www.blendkit.com/docs/licenses/
- FAQ de licence BlenderKit : https://www.blendkit.com/docs/licenses/licensing-faq/
- ambientCG : https://docs.ambientcg.com/license/

## Assets intégrés et crédits

| Catégorie | Asset / auteur | Source officielle | Licence retenue | Original local de référence | Dérivé Web / SHA-256 | Emploi réel |
|---|---|---|---|---|---|---|
| Canapé | **Leather Sofa** — Muhammed Ismayil | https://www.blendkit.com/asset-gallery-detail/4faac4b8-cc88-4ff2-b7fd-a7edf46d3518/ | CC0-1.0 (`cc_zero`) | `assets_external/furniture/living/sofa/original/sofa_4faac4b8-cc88-4ff2-b7fd-a7edf46d3518_library.glb` | `assets_external/furniture/living/sofa/optimized/sofa_web.glb` — `A1321C8B14FFC4170CECA330B581441ADE66B64CA87FF89D772E385367D21B3D` | Séjour RDC, 1 instance |
| Table | **Wooden table with metalic legs** — Nicușor Vatră | https://www.blendkit.com/asset-gallery-detail/bdff957c-a9e9-4827-b6c9-602b264a4fbf/ | CC0-1.0 (`cc_zero`) | `assets_external/furniture/dining/table/original/table_bdff957c-a9e9-4827-b6c9-602b264a4fbf_1k_source.blend` | `assets_external/furniture/dining/table/optimized/table_web.glb` — `A8BCD84ADADC29F9DC26EEFA068FA393823E2599493BCADB62797986D89F67B0` | Salle à manger RDC, 1 instance |
| Chaise | **Dining Chair 02** — James Ray Cock | https://polyhaven.com/a/dining_chair_02 | CC0-1.0 | `assets_external/furniture/dining/chair/original/dining_chair_02_1k.gltf` + `.bin` + 3 cartes 1K | `assets_external/furniture/dining/chair/optimized/chair_web.glb` — `6E5CC754877D49AF17EA2431693E29B07DEEA0A6B14163B1F23EF933E1FAAC71` | Salle à manger RDC, 6 instances |
| Lit | **Master bed** — Rohma Ansari | https://www.blendkit.com/asset-gallery-detail/3a845132-df64-4f02-8da6-44229fe774e4/ | CC0-1.0 (`cc_zero`) | `assets_external/furniture/bedroom/bed/original/bed_d493c69a-5c64-40bf-a7a6-a4e745bfbea8_library.glb` | `assets_external/furniture/bedroom/bed/optimized/bed_web.glb` — `AC6B3C975A1EE98F1288A5567D4C5F89C8A9973AF7D4CF3EAB88AC79AF205637` | Trois chambres de l’étage |
| Arbre | **Island Tree 02** — Rob Tuytel (scan/processing), Rico Cilliers (cleanup/processing) | https://polyhaven.com/a/island_tree_02 | CC0-1.0 | `assets_external/vegetation/trees/island_tree_02/original/island_tree_02_1k.gltf` + `.bin` + 9 cartes 1K | `assets_external/vegetation/trees/island_tree_02/optimized/island_tree_02_web.glb` — `845CD738030743A4592FDC10DB77A38E522E15C8901E6710C377C3D5C303CF76` | Jardin, 4 familles d’arbres |
| Haie | **Shrub** — Blendkit Community | https://www.blenderkit.com/asset-gallery-detail/2810ce15-1076-44e6-9b95-90487f8d5dc5/ | CC0-1.0 (`cc_zero`) | `assets_external/vegetation/hedges/blenderkit_shrub/original/hedge_2810ce15-1076-44e6-9b95-90487f8d5dc5_1k_source.blend` | `assets_external/vegetation/hedges/blenderkit_shrub/optimized/hedge_web.glb` — `552369C1C70CE040EC8971DA0F235D24ECB9CB915B9320B1ABCB4EA0C423B7C2` | 18 segments; 2 lots GPU instanciés |
| Façade PBR | **White Stucco** — Amal Kumar | https://polyhaven.com/a/white_stucco | CC0-1.0 | `assets_external/materials/facade/white_stucco/original/` — diffuse, normal GL, ARM 2K + métadonnées | 3 cartes WebP chargées; SHA dans le tableau ci-dessous | `V12_PBR_OFFWHITE_STUCCO`, `V10_STUCCO_NEW_BUILD` |
| Gazon PBR | **Grass 005** — ambientCG | https://ambientcg.com/a/Grass005 | CC0-1.0 Universal | `assets_external/materials/exterior/grass005/original/Grass005_2K-JPG.zip` — `89183D8DCEABC3C23A26978F426E1662143DD2F84F1DC3586A1592D101E5234B` | 3 cartes WebP chargées; SHA dans le tableau ci-dessous | `PBR_B_GRASS` |

### Cartes PBR réellement demandées par le viewer

| Catégorie | Carte | Octets | SHA-256 |
|---|---|---:|---|
| Façade | `white_stucco_color_1k.webp` | 63 686 | `5222252B203684A6949670D5D303D764DD3F4E40A2DF4B97D5301DD1BBE5EC42` |
| Façade | `white_stucco_normal_gl_1k.webp` | 391 816 | `1B7BED28D294A667574D7B346FC2A2D12F8363C8EDF86F9C1E2EFE6BB01EA44D` |
| Façade | `white_stucco_arm_1k.webp` | 34 456 | `BB1251D555396B1C5D5FB8199968D9714CAA1F4FEEB796AD037979405DCB640E` |
| Gazon | `Grass005_color_1k.webp` | 364 742 | `8FFAB3A46B9D178370B32A3FB076BABA00362BB8940BB56404C7205585123F40` |
| Gazon | `Grass005_normal_gl_1k.webp` | 541 710 | `EF7B7C71D9D4D01F89AE2D7BD85775F6F18B00037B8BA907FA975F6C94C28148` |
| Gazon | `Grass005_arm_1k.webp` | 651 874 | `DEDCBE2EDCED39A0D51166115CD499E339FA604E5033B2FE1E0A2D182B60D1BE` |

Total runtime : **6 cartes, 2 048 284 octets**. Les fichiers AO autonomes sont conservés comme dérivés dans `optimized/`, mais le viewer lit déjà l’occlusion dans le canal rouge de la carte ARM; ils ne sont donc pas téléchargés au runtime.

## Note de cohérence de provenance

Le fichier local `assets_external/furniture/dining/chair/original/library_metadata.json` conserve le libellé d’acquisition générique `author: "All"`. Le dossier de recherche officiel `analysis/pilot_furniture_candidates.json` identifie **James Ray Cock** pour Dining Chair 02; ce nom est donc celui affiché dans le registre, tandis que l’incohérence locale reste explicitement tracée.

## Modifications apportées aux sources

- GLB mobilier : copie/normalisation, matériaux Web compatibles, textures embarquées, contrôle de métrique; aucune URI externe.
- Arbre : copie Web optimisée auto-contenue, 47 000 triangles, neuf images embarquées.
- Haie : décimation attentive aux matériaux, conservation des UV/alpha, LOD déterministe des cartes de feuilles, export GLB WebP auto-contenu.
- Matériaux : conversion des cartes 2K vers WebP 1K; création de cartes ARM; la géométrie architecturale n’est pas modifiée.
- Les dérivés restent sous la même dédicace CC0 que les sources sélectionnées; les crédits d’origine ne sont pas supprimés.

## Candidats explicitement exclus

| Asset | État | Motif |
|---|---|---|
| BlenderKit Decorative Urban Tree — Davide Tirindelli — CC0 | Rejet après import | Silhouette hivernale sans feuilles; 123 949 triangles; GLB 7 032 388 octets; score post-import 29/60. La licence n’est pas le motif du rejet. |
| BlenderKit Tree LOD 2 | Rejet licence/redistribution | Licence « Royalty Free »; la condition d’extractibilité ne convient pas à un GLB public directement téléchargeable. |
| BlenderKit Wild Alpine Shrub Evergreen | Rejet licence/redistribution | Gratuit mais « Royalty Free », pas CC0; redistribution du modèle brut non retenue. |
| BlenderKit Realistic Tree | Rejet coût | Page officielle marquée Full Plan. |
| BlenderKit Soave sofa | Rejet droits tiers | Le champ API indique CC0 mais la description cite un produit Moooi/Sebastian Herkner et réserve les droits du design d’origine. |
| Alternatives Poly Haven / ambientCG / CGBookcase non téléchargées | Recherche seulement | Elles figurent dans les dossiers d’analyse; aucun binaire tiers correspondant n’est redistribué ici. |

## Traçabilité locale

- Recherche mobilier : `analysis/pilot_furniture_candidates.json`
- Recherche matériaux : `analysis/pilot_material_candidates.json`
- Recherche végétation : `analysis/pilot_vegetation_candidates.json`
- Validation de l’intégration : `validation/pilot_furniture_integration.json`, `validation/pilot_material_integration_validation.json`, `validation/pilot_vegetation_integration.json`
- Inventaire exhaustif : `assets_external/ASSET_MANIFEST.json`
