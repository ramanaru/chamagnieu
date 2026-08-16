# Éclairage live courant — V18 WebP

> **SOURCE = STATIC FILE AUDIT** pour les valeurs du code et de la configuration.
> **SOURCE = LIVE WEB VIEWER** s’applique au canvas de `/presentation/` et `/visite/`; **SOURCE = BLENDER** reste réservé aux images de galerie.

## Pipeline réellement configuré

| Élément | Valeur courante | Source |
|---|---|---|
| espace de sortie | `THREE.SRGBColorSpace` | `shared/live-realism.js` |
| tone mapping | `ACESFilmicToneMapping` | code + config |
| exposition | 0,92 | `project-config.json` |
| environnement | Canvas 512×256 → equirectangular → PMREM IBL | code runtime |
| intensité environnement scène | 0,85 | config + `scene.environmentIntensity` |
| HemisphereLight | ciel `0xeaf4ff`, sol `0x4e4737`, intensité 0,72 | code + config |
| AmbientLight | `0xfff2df`, intensité 0,06 | code + config |
| soleil | `0xffdfae`, intensité 2,4, position (-18,28,-10) | code + config |
| fill | `0xa9c8e8`, intensité 0,22, position (18,12,18) | code + config |
| ombres desktop | PCFSoft, 2048², frustum ±30, near 0,5, far 95 | code runtime |
| ombres mobile | désactivées | code runtime |
| shadow bias / normalBias | -0,00012 / 0,018 | code runtime |
| anisotropie textures | min(8, capacité GPU) | `tuneLiveModel()` |
| envMapIntensity matières | 0,8 standard; 1,15 réfléchissant | `tuneLiveModel()` |
| pixel ratio | max 1,6 desktop; 1,1 mobile | deux viewers |

Le même `setupLiveLighting()` et le même `tuneLiveModel()` sont importés par les deux viewers avec `?release=v18-live-sync-4`. Ils chargent le même `Chamagnieu_V18_REALISM_FINAL_WEBP.glb`.

## Ce qui est amélioré

- PMREM fournit un IBL cohérent aux 35 matériaux;
- ACES évite la sortie linéaire plate;
- l’environnement est réglé à 0,85 et les surfaces réfléchissantes à 1,15;
- les WebP haute définition rétablissent les normales et roughness jusqu’à 2048 px;
- les ombres desktop, l’anisotropie et les normal maps donnent plus de relief aux toits, sols, stucs, bois et tissus.

## Différence avec Blender/D5

| Fonction | Viewer Three.js | Galerie Blender/D5 | Impact |
|---|---|---|---|
| environnement | gradient procédural PMREM | environnement de rendu hors Web | reflets et ambiance différents |
| éclairage global | IBL + 4 lumières | moteur offline/preview | contraste moins riche |
| ombres | une directionnelle PCFSoft | ombres moteur de rendu | contact et pénombres plus simples |
| post-traitement | ACES uniquement | réglages moteur/caméra | pas de bloom/SSR/SSAO identifié |
| matériaux | glTF PBR, 20/35 texturés | shaders Blender/D5 | 15 matériaux live restent factoriels |
| végétation | 7 048 triangles, albedos 256² opaques | image de présentation | silhouette toujours low-poly |

Aucun HDRI photographique, lightmap, SSAO, SSR, path tracing ou texture d’environnement externe n’est chargé. La correction WebP rapproche la netteté des cartes du master, mais ne peut pas rendre identiques deux moteurs et deux jeux d’assets.

## Cache de l’éclairage

- `presentation.js`, `visite.js` et `live-realism.js` portent la query `v18-live-sync-4`;
- `project-config.json` est fetché avec `cache: no-store`;
- `environmentIntensity=0.85` vient donc de la configuration centrale courante;
- aucun service worker ne conserve un ancien pipeline.

## Verdict

```text
LIVE_LIGHTING_SOURCE=shared/live-realism.js
LIVE_LIGHTING_ENVIRONMENT=procedural_PMREM_IBL
LIVE_LIGHTING_TONEMAPPING=ACES_FILMIC
LIVE_LIGHTING_EXPOSURE=0.92
LIVE_LIGHTING_ENVIRONMENT_INTENSITY=0.85
LIVE_LIGHTING_DESKTOP_SHADOWS=PCFSOFT_2048
LIVE_LIGHTING_MOBILE_SHADOWS=OFF
LIVE_LIGHTING_ANISOTROPY_MAX=8
LIVE_LIGHTING_STATUS=PASS_CONFIG
PRESENTATION_PIXEL_MATCH=NO
```
