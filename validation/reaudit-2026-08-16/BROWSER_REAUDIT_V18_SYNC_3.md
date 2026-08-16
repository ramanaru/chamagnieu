# Réaudit navigateur public — Chamagnieu V18-LIVE-SYNC-3

- Date UTC : `2026-08-16T07:37:00.860Z`
- Navigateur : **Codex In-app Browser**
- URL : `https://ramanaru.github.io/chamagnieu/`
- Verdict : **PARTIAL — la synchronisation et le viewer sont chargés, mais le départ extérieur est placé dans l'intérieur et Pointer Lock échoue dans ce navigateur.**

## Matrice réelle des pages

| Page | Version/source | Ressources | Images | Console | Résultat |
|---|---|---:|---:|---:|---|
| `/` | V18 · V18-LIVE-SYNC-3 | 6/6 HTTP 200 | 0 cassée | 0 | PASS |
| `/presentation/` | V18 · LIVE WEB VIEWER | 12/12 HTTP 200 | 0 cassée | 0 | PASS |
| `/visite/` | V18 · LIVE WEB VIEWER | 12/12 HTTP 200 | 0 cassée | 2 après `Commencer dehors` | PARTIAL |
| `/rapide/` | V18 · 9 badges BLENDER | 12/12 HTTP 200 | 0/9 cassée | 0 propre à la page | PASS |
| `/gpt/` | V18 · LIVE WEB VIEWER + BLENDER | 3/3 HTTP 200 | 0 cassée | 0 | PASS |

## Viewer et GLB observés

```text
VIEWER_VERSION=V18
VIEWER_RELEASE=V18-LIVE-SYNC-3
VIEWER_READY=true
VIEWER_FAILED=false
MODEL=Chamagnieu_V18_REALISM_FINAL.glb
MODEL_URL=https://ramanaru.github.io/chamagnieu/shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3
MODEL_BYTES=27987896
WEBGL2=true
MESHES=795
MATERIALS=35
RUNTIME_TEXTURES=71
FURNITURE_MESHES=169
ANISOTROPY=8
ENVIRONMENT=procedural PMREM IBL
SHADOWS=PCFSoft-2048
```

Le bouton mobilier fonctionne dans `/presentation/` et `/visite/` : `true → false → true`, le libellé devient `Afficher les meubles`, puis revient à `Masquer les meubles`.

## Réseau, cache et erreurs de textures

```text
FAILED_SUBRESOURCES=0
BROKEN_IMAGES=0
CORS_ERRORS=0
GLB_FETCH_ERRORS=0
TEXTURE_NETWORK_ERRORS=0
SERVICE_WORKER_CONTROLLER=false
SERVICE_WORKER_REGISTRATIONS=0
CACHE_STORAGE_KEYS=0
```

Toutes les ressources observées ont `responseStatus=200`, y compris le GLB de 27 987 896 octets.

## Bug confirmé : « dehors » place la caméra dans la maison

Le point d'arrêt navigateur a été posé **après** `camera.position.fromArray(...)` et `camera.lookAt(...)`. Le gestionnaire de preset s'exécute réellement ; ce n'est pas seulement un problème de bouton ou de libellé.

### Preset `outside`

```json
{
  "cameraPosition": [
    -5.359,
    1.65,
    -0.537
  ],
  "cameraQuaternion": [
    0.010322831112713676,
    0.9838305632742708,
    0.06033855727893596,
    -0.1683155382926544
  ],
  "cameraRotation": [
    -3.011778496833943,
    -0.3362423587035748,
    -3.098545866398446,
    "XYZ"
  ],
  "key": "outside",
  "view": {
    "label": "Départ extérieur — avancez vers la porte pour entrer",
    "p": [
      -5.359,
      1.65,
      -0.537
    ],
    "t": [
      -4.684,
      1.4,
      1.378
    ]
  }
}
```

Après deux frames et plus de deux secondes, le rendu montre toujours le RDC près de la cuisine/escalier. La capture porte pourtant le statut « Départ extérieur » : les coordonnées sont donc mal classées ou mal choisies.

### Preset `garden`

```json
{
  "cameraPosition": [
    -12.5,
    1.65,
    -17.2
  ],
  "cameraQuaternion": [
    0.004852905666456097,
    0.8777547077399186,
    0.00889276109644052,
    -0.4790031744645168
  ],
  "cameraRotation": [
    -3.104156967716237,
    -0.9987746085091473,
    -3.1101121105518716,
    "XYZ"
  ],
  "key": "garden",
  "view": {
    "label": "Jardin — 4 arbres, 18 haies et sols du GLB Web",
    "p": [
      -12.5,
      1.65,
      -17.2
    ],
    "t": [
      -4.2,
      1.45,
      -11.86
    ]
  }
}
```

Ce preset rend bien à l'extérieur après reprise du moteur de rendu. Le changement de caméra est donc fonctionnel ; l'erreur est ciblée sur le point `outside`.

### Pointer Lock

Cliquer `Commencer dehors` a produit exactement :

```text
THREE.PointerLockControls: Unable to use Pointer Lock API
UnknownError: If you see this error we have a bug. Please report this bug to chromium.
```

Cette limite est observée dans le **Codex In-app Browser**. Elle empêche de prouver le trajet au clavier dehors → porte → intérieur dans cet environnement. Un fallback sans Pointer Lock est nécessaire pour les navigateurs qui refusent cette API.

## Correction obligatoire

1. Remplacer le preset `outside` par une position réellement extérieure, orientée vers la façade/porte.
2. Vérifier visuellement que le premier frame est dehors, et pas seulement que `window.__lastPreset === "outside"`.
3. Refaire un trajet extérieur → porte → intérieur.
4. Ajouter un fallback de déplacement quand Pointer Lock est indisponible.
5. Rejouer console, réseau, mobilier et captures après publication.

## Captures — source explicite

- `live-web-facade-v18-sync-3.png` — `SOURCE = LIVE WEB VIEWER`
- `live-web-garden-v18-sync-3.png` — `SOURCE = LIVE WEB VIEWER`
- `live-web-interior-v18-sync-3.png` — `SOURCE = LIVE WEB VIEWER`
- `live-visit-outside-working-v18-sync-3.png` — preuve du mauvais rendu intérieur du preset `outside`
- `live-visit-garden-after-camera-trace-v18-sync-3.png` — preuve que le preset `garden` rend dehors

## Fichiers de preuve

- `browser-audit-v18-live-sync-3.json` — sortie structurée complète
- `console-errors-sync-3.txt` — console par page
- `network-status-sync-3.txt` — toutes les ressources observées et leur statut
