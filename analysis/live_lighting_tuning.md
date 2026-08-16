# Réglage final de l’éclairage et du rendu live V18

> Ce document décrit l’état courant **V18-WEB-REALISM-1**.
> Les preuves finales marquées **PUBLIC CURRENT — SOURCE = LIVE WEB VIEWER** viennent du viewer Web GitHub Pages courant. Les anciennes preuves publiques `V18-LIVE-SYNC-4` sont conservées uniquement comme baseline avant amélioration.

## 1. Identité courante vérifiée

| Champ | Valeur courante |
|---|---|
| version | `V18` |
| release | `V18-WEB-REALISM-1` |
| cache key | `v18-web-realism-1` |
| modèle live | `shared/Chamagnieu_V18_WEB_REALISM_UPGRADED.glb` |
| taille du GLB | **22 687 292 octets** |
| SHA-256 du GLB | `9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E` |
| matériaux glTF | **41** |
| textures glTF | **90** |
| images WebP intégrées | **78/78** |
| bindings PBR valides | **95/95** |
| textures runtime Three.js | **119** |
| pipeline lumière | `V18-WEB-REALISM-LIGHTING-R2` |

La configuration centrale et le modèle ont bien changé par rapport à Sync-4 :

```text
CONFIG_MODEL_CHANGED=YES
PREVIOUS_RELEASE=V18-LIVE-SYNC-4
CURRENT_RELEASE=V18-WEB-REALISM-1
PREVIOUS_MODEL=Chamagnieu_V18_REALISM_FINAL_WEBP.glb
CURRENT_MODEL=Chamagnieu_V18_WEB_REALISM_UPGRADED.glb
```

Empreinte actuelle de `shared/project-config.json` :

```text
BYTES=2667
SHA256=A86A1DB6379384C4D4E30D5C00C5E77961C54D2F3F8907D2E490E684CBDE4892
```

## 2. Imports réellement actifs

Les deux viewers utilisent la nouvelle release et le cache-bust propre au pipeline R2 :

```js
// presentation/presentation.js et visite/visite.js
import { loadProjectConfig, applyProjectVersion, resolveProjectAsset } from '../shared/project-config.js?release=v18-web-realism-1';
import { setupLiveLighting, tuneLiveModel } from '../shared/live-realism.js?release=v18-web-realism-1&pipeline=lighting-r2';
```

Ils importent également `shared/live-vegetation.js` avec `release=v18-web-realism-1`. Aucun import actif ne conserve `v18-live-sync-4`.

## 3. Cause de l’ancien rendu délavé

Le pipeline précédent cumulait un environnement uniforme fort, une `HemisphereLight` trop présente, un brouillard proche de la maison et un fond gris-vert uni. Ces apports remplissaient les ombres et réduisaient la lecture du stuc, des tuiles, des sols, du vitrage et du mobilier.

Le pipeline R2 conserve ACES et sRGB, mais utilise une lumière principale plus lisible, moins de remplissage diffus, un brouillard repoussé et un ciel procédural directionnel converti en PMREM. Il n’ajoute aucun HDRI externe.

## 4. Pipeline exact `V18-WEB-REALISM-LIGHTING-R2`

### Tone mapping et environnement

| Réglage | Valeur appliquée |
|---|---:|
| espace de sortie | `THREE.SRGBColorSpace` |
| tone mapping | `THREE.ACESFilmicToneMapping` |
| exposition | **0.865** |
| intensité environnement | **0.765** |
| environnement | ciel procédural déterministe + PMREM IBL |
| fond | texture équirectangulaire procédurale |
| texture desktop | 1024×512 |
| texture mobile | 512×256 |
| rotation environnement/fond | -0.36 rad |
| brouillard desktop | `#aebcb7`, 78 → 172 |
| brouillard mobile | `#aebcb7`, 66 → 142 |

Le ciel contient un gradient bleu-chaud, un disque solaire et quatre bandes nuageuses à positions fixes. Il ne contient aucune valeur aléatoire et ne déclenche aucune requête HTTP.

### Lumières et ombres

| Composant | Valeur appliquée |
|---|---:|
| HemisphereLight | **0.518**, ciel `#dcecff`, sol `#302c22` |
| AmbientLight | **0.030**, `#ffe8cf` |
| soleil directionnel | **2.760**, `#ffd5a6`, position `(-22,31,-16)` |
| fill directionnel | **0.158**, `#92b9d8` |
| rim directionnel | **0.280 desktop / 0.200 mobile**, `#ffead0` |
| ombres desktop | PCFSoft 2048² |
| ombres mobile | désactivées |
| shadow bias / normalBias | -0.00010 / 0.014 |
| shadow radius | 2 |
| frustum solaire | ±32, near 0.5, far 105 |

## 5. Tuning matériau courant

`tuneLiveModel()` règle les 41 matériaux après chargement du GLB, sans réencoder leurs 78 images WebP. L’anisotropie est plafonnée à `8`.

| Famille | envMap | roughness | normalScale | action principale |
|---|---:|---:|---:|---|
| verre | 1.75 | 0.11–0.16 | — | transmission 0.68/0.88, IOR 1.48, verre mince opacity 0.42 |
| miroir | 2.05 | 0.06 | — | metalness 0.82 |
| métal / alu / chrome | 1.45 | valeur GLB | — | reflets renforcés |
| toiture | 0.62 | 0.78 | 1.18 | teinte chaude contrôlée |
| façade / stuc | 0.34 | 0.88 | 0.55 | micro-relief propre, sans salissure |
| pelouse | 0.25 | 0.94 | 1.05 | vert naturel, mat |
| gravier | 0.34 | 0.90 | 1.12 | relief minéral |
| **enrobé corrigé** | **0.26** | **0.92** | **1.02** | teinte `0.34/0.37/0.40`, plus sombre et distincte |
| carrelage / porcelaine | 0.68 | 0.62 | 0.74 | joints et reflets lisibles |
| béton | 0.40 | 0.82 | 0.78 | grain moins plat |
| literie coton V12 | 0.30 | 0.90 | 0.76 | crème `0.88/0.82/0.72` |
| bois | 0.48 | 0.66 | 0.80 | chêne/noix chaud |
| laque cuisine | 0.74 | 0.34 | — | greige contemporain |
| pierre / plan de travail | 0.72 | 0.40 | — | contraste minéral |

Les meshes exclusivement vitrés ne projettent plus d’ombres rectangulaires opaques. Le verre mince conserve `transparent=true` et `depthWrite=false`; le verre physique conserve une transmission forte et une épaisseur de 0.06 m.

### Matériaux ajoutés par le GLB upgraded

Les six matériaux V18 sont traités avant les expressions génériques. Leur albedo intégré reste intact :

| Matériau | Famille R2 | envMap | roughness | normalScale | albedo |
|---|---|---:|---:|---:|---|
| `V18_WEB_SOFA_WARM_WEAVE` | `sofa-warm-weave` | 0.36 | 0.82 | 0.88 | conservé |
| `V18_WEB_ARMCHAIR_OLIVE_WEAVE` | `armchair-olive-weave` | 0.30 | 0.83 | 0.90 | conservé |
| `V18_WEB_DINING_CHAIR_CARAMEL_WEAVE` | `chair-caramel-weave` | 0.34 | 0.80 | 0.88 | conservé |
| `V18_WEB_TREE_BARK` | `tree-bark` | 0.22 | 0.94 | 1.04 | conservé |
| `V18_WEB_TREE_LEAVES_DEEP` | `tree-leaves-deep` | 0.20 | 0.89 | 0.92 | conservé |
| `V18_WEB_TREE_LEAVES_FRESH` | `tree-leaves-fresh` | 0.22 | 0.87 | 0.92 | conservé |

`V12_PBR_BEIGE_COTTON` reste séparé sous `bedding-cream`, afin que la literie ne reçoive pas la teinte du canapé ou des chaises.

## 6. Identité et intégrité du GLB upgraded

```text
GLB_VERSION=2.0
BYTES=22687292
SHA256=9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E
MATERIALS=41
GLTF_TEXTURES=90
EMBEDDED_IMAGES=78/78
PBR_BINDINGS_VALID=95/95
EXTERNAL_URI_COUNT=0
ORPHAN_IMAGE_BYTES=0
ORPHAN_BUFFER_VIEWS=0
RUNTIME_TEXTURES=119
```

La géométrie du bâtiment reste identique au GLB corrigé Sync-4 : 2 454 accessors, payloads géométriques byte-identiques et SHA géométrique commun `88A02FD04C54274E372EA5CC16A6ED6BE0B045BB95775100FB2BFB7E1CF75E93`.

## 7. Végétation Web intégrée

Le viewer charge deux assets Web locaux Poly Haven CC0, puis masque les anciennes familles low-poly uniquement après succès du remplacement.

```text
TREE_INSTANCES=4
TREE_TRIANGLES_PER_INSTANCE=47000
TREE_DRAW_CALLS_PER_INSTANCE=3
HEDGE_LAYOUT_ANCHORS=18
HEDGE_CLONE_INSTANCES=108
HEDGE_TRIANGLES_PER_INSTANCE=8287
HEDGE_DRAW_CALLS_PER_INSTANCE=1
ENHANCED_VEGETATION_TRIANGLES=1082996
ENHANCED_VEGETATION_DRAW_CALLS=120
ORIGINALS_HIDDEN_AFTER_SUCCESS=38
```

Les 18 segments de haie sont développés en **108 clones** de buissons partagés, disposés en deux rangées décalées. Les 4 arbres réutilisent eux aussi les mêmes géométries et matériaux. Sur un appareil contraint (`deviceMemory < 4 Go` ou économie de données), le viewer garde la végétation low-poly et ne télécharge aucun GLB optionnel.

Validation du harness : desktop et mobile moderne `status=enhanced`; appareil contraint `status=mobile-fallback`; WebGL2 actif; aucune erreur console, requête en échec ou réponse HTTP incorrecte.

## 8. Audits runtime déterministes

`setupLiveLighting()` expose :

```js
window.__liveLightingAudit
```

`tuneLiveModel()` expose par le viewer :

```js
window.__liveMaterialAudit
```

Le chargement de végétation expose :

```js
window.__liveVegetationAudit
```

Les objets ne contiennent ni date ni nombre aléatoire. Le contrôle local avec le GLB courant a observé :

```text
PIPELINE=V18-WEB-REALISM-LIGHTING-R2
VIEWER_READY=true
WEBGL2=true
MESHES=795
UNIQUE_MATERIALS=41
UNIQUE_TEXTURES_RUNTIME=119
TUNED_MATERIALS=41
AUTHORED_V18_ALBEDOS_PRESERVED=6/6
CONSOLE_ERRORS=0
CONSOLE_WARNINGS=0
```

## 9. État des preuves

### Preuve publique actuelle

```text
EVIDENCE_SCOPE=PUBLIC_CURRENT
SOURCE=LIVE_WEB_VIEWER
RELEASE=V18-WEB-REALISM-1
MODEL_SHA256=9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E
STATIC_VALIDATION=PASS 19/19
PUBLIC_HTTP=PASS 13/13
VEGETATION_RUNTIME_HARNESS=PASS
PUBLIC_WEBGL2=true
PUBLIC_BROWSER_CONSOLE_ERRORS=0
```

Captures courantes : [`../validation/live_before_after/after/facade.png`](../validation/live_before_after/after/facade.png), [`../validation/live_before_after/after/garden.png`](../validation/live_before_after/after/garden.png), [`../validation/live_before_after/after/living.png`](../validation/live_before_after/after/living.png) et [`../validation/live_before_after/after/interior-floor-materials.png`](../validation/live_before_after/after/interior-floor-materials.png). Elles proviennent de la page publique et affichent le badge `SOURCE = LIVE WEB VIEWER`.

Les captures historiques présentes dans `analysis/` ont servi au réglage local R2; les fichiers `validation/live_before_after/after/` sont la preuve publique finale de `V18-WEB-REALISM-1`.

### Postflight public exécuté

```text
EVIDENCE_SCOPE=PUBLIC_CURRENT
PUBLIC_RELEASE_V18_WEB_REALISM_1=PASS
PUBLIC_GLTF_IDENTITY=PASS bytes=22687292 sha256=9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E
PUBLIC_BROWSER_CONSOLE=PASS errors=0 warnings=0
PUBLIC_NETWORK_AUDIT=PASS critical_assets=13/13 http_200
PUBLIC_VISUAL_CAPTURES=PASS raw_views=11 composites=6
```

Le postflight a rechargé les cinq pages publiques, vérifié le SHA et la taille du GLB servi, confirmé `41` matériaux et `119` textures runtime, contrôlé les 4 arbres et 108 clones de haies, puis capturé façade, jardin, sol extérieur, séjour et sol intérieur dans le viewer public.

## 10. Vérifications locales et publiques

```text
V18_WEB_REALISM_STATIC_VALIDATION=PASS
CHECKS_PASS=19
CHECKS_FAIL=0
HTTP_RESOURCES=13/13
GLB_REPRODUCIBLE_REBUILD_MATCH=YES
WEBP_DECODED=78/78
MATERIAL_TEXTURE_BINDINGS_VALID=95/95
GEOMETRY_IDENTICAL=YES
VEGETATION_ASSET_VALIDATION=PASS
VEGETATION_RUNTIME_VALIDATION=PASS
```

## 11. Empreinte courante du pipeline

L’empreinte ci-dessous est recalculée après la correction spécifique de l’enrobé :

```text
LIVE_REALISM_JS_BYTES=14333
LIVE_REALISM_JS_SHA256=8EAB0A78A0C8AB83BED4B387F7242C1904C3CE1C1C42A5F776EEC726862368EC
PIPELINE_ID=V18-WEB-REALISM-LIGHTING-R2
ASPHALT_PROFILE=env:0.26,roughness:0.92,normalScale:1.02,tint:0.34/0.37/0.40
```

## 12. Verdict documentaire courant

```text
LIVE_VERSION=V18
LIVE_RELEASE=V18-WEB-REALISM-1
LIVE_GLB_USED=Chamagnieu_V18_WEB_REALISM_UPGRADED.glb
LIVE_GLB_BYTES=22687292
LIVE_GLB_SHA256=9A5FD736CF5BFC4B8AF90A3B1A701C1532B83D2E6BDF0FA2C459B085B9A12B1E
LIVE_LIGHTING_PIPELINE=V18-WEB-REALISM-LIGHTING-R2
LIVE_MATERIALS=41
LIVE_TEXTURES_RUNTIME=119
CONFIG_MODEL_CHANGED=YES
LOCAL_CURRENT_EVIDENCE=PASS
PUBLIC_CURRENT_EVIDENCE=PASS
DOCUMENT_STATUS=PASS_CURRENT_PUBLIC_STATE
```
