# Verdict de synchronisation — Chamagnieu V18

Date de validation : 2026-08-15 (Europe/Paris)  
Branche corrigée : `agent/v18-live-sync`  
Release unique : `V18-LIVE-SYNC-3`  
Configuration centrale : `shared/project-config.json`

## Résultat demandé

| Champ | Valeur vérifiée |
|---|---|
| `PUBLIC_REPO_VERSION` | `V18-LIVE-SYNC-3` — commit publié `fbe3696b6db32710c0036890cbef70d34b6ef1bd` |
| `LIVE_VIEWER_VERSION` | `V18` sur `/presentation/` et `/visite/`; les cinq pages lisent la même configuration |
| `LIVE_GLB` | `shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3` |
| `LIVE_TEXTURES` | 56 objets glTF; 55 référencés; 37 images JPEG, toutes embarquées dans le BIN; 0 chemin externe |
| `LIVE_MATERIALS` | 35 matériaux; 20 texturés; 15 couleur/facteurs PBR seulement; 795/795 primitives ont UV, normales et matériau |
| `LIVE_VEGETATION` | 4 arbres et 18 haies présents; feuillages 256² base-color-only, opaques, low-poly |
| `LIVE_FURNITURE` | 167 nœuds glTF nommés, développés en 169 meshes runtime et tous contrôlés par le bouton; 12 assets détaillés à provenance Poly Haven, reste majoritairement procédural |
| `LIVE_LIGHTING` | IBL procédurale PMREM, tone mapping ACES Filmic, exposition 0,92, Hemisphere 0,72, Ambient 0,06, Directional 2,4, fill 0,22, ombres desktop 2048 |
| `CACHE_STATUS` | `PASS` — modèle au nom versionné, query `release=v18-live-sync-3`, configuration fetchée avec `cache: no-store`, aucun service worker ni Cache Storage |
| `CONSOLE_STATUS` | `PASS` sur le parcours navigateur live release 2; le correctif release 3 limité au toggle mobilier passe syntaxe et classification structurelle |
| `NETWORK_STATUS` | `PASS` — modèle, scripts, JSON, images de pages et 37 blobs d’images GLB chargés; aucun `loadingFailed`, 404 ou CORS |
| `PRESENTATION_MATCH` | `PARTIAL` — même géométrie V18 et mêmes textures intégrées, mais éclairage Web, végétation low-poly et géométrie procédurale diffèrent des rendus Blender |
| `FINAL_STATUS` | `PARTIAL` — la synchronisation technique est corrigée; la fidélité photoréaliste aux images de galerie n’est pas totale |

## Preuve d’identité du modèle

| Fichier | Octets | SHA-256 |
|---|---:|---|
| `shared/Chamagnieu_V18_REALISM_FINAL.glb` (live) | 27 987 896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` |
| `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb` (alias historique) | 27 987 896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` |

Les deux fichiers sont byte-identiques. Le nouveau nom rend la version réellement chargée non ambiguë sans modifier la géométrie V18 auditée.

## Pages ouvertes et vérifiées

| Page | Version centrale | Viewer | Modèle live | Source affichée | Résultat |
|---|---|---|---|---|---|
| `/` | `V18 / V18-LIVE-SYNC-3` | galerie/accueil | aucun GLB | `SOURCE = BLENDER` sur les deux références | PASS |
| `/presentation/` | `V18 / V18-LIVE-SYNC-3` | WebGL | `Chamagnieu_V18_REALISM_FINAL.glb` | `SOURCE = LIVE WEB VIEWER` | PASS |
| `/visite/` | `V18 / V18-LIVE-SYNC-3` | WebGL, départ extérieur | `Chamagnieu_V18_REALISM_FINAL.glb` | `SOURCE = LIVE WEB VIEWER` | PASS |
| `/rapide/` | `V18 / V18-LIVE-SYNC-3` | galerie | aucun GLB | neuf badges `SOURCE = BLENDER` | PASS |
| `/gpt/` | `V18 / V18-LIVE-SYNC-3` | page statique lisible | lien vers le GLB live | politique de source explicitée | PASS |

Preuves machine : `validation/live-browser-validation.json` pour le parcours visuel/console release 2 et `validation/verify_v18_runtime.py` pour les cinq routes et les octets publics release 3. Le passage release 3 ne modifie aucun réglage visuel; il propage le toggle aux enfants de deux nodes multi-primitives et change la clé de cache.

## Textures et HTTP

Les textures réellement utilisées par les matériaux sont embarquées dans le GLB via `bufferView`. Elles n’ont donc pas d’URL HTTP individuelle : le seul transfert HTTP est celui du GLB, qui contient les 37 JPEG.

| Ressource | URL runtime | HTTP | Octets | Utilisation | Statut |
|---|---|---:|---:|---|---|
| Modèle + 37 images intégrées | `../shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3` | 200 | 27 987 896 | 35 matériaux, 795 primitives | PASS |
| Configuration | `../shared/project-config.json` | 200 | contrôlé par le navigateur | version, modèle, sources, éclairage | PASS |
| Références WebP | `shared/gallery/*.webp?release=v18-live-sync-3` | 200 | voir Network | galerie uniquement, jamais appliquées au GLB | PASS |

Le détail des 37 images, de leur taille, de leur hash court et des matériaux consommateurs figure dans `audit/texture-path-report.md`.

## Pourquoi « V11 » pouvait encore apparaître

1. Le modèle V18 est cumulatif et conserve 416 noms de nœuds préfixés `V11`; ce préfixe décrit l’étape historique de création des objets, pas la version chargée par le viewer.
2. Avant correction, la version et le chemin du GLB étaient codés séparément dans plusieurs pages, `/rapide/` avait encore un titre V16 et les URLs utilisaient un ancien token `v18a`; un onglet ancien pouvait donc présenter un libellé incohérent.
3. Après correction, toutes les pages lisent `shared/project-config.json`, affichent `V18`, utilisent la release `V18-LIVE-SYNC-3`, et les deux viewers chargent le même nom de GLB.
4. Aucun service worker et aucun fallback V11/lite n’ont été trouvés.

## Pourquoi les images de présentation restent plus réalistes

- Les WebP sont des rendus raster Blender/Eevee avec éclairage et post-traitement déjà calculés; elles ne sont pas des maps PBR du GLB.
- Le live contient bien ses 37 images intégrées, mais 15/35 matériaux n’ont aucune texture.
- 495 objets partagent une géométrie procédurale de 188 triangles; les toitures et sols restent des volumes simples.
- Les 4 arbres et 18 haies utilisent une végétation V17 volontairement légère; aucun arbre botanique photoréaliste équivalent aux références n’est présent.
- Le viewer Web emploie maintenant une IBL PMREM et ACES, mais pas une HDRI photographique ni le moteur Blender/D5.

## Mobilier et contrôle de visibilité

Le correctif de bouton inclut désormais les préfixes historiques `V11_` et `V12_`. Le test live donne :

```text
furnitureState count=169 ready=true visible=true
furnitureHidden button=Afficher les meubles count=169 visible=false
furnitureRestored button=Masquer les meubles count=169 visible=true
result=PASS
```

Le GLB contient 167 nœuds classés mobilier. `V11_LIVING_ARMCHAIR` et `V12_LIVING_ARMCHAIR_2` ont chacun deux primitives, que `GLTFLoader` développe en quatre meshes enfants. Le flag mobilier est maintenant propagé aux enfants : les 169 meshes runtime sont masqués puis restaurés.

## Sources des captures

- `validation/live-v18-facade.png` — `SOURCE = LIVE WEB VIEWER`, capture release 2
- `validation/live-v18-garden.png` — `SOURCE = LIVE WEB VIEWER`, capture release 2
- `validation/live-v18-interior.png` — `SOURCE = LIVE WEB VIEWER`, capture release 2
- `audit/presentation-vs-live/reference-vs-live-*.png` — panneaux explicitement séparés `SOURCE = BLENDER` et `SOURCE = LIVE WEB VIEWER`

La release publique 3 sert le même GLB, le même pipeline de matériaux et le même éclairage que ces captures; son unique changement visuel potentiel est la disparition correcte des enfants de fauteuils lorsque l'utilisateur clique « Masquer les meubles ».

## Verdict littéral

```text
LIVE_VIEWER_USES_V18=YES
LIVE_TEXTURES_WORK=YES
LIVE_ASSETS_MATCH_PRESENTATION=NO
LIVE_VIEWER_REALISM_STATUS=PARTIAL
```

`PARTIAL` est volontairement honnête : l’erreur de synchronisation/version/cache est corrigée et les textures live fonctionnent, mais le modèle Web actuel ne contient pas tous les assets, la végétation et le pipeline lumineux photoréalistes suggérés par les rendus de présentation.
