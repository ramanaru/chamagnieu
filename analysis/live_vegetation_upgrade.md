# V18 — amélioration réelle de la végétation du Web viewer

## Résultat visé

Le rendu V18 utilisait 18 volumes de haie simples et quatre familles d'arbres composées de troncs/canopées géométriques. L'amélioration remplace ces volumes **dans la vraie scène Web** par des assets PBR Poly Haven optimisés, sans modifier la maison, son implantation, les 18 segments de haie ni les quatre positions d'arbres.

Le remplacement est additionnel et transactionnel au chargement : une famille d'assets d'amélioration ne masque sa famille low-poly qu'après son propre chargement réussi. Ainsi, une erreur réseau sur l'arbre conserve les arbres d'origine; une erreur sur le shrub conserve les haies d'origine.

## Sources, provenance et licence

Le build lit exclusivement les copies sources déjà présentes sous :

`C:\Users\jonat\Documents\Codex\2026-08-14\files-mentioned-by-the-user-c\outputs\Chamagnieu_3D_V10_REALISM_INTERACTIVE\assets\models`

Le manifeste vérifié est :

`C:\Users\jonat\Documents\Codex\2026-08-14\files-mentioned-by-the-user-c\outputs\Chamagnieu_3D_V10_REALISM_INTERACTIVE\assets\ASSET_MANIFEST_V10.json`

| Asset source | Auteur/source | Licence | Fichiers vérifiés | Poids source | Géométrie source |
|---|---|---:|---:|---:|---:|
| `shrub_03` | [Poly Haven](https://polyhaven.com/a/shrub_03) | CC0 1.0 | 5/5 | 1 628 793 octets | 8 287 triangles |
| `island_tree_02` | [Poly Haven](https://polyhaven.com/a/island_tree_02) | CC0 1.0 | 11/11 | 46 172 406 octets | 1 072 213 triangles dans le glTF source (1 072 212 mesurés après import Blender) |

Le validateur recalcule les tailles et SHA-256 de chaque fichier source et les compare au manifeste. Le build inventorie aussi chaque source avant/après conversion; la validation finale donne `CHECK_SOURCE_MANIFEST_HASHES_MATCH=PASS` et `CHECK_BUILD_SOURCE_PRESERVED=PASS`.

## Assets Web produits

| Asset Web | Transformation | Triangles | Meshes / primitives | Textures intégrées | Poids | SHA-256 |
|---|---|---:|---:|---:|---:|---|
| `shared/assets/vegetation/shrub_03_web.glb` | 4 meshes source réunis en un mesh, UV/matériau conservés | 8 287 | 1 / 1 | 3 images, maximum 512×512 | 675 924 octets | `C285AD37DDAA6014347AD1AD8A31311BAC46C384EE0D5F8C5D445186AA7960EE` |
| `shared/assets/vegetation/island_tree_02_web.glb` | séparation par matériau puis décimation contrôlée : tronc 5 000, branches 12 000, feuillage 30 000 | 47 000 | 3 / 3 | 9 images, maximum 512×512 | 4 268 472 octets | `845CD738030743A4592FDC10DB77A38E522E15C8901E6710C377C3D5C303CF76` |

Le poids réseau optionnel total est de **4 944 396 octets**. Le tree Web conserve trois matériaux distincts (tronc, branches, feuilles), les normales et les cartes de rugosité. Le shrub conserve sa couleur avec découpe, sa normale et son ARM/roughness.

Le builder reproductible est `validation/build_v18_web_vegetation.py`. Il utilise Blender 5.2.0 LTS, réduit les images en mémoire à 512 px, exporte deux GLB autonomes et refuse la sortie si un fichier source a changé.

## Remplacement live

Le module `shared/live-vegetation.js` exporte :

```js
await installLiveVegetation({ scene, house, renderer, mobile, cacheKey });
```

Son intégration se fait après l'ajout du GLB principal dans la scène et avant `viewerReady=true`. Le module :

1. recherche les noms réels `V17_TREE_LIGHT_XX_*` et `V17_HEDGE_LIGHT_XX` dans le GLB principal;
2. charge indépendamment les deux GLB optimisés avec un délai maximal de 15 s;
3. règle ombres, double face, rugosité, anisotropie (jusqu'à 8×) et profondeur;
4. place quatre clones d'arbre aux bases des quatre familles existantes, avec taille issue de la boîte englobante existante et rotation déterministe;
5. conserve **18 segments de haie**, mais place **deux rangées décalées de trois clumps par segment**, soit 108 clones shrub;
6. applique aux six clumps de chaque segment une variation déterministe et légère de longueur, hauteur, rotation et décalage longitudinal;
7. utilise `alphaTest = 0.08` pour le shrub, une hauteur `×1.28` et une épaisseur `×0.82` afin de préserver les petites feuilles, densifier la silhouette et supprimer l'effet trop clairsemé;
8. partage les mêmes géométries, textures et matériaux entre tous les clones;
9. masque la famille d'origine uniquement après succès de la famille améliorée.

### Densité et coût réellement affiché

| Famille live | Instances logiques | Clones affichés | Triangles affichés | Draw calls estimés |
|---|---:|---:|---:|---:|
| Arbres | 4 arbres | 4 | 188 000 | 12 |
| Haies | 18 segments | 108 clumps shrubs | 894 996 | 108 |
| **Total optionnel** | **22 implantations** | **112 clones** | **1 082 996** | **120** |

Cette densité reste très inférieure à un chargement direct des quatre arbres sources, qui aurait dépassé 4,28 millions de triangles rien que pour les arbres.

## Téléphone et repli de performance

- Un téléphone moderne reçoit les mêmes assets optimisés : `mode=enhanced-mobile`.
- Si l'utilisateur active l'économie de données (`navigator.connection.saveData`) ou si le navigateur annonce moins de 4 Go via `navigator.deviceMemory`, le module n'émet aucune requête vers les GLB optionnels et conserve la végétation low-poly du modèle principal : `mode=original-low-poly-constrained`.
- Une panne d'un seul asset produit `partial-fallback`; l'autre famille améliorée reste visible.
- Le module ne génère ni exception console ni absence de végétation lors d'un fallback.

## Audit exposé au navigateur

`window.__liveVegetationAudit` et les datasets `viewerVegetation*` exposent au minimum :

- `status`, `mode`, `mobile`, `deviceMemoryGb`, `saveData`;
- `originalTreeFamilies=4`, `originalHedges=18`;
- `treeInstances=4`, `hedgeInstances=18`, `hedgeCloneInstances=108`;
- `displayedTriangles=1082996`, `drawCalls=120`, `loadMs`;
- état, URL, triangles, meshes et erreurs éventuelles pour `tree` et `hedge`;
- `fallbackUsed` et `originalsHidden`.

## Validation réelle

Le harness `validation/vegetation-runtime-harness.html` importe le même module, les deux vrais GLB et une scène synthétique qui utilise les mêmes noms de nœuds que le projet. Le test `validation/run_vegetation_runtime_harness.py` ouvre cette page dans Chrome/WebGL2, vérifie les requêtes et écrit `validation/vegetation-runtime-validation.json`.

Sortie littérale vérifiée après ajout des deux rangées de trois clumps :

```text
VEGETATION_BROWSER_RUNTIME=PASS trees=4 hedge_segments=18 hedge_clones=108 displayed_triangles=1082996 draw_calls=120 load_ms=686 webgl2=True console_errors=0 request_failures=0 http_bad=0 mobile=enhanced mobile_glb_requests=2 constrained=mobile-fallback constrained_glb_requests=0
```

Le temps `load_ms` varie selon le cache et la machine; les compteurs structurels sont déterministes. Le screenshot réel du harness se trouve dans `validation/vegetation-runtime-harness.png`.

Validation asset et syntaxe :

```text
VEGETATION_ASSET_VALIDATION=PASS
VEGETATION_RUNTIME_BUDGET=desktop_trees=188000tris/12draws desktop_hedges=894996tris/108draws
```

Le détail complet, les formats d'images, hashes, seuils et résultats de `node --check` figurent dans `validation/vegetation-asset-validation.txt`.
