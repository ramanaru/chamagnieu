# Validation métrique et placement des assets — Chamagnieu V18

**État :** `PASS_LOCAL_WITH_NOTED_LIMITS`
**Release :** `V18-ASSET-PILOT-1`
**Référentiel :** Three.js en mètres, ordre des dimensions et positions `[X, Y, Z]`, `Y` vertical.
**Ancrage mobilier :** `HOUSE_REFERENCE_ORIGIN`.
**Architecture :** inchangée; modèle principal toujours `shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb`, 22 687 292 octets, SHA-256 `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E`.

## Méthode

1. Les boîtes englobantes des GLB optimisés sont mesurées dans Three.js.
2. Les dimensions placées sont recalculées à partir de l’échelle réellement appliquée.
3. Le mobilier est positionné par rapport à l’origine existante du logement; l’ancien mobilier n’est masqué qu’après chargement réussi de sa famille.
4. Les végétaux reprennent les boîtes/ancres des objets paysagers déjà présents : la volumétrie architecturale et les ouvertures ne bougent pas.
5. Les matériaux PBR se lient aux matériaux existants, sans créer ni déplacer de paroi, dalle ou toiture.

## Résultat synthétique des huit catégories

| Catégorie | Dimensions source Three.js (m) | Instances / règle | Dimensions placées ou répétition | Résultat |
|---|---:|---:|---|---|
| Canapé | `2.87251 × 1.00537 × 1.01168` | 1, échelle `0.85` | `2.4416 × 0.8546 × 0.8599` | PASS — gabarit 3 places lisible, circulation conservée |
| Table | `2.0000 × 0.7500 × 0.9000` | 1, échelle `0.9 × 1 × 1` | `1.8000 × 0.7500 × 0.9000` | PASS — hauteur repas 0,75 m |
| Chaise | `0.43357 × 0.97338 × 0.57642` | 6, échelle `0.94` | `0.40756 × 0.91498 × 0.54183` chacune | PASS — six chaises orientées vers la table |
| Lit | `1.76223 × 1.06038 × 2.22659` | 3 | `1.6001 × 0.9543 × 2.0000`, puis deux fois `1.4000 × 0.9543 × 2.0000` | PASS local — aucune traversée visible dans les vues validées |
| Arbre | `4.20032 × 3.40825 × 4.06767` | 4 familles dynamiques | Hauteur ajustée à la boîte de chaque famille existante | PASS — implantation d’origine conservée |
| Haie | Web `1.25462 × 0.76171 × 1.25224` | 18 segments, 2 lots GPU | Ajustement à chaque boîte `V17_HEDGE_LIGHT_*` | PASS — limites paysagères conservées |
| Façade PBR | tuile physique source `1.998 × 1.998` | 2 matériaux existants | répétitions `3 × 3` et `6 × 6` | PASS — géométrie/façades inchangées |
| Gazon PBR | taille physique non publiée | 1 matériau existant | répétition empirique `8 × 8` | PASS visuel, limite métrique explicitée |

> Incohérence d’axes résolue pour la haie : le rapport Blender donnait `1.2546 × 1.2522 × 0.7617`; la boîte Web/Three.js validée donne `1.25462 × 0.76171 × 1.25224`. Ce n’est pas un changement de taille, mais la conversion d’axes Blender → glTF/Three.js.

## Mobilier — coordonnées réellement validées

### Séjour

| Objet | Position `[X,Y,Z]` m | Rotation Y | Échelle | Contrôle |
|---|---|---:|---:|---|
| `PILOT_LIVING_SOFA_3_SEAT` | `[2.50, 0.02, -9.78]` | `0` | `[0.85, 0.85, 0.85]` | 1 canapé; ancien nœud masqué après succès |

### Salle à manger

| Objet | Position `[X,Y,Z]` m | Rotation Y (rad) | Échelle | Orientation |
|---|---|---:|---:|---|
| `PILOT_DINING_TABLE` | `[2.50, 0.02, -7.18]` | `0` | `[0.90, 1.00, 1.00]` | centre de la composition |
| `PILOT_DINING_CHAIR_01` | `[2.02, 0.02, -6.46]` | `3.141593` | `0.94` | vers le centre |
| `PILOT_DINING_CHAIR_02` | `[2.98, 0.02, -6.46]` | `3.141593` | `0.94` | vers le centre |
| `PILOT_DINING_CHAIR_03` | `[2.02, 0.02, -7.90]` | `0` | `0.94` | vers le centre |
| `PILOT_DINING_CHAIR_04` | `[2.98, 0.02, -7.90]` | `0` | `0.94` | vers le centre |
| `PILOT_DINING_CHAIR_05` | `[1.25, 0.02, -7.18]` | `1.570796` | `0.94` | vers le centre |
| `PILOT_DINING_CHAIR_06` | `[3.75, 0.02, -7.18]` | `-1.570796` | `0.94` | vers le centre |

La capture `validation/asset_pilot_screenshots/after_live/04-dining-live.png` (`SOURCE = LIVE WEB VIEWER`) confirme l’alignement visuel des six chaises avec la table. Le contrôle est visuel et géométrique; aucune simulation ergonomique normative n’est revendiquée.

### Chambres à l’étage

| Objet | Position `[X,Y,Z]` m | Échelle `[X,Y,Z]` | Dimensions placées `[X,Y,Z]` m |
|---|---|---|---|
| `PILOT_BEDROOM1_BED` | `[4.95, 2.69, -11.65]` | `[0.908, 0.900, 0.898]` | `[1.6001, 0.9543, 2.0000]` |
| `PILOT_BEDROOM2_BED` | `[1.70, 2.69, -8.15]` | `[0.7945, 0.900, 0.898]` | `[1.4000, 0.9543, 2.0000]` |
| `PILOT_BEDROOM3_BED` | `[1.70, 2.69, -5.25]` | `[0.7945, 0.900, 0.898]` | `[1.4000, 0.9543, 2.0000]` |

La capture `validation/asset_pilot_screenshots/after_live/05-bed-live.png` montre une chambre rapprochée avec le lit contenu dans la pièce. Le pilote a validé les trois boîtes placées; une passe future peut encore enrichir les tissus (texture quality du candidat : 4/10).

## Végétation — conservation des implantations

### Arbres

- Quatre familles existantes `V17_TREE_LIGHT_*` fournissent leurs propres boîtes englobantes.
- Chaque arbre réel reprend `X/Z` du tronc existant et `Y` du bas de boîte.
- Échelle uniforme : `hauteur_famille_existante / 3.40825`.
- Rotation : déterministe par identifiant de famille; aucune translation libre du paysage.
- Résultat runtime : 4 instances, 47 000 triangles par source, 12 appels de dessin.

### Haies

- Les 18 boîtes `V17_HEDGE_LIGHT_*` pilotent centre, base, longueur, épaisseur et hauteur.
- La source Web mesure `1.25462 × 0.76171 × 1.25224 m` dans Three.js.
- Variation déterministe : longueur ±1,8 % au maximum, hauteur ±2,4 % au maximum, yaw ±0,024 rad au maximum.
- Deux primitives deviennent deux `InstancedMesh`; 18 matrices par lot, soit 2 appels de dessin pour les haies.
- Résultat : 18 segments logiques, 18 instances, 2 lots GPU; les 18 limites d’origine sont conservées.

## Matériaux — échelle et liaison

| Matériau existant | Source | Répétition | Offset | Normal scale | Remarque |
|---|---|---:|---:|---:|---|
| `V12_PBR_OFFWHITE_STUCCO` | White Stucco | `[3,3]` | `[0,-2]` | `0.42` | tuile source 1,998 m |
| `V10_STUCCO_NEW_BUILD` | White Stucco | `[6,6]` | `[0,-5]` | `0.32` | répétition plus fine sur volume neuf |
| `PBR_B_GRASS` | Grass005 | `[8,8]` | `[0,0]` | `0.72` | taille physique officielle absente; réglage visuel |

Les cartes utilisent `RepeatWrapping`, mipmaps, anisotropie jusqu’à 8, base color sRGB et cartes normal/ARM en espace non colorimétrique. Les trois cartes d’une catégorie doivent toutes charger avant le remplacement; sinon le matériau embarqué reste visible.

## Budgets et limites métriques

- Mobilier : 11 instances, 221 660 triangles affichés, 22 appels de dessin.
- Végétation : 565 892 triangles affichés et 14 appels de dessin, contre 1 082 996 / 120 pour la végétation de référence.
- Grass005 : le service officiel v3 renvoie des dimensions nulles; `8 × 8` est donc un réglage visuel, pas une mesure physique certifiée.
- Le style de l’Island Tree 02 vaut 6/10 pour le contexte suburbain, mais son réalisme vaut 8/10 et il a gagné l’A/B contre l’arbre hivernal téléchargé.
- Le modèle architectural conserve exactement son hash; cette validation couvre les assets de visualisation, pas une conformité de chantier.

## Preuves

- Métriques mobilier : `validation/pilot_furniture_integration.json`, `validation/pilot_furniture_browser.json`
- Matériaux : `validation/pilot_material_integration_validation.json`
- Végétation : `validation/pilot_vegetation_integration.json`, `validation/vegetation-runtime-validation.json`
- Inventaire : `assets_external/ASSET_MANIFEST.json`
