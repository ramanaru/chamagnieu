# Preuve publique V18 Web Realism

```text
SOURCE = LIVE WEB VIEWER
EVIDENCE_SCOPE = PUBLIC CURRENT
BASE_URL = https://ramanaru.github.io/chamagnieu/
RELEASE = V18-WEB-REALISM-1
RUNTIME_COMMIT_AUDITED = 56f4a6ce191917d19e47d7f99dd24b834190f3c4
```

## Captures publiques brutes

Toutes les vues `after/*.png` ci-dessous ont été recapturées à `1440 × 900` depuis la vraie page GitHub Pages après publication :

- `after/facade.png`
- `after/general.png`
- `after/garden.png`
- `after/hedges.png`
- `after/exterior-ground.png`
- `after/living.png`
- `after/kitchen.png`
- `after/interior-floor-materials.png`
- `after/upstairs-doors.png`
- `after/visit-outside.png`
- `after/visit-after-move.png`

Les six fichiers `01_...` à `06_...` opposent la baseline publique V18-LIVE-SYNC-4 à ces nouvelles captures publiques V18-WEB-REALISM-1. Chaque composite affiche explicitement `SOURCE = LIVE WEB VIEWER`.

## Postflight navigateur

```text
PUBLIC_PRESENTATION_READY=true
PUBLIC_PRESENTATION_WEBGL2=true
PUBLIC_PRESENTATION_MESHES=795
PUBLIC_PRESENTATION_MATERIALS=41
PUBLIC_PRESENTATION_TEXTURES_RUNTIME=119
PUBLIC_PRESENTATION_VEGETATION=enhanced
PUBLIC_PRESENTATION_HEDGE_CLONES=108
PUBLIC_PRESENTATION_VEGETATION_TRIANGLES=1082996
PUBLIC_PRESENTATION_VEGETATION_DRAW_CALLS=120
PUBLIC_BROKEN_IMAGES=0
PUBLIC_JS_EXCEPTIONS=0
PUBLIC_VISIT_RESPONSES=108/108 HTTP 200
PUBLIC_VISIT_CONTROL_MODE=keyboard-drag-fallback
PUBLIC_VISIT_CONTROL_FALLBACK_REASON=WrongDocumentError
PUBLIC_ASSET_HASH_RESULT=PASS assets=6/6
```

Deux requêtes automatiques vers `https://ramanaru.github.io/favicon.ico` ont répondu 404 pendant un audit de la présentation. Le favicon propre au projet (`/chamagnieu/favicon.ico`) répond 200; le modèle, les modules, les textures et les assets du viewer n'ont aucun échec.

