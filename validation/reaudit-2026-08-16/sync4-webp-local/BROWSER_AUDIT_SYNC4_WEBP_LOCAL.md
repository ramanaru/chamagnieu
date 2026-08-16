# Audit navigateur local final — V18-LIVE-SYNC-4 WebP

- URL auditée : `http://127.0.0.1:8897/`
- Navigateur : **Codex In-app Browser**
- Verdict : **PASS**

## Cinq pages réellement ouvertes

| Page | Version / source | Ressources observées | Échecs | Images cassées | Console |
|---|---|---:|---:|---:|---:|
| `/` | V18 · V18-LIVE-SYNC-4 | 5/5 HTTP 200 | 0 | 0/2 | 0 |
| `/presentation/` | V18 · LIVE WEB VIEWER | 12/12 HTTP 200 | 0 | 0 | 0 |
| `/visite/` | V18 · LIVE WEB VIEWER | 12/12 HTTP 200 | 0 | 0 | 0 |
| `/rapide/` | V18 · 9 badges BLENDER | 12/12 HTTP 200 | 0 | 0/9 | 0 |
| `/gpt/` | V18 · LIVE WEB VIEWER + BLENDER | 3/3 HTTP 200 | 0 | 0 | 0 |

```text
FAILED_NETWORK_RESOURCES=0
BROKEN_IMAGES=0
CONSOLE_WARNINGS_OR_ERRORS=0
CORS_ERRORS=0
WEBGL_ERRORS=0
GLB_ERRORS=0
TEXTURE_NETWORK_ERRORS=0
SERVICE_WORKER_CONTROLLER=false
SERVICE_WORKER_REGISTRATIONS=0
CACHE_STORAGE_KEYS=0
```

## Modèle WebP réellement chargé

```text
MODEL=Chamagnieu_V18_REALISM_FINAL_WEBP.glb
MODEL_BYTES=25169320
MODEL_SHA256=69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE
GLB_IMAGES=37
MIME_COUNTS={'image/webp': 37}
ALL_WEBP=True
EMBEDDED_BUFFER_VIEWS=37
EXTERNAL_URIS=0
GLB_TEXTURES=56
GLB_MATERIALS=35
```

Décodage réel des 37 images embarquées :

```text
2048x2050 WEBP count=3
2048x2048 WEBP count=27
1024x1024 WEBP count=5
256x256 WEBP count=2
ALL_DECODED_WEBP=True
```

Le binding invalide annoncé est absent de la version corrigée : `/materials/31/pbrMetallicRoughness/metallicRoughnessTexture removed (invalid texture 50)`.

## Viewer, lumière et matériaux

```text
VIEWER_READY=true
VIEWER_FAILED=false
WEBGL2=true
MESHES=795
MATERIALS=35
RUNTIME_TEXTURES=71
FURNITURE_MESHES=169
ANISOTROPY=8
ENVIRONMENT=procedural PMREM IBL
ENVIRONMENT_INTENSITY_CONFIG=0.85
ENVIRONMENT_INTENSITY_RUNTIME=0.85
SHADOWS=PCFSoft-2048
```

## Visite extérieure et fallback

### Départ extérieur

```json
{
  "position": [1.941, 1.65, -15.173],
  "target": [-1.436, 1.4, -0.663],
  "lastPreset": "outside"
}
```

Le premier frame montre réellement la façade et le jardin depuis l'extérieur.

### Jardin

```json
{
  "position": [-12.5, 1.65, -17.2],
  "target": [-4.2, 1.45, -11.86],
  "lastPreset": "garden",
  "cameraChanged": true
}
```

### Clic `Commencer dehors`

Dans l'In-app Browser, Pointer Lock est rejeté, mais le fallback prend proprement le relais :

```text
VISIT_CONTROL_MODE=keyboard-drag-fallback
POINTER_LOCK_FALLBACK_REASON=UnknownError
POINTER_LOCKED=false
CONSOLE_ERRORS_AFTER_START=0
STATUS=Mode souris-glisser actif · utilisez ZQSD/WASD pour entrer · SOURCE = LIVE WEB VIEWER
```

Le fallback absorbe donc l'erreur navigateur au lieu de laisser `PointerLockControls` l'imprimer dans la console.

### Déplacement clavier

80 pressions `W`, espacées de 25 ms, font avancer la caméra vers la façade :

```text
BEFORE_SHA256=796545E66E31BB051A6EB92E3CDE02A362A56CF979773E1F216697AC67BA8883
AFTER_SHA256=CB37EED8576FD289488503C4DBC36209B2B65B6D4FE6C542235C29C788D95243
VISUAL_CHANGED=true
```

La capture après déplacement montre la maison nettement plus proche.

## Mobilier

Le bouton fonctionne sur `/presentation/` et `/visite/` :

```text
FURNITURE_MESHES=169
FURNITURE_VISIBLE=true -> false -> true
BUTTON=Masquer les meubles -> Afficher les meubles -> Masquer les meubles
```

## Captures — SOURCE = LIVE WEB VIEWER

- `sync4-webp-live-facade.png`
- `sync4-webp-live-garden.png`
- `sync4-webp-live-interior.png`
- `sync4-webp-visit-before-keyboard.png`
- `sync4-webp-visit-after-keyboard.png`

## Preuve structurée

`browser-audit-sync4-webp-local.json` contient les états DOM, configuration, ressources réseau, console, caméras, contrôle, mobilier et assertions booléennes des cinq pages.
