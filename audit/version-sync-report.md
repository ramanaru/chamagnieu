# Audit public courant — synchronisation V18 WebP

> **SOURCE = STATIC FILE AUDIT** pour les hashes, structures glTF et références de code.
> **SOURCE = LIVE WEB VIEWER** désigne uniquement `/presentation/` et `/visite/`.
> **SOURCE = BLENDER** désigne uniquement les WebP de galerie; ces images ne sont jamais appliquées au GLB.

## Vérité courante

| Champ | Valeur vérifiée |
|---|---|
| Version UI | `V18` |
| Release | `V18-LIVE-SYNC-4` |
| Clé de cache | `v18-live-sync-4` |
| Commit publié sur `origin/main` | `5314d8de6df6ba3e9175e3e5825c5a0189a2c706` |
| Configuration unique | `shared/project-config.json` |
| Modèle live | `shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb` |
| Octets | 25,169,320 |
| SHA-256 | `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE` |
| Géométrie | 794 nœuds, 793 meshes glTF, 795 primitives, 2 454 accessors |
| Matériaux / textures / images | 35 / 56 / 37 |
| Images actives | 37 WebP embarquées, 0 URI externe |
| Binding matière valide | 55/55; `texture[50]` inutilisée |
| Données image orphelines | 0 bufferView, 0 octet |

Le fichier live est le master WebP haute définition corrigé. Son chunk BIN (`F7E89CA346FAB71A658D3224FAE0D2D33B7966B39B93C5E4D5AF04717C22ED17`) est byte-identique au master source `97F842001CC77E65637271172D09A81043FFFDF3235591DCB1AFF0BA96D67DA0`. La seule modification sémantique du JSON glTF est la suppression du binding invalide `/materials/31/pbrMetallicRoughness/metallicRoughnessTexture` vers `texture[50]`, qui ne possède aucune source.

## Pages et chargements

| Page | Version/source | GLB | JSON | Scripts / images | Cache |
|---|---|---|---|---|---|
| `/` | `V18`; images `SOURCE = BLENDER` | aucun GLB runtime | `shared/project-config.json` via `page-version.js` | 2 rendus WebP Blender | entrée `?release=v18-live-sync-4`; config `no-store` |
| `/presentation/` | `V18`; `SOURCE = LIVE WEB VIEWER` | `Chamagnieu_V18_REALISM_FINAL_WEBP.glb?release=v18-live-sync-4` | config centrale | Three r179, OrbitControls, GLTFLoader, `presentation.js`, `live-realism.js` | CSS, entrée, helpers et GLB versionnés |
| `/visite/` | `V18`; `SOURCE = LIVE WEB VIEWER` | le même nom, hash et query | config centrale | Three r179, PointerLockControls, GLTFLoader, `visite.js`, `live-realism.js` | CSS, entrée, helpers et GLB versionnés |
| `/rapide/` | `V18`; 9 badges `SOURCE = BLENDER` | aucun | config centrale | 9 rendus WebP, pas des textures live | images et `page-version.js` versionnés |
| `/gpt/` | `V18`; politique de sources explicite | aucun chargement 3D | config + lien `house.json` | `page-version.js` | entrée et helper versionnés |

`presentation.js` et `visite.js` appellent `loadProjectConfig()`, résolvent `config.model`, puis posent `release=config.cacheKey` sur l’URL du GLB. Aucun viewer ne contient un chemin GLB historique codé en dur.

## Pourquoi le rendu détaillé n’apparaissait pas

| Fichier | Images réellement actives | Résolution | Octets images actives | Défaut |
|---|---:|---|---:|---|
| Master source WebP `97F842001CC7…` | 37 WebP | 27×2048², 3×2048×2050, 5×1024², 2×256² | 11 803 422 | binding t50 invalide |
| Ancien dérivé JPEG `79A0F908DCCA…` | 37 JPEG | 23×512², 12×1024², 2×256² | 2 818 542 | 37 anciens WebP conservés mais inaccessibles: **11 803 422 octets orphelins** |
| Nouveau live WebP `69F10EC076B6…` | 37 WebP | identique au master | 11 803 422 | aucun binding actif invalide; aucun octet orphelin |

L’ancien dérivé téléchargeait donc les images haute définition sans les utiliser, puis liait des JPEG réduits. Le correctif réactive exactement les payloads WebP du master et retire uniquement le binding t50 sans source.

## [DIAGNOSTIC INITIAL — PAS ÉTAT ACTIF] Pourquoi « V11 » pouvait être observé

Le token V11 est une nomenclature interne héritée, pas la version du viewer. Le GLB courant est cumulatif: 416 noms de nœuds commencent par ce préfixe, principalement du mobilier. Les deux scripts live conservent ces préfixes uniquement pour reconnaître les meubles et permettre le bouton Masquer/Afficher. L’UI, la configuration, le nom du GLB et la release courants restent V18.

## Matériaux, mobilier et végétation

- **Matériaux :** 35 au total; 20 texturés, 15 à facteurs; 20 bindings base color, 18 normal, 17 metallic/roughness, 0 occlusion, 0 emissive.
- **Mobilier :** 167 nœuds glTF nommés donnent 169 meshes runtime; 12 nœuds détaillés sourcés Poly Haven CC0 (191,047 triangles) et 155 nœuds procéduraux (28,272 triangles).
- **Végétation :** 4 arbres composés de 28 meshes (5,104 triangles) et 18 haies (1,944 triangles). Les deux matériaux feuillage utilisent seulement des albedos 256² opaques, sans normal map, roughness map ni alpha: l’aspect low-poly restant vient du contenu du GLB, pas d’un échec réseau.
- **Table extérieure :** aucun nœud `OUTDOOR`; `assets.outdoorDiningNodes=0`.

## Lumière live

Le viewer Web utilise sRGB, ACES Filmic, exposition 0,92, environnement procédural PMREM IBL à 0,85, Hemisphere 0,72, Ambient 0,06, soleil directionnel 2,4 et fill 0,22. Les ombres PCFSoft 2048 sont actives sur desktop et désactivées sur mobile. L’anisotropie est limitée à 8; l’intensité environnement matière vaut 0,8 ou 1,15 pour les surfaces réfléchissantes.

Ce pipeline reste différent d’un rendu Blender/D5: aucun HDRI photographique, path tracing, SSR ou SSAO n’est chargé. La correspondance de texture est corrigée, mais la végétation et les objets procéduraux limitent encore le photoréalisme.

## Cache et imports

- `project-config.json` est fetché avec `cache: 'no-store'`;
- les liens de navigation, CSS, scripts d’entrée, `project-config.js`, `live-realism.js`, galerie et GLB utilisent `v18-live-sync-4` dans leur query;
- les dépendances vendor Three.js gardent des URL stables, mais leur code n’a pas changé dans cette correction;
- aucun enregistrement Service Worker, CacheStorage ou Workbox n’existe dans les sources runtime;
- le nouveau nom `Chamagnieu_V18_REALISM_FINAL_WEBP.glb` empêche de confondre le GLB WebP avec l’ancien dérivé JPEG.

## Verdict courant

```text
CURRENT_VIEWER_VERSION=V18
CURRENT_RELEASE=V18-LIVE-SYNC-4
CURRENT_LIVE_GLB=shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb
CURRENT_LIVE_GLB_SHA256=69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE
CURRENT_TEXTURE_CODEC=WEBP
CURRENT_TEXTURES_EMBEDDED=37/37
CURRENT_EXTERNAL_TEXTURE_URIS=0
CURRENT_VALID_TEXTURE_BINDINGS=55/55
CURRENT_UNUSED_TEXTURES=[50]
CURRENT_ORPHAN_IMAGE_BYTES=0
CURRENT_SOURCE_LABEL_PRESENTATION=LIVE WEB VIEWER
CURRENT_SOURCE_LABEL_GALLERY=BLENDER
CURRENT_SYNC_STATUS=PASS_STATIC
CURRENT_PUBLIC_HTTP_STATUS=PASS
CURRENT_REALISM_STATUS=PARTIAL
```

Le 16 août 2026, `/`, `/presentation/`, `/visite/`, `/rapide/`, `/gpt/` et `shared/project-config.json` ont répondu HTTP 200 sur GitHub Pages. Le GLB public a livré 25,169,320 octets avec le SHA-256 attendu `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE`. `PASS_STATIC` et `PASS` HTTP prouvent la synchronisation des fichiers publiés; la preuve de rendu navigateur reste séparée et doit porter explicitement `SOURCE = LIVE WEB VIEWER`.
