# Audit navigateur final — V18-ASSET-PILOT-1

**Résultat fonctionnel : PASS.** Audit réel dans le navigateur intégré sur le serveur local, après rechargements avec cache désactivé puis restauré.

- Viewer : viewerReady=true, V18, V18-ASSET-PILOT-1
- Modèle : Chamagnieu_V18_WEB_REALISM_UPGRADED.glb
- Rendu : WebGL2
- Catégories : **8/8** visibles et chargées (canapé, table, chaises, lits, arbres, haies, façade PBR, herbe PBR)
- Mobilier : **true → false → true** dans Présentation et Visite
- Entrée : Présentation → Visite extérieure → Commencer dehors → repli souris/glisser + clavier → Cuisine intérieure
- Réseau froid : Présentation **138 réponses, 0 échec, 0 non-2xx** ; Visite **138 réponses, 0 échec, 0 non-2xx**
- Console : **0 erreur / avertissement** ; exceptions Runtime : **0** ; images cassées : **0**

## rAF observé honnêtement

Le navigateur intégré d’un sous-agent maintient l’onglet en arrière-plan et Chromium réduit sa cadence. Mesures brutes : Présentation **11.51 fps**, Visite **11.73 fps**. Elles prouvent une limitation d’ordonnancement en arrière-plan, pas la capacité GPU au premier plan ; le gate 30 fps est donc **indéterminé dans ce contexte précis**.

## Captures

Toutes les captures ci-dessous portent le badge **SOURCE = LIVE WEB VIEWER** :

- validation/asset_pilot_screenshots/browser_final/01-presentation-facade-live.png — 65536×4292542531, 123818 octets, SHA-256 56869D5894B879365CE6B49276B43228B364750A7251D00F461D4DCF38BA4E01
- validation/asset_pilot_screenshots/browser_final/02-presentation-hedges-live.png — 65536×4292542531, 140356 octets, SHA-256 71DF793E2C5CDAD2F3A8C254B6A200218801924788C530F18969F06B15E72FF9
- validation/asset_pilot_screenshots/browser_final/03-presentation-living-sofa-live.png — 65536×4292542531, 93489 octets, SHA-256 90B7805E9828F3D710FFE42D45811683E700A0B059B776E228C30BD92E42B9BA
- validation/asset_pilot_screenshots/browser_final/04-presentation-dining-table-chairs-live.png — 65536×4292542531, 96074 octets, SHA-256 D47833D4A674EFDE42032DC740B5D67AD955BC75C6E0C2E90A05FC10AE0AB3D6
- validation/asset_pilot_screenshots/browser_final/05-presentation-bedroom-bed-live.png — 65536×4292542531, 77588 octets, SHA-256 A3FE6D7C7FD915B69390480942AB1FECFB848ABF52604E447B42CEF391953830
- validation/asset_pilot_screenshots/browser_final/06-presentation-exterior-ground-live.png — 65536×4292542531, 142085 octets, SHA-256 678BBE39106A428B1FB01F3E0BC625647705AA8096D6A8E49968FABFE1DD31D4
- validation/asset_pilot_screenshots/browser_final/07-presentation-garden-trees-live.png — 65536×4292542531, 109016 octets, SHA-256 93E2C074A0B2DED9CD73169BE77A36004A15179B2C21E0B3765EFDE267E16D52
- validation/asset_pilot_screenshots/browser_final/08-visite-start-outside-live.png — 65536×4292542531, 124207 octets, SHA-256 1C0466CF086A3CF88D2E175FEB423A0FFB336D10E7374A9C2C73CB77BE97EA7C
- validation/asset_pilot_screenshots/browser_final/09-visite-inside-kitchen-live.png — 65536×4292542531, 82341 octets, SHA-256 438AF23ECFBB09B33C42600CD4878678429AF377D7F413C4578002C64F882353
