# V18 LIVE SYNC REPORT — FINAL

Date : 2026-08-16 (Europe/Paris)
Périmètre : dépôt public `ramanaru/chamagnieu`, GitHub Pages, viewer Three.js et GLB V18.

## Verdict synthétique

| Champ demandé | Résultat final |
|---|---|
| `PUBLIC_REPO_VERSION` | `V18-LIVE-SYNC-4` ; commit runtime public audité `5314d8de6df6ba3e9175e3e5825c5a0189a2c706` |
| `LIVE_VIEWER_VERSION` | `V18 / V18-LIVE-SYNC-4` sur les 5 pages |
| `LIVE_GLB` | `shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb?release=v18-live-sync-4` |
| `LIVE_TEXTURES` | 37/37 WebP intégrées ; 55/55 bindings valides ; 0 URI externe ; 131 215 360 pixels |
| `LIVE_MATERIALS` | 35/35 utilisés ; 20 texturés ; 15 factor-only ; 0 AO ; 0 emissive |
| `LIVE_VEGETATION` | 4 arbres + 18 haies présents ; 7 048 triangles ; feuillage 256 px low-poly |
| `LIVE_FURNITURE` | 167 nœuds / 169 meshes runtime ; 12 assets détaillés, 155 nœuds procéduraux/non sourcés |
| `LIVE_LIGHTING` | ACES, PMREM procédurale, env `0.85`, anisotropie `8`, ombres desktop ; aucune HDRI Blender/D5 |
| `CACHE_STATUS` | PASS : aucun Service Worker/CacheStorage ; GLB et entrées versionnés Sync-4 ; HTML GitHub Pages `max-age=600` |
| `CONSOLE_STATUS` | PASS PUBLIC : 0 erreur, 0 avertissement sur 5 pages ; fallback Pointer Lock sans erreur |
| `NETWORK_STATUS` | PASS PUBLIC : 44/44 ressources HTTP 200, 0 échec, 0 image cassée |
| `PRESENTATION_MATCH` | PARTIAL : textures master restaurées ; moteur, éclairage, végétation et certains meubles restent différents |
| `FINAL_STATUS` | `PARTIAL` — synchronisation/version/textures PASS ; photoréalisme complet non atteint par les assets actuels |

```text
LIVE_VIEWER_USES_V18=YES
LIVE_TEXTURES_WORK=YES
LIVE_ASSETS_MATCH_PRESENTATION=NO
LIVE_VIEWER_REALISM_STATUS=PARTIAL
```

## Cause racine trouvée et correction

L’ancien fichier public `Chamagnieu_V18_REALISM_FINAL.glb` était bien une V18,
mais une conversion JPEG dégradée du master WebP :

| Variante | Octets | SHA-256 | Images actives | Pixels | Données orphelines |
|---|---:|---|---|---:|---:|
| Master WebP source | 25 169 404 | `97F842001CC77E65637271172D09A81043FFFDF3235591DCB1AFF0BA96D67DA0` | 37 WebP | 131 215 360 | 0 |
| Ancien live JPEG | 27 987 896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | 37 JPEG, majorité 512 px | 18 743 296 | 11 803 422 octets WebP |
| **Live Sync-4 corrigé** | **25 169 320** | `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE` | **37 WebP jusqu’à 2048 px** | **131 215 360** | **0** |

La géométrie des trois fichiers est identique. Le master brut avait un seul
binding invalide `material[31].metallicRoughnessTexture → texture[50]`, cause
compatible avec l’ancienne erreur `Cannot read properties of undefined
(reading 'uri')`. La Sync-4 retire uniquement ce binding ; le BIN du master est
strictement préservé.

## Pages publiques auditées réellement

| Page | Version DOM/config | GLB chargé | Source visuelle | Résultat navigateur public |
|---|---|---|---|---|
| `/` | `V18 / Sync-4` | aucun, page d’entrée | `SOURCE = BLENDER` pour la galerie | PASS, 5/5 ressources |
| `/presentation/` | `V18 / Sync-4` | `FINAL_WEBP.glb`, 25 169 320 o | `SOURCE = LIVE WEB VIEWER` | PASS, viewerReady, 12/12 ressources |
| `/visite/` | `V18 / Sync-4` | même GLB/hash | `SOURCE = LIVE WEB VIEWER` | PASS, départ extérieur + déplacement, 12/12 ressources |
| `/rapide/` | `V18 / Sync-4` | aucun, galerie | `SOURCE = BLENDER` | PASS, 9 images, 12/12 ressources |
| `/gpt/` | `V18 / Sync-4` | lien/documentation | sources explicites | PASS, 3/3 ressources |

Le texte `V11` n’est plus une version affichée. Les occurrences restantes sont
les noms internes de nœuds de mobilier dans un GLB cumulatif et les listes de
classification du bouton meubles ; elles ne sélectionnent aucun viewer V11.

## Interaction depuis l’extérieur

```text
CAMERA_OUTSIDE=[1.941,1.65,-15.173]
CAMERA_TARGET=[-1.436,1.4,-0.663]
GARDEN_CAMERA=[-12.5,1.65,-17.2]
POINTER_LOCK_API=REJECTED_IN_EMBEDDED_BROWSER
CONTROL_FALLBACK=keyboard-drag-fallback
FALLBACK_CONSOLE_ERRORS=0
KEYBOARD_MOVEMENT=PASS (80 pressions W, image avant/après différente)
FURNITURE_TOGGLE=PASS (169 meshes, true -> false -> true)
```

## Tests machine et navigateur

### Validation statique + HTTP public

```text
V18_REAUDIT_STATIC_RESULT=PASS pages=5 http_200=14/14 version=V18 release=V18-LIVE-SYNC-4 model=Chamagnieu_V18_REALISM_FINAL_WEBP.glb model_bytes=25169320 glb_sha256=69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE nodes=794 meshes=793 primitives=795 materials=35 textures=56 used_textures=55 images=37 embedded_images=37 external_images=0 furniture_nodes=167 furniture_runtime_meshes=169 displayed_v11=false legacy_model_refs=0 service_worker_registrations=0 public_config_match=true public_model_match=true failures=0
V18_RUNTIME_VALIDATION=PASS pages=5 http_200=14 version=V18 release=V18-LIVE-SYNC-4 model=Chamagnieu_V18_REALISM_FINAL_WEBP.glb model_bytes=25169320 glb_sha256=69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE materials=35 textures=56 images=37 embedded_images=37 external_images=0 furniture_nodes=167 furniture_runtime_meshes=169
```

### Validation navigateur public

```text
PUBLIC_BROWSER_CONSOLE_RESULT=PASS pages=5 errors=0 warnings=0
PUBLIC_BROWSER_NETWORK_RESULT=PASS resources=44 http_200=44 failed=0 broken_images=0
PUBLIC_VIEWER_READY_PRESENTATION=true
PUBLIC_VIEWER_READY_VISITE=true
PUBLIC_WEBGL2=true
PUBLIC_MODEL_HTTP=200 size=25169320
```

## Captures finales

Les trois fichiers suivants sont des captures du GitHub Pages public, pas des
rendus Blender/D5 :

- `validation/live-v18-facade.png` — **SOURCE = LIVE WEB VIEWER**
- `validation/live-v18-garden.png` — **SOURCE = LIVE WEB VIEWER**
- `validation/live-v18-interior.png` — **SOURCE = LIVE WEB VIEWER**

Les références et montages avant/après sont dans
`audit/presentation-vs-live/`; chaque moitié porte sa source directement dans
l’image.

## Limites honnêtes

Le retour aux WebP haute définition corrige la livraison des textures, pas la
géométrie intrinsèque. Les 4 arbres et 18 haies sont réellement low-poly ; 15
matériaux restent sans texture ; le GLB ne contient ni HDRI, ni lumières glTF,
ni AO/emissive ; 155 nœuds de mobilier restent procéduraux/non sourcés. Ces
écarts expliquent le statut `PARTIAL` face aux images Blender/D5.
