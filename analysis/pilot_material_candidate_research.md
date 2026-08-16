# Phase pilote — recherche officielle de matériaux PBR Web

**Date de vérification :** 2026-08-16
**Périmètre :** enduit de façade propre et pelouse crédible pour Chamagnieu V18; toiture et sol extérieur examinés en option.
**État :** recherche et sélection seulement; aucun asset n’a encore été téléchargé ni intégré.
**Sources :** pages, licences et API officielles uniquement.

## Verdict court

| Besoin | Candidat | Source | Score | Décision |
|---|---|---:|---:|---|
| Façade | **White Stucco** | Poly Haven | **56/60** | **Conserver la source déjà présente**, puis corriger tiling, AO, normal et ARM. Tester `Plaster001` seulement si le rendu reste trop lisse. |
| Pelouse | **Grass005** | ambientCG | **55/60** | **Pilote de remplacement** : pelouse courte, propre, verte et PBR complète. `Grass004` est le repli plus sombre. |
| Toiture, option | **Clay Roof Tiles 03** | Poly Haven | **53/60** | Très bon PBR terre cuite pour une passe suivante; ne remplace pas les corrections de géométrie du toit. |
| Accès/parking, option | **Clean Asphalt** | Poly Haven | **53/60** | PBR sombre fin et crédible, à limiter strictement aux zones prévues par le plan. |

Le diagnostic important est asymétrique : **la façade possède déjà une bonne source PBR**, alors que **la pelouse live utilise une source dont les feuilles brunes et brindilles expliquent précisément l’aspect beige signalé**.

## Méthode et barème

Chaque candidat reçoit six notes sur 10 :

1. `realism` : crédibilité de la matière et absence d’aspect synthétique;
2. `style_match` : adéquation à une maison neuve et un jardin résidentiel à Chamagnieu;
3. `geometry_quality` : pour un matériau 2D, fidélité du relief normal/height/displacement, échelle physique et tileabilité — pas un maillage;
4. `texture_quality` : qualité et complétude des maps PBR, résolutions et conventions normal;
5. `performance` : poids de source, nombre de maps et capacité à produire un profil Web/mobile compact;
6. `license_confidence` : clarté de la licence et compatibilité usage/redistribution Web.

`TOTAL = somme des six critères /60`. Ce sont des scores de présélection documentaire; le `PASS` final dépendra d’un A/B dans le **LIVE WEB VIEWER**.

## Audit des licences et de l’automatisation

### Poly Haven

La [licence officielle Poly Haven](https://polyhaven.com/license) place tous ses HDRI, textures et modèles sous **CC0**. Elle autorise usage commercial, modification, redistribution et inclusion dans un produit sans attribution obligatoire.

L’[API officielle](https://polyhaven.com/our-api) est gratuite, y compris commercialement. Les endpoints `GET /info/{id}` et `GET /files/{id}` donnent métadonnées, URL, tailles, MD5 et dépendances. Deux obligations concernent le **service API live**, pas les assets CC0 :

- afficher un crédit clair à Poly Haven si l’application déployée appelle directement l’API;
- envoyer un `User-Agent` propre à l’application.

Le pipeline recommandé télécharge pendant le build, conserve les URL/licences et sert ensuite les copies locales optimisées. Un crédit Poly Haven dans le manifeste reste recommandé même s’il n’est pas imposé par CC0.

### ambientCG

La [documentation de licence ambientCG](https://docs.ambientcg.com/license/) indique que tous les fichiers téléchargeables et rendus de prévisualisation sont sous **CC0 1.0**. Copie, modification, redistribution, usage commercial et inclusion des fichiers bruts dans un jeu/projet sont permis; l’attribution n’est pas obligatoire.

L’[API officielle v3](https://docs.ambientcg.com/api/v3/) expose `https://ambientcg.com/api/v3/assets`. Les enregistrements consultés publient maps, résolutions, formats, URL et poids. Les URL `https://ambientcg.com/get?file=...` répondent par redirection officielle vers le fichier; les probes `Range: bytes=0-0` ont abouti sans télécharger les archives.

### CGBookcase

Le [catalogue officiel CGBookcase](https://www.cgbookcase.com/textures?category=All) annonce les textures sous **CC0 1.0**, gratuites et utilisables sans crédit. Chaque page de candidat est marquée « free PBR material (cc0 texture) » et liste AO, Base Color, Height, Normal DirectX et Roughness.

Les pages exposent des fichiers sur `cgbookcase-volume.b-cdn.net`. Un GET borné avec `User-Agent` navigateur et `Referer` officiel retourne `206`; un `HEAD` retourne `403`. L’automatisation est donc **moyenne** : télécharger au build, conserver localement, ne pas hotlinker et prévoir un contrôle de taille/hash. Les normals publiées sont DirectX; le canal vert doit être inversé si le pipeline glTF/WebGL attend OpenGL.

## Référence live actuellement en place

| Zone | Matériau live | Source | Constat |
|---|---|---|---|
| Façade | `V12_PBR_OFFWHITE_STUCCO`, `V10_STUCCO_NEW_BUILD` | [Poly Haven White Stucco](https://polyhaven.com/a/white_stucco) | Bonne source fine et chaude déjà présente. Le gain doit venir du branchement PBR complet, de l’échelle UV et de la lumière. |
| Pelouse | `PBR_B_GRASS` | [Poly Haven Leafy Grass](https://polyhaven.com/a/leafy_grass) | Herbe piétinée avec feuilles brunes et brindilles : réaliste en bordure sauvage, mais trop beige pour la pelouse principale. |

## Candidats façade

| Rang | Candidat | Maps / résolutions | Profil automatisable contrôlé | R / S / G / T / P / L | Total | Décision |
|---:|---|---|---|---|---:|---|
| 1 | [White Stucco](https://polyhaven.com/a/white_stucco) · Poly Haven · CC0 | Diffuse, AO, ARM, roughness, normal GL/DX, displacement; 1K–8K; échelle 1,998 m | API `/files/white_stucco`; glTF 2K + dépendances 10 116 001 o, dont 7 742 799 o d’images utiles | 9 / 10 / 9 / 10 / 8 / 10 | **56** | **Primaire : conserver et retuner** |
| 2 | [Plaster001](https://ambientcg.com/a/Plaster001) · ambientCG · CC0 | Color, displacement, normal, roughness; JPG/PNG 1K–8K | `Plaster001_2K-JPG.zip`, 26 140 483 o | 8 / 9 / 8 / 9 / 7 / 10 | **51** | A/B si White Stucco reste trop lisse |
| 3 | [White Stucco Wall 03](https://www.cgbookcase.com/textures/white-stucco-wall-03) · CGBookcase · CC0 | AO, Base Color, Height, Normal DX, Roughness; 1K–4K | `WhiteStuccoWall03_MR_2K.zip`, 25 941 850 o; GET avec Referer | 8 / 9 / 8 / 9 / 7 / 10 | **51** | Alternative; convertir normal DX |
| 4 | [White Plaster 02](https://polyhaven.com/a/white_plaster_02) · Poly Haven · CC0 | Diffuse, AO, ARM, roughness, normal GL/DX, displacement/bump; 1K–8K; 1 m | API `/files/white_plaster_02`; glTF 2K + dépendances 9 925 375 o | 8 / 8 / 7 / 9 / 8 / 10 | **50** | Repli propre mais plus plat |

### Choix façade

`White Stucco` montre un grain fin, des pores subtils et une teinte blanc cassé chaude cohérente avec une maison neuve. Il est déjà utilisé : le remplacer immédiatement ajouterait du risque sans résoudre le mauvais wiring. Le pilote doit d’abord :

- vérifier que diffuse, normal GL et ARM atteignent réellement le matériau visible;
- calibrer le tiling avec l’échelle physique d’environ 2 m;
- limiter l’intensité normal pour éviter un crépi surdimensionné;
- comparer façade rapprochée et vue générale sur desktop/téléphone;
- lancer seulement ensuite un A/B contre `Plaster001`.

## Candidats pelouse

| Rang | Candidat | Maps / résolutions | Profil automatisable contrôlé | R / S / G / T / P / L | Total | Décision |
|---:|---|---|---|---|---:|---|
| 1 | [Grass005](https://ambientcg.com/a/Grass005) · ambientCG · CC0 | Color, displacement, normal, roughness, AO; JPG/PNG 1K–8K | `Grass005_2K-JPG.zip`, 39 523 019 o | 9 / 10 / 9 / 10 / 7 / 10 | **55** | **Pilote primaire** |
| 2 | [Grass004](https://ambientcg.com/a/Grass004) · ambientCG · CC0 | Color, displacement, normal, roughness, AO; 1K–8K; échelle 1,4 m | `Grass004_2K-JPG.zip`, 39 900 302 o | 9 / 9 / 9 / 10 / 7 / 10 | **54** | Repli plus sombre/luxuriant |
| 3 | [Leafy Grass](https://polyhaven.com/a/leafy_grass) · Poly Haven · CC0 | Diffuse, AO, ARM, roughness, normal GL/DX, displacement, mask; 1K–8K; 2 m | API `/files/leafy_grass`; glTF 2K + dépendances 17 303 259 o | 8 / 4 / 9 / 10 / 6 / 10 | **47** | Écarter de la pelouse; garder en bordure sauvage |
| 4 | [Grass 01](https://www.cgbookcase.com/textures/grass-01) · CGBookcase · CC0 | AO, Base Color, Height, Normal DX, Roughness; 1K–2K | `Grass01_MR_2K.zip`, 34 906 867 o; GET avec Referer | 7 / 6 / 7 / 9 / 7 / 10 | **46** | Écarter : trop pâle/sec |

### Choix pelouse

`Grass005` est le meilleur pilote : les tags officiels le décrivent comme propre, vert, court et destiné à une pelouse. `Grass004`, explicitement suburbain/jardin/luxuriant, forme un excellent A/B plus sombre. Le ZIP 2K n’est jamais un payload runtime : la phase suivante doit extraire les maps, vérifier la convention normal, produire des WebP/KTX2 ou équivalents locaux et conserver un profil mobile 1K si nécessaire.

Pour éviter un grand tapis répétitif, le matériau live devra combiner :

- tiling principal à échelle physique;
- macro-variation couleur très douce à basse fréquence;
- roughness élevée et normal mesuré;
- transition contrôlée vers bordures/terre, où `Leafy Grass` peut éventuellement rester;
- aucune texture chargée depuis un CDN tiers au runtime.

## Options toiture et sol extérieur

| Rang | Usage | Candidat | Maps / profil | Score | Décision |
|---:|---|---|---|---:|---|
| 1 | Toiture | [Clay Roof Tiles 03](https://polyhaven.com/a/clay_roof_tiles_03) · Poly Haven · CC0 | Diffuse, AO/ARM, roughness, normal GL/DX, displacement; 1K–8K; 2,6 m; glTF 2K 12 423 671 o | **53/60** | Passe suivante après correction du toit |
| 2 | Accès/parking | [Clean Asphalt](https://polyhaven.com/a/clean_asphalt) · Poly Haven · CC0 | Diffuse, AO/ARM, roughness, normal GL/DX, displacement; 1K–8K; 2,1 m; glTF 2K 13 073 081 o | **53/60** | Primaire sol minéral |
| 3 | Accès/parking | [Asphalt 01](https://www.cgbookcase.com/textures/asphalt-01) · CGBookcase · CC0 | AO, Base Color, Height, Normal DX, Roughness; ZIP MR 2K 35 399 047 o | **49/60** | Alternative plus lourde |

## Probes d’URL sans téléchargement d’asset

| Source | Métadonnées/page | Fichier borné | Résultat |
|---|---|---|---|
| Poly Haven | `info` et `files` pour 5 IDs | descripteurs glTF en `Range: bytes=0-0` | API `200`; fichier `206`; confiance **haute** |
| ambientCG | API v3 pour 3 IDs | `/get?file=...` puis `Range: bytes=0-0` | API `200`; redirection `302`; fichier `206`; confiance **haute** |
| CGBookcase | 3 pages officielles | CDN avec User-Agent/Referer et `Range: bytes=0-0` | page `200`; fichier `206`; `HEAD 403`; confiance **moyenne** |

Aucune archive, image de map ou scène glTF n’a été téléchargée : seuls les contenus de pages/API et un octet de contrôle par URL ont été lus.

## Plan de phase suivante

1. Conserver les fichiers live et leurs hashes; ne modifier qu’une copie de travail.
2. Pour la façade, **ne rien télécharger d’abord** : contrôler le wiring actuel de `white_stucco`, corriger UV/normal/ARM et mesurer l’image.
3. Télécharger seulement `Grass005_2K-JPG.zip` via l’URL officielle, vérifier taille/hash, extraire dans une zone source immuable et enregistrer la licence.
4. Convertir les maps en profil Web local; garder `PBR_B_GRASS` comme fallback et utiliser `Leafy Grass` uniquement sur zones sauvages si utile.
5. Produire A/B desktop + téléphone dans le vrai viewer; vérifier réseau 200, console, chargement, tiling, couleur, normal, FPS et mémoire.
6. Tester `Grass004` ou `Plaster001` uniquement si le candidat primaire n’apporte pas un gain visuel net.

## Verdict de recherche

```text
FACADE_CLEAR_LICENSE_CANDIDATES=4
GRASS_CLEAR_LICENSE_CANDIDATES=4
OPTIONAL_ROOF_GROUND_CANDIDATES=3
PRIMARY_FACADE=Poly Haven White Stucco / CC0 / 56/60 / RETAIN_AND_RETUNE
PRIMARY_GRASS=ambientCG Grass005 / CC0 / 55/60 / PILOT_REPLACEMENT
CURRENT_LEAFY_GRASS_MAIN_LAWN=REJECT
ASSET_BODY_DOWNLOADED=NO
INTEGRATION_PERFORMED=NO
```
