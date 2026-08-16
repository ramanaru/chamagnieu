# Rapport courant des textures — modèle live WebP

> **SOURCE = STATIC FILE AUDIT**. Les images listées ici sont les payloads réellement liés dans le GLB.
> Les images de `/rapide/` portent **SOURCE = BLENDER** et ne sont pas des textures du viewer.

## Livraison

| Contrôle | Résultat |
|---|---|
| Modèle | `shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb` |
| SHA-256 | `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE` |
| Images embarquées | 37/37 |
| Codec | WebP |
| URI images externes | 0 |
| URI buffers externes | 0 |
| Bindings matière | 55/55 valides |
| Images atteignables depuis un binding | 37/37 |
| Texture inutilisée | `texture[50]` uniquement |
| BufferViews non référencées | 0 |
| Octets image orphelins | 0 |
| Décodage WebP | PASS, Three.js r179 + `GLTFTextureWebPExtension` |

Les textures ne font l’objet d’aucune requête HTTP individuelle. Le réseau télécharge uniquement `Chamagnieu_V18_REALISM_FINAL_WEBP.glb?release=v18-live-sync-4`; les 37 payloads sont lus depuis son chunk BIN.

## Comparaison source / ancien dérivé / live

- Source et live: 11,803,422 octets d’images WebP actives; 27×2048², 3×2048×2050, 5×1024², 2×256².
- Ancien dérivé: 2,818,542 octets JPEG actifs; 23×512², 12×1024², 2×256².
- L’ancien fichier conservait en plus les 11,803,422 octets WebP source dans 37 bufferViews orphelines.
- Le live réutilise byte-for-byte les payloads du master; il ne rééchantillonne aucune image.

## Images embarquées et usages exacts

| i | Image | Résolution live | Octets live | SHA-256 payload WebP | Ancien JPEG actif | Textures / matériaux actifs |
|---:|---|---:|---:|---|---|---|
| 0 | `white_stucco_nor_gl_2k` | 2048×2048 | 537,704 | `00D47A9B0FDD1E09E0CFE4C4D1C5756BAAA8B274841F929D3F6BAADE2B92D82D` | 512×512 JPEG / 12,903 | t0 · m2 V12_PBR_OFFWHITE_STUCCO:normal<br>t27 · m15 V10_STUCCO_NEW_BUILD:normal |
| 1 | `white_stucco_diff_2k` | 2048×2048 | 150,348 | `65C6FE3D9A78FFFE5D54F7068C2F87B520D69312FB8DB6841ED671FF91108615` | 512×512 JPEG / 6,046 | t1 · m2 V12_PBR_OFFWHITE_STUCCO:base<br>t28 · m15 V10_STUCCO_NEW_BUILD:base |
| 2 | `white_stucco_rough_2k` | 2048×2048 | 19,038 | `D329EE064A72D3479A9083F7A48F69EAA4A8B0ACDA1424FE7026B02BB7795F66` | 512×512 JPEG / 2,548 | t2 · m2 V12_PBR_OFFWHITE_STUCCO:rough/metal<br>t29 · m15 V10_STUCCO_NEW_BUILD:rough/metal |
| 3 | `floor_tiles_02_nor_gl_2k` | 2048×2048 | 33,962 | `044A9436906D22D8FD320ECBBF1577E98059CF77A777BE08CD88DC3365A050EC` | 512×512 JPEG / 7,174 | t3 · m3 PBR_B_FLOOR:normal<br>t42 · m25 V12_PBR_LIGHT_PORCELAIN:normal |
| 4 | `floor_tiles_02_diff_2k` | 2048×2048 | 154,188 | `FA5803336B6445066117BC3EB022AF27D5C66B178944DA0639CBCB3AE156034F` | 512×512 JPEG / 20,708 | t4 · m3 PBR_B_FLOOR:base<br>t43 · m25 V12_PBR_LIGHT_PORCELAIN:base |
| 5 | `floor_tiles_02_rough_2k` | 2048×2048 | 138,314 | `1D358B3CD7D6D75F38CE37F196F810F451C3B28CF57CA985DCDF45BFBE8BBF6B` | 512×512 JPEG / 21,295 | t5 · m3 PBR_B_FLOOR:rough/metal<br>t44 · m25 V12_PBR_LIGHT_PORCELAIN:rough/metal |
| 6 | `brushed_concrete_04_nor_gl_2k` | 2048×2048 | 684,500 | `A468FED2E241950DC40E9B485ABD710AF2A764A060ABD111219D3677EF08B091` | 512×512 JPEG / 42,600 | t6 · m5 PBR_B_CONCRETE:normal<br>t21 · m10 V10_BRUSHED_CONCRETE:normal<br>t45 · m28 V12_PBR_BRUSHED_CONCRETE:normal |
| 7 | `brushed_concrete_04_diff_2k` | 2048×2048 | 576,298 | `4541A8FD181FC790539970412B0208B5ECBBB62F2EA0958BBBA12897A8318E32` | 512×512 JPEG / 30,028 | t7 · m5 PBR_B_CONCRETE:base<br>t22 · m10 V10_BRUSHED_CONCRETE:base<br>t46 · m28 V12_PBR_BRUSHED_CONCRETE:base |
| 8 | `brushed_concrete_04_rough_2k` | 2048×2048 | 78,606 | `CC60F8E1C77D23631CB2778F78550BC4E0F620DC64B4647CE038E013E7FC8F65` | 512×512 JPEG / 6,023 | t8 · m5 PBR_B_CONCRETE:rough/metal<br>t23 · m10 V10_BRUSHED_CONCRETE:rough/metal<br>t47 · m28 V12_PBR_BRUSHED_CONCRETE:rough/metal |
| 9 | `clay_roof_tiles_02_nor_gl_2k` | 2048×2048 | 400,736 | `2E3E9862AAB84AE93D0C30B9185B1328F2C0AAFCF9A52F1543B2617B7916F43A` | 1024×1024 JPEG / 228,353 | t9 · m6 PBR_B_ROOF:normal |
| 10 | `clay_roof_tiles_02_diff_2k` | 2048×2048 | 388,540 | `BBBEAD143047E55CD8D7B7DB3AB2A9DE6EBDDCC556FBB33BE23CF1C745E522D1` | 1024×1024 JPEG / 207,755 | t10 · m6 PBR_B_ROOF:base |
| 11 | `clay_roof_tiles_02_rough_2k` | 2048×2048 | 31,210 | `35281DB73F58E0241A08EA671B87FB4EFD8D7A078A3E79D444ECC445984096E3` | 1024×1024 JPEG / 38,061 | t11 · m6 PBR_B_ROOF:rough/metal |
| 12 | `asphalt_01_nor_gl_2k` | 2048×2048 | 909,206 | `58FEE453FDB7B82E7FBDFE7CE6D3E0DE95D475259E2D7261CDAEB76CD3678E4D` | 1024×1024 JPEG / 310,248 | t12 · m7 PBR_B_ASPHALT:normal<br>t33 · m19 V10_ASPHALT:normal |
| 13 | `asphalt_01_diff_2k` | 2048×2048 | 388,102 | `0318AA197F715818C3DFD236AC1E2E38881758FE7C26BDDFAEBF8204D57ECF91` | 1024×1024 JPEG / 153,146 | t13 · m7 PBR_B_ASPHALT:base<br>t34 · m19 V10_ASPHALT:base |
| 14 | `asphalt_01_rough_2k` | 2048×2048 | 11,974 | `010143F740338D178BEE9DDDE9DDD7253177D3360B200BCB649617C4281445F2` | 1024×1024 JPEG / 9,703 | t14 · m7 PBR_B_ASPHALT:rough/metal<br>t35 · m19 V10_ASPHALT:rough/metal |
| 15 | `leafy_grass_nor_gl_2k` | 2048×2048 | 1,504,130 | `27E8CE520A4132DD561CC7A567053E83202ADCE7C35ABF49F56956E64051AADD` | 1024×1024 JPEG / 420,868 | t15 · m8 PBR_B_GRASS:normal |
| 16 | `leafy_grass_diff_2k` | 2048×2048 | 1,011,820 | `64206D056511DE99E781DC82AFBC5ABEF9651205A27AC0ED889C83C6278848E3` | 1024×1024 JPEG / 317,207 | t16 · m8 PBR_B_GRASS:base |
| 17 | `leafy_grass_rough_2k` | 2048×2048 | 61,420 | `A01243FDED9287BA07123D2405C4428CEA2C3ECE5388A61DB7A2CF4FD8E27578` | 1024×1024 JPEG / 36,745 | t17 · m8 PBR_B_GRASS:rough/metal |
| 18 | `american_walnut_veneer_nor_gl_2k` | 2048×2048 | 35,670 | `E83D0367F3DE80797C62E6AD2AEA6097B7C49F97A3E5E0557C038A2D3B2CCD4F` | 512×512 JPEG / 4,589 | t18 · m9 PBR_B_WOOD:normal<br>t24 · m14 V10_ENTRY_WOOD:normal |
| 19 | `american_walnut_veneer_diff_2k` | 2048×2048 | 192,060 | `470E15C6A41ECEE17B7F9C25024CD980662935138D8F939A189BFBF8B00EA003` | 512×512 JPEG / 17,354 | t19 · m9 PBR_B_WOOD:base<br>t25 · m14 V10_ENTRY_WOOD:base |
| 20 | `american_walnut_veneer_rough_2k` | 2048×2048 | 351,456 | `830E3E07FE2155EA00B8DC45796A7D4139DF377B9C49623378B2E358FEAFB3DE` | 512×512 JPEG / 21,580 | t20 · m9 PBR_B_WOOD:rough/metal<br>t26 · m14 V10_ENTRY_WOOD:rough/metal |
| 21 | `gravel_nor_gl_2k` | 2048×2048 | 1,319,230 | `8E0409C556B5643219B209968E8EBA935833B10DDCD61580923CBFAD9F733C87` | 1024×1024 JPEG / 459,912 | t30 · m17 V10_GRAVEL:normal |
| 22 | `gravel_diff_2k` | 2048×2048 | 430,502 | `956AC9EE371120EFE510A4360C54A4D6C6B5DB89974049454A75692316C4D994` | 1024×1024 JPEG / 219,000 | t31 · m17 V10_GRAVEL:base |
| 23 | `gravel_rough_2k` | 2048×2048 | 34,192 | `ACB8EE0E7480986503A2D61E86A9E6F7B0D88C62F02FB031FF3F87291CDD5EE5` | 1024×1024 JPEG / 27,346 | t32 · m17 V10_GRAVEL:rough/metal |
| 24 | `cotton_jersey_nor_gl_2k` | 2048×2050 | 240,428 | `24966716F403B7A66680151C701946E1D3530045CDB1E5B7A5636755F1DFD4C1` | 512×512 JPEG / 2,939 | t36 · m21 V12_PBR_BEIGE_COTTON:normal |
| 25 | `cotton_jersey_diff_2k` | 2048×2050 | 411,170 | `6832EDF8DF81DB15E73EE923DE12DD804A260AF1E27837785DECF480702FE4F7` | 512×512 JPEG / 5,118 | t37 · m21 V12_PBR_BEIGE_COTTON:base |
| 26 | `cotton_jersey_rough_2k` | 2048×2050 | 950,082 | `3D86B2EA176A6730234435BC8862C49A0A3C076A71EBA74DB3E140434964A5D8` | 512×512 JPEG / 14,427 | t38 · m21 V12_PBR_BEIGE_COTTON:rough/metal |
| 27 | `white_oak_veneer_nor_gl_2k` | 2048×2048 | 150,660 | `4D040277FECE19B7343842E12E3F1920E834D0E98BBECACF4D4E9BBCA240A04C` | 512×512 JPEG / 9,632 | t39 · m22 V12_PBR_WHITE_OAK:normal |
| 28 | `white_oak_veneer_diff_2k` | 2048×2048 | 214,838 | `354C22E28A3B5BB172A14F9A02F90F2F5C39516480990BEC5E056FD662E8B1DB` | 512×512 JPEG / 19,124 | t40 · m22 V12_PBR_WHITE_OAK:base |
| 29 | `white_oak_veneer_rough_2k` | 2048×2048 | 102,822 | `509C00EF7FB0C54C1B991A04B6184138D7F76EEB053C423E458CF0F0A7DEA530` | 512×512 JPEG / 8,926 | t41 · m22 V12_PBR_WHITE_OAK:rough/metal |
| 30 | `modern_coffee_table_01_nor_gl_1k` | 1024×1024 | 9,598 | `734B2FCB591EF8CE76413FB9C378431DAC2A851C9F2EF5B300FD07A77356FC8A` | 512×512 JPEG / 5,644 | t48 · m31 modern_coffee_table_01.001:normal |
| 31 | `modern_coffee_table_01_diff_1k` | 1024×1024 | 28,144 | `FA3E4BD88A241F14F0DF35E79E9DA278C460996B3E2BC98CA721FE2E7C8CDE15` | 512×512 JPEG / 15,246 | t49 · m31 modern_coffee_table_01.001:base |
| 32 | `potted_plant_04_nor_gl_1k` | 1024×1024 | 132,176 | `81F2082AFB0A6C77BD9F5AC795BE12C5FAC1119D38FF3C64597AD9AD7CF8786A` | 512×512 JPEG / 45,157 | t51 · m32 potted_plant_04:normal |
| 33 | `potted_plant_04_diff_1k` | 1024×1024 | 72,792 | `E95B133032CC2099029F652B26D4253A53A30DC3B7D681A34890829C5B81C6D7` | 512×512 JPEG / 36,667 | t52 · m32 potted_plant_04:base |
| 34 | `potted_plant_04_arm_1k` | 1024×1024 | 41,082 | `11C93EF226630F29817A38D16D0EE18FBDA771A4F0558B580725E3FE12B583D1` | 512×512 JPEG / 23,605 | t53 · m32 potted_plant_04:rough/metal |
| 35 | `v17_foliage_deep` | 256×256 | 3,018 | `B9E8B4D56661FBFFD5DE2A3222573F0251BD120EE074BD00BA9ACFF74883EC68` | 256×256 JPEG / 5,169 | t54 · m33 V17_PBR_FOLIAGE_DEEP:base |
| 36 | `v17_foliage_fresh` | 256×256 | 3,406 | `35E265FDD61230E6EF86790E964FE1861DBF02AB777548E018E5E6FF7C5D5E79` | 256×256 JPEG / 5,696 | t55 · m34 V17_PBR_FOLIAGE_FRESH:base |

## Correction t50

Le master liait `materials[31].pbrMetallicRoughness.metallicRoughnessTexture.index=50`, mais `textures[50]` ne possède ni `source` core ni `EXT_texture_webp.source`. Le nouveau modèle supprime ce seul binding. `texture[50]` reste un objet mort non lié; tous les 55 bindings restants résolvent une image WebP valide.

## Statut HTTP

| Ressource | URL runtime | Requête requise | Statut structurel |
|---|---|---:|---|
| Modèle + 37 images | `shared/Chamagnieu_V18_REALISM_FINAL_WEBP.glb?release=v18-live-sync-4` | 1 | publié; HTTP 200; 25,169,320 octets; SHA public vérifié |
| Sidecars textures | aucun | 0 | non applicable |
| Galerie Blender | `shared/gallery/*.webp?release=v18-live-sync-4` | 9 images statiques | distincte du GLB |

Vérification publique du 16 août 2026: le modèle GitHub Pages répond HTTP 200, `Content-Type: model/gltf-binary`, taille 25,169,320 et SHA-256 `69F10EC076B68968CA91F0412481956F5CE0E1DE972ECB5E25CBF69990306DDE`. Cette preuve HTTP confirme le binaire publié; elle ne présente pas la galerie Blender comme preuve de texture live.
