# Inventaire GLB réellement présent — Chamagnieu V18

## Verdict factuel

- Recherche récursive dans `C:\Users\jonat\Documents\Codex\2026-08-14\files-mentioned-by-the-user-c\outputs\Chamagnieu_3D_V18_LIVE_SYNC` : **2 fichiers `.glb`**.
- `shared/project-config.json` est désormais la source de vérité live et sélectionne `./Chamagnieu_V18_REALISM_FINAL.glb`; `presentation/presentation.js` et `visite/visite.js` chargent tous deux cette configuration puis résolvent `config.model`.
- `Chamagnieu_V18_REALISM_FINAL.glb` et l'ancien nom `Chamagnieu_V18_ROOF_GROUND_REALISM.glb` sont **deux fichiers physiques mais un contenu binaire strictement identique** : même taille, même SHA-256, même mtime. Le second est un alias de compatibilité, pas une ancienne géométrie concurrente.
- URL runtime calculée : `../shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3` depuis les pages `presentation/` et `visite/`.

## Fichier et intégrité conteneur

| Chemin relatif | Octets | Mio | SHA-256 | mtime local |
|---|---:|---:|---|---|
| `shared/Chamagnieu_V18_REALISM_FINAL.glb` **(live)** | 27 987 896 | 26.691 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | 2026-08-15T20:41:33.030760+02:00 |
| `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb` **(alias identique)** | 27 987 896 | 26.691 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | 2026-08-15T20:41:33.030760+02:00 |

- En-tête : magic `glTF`  glTF **2**  longueur déclarée **27 987 896** = longueur physique **27 987 896**.
- Chunks : JSON **754 700 octets**  BIN **27 233 168 octets**; les deux tailles sont alignées sur 4 octets.
- `buffers[0].byteLength` = **27 233 168**  fin maximale des `bufferViews` = **27 233 168** : aucune sortie du BIN détectée par ce contrôle structurel.
- Les références d’accessor, matériau et image contrôlées sont dans les bornes. Ceci est un contrôle structurel ciblé, pas un passage complet du Khronos glTF Validator.

> La structure ci-dessous est calculée sur le GLB live; elle vaut byte pour byte pour l’alias de compatibilité.

## Structure glTF chiffrée

| Élément | Nombre / valeur |
|---|---:|
| Scènes | 1 |
| Scène active | 0 |
| Nœuds | 794 |
| Meshes | 793 |
| Primitives | 795 |
| Matériaux | 35 |
| Textures glTF | 56 |
| Images | 37 |
| Samplers | 1 |
| Accessors | 2 454 |
| BufferViews | 2 528 |
| Buffers | 1 |
| Animations | 1 |
| Vertices déclarés par primitives | 377 701 |
| Indices | 950 343 |
| Triangles calculés | 316 781 |

- **795/795** primitives sont des triangles (`mode=4`), ont `POSITION`, `NORMAL`, `TEXCOORD_0` et un matériau assigné; UV présentes sur **795/795** et normales sur **795/795**.
- **793 meshes / 794 nœuds** : le nœud sans mesh est `HOUSE_REFERENCE_ORIGIN`; les deux fauteuils importés sont les seuls meshes à deux primitives, d’où 795 primitives pour 793 meshes.
- Extensions utilisées : `KHR_materials_transmission, KHR_materials_ior, KHR_texture_transform`. Extension requise : `KHR_texture_transform`.
- Pas de `KHR_draco_mesh_compression`, KTX2/Basis, skin, caméra embarquée ou HDR/EXR; le fichier est un GLB non-Draco avec textures JPEG intégrées.
- Animation : `modern_wooden_cabinet_body` avec 3 canaux STEP (translation, rotation, scale) ciblant `V11_LIVING_TV_CONSOLE`; elle provient vraisemblablement de l’asset cabinet, sans action lancée par le viewer.

## Graphe de scène et métadonnées V18

- Racines de scène : **49**; `HOUSE_REFERENCE_ORIGIN` contient **745** enfants, tandis que végétation V17 et sol visible V18 sont aussi des racines de scène.
- `v18_changed_branch_field` = `V18_ROOF_GROUND_REALISM / outdoor_dining::removed_29_nodes; roof_geometry::front_hip_rebuilt+garage_winding_fixed+duplicate_faces_removed; roof_uv::consistent_cube_projection; exterior_ground::top_facing_solid_textured; texture_delivery::1024px_key_pbr; landscape::4_trees+18_hedges_retained; visit::start_outside`
- `v18_outdoor_dining_removed_nodes` = `29`
- `v18_roof_objects_rebuilt` = `3`
- `v18_ground_objects_rebuilt` = `3`
- `v18_tree_roots_retained` = `4`
- `v18_hedges_retained` = `18`
- `v18_key_texture_resolution` = `1024`
- `v18_visit_starts_outside` = `True`
- `v18_source_v17_glb_sha256` = `7DDD96CCA202D30F28E1000E715755B679FF53C6776DCA0ACDAD741EB8074F68`

## Répartition géométrique utile au diagnostic

- Préfixes : V11 **416 nœuds / 257 659 triangles**, V10 **165 / 32 460**, V12 **30 / 12 752**, V17 **46 / 7 048**, architecture GF+UF+FRAME **128 / 6 544**, ROOF **3 / 18**, SITE+GROUND+V18 **4 / 208**.
- Signature répétée : **495 nœuds à exactement 188 triangles**, typique des volumes paramétriques/bevelled boxes de ce modèle; **75 nœuds à 12 triangles** et **3 toitures principales à 6 triangles**.
- Les **12 nœuds** portant une provenance `asset_source` totalisent **191 047 triangles (60.3% du modèle)**; leur détail est dans `live-materials.md`.

## Limites de l’inférence

- Les noms, métadonnées et nombres de triangles permettent de distinguer assets sourcés et volumes procéduraux, mais ne prouvent pas à eux seuls la qualité perçue, l’échelle correcte ou l’absence de pénétration entre objets.
- Le hash identique prouve que les deux fichiers locaux sont le même modèle. Il ne prouve pas à lui seul que GitHub/CDN sert ce hash sans contrôle HTTP séparé.
- Les collections Blender (`FURNITURE_EDITABLE`, etc.) ne sont pas conservées comme collections glTF; la mention de non-contractualité existe au niveau scène, mais ne permet pas de classer chaque nœud de mobilier contractuellement.
