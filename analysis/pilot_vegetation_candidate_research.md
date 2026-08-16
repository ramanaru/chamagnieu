# Phase pilote — recherche officielle d’assets végétation Web

**Date de vérification :** 2026-08-16
**Périmètre :** un arbre réaliste Web et une haie/un buisson réaliste pour Chamagnieu V18.
**État :** recherche et sélection seulement; aucun candidat n’a encore été téléchargé ni intégré.
**Sources utilisées :** pages, licences et API officielles uniquement.

## Verdict court

| Besoin | Candidat pilote | Source | Score | Pourquoi |
|---|---|---:|---:|---|
| Arbre | **Decorative Urban Tree** | BlenderKit | **51/60** | Silhouette urbaine/résidentielle de 6,24 m, 29 641 faces publiées, CC0, variante Blend 1K de 8,06 Mo. Plus adaptée que l’actuel arbre côtier. |
| Haie/buisson | **Shrub** | BlenderKit | **51/60** | Buisson de jardin de 1,25 × 1,26 × 0,77 m, 15 980 faces publiées, feuillage transparent, CC0, Blend 1K de 1,33 Mo. |

Le pilote doit conserver `island_tree_02_web.glb` et `shrub_03_web.glb` comme replis tant que les remplaçants n’ont pas passé l’import, l’optimisation, la mesure réelle du GLB et l’inspection du **LIVE WEB VIEWER**.

## Méthode et barème

Chaque candidat reçoit six notes sur 10 :

1. `realism` : silhouette, tronc/branches/feuillage et crédibilité en vue rapprochée;
2. `style_match` : adéquation à un jardin résidentiel de Chamagnieu plutôt qu’à un décor côtier, tropical ou désertique;
3. `geometry_quality` : topologie déclarée, densité, dimensions et possibilité de produire un LOD Web propre;
4. `texture_quality` : UV, alpha et cartes diffuse/normal/roughness/ARM disponibles;
5. `performance` : coût géométrique, poids fourni, nombre d’instances nécessaire et travail d’optimisation restant;
6. `license_confidence` : licence explicite sur la page officielle et compatibilité redistribution Web.

`TOTAL = somme des six critères /60`. Les notes sont une présélection documentaire. Elles ne constituent pas encore un `PASS` d’intégration.

## Vérification des licences

### Poly Haven

La [licence officielle Poly Haven](https://polyhaven.com/license) indique que tous ses HDRI, textures et modèles 3D sont sous **CC0**. Elle autorise explicitement tout usage, y compris commercial, ne demande pas d’attribution et autorise la redistribution ou l’inclusion dans un produit. Les candidats Poly Haven sont donc compatibles avec un GLB embarqué dans une application Web publique.

Les métadonnées et téléchargements sont automatisables via les API officielles `https://api.polyhaven.com/info/{asset}` et `https://api.polyhaven.com/files/{asset}`. L’API `files` publie les URL directes, tailles et MD5 des fichiers. Aucun téléchargement n’a été déclenché pendant cette recherche.

### BlenderKit

La [page officielle des licences BlenderKit](https://www.blenderkit.com/docs/licenses/) distingue `Royalty Free` et `CC0`. Les deux candidats retenus affichent explicitement **Creative Commons Zero** sur leur page et `license=cc_zero`, `isFree=true`, `canDownload=true` dans l’API officielle.

L’[add-on officiel BlenderKit](https://github.com/BlenderKit/BlenderKit) annonce le téléchargement de plus de 10 000 modèles gratuits sans connexion. Les endpoints de téléchargement existent dans les enregistrements API des deux candidats; ils seront appelés par l’outil officiel pendant la phase suivante, pas pendant cette recherche.

Les assets BlenderKit seulement `Royalty Free` sont écartés du pilote public : la [FAQ officielle](https://www.blenderkit.com/docs/licenses/licensing-faq/) conditionne l’usage dans un jeu au fait que l’asset ne soit pas facilement extractible. Un GLB public l’est. Seuls les candidats `CC0` sont donc retenus sans revue juridique manuelle.

## Référence actuelle mesurée dans le projet

| Famille | Asset actuel | Mesure réelle du GLB | Qualité | Score |
|---|---|---|---|---:|
| Arbre | `shared/assets/vegetation/island_tree_02_web.glb` | 4 268 472 octets; 47 000 triangles; 3 meshes/primitives; 3 matériaux; 9 textures embarquées; 0 URI externe | Source photogrammétrique crédible et bonne performance, mais silhouette côtière, basse et très étalée. | **48/60** = 8 + 6 + 7 + 8 + 9 + 10 |
| Haie | `shared/assets/vegetation/shrub_03_web.glb` | 675 924 octets; 8 287 triangles; 1 mesh; 1 matériau; 3 textures embarquées; 0 URI externe | Le modèle est un couvre-sol de prairie. Les 108 clones live totalisent 894 996 triangles et environ 108 draw calls, avec répétition visible. | **39/60** = 6 + 4 + 7 + 7 + 5 + 10 |

Sources actuelles : [Island Tree 02](https://polyhaven.com/a/island_tree_02) et [Shrub 03](https://polyhaven.com/a/shrub_03), tous deux CC0.

## Candidats arbre

### Classement

| Rang | Candidat | Auteur | Licence | Formats / poids pertinent | Géométrie et textures | R / S / G / T / P / L | Total | Décision |
|---:|---|---|---|---|---|---|---:|---|
| 1 | [Decorative Urban Tree](https://www.blenderkit.com/asset-gallery-detail/c8af7417-b4d3-4cff-8a7a-b0afdb5a577f/) | Davide Tirindelli | CC0; attribution non requise; redistribution et commercial autorisés | Blend, GLB, Godot GLB; GLB stock 146 996 520 o; Blend 1K 8 062 649 o; Blend 0,5K 3 443 031 o | 29 641 faces publiées, 4 objets, 3,60 × 4,54 × 6,24 m; 20 textures, 1080–4096 px; UV, Principled + translucence | 9 / 9 / 8 / 8 / 7 / 10 | **51** | **Pilote primaire** |
| 2 | [Tree Small 02](https://polyhaven.com/a/tree_small_02) | Rico Cilliers | CC0 | Blend, glTF, USD, FBX; package glTF 1K 100 974 143 o | 4 652 585 triangles, 2,92 × 4,29 × 4,65 m; 9 textures PBR dans le glTF 1K, source 8K | 9 / 8 / 9 / 9 / 2 / 10 | **47** | Repli haute définition, décimation lourde requise |
| 3 | [Jacaranda Tree](https://polyhaven.com/a/jacaranda_tree) | Rico Cilliers; Rob Tuytel | CC0 | Blend, glTF, USD, FBX; package glTF 1K 214 609 299 o | 312 356 triangles publiés, 24,17 × 18,03 × 19,83 m; 9 textures PBR dans le glTF 1K, source 8K | 9 / 6 / 8 / 9 / 3 / 10 | **45** | Variation lointaine seulement; hors échelle actuelle |
| 4 | [Island Tree 01](https://polyhaven.com/a/island_tree_01) | Rob Tuytel; Rico Cilliers | CC0 | Blend, glTF, USD, FBX; package glTF 1K 66 337 268 o | 3 729 692 triangles, 12,46 × 4,82 × 5,03 m; 9 textures PBR 1K, source 8K | 9 / 5 / 9 / 9 / 3 / 10 | **45** | Non retenu : même langage côtier que l’actuel, beaucoup plus lourd |

### Pourquoi `Decorative Urban Tree` passe devant l’actuel

- sa forme verticale et sa hauteur réelle de 6,24 m correspondent mieux à un arbre de jardin/voirie résidentielle;
- les 29 641 faces publiées sont déjà proches d’un budget Web, contre 1,76 million de triangles à la source pour `Island Tree 02`;
- la page officielle lui donne une qualité 10/10 et une licence CC0;
- une source Blend 1K de 8,06 Mo permet d’éviter le GLB stock de 146,99 Mo;
- le candidat dérive d’un arbre Poly Haven CC0, mais a déjà reçu une simplification urbaine par Davide Tirindelli.

Contrôles obligatoires après téléchargement : supprimer les objets/matériaux de sol superflus, vérifier les 20 textures, préserver l’alpha et la translucence des feuilles, mesurer les triangles après export, embarquer les textures et viser `<= 45k triangles` et `<= 5 Mo`.

## Candidats haie / buisson

| Rang | Candidat | Auteur | Licence | Formats / poids pertinent | Géométrie et textures | R / S / G / T / P / L | Total | Décision |
|---:|---|---|---|---|---|---|---:|---|
| 1 | [Shrub](https://www.blenderkit.com/asset-gallery-detail/2810ce15-1076-44e6-9b95-90487f8d5dc5/) | Blendkit Community | CC0; attribution non requise; redistribution et commercial autorisés | Blend; Blend 1K 1 327 924 o; Blend 0,5K 1 119 294 o | 15 980 faces publiées, quad-dominant, 1 objet, 1,25 × 1,26 × 0,77 m; UV, 2K, Principled/mix/translucent/transparent | 8 / 8 / 8 / 8 / 9 / 10 | **51** | **Pilote primaire** |
| 2 | [Shrub 02](https://polyhaven.com/a/shrub_02) | Rico Cilliers | CC0 | Blend, glTF, USD, FBX; package glTF 1K 1 966 425 o | 52 317 triangles; 5,34 × 2,06 × 2,07 m; diffuse + normal GL + ARM 1K, alpha/AO/displacement/roughness disponibles | 8 / 7 / 8 / 9 / 7 / 10 | **49** | Repli en module long; éviter l’étirement uniforme |
| 3 | [Shrub 04](https://polyhaven.com/a/shrub_04) | Rico Cilliers | CC0 | Blend, glTF, USD, FBX; package glTF 1K 1 907 514 o | 47 813 triangles; 0,75 × 0,19 × 0,28 m; diffuse + normal GL + ARM 1K, alpha/AO/displacement/roughness disponibles | 8 / 6 / 8 / 9 / 6 / 10 | **47** | Variation/filler clairsemé; trop coûteux comme unique haie |

### Pourquoi `Shrub` passe devant l’actuel

- sa forme est un buisson de jardin de 0,77 m de haut, pas un couvre-sol de prairie;
- le feuillage est conçu avec transparence/translucence et une texture 2K;
- 15 980 faces publiées restent compatibles avec un GLB Web compact;
- le Blend 1K ne pèse que 1,33 Mo;
- deux ou trois variantes déterministes par segment, rendues par instancing GPU, peuvent casser la répétition sans conserver 108 draw calls.

Le shader Blender devra être converti en matériau PBR Web avec alpha. Le vrai compte de triangles après triangulation reste un gate : `faceCount=15 980` est la mesure du fournisseur, pas encore le nombre de triangles du GLB final.

## Assets écartés par la licence ou le coût

| Asset | Source | État | Motif |
|---|---|---|---|
| Tree LOD 2 | BlenderKit | `MANUAL_LICENSE_REVIEW_REQUIRED` | Gratuit mais `Royalty Free`; un GLB public est extractible. |
| Wild Alpine Shrub Evergreen | BlenderKit | `MANUAL_LICENSE_REVIEW_REQUIRED` | Gratuit mais `Royalty Free`, donc non retenu pour redistribution brute Web. |
| Realistic Tree | BlenderKit | `SKIP` | Page officielle marquée Full Plan. |
| [Shrub 01](https://polyhaven.com/a/shrub_01) | Poly Haven | `NOT_SHORTLISTED` | CC0 mais 282 224 triangles, glTF 1K de 6,88 Mo et forme florale basse peu adaptée à une haie. |

## Plan de téléchargement contrôlé suivant

1. Télécharger **uniquement** le Blend 1K officiel de `Decorative Urban Tree` et le Blend 1K officiel de `Shrub` en conservant les originaux immuables.
2. Recalculer SHA-256, tailles, objets, matériaux, textures, faces et triangles; compléter le manifeste de licences.
3. Produire un GLB Web indépendant avec textures intégrées et sans matériaux/objets inutilisés.
4. Garder les deux assets actuels comme fallback; ne masquer l’ancienne famille qu’après chargement réussi du remplacement.
5. Faire un A/B dans le vrai `LIVE WEB VIEWER`, vérifier réseau HTTP 200, console, transparence du feuillage, échelle, implantation, absence de traversée et `>= 30 FPS`.
6. N’accepter le remplacement qu’avec un gain visuel net; sinon tester `Tree Small 02` décimé ou `Shrub 02` sans supprimer le fallback.

## Verdict de recherche

```text
TREE_CANDIDATES_WITH_CLEAR_FREE_LICENSE=4
HEDGE_CANDIDATES_WITH_CLEAR_FREE_LICENSE=3
PRIMARY_TREE=BlenderKit Decorative Urban Tree / CC0 / 51/60
PRIMARY_HEDGE=BlenderKit Shrub / CC0 / 51/60
CURRENT_TREE_RETAINED_AS_FALLBACK=YES
CURRENT_HEDGE_RETAINED_AS_FALLBACK=YES
DOWNLOAD_PERFORMED=NO
INTEGRATION_PERFORMED=NO
RESEARCH_STATUS=READY_FOR_CONTROLLED_DOWNLOAD_AND_IMPORT
```
