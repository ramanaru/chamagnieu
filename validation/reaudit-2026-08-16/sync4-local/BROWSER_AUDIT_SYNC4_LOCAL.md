# Audit navigateur local — V18-LIVE-SYNC-4

- URL : `http://127.0.0.1:8897/visite/?reaudit=sync4local`
- Navigateur : **Codex In-app Browser**
- Verdict : **PARTIAL**

## Correctifs vérifiés

```text
VIEWER_VERSION=V18
VIEWER_RELEASE=V18-LIVE-SYNC-4
VIEWER_READY=true
VIEWER_FAILED=false
MODEL=Chamagnieu_V18_REALISM_FINAL.glb
MODEL_BYTES=27987896
WEBGL2=true
ENVIRONMENT_INTENSITY_CONFIG=0.85
ENVIRONMENT_INTENSITY_RUNTIME=0.85
BROKEN_IMAGES=0
FAILED_NETWORK_RESOURCES=0
```

Le premier frame de `/visite/` montre réellement la façade et le jardin depuis l'extérieur. Le badge `SOURCE = LIVE WEB VIEWER` est visible.

### Preset `outside`

```json
{
  "position": [1.941, 1.65, -15.173],
  "target": [-1.436, 1.4, -0.663],
  "lastPreset": "outside",
  "status": "Départ réellement extérieur — avancez vers la porte pour entrer · SOURCE = LIVE WEB VIEWER"
}
```

Résultat visuel : **PASS**, la façade est réellement visible depuis l'extérieur.

### Preset `garden`

```json
{
  "position": [-12.5, 1.65, -17.2],
  "target": [-4.2, 1.45, -11.86],
  "lastPreset": "garden",
  "cameraChanged": true
}
```

Résultat visuel : **PASS**, la caméra passe au jardin et affiche quatre arbres, les haies et le terrain.

### Mobilier

```text
FURNITURE_MESHES=169
FURNITURE_VISIBLE=true -> false -> true
BUTTON=Masquer les meubles -> Afficher les meubles -> Masquer les meubles
```

## Réseau

Les 13 ressources observées ont toutes `responseStatus=200`, y compris :

- `project-config.json`
- `visite.js?release=v18-live-sync-4`
- `live-realism.js?release=v18-live-sync-4`
- `Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-4` (`27 987 896` octets)

```text
FAILED_NETWORK_RESOURCES=0
CORS_ERRORS=0
GLB_ERRORS=0
TEXTURE_NETWORK_ERRORS=0
SERVICE_WORKER_CONTROLLER=false
SERVICE_WORKER_REGISTRATIONS=0
CACHE_STORAGE_KEYS=0
```

## Erreur restante après `Commencer dehors`

Le test console à froid est propre. Cependant, cliquer `Commencer dehors` dans le Codex In-app Browser produit encore :

```text
THREE.PointerLockControls: Unable to use Pointer Lock API
UnknownError: If you see this error we have a bug. Please report this bug to chromium.
```

État observé :

```text
POINTER_LOCKED=false
CONSOLE_ERRORS_AFTER_START=2
```

Le placement extérieur Sync-4 est donc corrigé, mais le critère « console 0 erreur après démarrage » reste en échec dans ce navigateur. Il faut intercepter l'indisponibilité Pointer Lock et activer un déplacement clavier/tactile sans verrouillage.

## Captures

- `sync4-local-visit-outside.png` — vraie façade depuis l'extérieur, `SOURCE = LIVE WEB VIEWER`
- `sync4-local-visit-garden.png` — preset jardin, `SOURCE = LIVE WEB VIEWER`
- `browser-audit-sync4-local.json` — sortie structurée, réseau et console
