# Éclairage et matériaux du rendu live — V18-LIVE-SYNC-3

## Verdict

**Statut global : `PARTIAL`.**

La synchronisation technique est maintenant démontrée localement : `/presentation/` et `/visite/` chargent la même configuration, le même GLB V18, la même version de cache et le même module de réglage visuel. Le rendu Web final gagne en contraste, ombres, filtrage oblique et réponse des matériaux physiques. Il ne devient toutefois pas un rendu Blender/D5 équivalent.

```text
RUNTIME_SYNC_STATUS=PASS_PUBLIC_HTTP
LIVE_GLTF_LOAD_STATUS=PASS_PUBLIC_HTTP
SOURCE_LABEL_STATUS=PASS
LIVE_LIGHTING_IMPROVEMENT=YES
LIVE_MATCHES_BLENDER_D5=NO
PUBLIC_DEPLOYMENT_VERIFIED=YES_HTTP
PUBLIC_BROWSER_VISUAL_RELEASE=V18-LIVE-SYNC-2
FINAL_PUBLIC_RELEASE=V18-LIVE-SYNC-3
OVERALL_REALISM_STATUS=PARTIAL
```

## Preuves navigateur et publication finale

La preuve visuelle/console principale est `../validation/live-browser-validation.json`, issue du vrai viewer Web `V18-LIVE-SYNC-2` sur `http://127.0.0.1:8896/`. Le dernier changement `V18-LIVE-SYNC-3` propage uniquement le toggle mobilier aux enfants de deux fauteuils multi-primitives et renouvelle la clé de cache; il ne modifie ni modèle, ni matériaux, ni caméra, ni éclairage, ni pixels des trois captures.

La release publique finale `V18-LIVE-SYNC-3` a été vérifiée séparément par lecture HTTP de ses cinq pages, huit ressources runtime et du GLB complet, puis par hash et parsing glTF. Cette distinction évite d'attribuer une preuve navigateur release 2 à la release 3.

| Route | HTTP | Version/release | Modèle | État | Provenance affichée |
|---|---:|---|---|---|---|
| `/` | 200 | `V18` / `V18-LIVE-SYNC-3` | page statique | images décodées | 2 × `SOURCE = BLENDER` |
| `/presentation/` | 200 | `V18` / `V18-LIVE-SYNC-3` | `Chamagnieu_V18_REALISM_FINAL.glb` | `viewerReady=true` | `SOURCE = LIVE WEB VIEWER` |
| `/visite/` | 200 | `V18` / `V18-LIVE-SYNC-3` | `Chamagnieu_V18_REALISM_FINAL.glb` | `viewerReady=true` | `SOURCE = LIVE WEB VIEWER` |
| `/rapide/` | 200 | `V18` / `V18-LIVE-SYNC-3` | galerie statique | 9 images décodées | 9 × `SOURCE = BLENDER` |
| `/gpt/` | 200 | `V18` / `V18-LIVE-SYNC-3` | page statique dédiée | URL conservée | pas de faux libellé live |

Résultat navigateur release 2 : 5 navigations HTTP 200, aucune réponse observée hors 200, aucune image cassée, aucune erreur console d’origine page, aucun service worker et aucune clé Cache Storage. Les seuls messages supplémentaires provenaient de l’extension Chrome `mv-walker`, pas de la maison.

Résultat public final release 3 : `V18_RUNTIME_VALIDATION=PASS pages=5 http_200=14 ... model_bytes=27987896 ... embedded_images=37 external_images=0 furniture_nodes=167 furniture_runtime_meshes=169`.

## Chaîne runtime réellement utilisée

Les deux viewers importent maintenant :

1. `shared/project-config.js` ;
2. `shared/project-config.json` ;
3. `shared/live-realism.js` ;
4. `shared/Chamagnieu_V18_REALISM_FINAL.glb?release=v18-live-sync-3`.

Le GLB chargé fait **27 987 896 octets** et sa valeur attendue est :

```text
SHA256=79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28
```

Le nom historique `Chamagnieu_V18_ROOF_GROUND_REALISM.glb` désigne une copie byte-identique. L’ancienne différence observée entre présentation et visite ne venait donc pas du contenu binaire : `/presentation/` utilisait un pipeline lumineux autonome tandis que `/visite/` chargeait déjà les réglages centralisés. Cette divergence est corrigée en `V18-LIVE-SYNC-3`.

## Réglages lumineux finaux

| Élément | Valeur finale | Effet vérifiable | Limite |
|---|---:|---|---|
| Espace couleur | sRGB | albédo interprété correctement | ne corrige pas la qualité des maps |
| Tone mapping | ACES Filmic | hautes lumières moins brutes | rendu différent d’Eevee/D5 |
| Exposition | `0.92` | moins de surfaces brûlées | intérieur encore très clair |
| IBL | PMREM issue d’un Canvas 512 × 256 | reflets plus cohérents | gradient procédural, pas une HDRI photographique |
| HemisphereLight | `0.72` | remplissage ciel/sol | conserve un aspect studio simplifié |
| AmbientLight | `0.06` | ombres moins délavées | aucune occlusion ambiante texturée |
| DirectionalLight | `2.4` | direction et ombres plus lisibles | une seule source solaire principale |
| Fill light | `0.22` | débouche le côté opposé | ne reproduit pas les luminaires Blender |
| Ombres desktop | PCFSoft 2048 | profondeur/contact améliorés | désactivées sur mobile |
| Anisotropie | jusqu’à `8` | toit/sol moins flous en incidence rasante | dépend du GPU |
| `envMapIntensity` | `0.90` verre/métal, `0.55` autres | réponse physique plus lisible | valeurs globales, sans étalonnage matériau par matériau |

L’audit runtime de `/presentation/` et `/visite/` retourne exactement les mêmes valeurs :

```text
meshes=795
uniqueMaterials=35
uniqueTextures=71
texturedMaterialBindings=501
anisotropy=8
environment=procedural PMREM IBL
shadows=PCFSoft-2048
```

`uniqueTextures=71` correspond aux objets `THREE.Texture` après décodage/instanciation runtime ; l’inventaire glTF brut contient 56 objets texture et 37 images JPEG intégrées.

## Pourquoi le résultat reste partiel

1. **Les images Blender sont des rendus 2D, pas des maps 3D.** Elles contiennent déjà lumière, ombres, exposition et post-traitement. Aucun viewer ne peut les « remettre » sur toute la maison comme des textures de matériau.
2. **Les textures du GLB sont présentes.** Les 37 images sont embarquées dans le binaire ; `externalTextureCount=0`, donc aucun chemin externe cassé n’explique le rendu.
3. **Seulement 20/35 matériaux possèdent une texture.** Les 15 autres utilisent couleur/metallic/roughness sans grain local : alu, verre, chrome, pierre, laque, miroir, appareils noirs, greige cuisine, etc.
4. **Aucune texture AO ou emissive.** Les contacts mobilier/sol et l’éclairage intérieur restent plus plats qu’en Blender/D5.
5. **Géométrie simplifiée.** Les trois grands pans de toiture comptent chacun 6 triangles ; les sols restent des surfaces simples. Une normal map ne crée pas une vraie géométrie de tuile.
6. **Végétation Web légère.** Les quatre arbres et dix-huit haies utilisent des silhouettes low-poly et deux JPEG 256² base-color-only, sans alpha, normale ou roughness.
7. **Mobilier mixte.** Douze nœuds détaillés/sourcés Poly Haven représentent 60,3 % des triangles, mais 495 nœuds partagent une topologie répétée de 188 triangles, ce qui conserve un aspect procédural/bloc sur plusieurs meubles.
8. **Qualité mobile volontairement réduite.** Ombres coupées et pixel ratio plafonné à 1,1 ; les textures restent présentes, mais la profondeur baisse.
9. **Preuve navigateur segmentée.** Les captures et la console proviennent de la release 2; l'identité publique finale release 3 est prouvée par HTTP, hash du GLB, parsing glTF et syntaxe des modules. Le correctif release 3 ne change pas le rendu visuel.

## Lecture des trois vues

### Façade

L’après montre un toit plus sombre, une texture rasante mieux filtrée et des ombres plus présentes sur les volumes et le chemin. La couverture, le sol et la haie restent néanmoins géométriquement simples. La référence Blender conserve davantage de micro-contraste, de relief de tuiles et de séparation lumineuse.

### Jardin

L’après ajoute des ombres au sol et un vert moins uniformément éclairé. Les masses rondes des canopées et les blocs de haie ne changent pas : leur limite est géométrique et liée aux deux feuillages 256², pas au chargement réseau.

### Intérieur

L’après réduit légèrement l’effet surexposé et rend le bois/sol plus lisible. Le canapé, plusieurs chaises et surfaces blanches restent très pâles ; l’absence d’AO, de lumières intérieures élaborées et les matériaux facteur-seulement empêchent une correspondance avec la référence Blender.

## Conclusion

`V18-LIVE-SYNC-3` règle la **cohérence de livraison et de runtime** : une source de vérité, un modèle, un cache key, un pipeline lumineux et des libellés de provenance. Le diagnostic « les textures ne chargent pas » est rejeté. Le manque de photoréalisme restant vient principalement de la différence de moteur, de la lumière procédurale, des matériaux non texturés, de l’absence d’AO/emissive et de la géométrie Web allégée. Le statut reste donc honnêtement **`PARTIAL`**.
