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

## Ce qui est visible dans cette version

- Trois volumes de toiture fermés avec des tuiles terre cuite texturées.
- Des sols extérieurs différenciés : pelouse, enrobé et gravier.
- Quatre arbres optimisés et dix-huit segments de haie densifiés en 108 clumps partagés dans l'environnement live.
- La table extérieure parasite a été supprimée.
- La visite interactive commence à l'extérieur et permet d'entrer dans la maison.

## Fichiers directs pour GPT

- [Description structurée `house.json`](house.json)
- [Image façade/toiture brute](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/images/v18-facade-roof-ground.webp)
- [Image jardin/textures brute](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/images/v18-jardin-textures.webp)
- [Modèle 3D GLB réellement chargé](https://raw.githubusercontent.com/ramanaru/chamagnieu/main/shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb)
- [Configuration centrale du viewer](shared/project-config.json)
- [Audit de synchronisation V18](audit/version-sync-report.md)
- [Verdict réalisme du vrai viewer V18](validation/V18_WEB_REALISM_FIX_REPORT.md)
- [Comparaisons avant/après — SOURCE = LIVE WEB VIEWER](validation/live_before_after/)

Version : `V18-WEB-REALISM-1`<br>
Modèle GLB : `22 687 292 octets`<br>
SHA-256 : `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E`

## Sources visuelles

- Les pages `/presentation/` et `/visite/` affichent le modèle Web et portent le badge **`SOURCE = LIVE WEB VIEWER`**.
- Les images de cette page et de `/rapide/` sont des rendus de référence et portent le badge **`SOURCE = BLENDER`** dans le site.
- Les deux sources restent volontairement séparées : les WebP de galerie ne sont pas des textures du GLB. Le modèle live utilise 78 images WebP embarquées et compactées, avec 41 matériaux, 95 bindings PBR, un éclairage Web R2 et une végétation CC0 optimisée.
