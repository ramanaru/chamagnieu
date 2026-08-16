**Audit visuel ciblé V18-WEB-REALISM-1**

Les constats et résultats ci-dessous proviennent du viewer Web local courant (`http://127.0.0.1:8899/`) et des captures 1440×900 marquées `SOURCE = LIVE WEB VIEWER`. La publication publique de cette release n'est pas revendiquée dans ce rapport local.

## FACADE

**CURRENT_PROBLEM:** L'enduit extérieur de Sync-4 paraissait blanc, uniforme et peu sensible à la lumière.

**CAUSE:** Le micro-normal du stuc était trop discret, aucune occlusion dédiée n'accentuait le grain et le remplissage lumineux effaçait les faibles variations.

**CORRECTION_APPLIED:** Les cartes stuc WebP 2K ont été conservées, complétées par une micro-AO compacte et réglées avec un profil façade propre (`roughness 0,88`, `normalScale 0,55`, `envMap 0,34`) sous le pipeline LIGHTING-R2.

**RESULT:** La façade reste propre comme une maison neuve, mais son grain, ses arêtes, les tableaux et les différences d'éclairement sont maintenant lisibles dans `01_facade_before_after.png`.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## ROOF

**CURRENT_PROBLEM:** Les tuiles étaient présentes, mais leur relief et leurs creux se confondaient encore sur les pentes.

**CAUSE:** La normal map et l'occlusion contribuaient trop peu, tandis que l'ancien éclairage diffus réduisait le contraste entre rangs de tuiles.

**CORRECTION_APPLIED:** Le triplet PBR tuile 2K a été conservé, son relief a été renforcé, une AO compacte a été intégrée et le profil runtime toiture applique une roughness mate contrôlée avec une lumière solaire plus directionnelle.

**RESULT:** Les rangs, arêtiers, bords et changements de pente se détachent mieux sans rendre la toiture brillante ou artificielle.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## GRASS

**CURRENT_PROBLEM:** La parcelle ressemblait à une surface beige-verte uniforme et ne se lisait pas comme une pelouse.

**CAUSE:** L'albédo herbe précédent était trop brun, la variation était faible et l'éclairage aplatissait la normal map à moyenne distance.

**CORRECTION_APPLIED:** Un pack herbe compact 768 px base/normal/MR/AO a remplacé l'apparence précédente avec un tiling 8×, une teinte plus naturelle et un profil mat (`roughness 0,94`, `normalScale 1,05`).

**RESULT:** La pelouse devient verte, nuancée et texturée à moyenne distance; la différence est visible sur la façade, le jardin et les sols extérieurs.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## HEDGES

**CURRENT_PROBLEM:** Les haies Sync-4 apparaissaient comme une suite de blocs arrondis, répétitifs et peu feuillus.

**CAUSE:** Les 18 volumes fallback réutilisaient des textures 256 px sans normal ni AO et leur silhouette restait strictement low-poly.

**CORRECTION_APPLIED:** Le chemin runtime enhanced charge `shrub_03_web.glb`, conserve les 18 emplacements de haie et distribue 108 clones feuillus en deux rangs; le fallback GLB reste disponible sur appareil contraint ou en cas d'échec réseau.

**RESULT:** Les haies ont davantage de volume, une silhouette moins répétitive et une matière feuillue plus riche; le harness WebGL2 confirme 18 segments et 108 clones sans erreur console ou réseau.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## TREES

**CURRENT_PROBLEM:** Les quatre arbres ressemblaient à des boules vertes sur des troncs simplifiés.

**CAUSE:** Les canopées fallback partageaient les matériaux de haie et ne possédaient ni silhouette ramifiée crédible, ni écorce ou feuillage PBR dédiés.

**CORRECTION_APPLIED:** Le viewer enhanced charge quatre instances de `island_tree_02_web.glb` avec tronc et feuillage séparés; le GLB principal embarque aussi des matériaux écorce et feuilles complets pour son fallback.

**RESULT:** Les quatre arbres présentent des troncs ramifiés, des couronnes irrégulières et des feuilles moins plastiques, clairement visibles dans `02_garden_before_after.png`.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## DRIVEWAY

**CURRENT_PROBLEM:** Enrobé, gravier, terrasse et terrain se mélangeaient dans une masse extérieure claire et uniforme.

**CAUSE:** Les albédo étaient trop proches, certaines textures avaient une mauvaise teinte ou échelle et les micro-reliefs manquaient de contraste.

**CORRECTION_APPLIED:** L'enrobé a reçu un profil charbon mat, le gravier un pack clair 768 px base/normal/MR/AO, et la terrasse un pack de dalles pierre 768 px; les profils runtime séparent leurs roughness, normalScale et réponse environnementale.

**RESULT:** L'accès, les bandes minérales, les dalles et la pelouse sont identifiables comme des zones distinctes dans `03_driveway_before_after.png` et la vue brute `after/exterior-ground.png`.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## INTERIOR_FLOOR

**CURRENT_PROBLEM:** Le sol intérieur était peu lisible et pouvait apparaître comme une grande image claire presque sans joints.

**CAUSE:** L'échelle et le contraste des carreaux étaient insuffisants, sans AO dédiée pour asseoir les joints et le contact du mobilier.

**CORRECTION_APPLIED:** Les matériaux `PBR_B_FLOOR` et `V12_PBR_LIGHT_PORCELAIN` utilisent un pack calcaire compact 768 px base/normal/MR/AO, avec des tilings adaptés et un profil porcelaine plus réactif à l'environnement.

**RESULT:** Les carreaux, joints, nuances minérales et reflets doux sont lisibles dans `05_floor_before_after.png` et `after/interior-floor-materials.png`.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## SOFA

**CURRENT_PROBLEM:** Le canapé partageait le coton de la literie et apparaissait blanc, surexposé et sans trame convaincante.

**CAUSE:** Un matériau textile unique desservait des usages incompatibles et empêchait tout réglage indépendant du séjour.

**CORRECTION_APPLIED:** `V18_WEB_SOFA_WARM_WEAVE` a été créé avec base/normal/MR/AO WebP 512 px et affecté uniquement au canapé, puis réglé comme un tissu taupe chaud et mat.

**RESULT:** Le canapé est distinct de la literie, sa trame et ses volumes sont lisibles et le séjour n'est plus dominé par une masse blanche dans `04_living_before_after.png`.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## CHAIRS

**CURRENT_PROBLEM:** Les six chaises reprenaient le même textile pâle que les lits et le canapé, avec peu de séparation par rapport à la table.

**CAUSE:** Le matériau coton partagé supprimait la hiérarchie chromatique et la micro-texture autour de la table.

**CORRECTION_APPLIED:** `V18_WEB_DINING_CHAIR_CARAMEL_WEAVE` fournit aux six chaises un pack WebP 512 px base/normal/MR/AO dédié, avec une teinte caramel contemporaine; les fauteuils utilisent séparément un tissu olive dédié.

**RESULT:** Les assises et dossiers se détachent du bois et du sol, tandis que l'ensemble reste cohérent et chaleureux.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## TABLE

**CURRENT_PROBLEM:** Le plateau en chêne paraissait pâle, plat et peu différencié des autres surfaces claires.

**CAUSE:** Le bois blanc partagé manquait de chaleur, de relief perçu et d'occlusion dans le nouvel angle de cuisine/séjour.

**CORRECTION_APPLIED:** Le PBR chêne a été conservé mais réchauffé, son relief et sa réponse mate ont été rééquilibrés et une AO compacte a été ajoutée sans modifier la géométrie du meuble.

**RESULT:** Le veinage et l'épaisseur du plateau se lisent mieux, avec une séparation plus nette des chaises et du carrelage.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## GLASS

**CURRENT_PROBLEM:** Les vitrages étaient soit presque invisibles, soit perçus comme des aplats gris peu réalistes.

**CAUSE:** La réflexion environnementale était pauvre, les paramètres alpha/transmission étaient hétérogènes et les ombres des surfaces vitrées pouvaient paraître opaques.

**CORRECTION_APPLIED:** Le tuning runtime emploie un verre physique avec `IOR 1,48`, transmission `0,68–0,88`, roughness `0,11–0,16`, réflexion renforcée et traitement mince transparent; les meshes exclusivement vitrés ne projettent plus d'ombre rectangulaire opaque.

**RESULT:** Fenêtres et baies restent transparentes mais captent le ciel PMREM et conservent une présence visuelle propre, sans voile gris sale.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## LIGHTING

**CURRENT_PROBLEM:** Sync-4 était délavée: ombres remplies, surfaces grisées et faible profondeur générale.

**CAUSE:** Un environnement uniforme fort, une lumière hémisphérique dominante et un brouillard trop proche réduisaient le contraste matériel.

**CORRECTION_APPLIED:** `V18-WEB-REALISM-LIGHTING-R2` applique ACES Filmic, exposition `0,865`, ciel procédural déterministe converti en PMREM (`0,765`), soleil `2,760`, fill `0,158`, rim `0,280`, ambient `0,030`, ombres PCFSoft 2048² desktop et brouillard repoussé à 78–172 m.

**RESULT:** L'image gagne en profondeur, les reliefs PBR deviennent lisibles et les intérieurs restent chaleureux sans noirs bouchés ni hautes lumières brûlées.

**STATUS:** PASS — LOCAL CURRENT — SOURCE = LIVE WEB VIEWER.

## OVERALL_REALISM

**CURRENT_PROBLEM:** La scène Web synchronisée restait visuellement proche d'une maquette: sols uniformes, végétation simplifiée, textiles fades et éclairage plat.

**CAUSE:** Les limites provenaient à la fois du GLB Sync-4 (matériaux partagés et maps insuffisantes), des assets végétaux low-poly et du pipeline de lumière, pas de la version affichée.

**CORRECTION_APPLIED:** Le viewer charge désormais `Chamagnieu_V18_WEB_REALISM_UPGRADED.glb` (41 matériaux, 90 textures, 78 WebP, 95 bindings PBR), LIGHTING-R2 et la végétation enhanced, sans modification des 2 454 payloads d'accessors géométriques.

**RESULT:** Les six comparatifs 1440×900 et les neuf vues brutes locales montrent une amélioration nette de la façade, du jardin, des sols, du séjour, de la cuisine et de l'étage; toutes portent la provenance `SOURCE = LIVE WEB VIEWER`.

**STATUS:** PASS — LOCAL CURRENT; preuve publique V18-WEB-REALISM-1 encore à produire après publication.
