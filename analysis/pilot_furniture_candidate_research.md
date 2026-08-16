# Recherche officielle — candidats mobilier du pilote Chamagnieu

- **Instantané vérifié :** `2026-08-16T15:05:58Z`
- **Périmètre :** recherche, comparaison, licence et téléchargeabilité uniquement.
- **Téléchargement binaire / intégration :** **aucun**. Les appels `downloads/...` Blendkit ont récupéré uniquement le JSON d’autorisation (0 octet d’asset) ; les URL Poly Haven ont été testées en `HEAD`.
- **Statut contractuel :** `VISUALISATION_ONLY = TRUE` ; `CONTRACTUAL = FALSE`.

## Conclusion opérationnelle

| Élément | Choix pilote | Décision | Point de vigilance |
|---|---|---|---|
| Canapé contemporain 3 places | **Leather Sofa** (`4faac4b8-cc88-4ff2-b7fd-a7edf46d3518`) | `PILOT_SELECTED` | Explicit 3-seat model, CC0, free, direct 0.73 MB glTF, manageable 30k source faces. |
| Table contemporaine | **Wooden table with metalic legs** (`bdff957c-a9e9-4827-b6c9-602b264a4fbf`) | `PILOT_SELECTED` | Correct dining dimensions, modern neutral style, rich PBR metadata and light 1K source. |
| Chaise assortie | **Dining Chair 02** (`dining_chair_02`) | `PILOT_SELECTED` | Poly Haven direct CC0 glTF, 22k polygons, complete 1K PBR bundle and coherent wood/leather style. |
| Lit réaliste | **Master bed** (`3a845132-df64-4f02-8da6-44229fe774e4`) | `PILOT_SELECTED_CONDITIONAL_MATERIAL_QA` | Only contemporary CC0 double-bed candidate in the verified free set; compact direct glTF, but no texture maps reported. |

**Verdict :** le canapé, la table et la chaise ont chacun une option CC0, gratuite et automatiquement accessible. Le lit moderne a une option CC0 légère, mais son absence de textures déclarées impose un contrôle visuel/matériau avant intégration.

## Règle de licence appliquée

- **Poly Haven :** la page officielle [https://polyhaven.com/license](https://polyhaven.com/license) indique CC0, usage commercial permis, attribution facultative et redistribution permise, y compris dans un produit.
- **Blendkit CC0 :** la documentation [https://www.blendkit.com/docs/licenses/](https://www.blendkit.com/docs/licenses/) et les [conditions 2026](https://www.blendkit.com/terms-and-conditions-2026/) autorisent l’usage très large des fichiers CC0. Les auteurs sont tout de même conservés dans les métadonnées.
- **Blendkit Royalty Free :** les [conditions 2026](https://www.blendkit.com/terms-and-conditions-2026/) interdisent d’embarquer un modèle 3D en format ouvert sous cette licence. Comme le viewer sert des `.glb` récupérables par le navigateur, ces candidats sont rejetés.
- **Répliques de produits de marque :** le drapeau CC0 de l’uploader ne suffit pas à libérer les droits séparés du designer/fabricant. Ces fichiers sont isolés en `MANUAL_IP_REVIEW_REQUIRED`.
- **Sketchfab/Fab :** aucun candidat n’est compté dans cette phase, car le minimum a été atteint sur les deux sources prioritaires avec un chemin anonyme vérifié.

### Sorties HTTP primaires

- `HTTP 200; final_url=https://www.blendkit.com/docs/licenses/` — [https://www.blendkit.com/docs/licenses/](https://www.blendkit.com/docs/licenses/)
- `HTTP 200; final_url=https://www.blendkit.com/docs/licenses/licensing-faq/` — [https://www.blendkit.com/docs/licenses/licensing-faq/](https://www.blendkit.com/docs/licenses/licensing-faq/)
- `HTTP 200; final_url=https://www.blendkit.com/terms-and-conditions-2026/` — [https://www.blendkit.com/terms-and-conditions-2026/](https://www.blendkit.com/terms-and-conditions-2026/)
- `HTTP 200; final_url=https://polyhaven.com/license` — [https://polyhaven.com/license](https://polyhaven.com/license)

Tous les candidats retenus ci-dessous ont également : page officielle HTTP 200, API officielle HTTP 200 et probe anonyme HTTP 200. Les sorties exactes sont conservées dans le JSON compagnon.

## Canapé contemporain 3 places

| Candidat | Source | Réalisme | Style | Géométrie | Textures | Perf. | Licence | TOTAL | Statut |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [Leather Sofa](https://www.blendkit.com/asset-gallery-detail/4faac4b8-cc88-4ff2-b7fd-a7edf46d3518/) | Blendkit | 8 | 8 | 8 | 8 | 8 | 10 | **50/60** | `PILOT_SELECTED` |
| [Sofa 3](https://www.blendkit.com/asset-gallery-detail/8c310d7f-74d1-422f-a2fb-4c11b773cf7b/) | Blendkit | 8 | 8 | 8 | 7 | 8 | 10 | **49/60** | `SHORTLIST_VISUAL_SEAT_COUNT_CHECK` |
| [3 seater sofa](https://www.blendkit.com/asset-gallery-detail/15198828-3421-4d08-bc61-45a32570f3be/) | Blendkit | 9 | 9 | 9 | 9 | 2 | 10 | **48/60** | `REJECT_PERFORMANCE_FOR_LIVE_WEB` |

### Leather Sofa — `4faac4b8-cc88-4ff2-b7fd-a7edf46d3518`

- **Auteur :** Muhammed Ismayil
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/4faac4b8-cc88-4ff2-b7fd-a7edf46d3518/](https://www.blendkit.com/asset-gallery-detail/4faac4b8-cc88-4ff2-b7fd-a7edf46d3518/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A4faac4b8-cc88-4ff2-b7fd-a7edf46d3518](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A4faac4b8-cc88-4ff2-b7fd-a7edf46d3518)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 2.873 × 1.012 × 1.005 m
- **Géométrie :** 30328 source / 30328 rendu
- **Textures :** 4096 px max; 4 texture(s)
- **Formats source :** blend, gltf, gltf_godot, resolution_0_5K, resolution_1K, resolution_2K, resolution_4K
- **Fichier de travail recommandé :** gltf · 731828 octets · conversion GLB=non
- **Preuve anonyme :** `HTTP 200; fileType=gltf; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SELECTED` — Explicitly described by the author as a 3-seat leather sofa; direct compact glTF is available. At 2.87 m wide it must be scale-checked against the living room plan.

### Sofa 3 — `8c310d7f-74d1-422f-a2fb-4c11b773cf7b`

- **Auteur :** Yasin Gohary
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/8c310d7f-74d1-422f-a2fb-4c11b773cf7b/](https://www.blendkit.com/asset-gallery-detail/8c310d7f-74d1-422f-a2fb-4c11b773cf7b/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A8c310d7f-74d1-422f-a2fb-4c11b773cf7b](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A8c310d7f-74d1-422f-a2fb-4c11b773cf7b)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 2.417 × 1.165 × 0.799 m
- **Géométrie :** 24861 source / 435936 rendu
- **Textures :** 2048 px max; 1 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K
- **Fichier de travail recommandé :** resolution_1K · 1764695 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `SHORTLIST_VISUAL_SEAT_COUNT_CHECK` — 2.42 m contemporary sofa with moderate geometry and a light 1K source. The API name “Sofa 3” does not explicitly state three seats, so visual seat-count QA is still required.

### 3 seater sofa — `15198828-3421-4d08-bc61-45a32570f3be`

- **Auteur :** Rinkesh Purohit
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/15198828-3421-4d08-bc61-45a32570f3be/](https://www.blendkit.com/asset-gallery-detail/15198828-3421-4d08-bc61-45a32570f3be/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A15198828-3421-4d08-bc61-45a32570f3be](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A15198828-3421-4d08-bc61-45a32570f3be)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 2.622 × 1.02 × 0.915 m
- **Géométrie :** 125438 source / 798078 rendu
- **Textures :** 4096 px max; 12 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K, resolution_4K
- **Fichier de travail recommandé :** resolution_1K · 9710541 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `REJECT_PERFORMANCE_FOR_LIVE_WEB` — Exact three-seater and visually detailed, but 125k source faces, 798k render faces and very large source packages make it unsuitable for the phone-first viewer without a separate retopology/LOD pass.

## Table contemporaine

| Candidat | Source | Réalisme | Style | Géométrie | Textures | Perf. | Licence | TOTAL | Statut |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [Wooden table with metalic legs](https://www.blendkit.com/asset-gallery-detail/bdff957c-a9e9-4827-b6c9-602b264a4fbf/) | Blendkit | 8 | 9 | 6 | 9 | 9 | 10 | **51/60** | `PILOT_SELECTED` |
| [Dining Table 01](https://www.blendkit.com/asset-gallery-detail/d90a729f-7e97-41e5-a9c3-650381f3d06a/) | Blendkit | 8 | 8 | 8 | 9 | 7 | 10 | **50/60** | `PILOT_SHORTLIST` |
| [Scandinavian Dining Table](https://www.blendkit.com/asset-gallery-detail/08dee582-4ac7-47fc-a1e1-192e677da403/) | Blendkit | 7 | 9 | 6 | 8 | 9 | 10 | **49/60** | `CONDITIONAL_RESCALE_HEIGHT` |
| [Dining Table Medium](https://www.blendkit.com/asset-gallery-detail/b7b0eac0-f441-4077-bdcc-5c5f6739a7fe/) | Blendkit | 7 | 8 | 6 | 7 | 10 | 10 | **48/60** | `PILOT_SHORTLIST` |

### Wooden table with metalic legs — `bdff957c-a9e9-4827-b6c9-602b264a4fbf`

- **Auteur :** Nicușor Vatră
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/bdff957c-a9e9-4827-b6c9-602b264a4fbf/](https://www.blendkit.com/asset-gallery-detail/bdff957c-a9e9-4827-b6c9-602b264a4fbf/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Abdff957c-a9e9-4827-b6c9-602b264a4fbf](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Abdff957c-a9e9-4827-b6c9-602b264a4fbf)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 2 × 0.9 × 0.75 m
- **Géométrie :** 42 source / 58 rendu
- **Textures :** 4096 px max; 12 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K
- **Fichier de travail recommandé :** resolution_1K · 1599907 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SELECTED` — Generic contemporary wood top/metal leg dining table, correct 2.00 × 0.90 × 0.75 m scale and rich PBR texture metadata; geometry is extremely simple but appropriate for this rectilinear object.

### Dining Table 01 — `d90a729f-7e97-41e5-a9c3-650381f3d06a`

- **Auteur :** The Doctor By Design
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/d90a729f-7e97-41e5-a9c3-650381f3d06a/](https://www.blendkit.com/asset-gallery-detail/d90a729f-7e97-41e5-a9c3-650381f3d06a/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ad90a729f-7e97-41e5-a9c3-650381f3d06a](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ad90a729f-7e97-41e5-a9c3-650381f3d06a)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 1.789 × 0.974 × 0.75 m
- **Géométrie :** 6536 source / 104576 rendu
- **Textures :** 4096 px max; 8 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K, resolution_4K
- **Fichier de travail recommandé :** resolution_1K · 2302449 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SHORTLIST` — Generic 1.79 m dining table with 4K texture metadata and usable dimensions; 1K source remains modest, but conversion from Blend to GLB is required.

### Scandinavian Dining Table — `08dee582-4ac7-47fc-a1e1-192e677da403`

- **Auteur :** Calebe Moreira
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/08dee582-4ac7-47fc-a1e1-192e677da403/](https://www.blendkit.com/asset-gallery-detail/08dee582-4ac7-47fc-a1e1-192e677da403/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A08dee582-4ac7-47fc-a1e1-192e677da403](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A08dee582-4ac7-47fc-a1e1-192e677da403)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 1.5 × 1 × 0.69 m
- **Géométrie :** 42 source / 42 rendu
- **Textures :** 4096 px max; 4 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K, resolution_4K
- **Fichier de travail recommandé :** resolution_1K · 528231 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `CONDITIONAL_RESCALE_HEIGHT` — Clear Scandinavian style and light package, but the reported 0.6902 m height is below normal dining height; scale to 0.74–0.76 m and recheck top thickness.

### Dining Table Medium — `b7b0eac0-f441-4077-bdcc-5c5f6739a7fe`

- **Auteur :** /Unwrapped
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/b7b0eac0-f441-4077-bdcc-5c5f6739a7fe/](https://www.blendkit.com/asset-gallery-detail/b7b0eac0-f441-4077-bdcc-5c5f6739a7fe/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ab7b0eac0-f441-4077-bdcc-5c5f6739a7fe](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ab7b0eac0-f441-4077-bdcc-5c5f6739a7fe)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 0.9 × 1.5 × 0.75 m
- **Géométrie :** 130 source / 130 rendu
- **Textures :** 2048 px max; 4 texture(s)
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K
- **Fichier de travail recommandé :** resolution_1K · 1186507 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SHORTLIST` — Correct real-world dimensions (1.50 × 0.90 × 0.75 m) and very low geometry; best as a performance fallback after close-up material QA.

## Chaise assortie

| Candidat | Source | Réalisme | Style | Géométrie | Textures | Perf. | Licence | TOTAL | Statut |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [Dining Chair 02](https://polyhaven.com/a/dining_chair_02) | Poly Haven | 9 | 8 | 9 | 10 | 8 | 10 | **54/60** | `PILOT_SELECTED` |
| [Wooden Dining Chair](https://www.blendkit.com/asset-gallery-detail/53195601-f0c2-4c34-871a-34aa32472e7e/) | Blendkit | 8 | 9 | 8 | 7 | 9 | 10 | **51/60** | `PILOT_SHORTLIST` |
| [Plastic chair](https://www.blendkit.com/asset-gallery-detail/0e9aa213-afd4-4b45-ba88-d3b76bcef9ce/) | Blendkit | 7 | 7 | 7 | 7 | 10 | 10 | **48/60** | `PERFORMANCE_FALLBACK` |
| [Wooden Chair](https://www.blendkit.com/asset-gallery-detail/30ad483f-9438-4758-9fab-d0ff1caab348/) | Blendkit | 8 | 9 | 8 | 5 | 3 | 10 | **43/60** | `REJECT_PERFORMANCE_FOR_LIVE_WEB` |

### Dining Chair 02 — `dining_chair_02`

- **Auteur :** James Ray Cock
- **Page officielle :** [https://polyhaven.com/a/dining_chair_02](https://polyhaven.com/a/dining_chair_02)
- **API officielle :** [https://api.polyhaven.com/files/dining_chair_02](https://api.polyhaven.com/files/dining_chair_02)
- **Licence / prix :** CC0 / Public Domain dedication · gratuit=`true` · téléchargeable=`true` · attribution : Not required; author retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Explicitly allowed by Poly Haven’s CC0 license page, including redistribution inside a product.
- **Dimensions API :** 0.434 × 0.576 × 0.973 m
- **Géométrie :** 22013 polygones (champ API)
- **Textures :** 8192 px max; canaux Diffuse, nor_dx, nor_gl, Metal, arm, AO, Rough
- **Formats source :** blend, gltf, usd, fbx
- **Fichier de travail recommandé :** glTF 1k · bundle 921075 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; Content-Length=2723; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SELECTED` — Modern tufted leather dining chair with direct 1K glTF bundle, strong PBR maps and reliable real-world scale; dark wood/leather is coherent with the selected wood/metal table.

### Wooden Dining Chair — `53195601-f0c2-4c34-871a-34aa32472e7e`

- **Auteur :** Brian Pickens
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/53195601-f0c2-4c34-871a-34aa32472e7e/](https://www.blendkit.com/asset-gallery-detail/53195601-f0c2-4c34-871a-34aa32472e7e/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A53195601-f0c2-4c34-871a-34aa32472e7e](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A53195601-f0c2-4c34-871a-34aa32472e7e)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 0.521 × 0.49 × 0.955 m
- **Géométrie :** 3388 source / 3388 rendu
- **Textures :** 4096 px max
- **Formats source :** blend, resolution_0_5K, resolution_1K, resolution_2K
- **Fichier de travail recommandé :** resolution_1K · 1138331 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; fileType=resolution_1K; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SHORTLIST` — Generic mapped wooden dining chair with correct scale and modest geometry; visually matches wood dining tables, but the API omits texture count so material channels need inspection.

### Plastic chair — `0e9aa213-afd4-4b45-ba88-d3b76bcef9ce`

- **Auteur :** abd3d
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/0e9aa213-afd4-4b45-ba88-d3b76bcef9ce/](https://www.blendkit.com/asset-gallery-detail/0e9aa213-afd4-4b45-ba88-d3b76bcef9ce/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A0e9aa213-afd4-4b45-ba88-d3b76bcef9ce](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A0e9aa213-afd4-4b45-ba88-d3b76bcef9ce)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 0.54 × 0.601 × 0.734 m
- **Géométrie :** 1208 source / 19328 rendu
- **Textures :** 2048 px max; 3 texture(s)
- **Formats source :** blend, gltf, gltf_godot, resolution_0_5K, resolution_1K, resolution_2K
- **Fichier de travail recommandé :** gltf · 260704 octets · conversion GLB=non
- **Preuve anonyme :** `HTTP 200; fileType=gltf; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PERFORMANCE_FALLBACK` — Compact direct glTF and only 1.2k faces; modern silhouette, but plastic styling is less coherent with the selected wood/metal table.

### Wooden Chair — `30ad483f-9438-4758-9fab-d0ff1caab348`

- **Auteur :** abd3d
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/30ad483f-9438-4758-9fab-d0ff1caab348/](https://www.blendkit.com/asset-gallery-detail/30ad483f-9438-4758-9fab-d0ff1caab348/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A30ad483f-9438-4758-9fab-d0ff1caab348](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A30ad483f-9438-4758-9fab-d0ff1caab348)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 0.604 × 0.662 × 0.816 m
- **Géométrie :** 77843 source / 323598 rendu
- **Textures :** résolution n/d; 0 texture(s)
- **Formats source :** blend, gltf, gltf_godot, resolution_0_5K, resolution_1K
- **Fichier de travail recommandé :** gltf · 14911524 octets · conversion GLB=non
- **Preuve anonyme :** `HTTP 200; fileType=gltf; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `REJECT_PERFORMANCE_FOR_LIVE_WEB` — Contemporary wood/cane look, but 77.8k faces and a 14.9 MB generated glTF are excessive for repeated dining-chair instances; source API also reports no texture set.

## Lit réaliste

| Candidat | Source | Réalisme | Style | Géométrie | Textures | Perf. | Licence | TOTAL | Statut |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| [Master bed](https://www.blendkit.com/asset-gallery-detail/3a845132-df64-4f02-8da6-44229fe774e4/) | Blendkit | 8 | 9 | 7 | 4 | 10 | 10 | **48/60** | `PILOT_SELECTED_CONDITIONAL_MATERIAL_QA` |
| [Vintage Day Bed](https://polyhaven.com/a/vintage_day_bed) | Poly Haven | 9 | 2 | 8 | 10 | 8 | 10 | **47/60** | `REJECT_STYLE_AND_SIZE` |
| [Gothic Bed 01](https://polyhaven.com/a/GothicBed_01) | Poly Haven | 9 | 2 | 9 | 9 | 7 | 10 | **46/60** | `REJECT_STYLE_MISMATCH` |
| [Old Bed Frame](https://polyhaven.com/a/old_bed_frame) | Poly Haven | 8 | 1 | 8 | 9 | 5 | 10 | **41/60** | `REJECT_INCOMPLETE_AND_STYLE` |

### Master bed — `3a845132-df64-4f02-8da6-44229fe774e4`

- **Auteur :** Rohma Ansari
- **Page officielle :** [https://www.blendkit.com/asset-gallery-detail/3a845132-df64-4f02-8da6-44229fe774e4/](https://www.blendkit.com/asset-gallery-detail/3a845132-df64-4f02-8da6-44229fe774e4/)
- **API officielle :** [https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A3a845132-df64-4f02-8da6-44229fe774e4](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A3a845132-df64-4f02-8da6-44229fe774e4)
- **Licence / prix :** CC0 (API value: cc_zero) · gratuit=`true` · téléchargeable=`true` · attribution : Not legally required by CC0; author credit retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Allowed for this CC0 asset; retain the asset/author record. This conclusion does not extend to Blendkit Royalty Free assets.
- **Dimensions API :** 1.762 × 2.227 × 1.06 m
- **Géométrie :** 4195 source / 4195 rendu
- **Textures :** résolution n/d; 0 texture(s)
- **Formats source :** blend, gltf, gltf_godot, resolution_0_5K
- **Fichier de travail recommandé :** gltf · 133244 octets · conversion GLB=non
- **Preuve anonyme :** `HTTP 200; fileType=gltf; filePath_host=assets.blenderkit.com; asset_payload_bytes_fetched=0`
- **Décision :** `PILOT_SELECTED_CONDITIONAL_MATERIAL_QA` — Only free CC0 candidate found that clearly fits a modern double-bedroom brief; correct 1.76 × 2.23 m footprint and tiny direct glTF. No texture maps are reported, so it needs close-up material QA and, if necessary, a separately licensed PBR fabric/wood material.

### Vintage Day Bed — `vintage_day_bed`

- **Auteur :** Aron Łyczek
- **Page officielle :** [https://polyhaven.com/a/vintage_day_bed](https://polyhaven.com/a/vintage_day_bed)
- **API officielle :** [https://api.polyhaven.com/files/vintage_day_bed](https://api.polyhaven.com/files/vintage_day_bed)
- **Licence / prix :** CC0 / Public Domain dedication · gratuit=`true` · téléchargeable=`true` · attribution : Not required; author retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Explicitly allowed by Poly Haven’s CC0 license page, including redistribution inside a product.
- **Dimensions API :** 1.973 × 0.855 × 1.127 m
- **Géométrie :** 2715 polygones (champ API)
- **Textures :** 8192 px max; canaux arm, Diffuse, Metal, nor_dx, nor_gl, Rough
- **Formats source :** blend, gltf, usd, fbx
- **Fichier de travail recommandé :** glTF 1k · bundle 2425779 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; Content-Length=2791; asset_payload_bytes_fetched=0`
- **Décision :** `REJECT_STYLE_AND_SIZE` — Excellent scan-like detail and light mesh, but it is a narrow vintage day bed rather than a contemporary double bed.

### Gothic Bed 01 — `GothicBed_01`

- **Auteur :** Kirill Sannikov
- **Page officielle :** [https://polyhaven.com/a/GothicBed_01](https://polyhaven.com/a/GothicBed_01)
- **API officielle :** [https://api.polyhaven.com/files/GothicBed_01](https://api.polyhaven.com/files/GothicBed_01)
- **Licence / prix :** CC0 / Public Domain dedication · gratuit=`true` · téléchargeable=`true` · attribution : Not required; author retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Explicitly allowed by Poly Haven’s CC0 license page, including redistribution inside a product.
- **Dimensions API :** 1.494 × 2.04 × 1.534 m
- **Géométrie :** 18741 polygones (champ API)
- **Textures :** 4096 px max; canaux Diffuse, nor_dx, nor_gl, Metal, arm, Rough
- **Formats source :** blend, gltf, usd, fbx
- **Fichier de travail recommandé :** glTF 1k · bundle 1155213 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; Content-Length=2683; asset_payload_bytes_fetched=0`
- **Décision :** `REJECT_STYLE_MISMATCH` — Complete, realistic and technically clean bed, but ornate Gothic design is incompatible with the contemporary Chamagnieu interior.

### Old Bed Frame — `old_bed_frame`

- **Auteur :** Luca B
- **Page officielle :** [https://polyhaven.com/a/old_bed_frame](https://polyhaven.com/a/old_bed_frame)
- **API officielle :** [https://api.polyhaven.com/files/old_bed_frame](https://api.polyhaven.com/files/old_bed_frame)
- **Licence / prix :** CC0 / Public Domain dedication · gratuit=`true` · téléchargeable=`true` · attribution : Not required; author retained voluntarily in project metadata.
- **Redistribution Web embarquée :** Explicitly allowed by Poly Haven’s CC0 license page, including redistribution inside a product.
- **Dimensions API :** 0.905 × 2.002 × 1.201 m
- **Géométrie :** 49990 polygones (champ API)
- **Textures :** 8192 px max; canaux AO, arm, Diffuse, Metal, nor_dx, nor_gl, Rough
- **Formats source :** blend, gltf, usd, fbx
- **Fichier de travail recommandé :** glTF 1k · bundle 4041628 octets · conversion GLB=oui
- **Preuve anonyme :** `HTTP 200; Content-Length=3326; asset_payload_bytes_fetched=0`
- **Décision :** `REJECT_INCOMPLETE_AND_STYLE` — Realistic CC0 metal frame, but single-size, rusted, and supplied without a complete modern mattress/bedding assembly.

## Candidats explicitement rejetés

| Élément | Candidat | Source | Gratuit | Licence API | TOTAL | Rejet |
|---|---|---|---:|---|---:|---|
| Canapé contemporain 3 places | [Soave sofa](https://www.blendkit.com/asset-gallery-detail/d2de37df-d634-4781-800d-d947855e6107/) (`d2de37df-d634-4781-800d-d947855e6107`) | Blendkit | `true` | `cc_zero` | 45/60 | `MANUAL_IP_REVIEW_REQUIRED` |
| Table contemporaine | [Cross FIxed Table](https://www.blendkit.com/asset-gallery-detail/e64560f8-33db-4802-85a0-59ecababb44b/) (`e64560f8-33db-4802-85a0-59ecababb44b`) | Blendkit | `true` | `cc_zero` | 46/60 | `MANUAL_IP_REVIEW_REQUIRED` |
| Chaise assortie | [Carl-hansen-son CHAIR 29](https://www.blendkit.com/asset-gallery-detail/dfdffe2b-4c26-4c33-9f13-784fe54c5570/) (`dfdffe2b-4c26-4c33-9f13-784fe54c5570`) | Blendkit | `true` | `cc_zero` | 48/60 | `MANUAL_IP_REVIEW_REQUIRED` |
| Lit réaliste | [Minimalist Modern Bed](https://www.blendkit.com/asset-gallery-detail/5ac710d1-6c79-4a4d-91c7-a583384c51ef/) (`5ac710d1-6c79-4a4d-91c7-a583384c51ef`) | Blendkit | `true` | `royalty_free` | 38/60 | `REJECT_LICENSE_OPEN_WEB_GLB` |
| Lit réaliste | [Bed](https://www.blendkit.com/asset-gallery-detail/7e7e8c77-e434-4470-8e73-a202289bc43b/) (`7e7e8c77-e434-4470-8e73-a202289bc43b`) | Blendkit | `true` | `royalty_free` | 41/60 | `REJECT_LICENSE_OPEN_WEB_GLB` |
| Lit réaliste | [Modern foldable sofa bed](https://www.blendkit.com/asset-gallery-detail/5a27f876-2384-4256-909d-a5c59bb01ae6/) (`5a27f876-2384-4256-909d-a5c59bb01ae6`) | Blendkit | `false` | `royalty_free` | 42/60 | `REJECT_PAID` |

- **Soave sofa** — Uploader marks the file CC0 but describes it as a fan-made Moooi/Sebastian Herkner product and expressly notes third-party design rights. CC0 cannot waive rights the uploader does not own.
  Preuve API : `HTTP 200; count=1; assetBaseId=d2de37df-d634-4781-800d-d947855e6107` · [page](https://www.blendkit.com/asset-gallery-detail/d2de37df-d634-4781-800d-d947855e6107/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ad2de37df-d634-4781-800d-d947855e6107)
- **Cross FIxed Table** — The description identifies a named manufacturer product and reproduces manufacturer wording. The uploader CC0 flag does not independently clear third-party product-design/trademark rights.
  Preuve API : `HTTP 200; count=1; assetBaseId=e64560f8-33db-4802-85a0-59ecababb44b` · [page](https://www.blendkit.com/asset-gallery-detail/e64560f8-33db-4802-85a0-59ecababb44b/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Ae64560f8-33db-4802-85a0-59ecababb44b)
- **Carl-hansen-son CHAIR 29** — Asset is labeled as a Carl Hansen & Søn CHAIR 29 product. Despite the uploader CC0 flag, separate manufacturer/design rights are not cleared by the official metadata.
  Preuve API : `HTTP 200; count=1; assetBaseId=dfdffe2b-4c26-4c33-9f13-784fe54c5570` · [page](https://www.blendkit.com/asset-gallery-detail/dfdffe2b-4c26-4c33-9f13-784fe54c5570/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3Adfdffe2b-4c26-4c33-9f13-784fe54c5570)
- **Minimalist Modern Bed** — Free download, but licensed Royalty Free. Blendkit’s 2026 terms prohibit embedding an open-format 3D model under this license; the live viewer serves open GLB assets.
  Preuve API : `HTTP 200; count=1; assetBaseId=5ac710d1-6c79-4a4d-91c7-a583384c51ef` · [page](https://www.blendkit.com/asset-gallery-detail/5ac710d1-6c79-4a4d-91c7-a583384c51ef/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A5ac710d1-6c79-4a4d-91c7-a583384c51ef)
- **Bed** — Free download, but Royalty Free rather than CC0; open-format GLB embedding conflicts with the official 2026 terms.
  Preuve API : `HTTP 200; count=1; assetBaseId=7e7e8c77-e434-4470-8e73-a202289bc43b` · [page](https://www.blendkit.com/asset-gallery-detail/7e7e8c77-e434-4470-8e73-a202289bc43b/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A7e7e8c77-e434-4470-8e73-a202289bc43b)
- **Modern foldable sofa bed** — Official API reports isFree=false, canDownload=false and access=full. No purchase or account/payment bypass is permitted.
  Preuve API : `HTTP 200; count=1; assetBaseId=5a27f876-2384-4256-909d-a5c59bb01ae6` · [page](https://www.blendkit.com/asset-gallery-detail/5a27f876-2384-4256-909d-a5c59bb01ae6/) · [API](https://www.blenderkit.com/api/v1/search/?query=asset_base_id%3A5a27f876-2384-4256-909d-a5c59bb01ae6)

## Limites et prochaine passe

- Les scores sont un **screening de recherche** fondé sur métadonnées officielles, miniatures et poids de fichiers ; ils ne remplacent pas l’ouverture dans Blender puis le test dans le live Web viewer.
- Avant intégration : ouvrir la source choisie, vérifier UV/matériaux/normales, mesurer à l’échelle, produire un GLB optimisé, tester instanciation, collision et 30 FPS sur téléphone/PC.
- Pour le **lit**, si le `Master bed` ne passe pas le contrôle matériau, ne pas basculer vers un Royalty Free ouvert : poursuivre la recherche CC0 ou fabriquer seulement les matériaux avec une source CC0 distincte.

JSON machine-readable : `C:\Users\jonat\Documents\Codex\2026-08-16\chamagnieu-v18-assets-pilot\analysis\pilot_furniture_candidates.json`
