# Comparaison V18 — présentation, avant/après et viewer public

## Règle de provenance

- **`SOURCE = LIVE WEB VIEWER`** : capture réelle du canvas Three.js.
- **`SOURCE = BLENDER`** : rendu de référence précalculé.
- Aucun rendu D5 n’est présenté comme résultat live.

## Comparaisons finales

| Vue | Blender vs viewer public | Avant JPEG vs après WebP |
|---|---|---|
| Façade | [`comparison-facade-blender-vs-live.png`](./comparison-facade-blender-vs-live.png) | [`before-after-facade-live.png`](./before-after-facade-live.png) |
| Jardin | [`comparison-garden-blender-vs-live.png`](./comparison-garden-blender-vs-live.png) | [`before-after-garden-live.png`](./before-after-garden-live.png) |
| Intérieur | [`comparison-interior-blender-vs-live.png`](./comparison-interior-blender-vs-live.png) | [`before-after-interior-live.png`](./before-after-interior-live.png) |

Chaque montage porte ses sources directement dans l’image. Les moitiés droites
proviennent du viewer GitHub Pages public `V18-LIVE-SYNC-4` et du GLB
`Chamagnieu_V18_REALISM_FINAL_WEBP.glb`.

## Causes exactes des écarts

| Vue | Ce que la Sync-4 corrige | Écart restant | Cause mesurée |
|---|---|---|---|
| Façade | 37 WebP du master, jusqu’à 2048 px ; anisotropie 8 ; IBL PMREM | relief et fond moins riches que Blender | Three.js n’embarque ni HDRI Blender, ni AO, ni post-traitement Eevee ; grands pans de toit très simples |
| Jardin | même texture herbe que le master, 4 arbres et 18 haies confirmés | arbres ronds et haies en blocs | géométrie réellement low-poly du master ; feuillage 256 px baseColor-only, opaque, sans normal/roughness |
| Intérieur | bois, sol, enduit et textiles ne sont plus réduits à 512 px JPEG | contacts et certains meubles restent plats | 15/35 matériaux sans map ; aucun AO/emissive ; 155 nœuds de mobilier procéduraux/non sourcés |

## Avant et après

L’ancien GLB public avait la même géométrie mais convertissait 23 images en
JPEG 512 px et 12 images en JPEG 1024 px. Il conservait en plus
`11 803 422` octets de WebP devenus orphelins. La Sync-4 restaure exactement
les `37` WebP du master et retire seulement le binding invalide
`material[31] → texture[50]`.

```text
SOURCE_AVANT=LIVE WEB VIEWER release V18-LIVE-SYNC-3
SOURCE_APRES=LIVE WEB VIEWER PUBLIC release V18-LIVE-SYNC-4
SOURCE_REFERENCE=BLENDER
GEOMETRY_CHANGED=NO
TEXTURE_PIXEL_RETENTION_BEFORE=14.28%
TEXTURE_PIXEL_RETENTION_AFTER=100%
LIVE_MATCHES_BLENDER_D5=NO
FINAL_STATUS=PARTIAL
```

Le statut reste **PARTIAL** : la livraison, la version et les textures sont
maintenant correctes, tandis que la végétation, une partie du mobilier et le
pipeline lumineux restent intrinsèquement moins réalistes que Blender/D5.
