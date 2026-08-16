# Inventaire GLB courant — V18 WebP

> `SOURCE = STATIC FILE AUDIT`. Aucun rendu Blender n’est utilisé comme preuve de structure.

## Identité des fichiers

| Fichier / rôle | Octets | SHA-256 | JSON | BIN | Codec images | Actif |
|---|---:|---|---:|---:|---|---|
| Master source `Chamagnieu_V18_ROOF_GROUND_REALISM_WEBP.glb` | 25,169,404 | `97F842001CC77E65637271172D09A81043FFFDF3235591DCB1AFF0BA96D67DA0` | 754,796 | 24,414,580 | 37 WebP | non publié; source immuable |
| `shared/Chamagnieu_V18_REALISM_FINAL.glb` ancien dérivé | 27,987,896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | 754,700 | 27,233,168 | 37 JPEG actives + WebP orphelines | non |
| `shared/Chamagnieu_V18_ROOF_GROUND_REALISM.glb` alias ancien | 27,987,896 | `79A0F908DCCA94ADE328A46247D51118BDEB51CE1217DE567E2040DB05D58C28` | 754,700 | 27,233,168 | identique au dérivé JPEG | non |
| `shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb` **live** | 25,169,320 | `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE` | 754,712 | 24,414,580 | 37 WebP | **oui** |

Les deux anciens fichiers partagent exactement les mêmes octets. Il n’existe aucun `.gltf`, GLB lite, GLB presentation, GLB viewer ou fallback distinct.

## Structure comparée

| Mesure | Master WebP | Ancien dérivé JPEG | Nouveau live WebP |
|---|---:|---:|---:|
| scènes | 1 | 1 | 1 |
| nœuds | 794 | 794 | 794 |
| meshes glTF | 793 | 793 | 793 |
| primitives | 795 | 795 | 795 |
| accessors | 2454 | 2454 | 2454 |
| bufferViews | 2491 | 2528 | 2491 |
| matériaux | 35 | 35 | 35 |
| textures | 56 | 56 | 56 |
| images | 37 | 37 | 37 |
| images externes | 0 | 0 | 0 |
| bindings matière | 56 | 55 | 55 |
| bindings actifs invalides | 1 | 0 | 0 |
| bufferViews orphelines | 0 | **37** | 0 |
| octets bufferView orphelins | 0 | **11,803,422** | 0 |

## Preuve de géométrie inchangée

| Sous-ensemble canonique | SHA-256 commun |
|---|---|
| accessors / payloads géométriques | `958B7BB2D4531F49BB2001D8ABD02850CDB88BC6A4CE9D60567EADA74365E5B9` |
| nœuds JSON | `ADC58148C34EDE75C601C65498625EE8AF18EEE8BC9561D98214A4941B0C0A47` |
| meshes JSON | `8068BC0209DBD7D65060946C213C8FAD87332A8D4DAFC5A6008B70BAADA6688A` |
| accessors JSON | `4A069FE680770C0FA565A738F82605FDE480F0B5AA662D7A2065E37C9BFF1FA8` |

Le chunk BIN du nouveau live est byte-identique au master: 24,414,580 octets, SHA-256 `F7E89CA346FAB71A658D3224FAE0D2D33B7966B39B93C5E4D5AF04717C22ED17`. Le JSON courant est le master moins une seule propriété: le binding t50 invalide.

## Défaut de l’ancien dérivé JPEG

Les 37 images WebP du master occupaient 11,803,422 octets dans 37 bufferViews conservées, mais aucune image active ne les référençait. Trente-sept JPEG réduits (2,818,542 octets) avaient été ajoutés et devenaient les sources actives. Le fichier était donc plus lourd tout en affichant moins de détails.

BufferViews orphelines exactes:

```text
106,107,108,204,205,206,238,239,240,245,246,247,260,261,262,267,268,269,273,274,275,752,753,754,949,950,951,958,959,960,1870,1871,1876,1877,1878,2332,2339
```

## Binding t50

| État | `/materials/31/pbrMetallicRoughness/metallicRoughnessTexture` | `texture[50]` | Résultat |
|---|---|---|---|
| Master source | présent, index 50 | `{"extensions":{},"sampler":0}`, aucune source | invalide |
| Ancien JPEG | absent | objet mort | valide mais basse définition |
| Nouveau live | absent | objet inutilisé, non lié | 55/55 bindings valides |

## Extensions du modèle live

```text
extensionsUsed=KHR_materials_transmission,KHR_materials_ior,KHR_texture_transform,EXT_texture_webp
extensionsRequired=KHR_texture_transform,EXT_texture_webp
Three.js=179
GLTFLoader_EXT_texture_webp=SUPPORTED
```

Preuve indépendante: `validation/webp-model-validation.txt` se termine par `WEBP_MODEL_VALIDATION=PASS`.
