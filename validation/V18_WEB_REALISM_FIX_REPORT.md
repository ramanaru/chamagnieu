**Rapport final public — V18 Web Realism**

Ce verdict porte sur l'état public courant réellement exécuté dans le viewer Web à `https://ramanaru.github.io/chamagnieu/`. Les captures finales proviennent de la page publique et portent `SOURCE = LIVE WEB VIEWER`.

**LIVE_VERSION:** `V18` — release `V18-WEB-REALISM-1` — cache key `v18-web-realism-1` — statut de preuve `PUBLIC CURRENT`.

**LIVE_GLB_USED:** `shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb` — `22 687 292` octets — SHA-256 `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E` — GLB 2.0 valide.

**MATERIAL_UPGRADES:** `41` matériaux, `90` textures, `78/78` images WebP intégrées et atteignables, `95/95` bindings PBR valides, aucune URI externe, aucun octet d'image orpheline, aucun bufferView orphelin. Six matériaux dédiés ont été ajoutés pour le canapé, le fauteuil, les chaises, l'écorce et les deux variantes de feuilles; les 2 454 payloads d'accessors géométriques restent byte-identiques à Sync-4.

**ROOF:** Triplet PBR tuile 2K conservé et mieux exploité, relief/AO renforcés, roughness mate contrôlée et éclairage directionnel rendant rangs, pentes, arêtiers et bords plus lisibles.

**FACADE:** Enduit propre de maison neuve avec stuc WebP 2K, micro-AO, roughness `0,88`, normalScale `0,55` et variation lumineuse mieux perceptible; l'uniformité blanche de Sync-4 est réduite sans ajouter de salissure.

**GRASS:** Pack herbe compact 768 px base/normal/MR/AO, tiling 8× et profil mat naturel (`roughness 0,94`, `normalScale 1,05`); la parcelle beige uniforme devient une pelouse verte et nuancée à moyenne distance.

**HEDGES:** `18` emplacements de haie remplacés sur le chemin enhanced par `shrub_03_web.glb`, distribués en deux rangs et `108` clones feuillus; le fallback compact reste disponible pour les appareils contraints.

**TREES:** `4` instances de `island_tree_02_web.glb` remplacent les canopées en boules sur le chemin enhanced, avec tronc ramifié et feuillage séparé; des matériaux fallback écorce/feuilles PBR sont aussi intégrés au GLB principal.

**EXTERIOR_GROUND:** Enrobé charbon mat, gravier clair PBR 768 px, terrasse en dalles pierre PBR et pelouse sont désormais visuellement différenciés par leur albédo, leur échelle, leur normal et leur roughness.

**INTERIOR_FLOOR:** `PBR_B_FLOOR` et `V12_PBR_LIGHT_PORCELAIN` utilisent un pack calcaire 768 px base/normal/MR/AO avec tiling adapté; les carreaux, joints, nuances minérales et reflets doux sont lisibles.

**FURNITURE_MATERIALS:** Le canapé reçoit `V18_WEB_SOFA_WARM_WEAVE`, les fauteuils `V18_WEB_ARMCHAIR_OLIVE_WEAVE`, les six chaises `V18_WEB_DINING_CHAIR_CARAMEL_WEAVE`; chaque tissu dispose de base/normal/MR/AO WebP 512 px. Le chêne de la table est réchauffé et mieux séparé du sol et des assises.

**GLASS:** Tuning physique runtime avec IOR `1,48`, transmission `0,68–0,88`, roughness `0,11–0,16`, réflexion PMREM renforcée et traitement mince transparent; les vitrages gagnent en présence sans voile gris ni ombre opaque.

**LIGHTING:** Pipeline `V18-WEB-REALISM-LIGHTING-R2`: sortie sRGB, ACES Filmic, exposition `0,865`, ciel procédural déterministe + PMREM `0,765`, hemisphere `0,518`, ambient `0,030`, soleil `2,760`, fill `0,158`, rim `0,280`, ombres PCFSoft 2048² desktop et brouillard 78–172 m.

**PERFORMANCE:** Le GLB amélioré mesure `2 482 028` octets de moins que Sync-4. Le viewer public WebGL2 affiche `1 082 996` triangles de végétation, `120` draw calls et charge la végétation en `173 ms` sur la présentation auditée (`162 ms` dans la visite). Le harness reproductible confirme le fallback sans téléchargement optionnel sur appareil 2 Go.

**BEFORE_AFTER_SUMMARY:** Six comparatifs 1440×900 existent dans `validation/live_before_after/`: façade, jardin, sols extérieurs, séjour, sol intérieur et matériaux/cuisine. Onze vues brutes publiques after couvrent façade, générale, jardin, haies, sol extérieur, séjour, cuisine, sol intérieur, étage/portes, départ extérieur et déplacement vers la maison. Chaque composite affiche explicitement `SOURCE = LIVE WEB VIEWER`; les deux côtés viennent des releases publiques correspondantes.

**FINAL_STATUS:** `PASS — PUBLIC CURRENT`. Le modèle public et ses cinq assets critiques sont byte-identiques aux blobs Git; les validations structurelles, GLB, PBR, WebGL2, végétation, visite extérieure et comparatifs live passent. La visite publique répond 108/108 en HTTP 200; la présentation n'a aucune exception JavaScript et les deux seules réponses auxiliaires non-200 observées sont des demandes automatiques du favicon racine GitHub Pages, sans effet sur le viewer.

LIVE_WEB_REALISM_IMPROVED=YES
TEXTURE_QUALITY_IMPROVED=YES
GROUND_REALISM_IMPROVED=YES
VEGETATION_REALISM_IMPROVED=YES
INTERIOR_REALISM_IMPROVED=YES
FINAL_STATUS=PASS
