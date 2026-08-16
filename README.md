# Maison de Chamagnieu — V18

Ce dépôt public présente la maison neuve de Chamagnieu dans un format directement lisible par GPT : description textuelle, images intégrées, données JSON et modèle 3D.

## Voir la maison

[**Ouvrir la page propre de la maison**](https://ramanaru.github.io/chamagnieu/) · [Commencer dehors et entrer](https://ramanaru.github.io/chamagnieu/visite/) · [Présentation 3D](https://ramanaru.github.io/chamagnieu/presentation/) · [Dépôt GitHub lisible par GPT](https://github.com/ramanaru/chamagnieu)

### Façade, toiture complète et sols extérieurs

![Façade de la maison de Chamagnieu avec toiture complète en tuiles et sols extérieurs texturés](images/v18-facade-roof-ground.webp)

`SOURCE = BLENDER` — rendu de référence, distinct de la vraie scène Web.

### Jardin, textures et façade arrière

![Jardin et façade arrière de la maison de Chamagnieu avec textures de sol et vue sur l'intérieur](images/v18-jardin-textures.webp)

`SOURCE = BLENDER` — rendu de référence, distinct de la vraie scène Web.

## Ce qui est visible dans cette version pilote

- Trois volumes de toiture fermés avec des tuiles terre cuite texturées.
- Des sols extérieurs différenciés : pelouse, enrobé et gravier.
- Un canapé trois places, une table de six personnes, six chaises assorties et trois lits issus de bibliothèques CC0, optimisés et placés à l’échelle métrique.
- Quatre arbres Poly Haven et dix-huit segments de haie BlenderKit, optimisés et instanciés dans l’environnement live.
- Deux familles de matériaux PBR CC0 : enduit de façade White Stucco et pelouse Grass005, chacune avec Base Color, Normal et ARM.
- La table extérieure parasite a été supprimée.
- La visite interactive commence à l'extérieur et permet d'entrer dans la maison.

## Fichiers directs pour GPT

- [Description structurée `house.json`](house.json)
- [Image façade/toiture brute](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/images/v18-facade-roof-ground.webp)
- [Image jardin/textures brute](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/images/v18-jardin-textures.webp)
- [Modèle 3D GLB réellement chargé](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb)
- [Configuration centrale du viewer](shared/project-config.json)
- [Audit de synchronisation V18](audit/version-sync-report.md)
- [Manifeste complet des assets](assets_external/ASSET_MANIFEST.json)
- [Licences et provenance](assets_external/ASSET_LICENSES.md)
- [Verdict du pilote dans le vrai viewer V18](validation/ASSET_REALISM_INTEGRATION_REPORT.md)
- [Comparaisons avant/après — SOURCE = LIVE WEB VIEWER](validation/asset_pilot_screenshots/comparisons/)

Version : `V18-ASSET-PILOT-1`<br>
Modèle GLB : `22 687 292 octets`<br>
SHA-256 : `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E`

## Sources visuelles

- Les pages `/presentation/` et `/visite/` affichent le modèle Web et les huit catégories pilotes, avec le badge **`SOURCE = LIVE WEB VIEWER`**.
- Les images de cette page et de `/rapide/` sont des rendus de référence et portent le badge **`SOURCE = BLENDER`** dans le site.
- Les deux sources restent volontairement séparées : les WebP de galerie ne sont pas des textures du GLB. Le modèle architectural live reste inchangé ; les meubles, la haie et les six cartes PBR pilotes sont des ressources Web locales explicitement testées avec repli par famille.
