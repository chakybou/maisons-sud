# -*- coding: utf-8 -*-
"""Source de vérité : les biens de la short-list.

Pour ajouter ou modifier un bien, on édite CE fichier — jamais le HTML,
jamais le PDF. Les deux générateurs (generer-page-maisons.py et
generer-pdf-maisons.py) lisent ces données.

Champ `photos`    : 1 à 3 URLs de photos sur le serveur de l'annonce (utilisées par le
                    HTML). La première est affichée en grand, les suivantes en vignettes.
                    Les URLs des annonces expirent : si une photo est cassée, la relever
                    à nouveau sur l'annonce.
Champ `autres_annonces` : liste optionnelle de (libellé, url) — le même bien publié
                    ailleurs. Omettre le champ si le bien n'est que sur une annonce.
Champ `rouge`     : True = fiche affichée en rouge et reléguée en fin de page.
                    Omettre le champ (ou False) pour une fiche normale.
Champ `photo_fichier` : nom du fichier dans photos/ (utilisé par le PDF, qui doit
                    embarquer l'image ; les serveurs d'annonces bloquent l'accès
                    automatisé, donc la photo est stockée localement).
"""

BIENS = [
  dict(ref="103041457", titre="Villa avec piscine en bord de mer",
       commune="Saint-Aygulf", secteur="Var (83)",
       agence="Côte d'Azur Sotheby's International Realty", source="Le Figaro Propriétés",
       prix=1570000, prixM2="8 722 € / m²",
       negociation="Négociable entre 1,3 et 1,4 M€ selon l'agence",
       surface="180 m²", terrain="1 560 m²", pieces="5", chambres="4",
       piscine="Oui", dpe="D / GES D", vue="Mer et Estérel",
       commentaire="La maison idéale du padre.",
       url="https://proprietes.lefigaro.fr/annonces/villa-var-provence+alpes+cote+d+azur-france/103041457/?priceMin=1000000&priceMax=1600000",
       photos=[
         "https://lh3.googleusercontent.com/T_adkzJJ4w3g1e4OrnQvq87y_Jw7D3hZOU1wVMsCLTYQw2JvgHbvzIzW59qTQosYP63BWAYjRcBfkIaclI45VLEPjxDHmrG5yUAhUA=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/7Jl7y35YQAhNRSAfR8ue-toWrGvrIKyDJvKEfcizPF7phkurCXPkjboigmvlrO0WVETsdDCzYMIJHCgCuCjXSnlneVdDzdcgUNtV=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/DBmPFBFLiSqxRDFzvCS07ZXXNRcpP6m-WaYS4Zo_IzruZE17UDLPnOj0TWhdsSNzlnWxanZg0Yp8Mcs_qdZlyejxbqr3PW_RSqTF=rj-w900-h675-n-l80",
       ],
       photo_fichier="103041457.webp"),

  dict(ref="107859973", titre="Villa avec piscine et jardin",
       commune="Agay", secteur="Var (83)",
       agence="Millesime Immobilier Agay", source="Le Figaro Propriétés",
       prix=1260000, prixM2="11 150 € / m²", negociation=None,
       surface="113 m²", terrain="950 m²", pieces="4", chambres="3",
       piscine="Oui, à débordement", dpe="E / GES C", vue=None,
       commentaire="Petite maison. Tout est à buller et à refaire. Belle vue. À 11 150 € le m², chère au m².",
       url="https://proprietes.lefigaro.fr/annonces/villa-var-provence+alpes+cote+d+azur-france/107859973/?priceMin=800000&priceMax=1800000",
       photos=[
         "https://lh3.googleusercontent.com/Udp-XOXwBosxMMg5EcZKoMqYJxIVj6QfzxfjQzLuNm7hE29_FlVfXER2sJnSPyjFwWBxBAjaHSKCwfyQnMACWZlXZAWjrpQ__81p0LA=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/CxvXojF1G1Zj6q9lch-IXh9gAI4TSvqqP7lqUqbcTMuVOLHbh_QiiQjoKqMDfyKzy2Crvf9CVNyAL58MCSWT9CiyptKdMHx1jKue9g=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/SiZTkUz9S0MVsPJKgIybaGXr2UtAU-byT2IILUHL41C16ycaaFnyNMdTIpD-zDQjiv03dDNbPa9dA0Br30pBQ90nuS7pdKG130tBMfI=rj-w900-h675-n-l80",
       ],
       photo_fichier="107859973.webp"),

  dict(ref="96300379", rouge=True, titre="Villa avec jardin et terrasse",
       commune="Agay", secteur="Var (83)",
       agence="Millesime Immobilier Agay", source="Le Figaro Propriétés",
       prix=1380000, prixM2="5 208 € / m²", negociation=None,
       surface="265 m²", terrain="1 370 m²", pieces="8", chambres="5",
       piscine="Non — terrain piscinable", dpe="C / GES A", vue="Mer à 180°, plein sud",
       commentaire="Pas de piscine mais piscinable selon l'annonce — à voir, et surtout où.",
       url="https://proprietes.lefigaro.fr/annonces/villa-var-provence+alpes+cote+d+azur-france/96300379/?priceMin=800000&priceMax=1800000",
       photos=[
         "https://lh3.googleusercontent.com/1hPhVUWvSDLELz6Yoo7z7MgV_lBAwwNazITkmN_WDUtN63Utdolpznj8Dplys419CexzxN48RMN5On7feU8M0Z3vpH_-5OtTPlWl16k=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/qGaldVGy4lZg6FMdwuG6T-0Jzg7_agH8K2tKg0hQOwvtCTJbOpW3HszuDwmXgqL5r74w1ZHtZqbZUyMS2jSKr5CUnaIyu8VTO_dHkQ=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/rMcOM9h7fHd4KGZRYjtX7X1MaOZOiFLa1alUsjmF6-A_2YrIrfT6hTsNZHacIKorVvEmbLhyp2-BVjXGvUNbqqe4VrQSltbFf7pN_A=rj-w900-h675-n-l80",
       ],
       photo_fichier="96300379.webp"),

  dict(ref="89126557", rouge=True, titre="Villa avec piscine et terrasse",
       commune="Saint-Raphaël — Boulouris", secteur="Var (83)",
       agence="Agence du Cap Immogolf", source="Le Figaro Propriétés",
       prix=1300000, prixM2="5 909 € / m²", negociation=None,
       surface="220 m²", terrain="692 m²", pieces="9", chambres="5",
       piscine="Oui", dpe=None, vue=None,
       commentaire="À Bouloris. Mais la vue mer semble limitée.",
       url="https://proprietes.lefigaro.fr/annonces/villa-var-provence+alpes+cote+d+azur-france/89126557/?priceMin=800000&priceMax=1800000",
       photos=[
         "https://lh3.googleusercontent.com/2MPoKeWKi0KyCTgoQISIwqX7XtvYUJr-8yvC_lvY1d0rKAHYBzAoXIQTnQfedM2fUoZJZXbBGmuqoXdzBcZFfiU3F8tL_N1Ta4307g=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/sIJ0tTqIKYYZUGR01BaQmVSAVeLipFvk0ImL-GuG3q58oeefG-KLcMUWPjnt5u-pIgVv2uaJDp--3elr_C_CnnDCBHUCMMbyXkdxeQ=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/Zq8oE755ti-pbOvyHVGWMSrCVKmOVr37PE8U27bqpcKd7Dof9ARl9lEzoh-ndw2TxwpwIASrGYTfpuN1I1_8xvqcJf44lr1Lo7Vm5EY=rj-w900-h675-n-l80",
       ],
       photo_fichier="89126557.webp"),

  dict(ref="3250258132", titre="Villa 6 pièces",
       commune="Saint-Raphaël — Aiguebonne", secteur="Var (83)",
       agence="Canat & Warton", source="leboncoin",
       prix=1370000, prixM2="7 611 € / m²", negociation=None,
       surface="180 m²", terrain="1 200 m²", pieces="6", chambres="4",
       piscine=None, dpe=None, vue="Mer, plein sud",
       commentaire="La maison à Bouloris (Ayguebonne), à 80 m du train.",
       url="https://www.leboncoin.fr/ad/ventes_immobilieres/3250258132",
       photos=[
         "https://img.leboncoin.fr/api/v1/lbcpb1/images/81/87/b7/8187b733813d4079b7b488203216033dc673493c.jpg?rule=ad-image",
         "https://img.leboncoin.fr/api/v1/lbcpb1/images/ec/13/3a/ec133aae1001fed651657620d14e6df2372deb84.jpg?rule=ad-image",
         "https://img.leboncoin.fr/api/v1/lbcpb1/images/6e/cb/2f/6ecb2f49df11039adb421e5a56d53bb94f6cd77f.jpg?rule=ad-image",
       ],
       photo_fichier="3250258132.webp"),

  dict(ref="107349341", titre="Maison en bord de mer avec terrasse",
       commune="Saint-Aygulf", secteur="Var (83)",
       agence="Bonaparte", source="Le Figaro Propriétés",
       prix=1199000, prixM2="7 993 € / m²", negociation=None,
       surface="150 m²", terrain="1 455 m²", pieces="6", chambres="3",
       piscine="Oui", dpe="C / GES A", vue="Mer, plein sud",
       commentaire="Aussi en vente chez SAFTI (réf. 1691651) : 12 photos, dont terrasse, piscine et boulodrome. Écarts à vérifier : 136 m² / 5 pièces / terrain 1 125 m² chez SAFTI contre 150 m² / 6 pièces / terrain 1 455 m² ici.",
       url="https://proprietes.lefigaro.fr/annonces/maison-var-provence+alpes+cote+d+azur-france/107349341/?priceMin=1000000&priceMax=1600000",
       photos=[
         "https://lh3.googleusercontent.com/RV5HclbK5WNv9JlMSDxCOylFRLIx3HN1gUhyqTq5swpoVuGTgtWWMzOnOrt66TX4XY08RpoAbpJvexrHhD3lqpMUBrVpQlW3BlWQng=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/kpGe-uGP65pseV-3cMF_GGe38D_Y2mfApEXK4Xl5ew3OSaKbbg7a_QyQ5mHZVcUwFpNBpLJKg_YkIevZfHeYpEaY_5Qh-4s2iQ1L1_U=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/HgXMd-TzVUZkfT_-dTuw-vQB6fSanoI9Z2Z1fHjUx6bnAFb8YCSWDkEnRUEKV8UhuJWkbvDUm8nJ1vr4RtErFP8oz8dqtJ9lYKhoeg=rj-w900-h675-n-l80",
       ],
       photo_fichier=None,
       autres_annonces=[
         ("SAFTI — 12 photos", "https://www.safti.fr/annonces/achat/maison/saint-aygulf-83370/1691651"),
         ("ParuVendu", "https://www.paruvendu.fr/immobilier/vente/maison/1293380043A1KIVHMN000"),
         ("Superimmo", "https://www.superimmo.com/annonces/achat-maison-136m-saint-aygulf-83370-x11p72a"),
       ]),

  dict(ref="98255163", titre="Maison avec piscine en bord de mer",
       commune="Rayol-Canadel-sur-Mer", secteur="Var (83)",
       agence="Coldwell Banker St Barth Azur", source="Le Figaro Propriétés",
       prix=1500000, prixM2="10 000 € / m²", negociation=None,
       surface="150 m²", terrain="2 200 m²", pieces="7", chambres="5",
       piscine="Oui", dpe="E / GES F", vue="Mer, sud-est",
       commentaire="Après Bormes-les-Mimosas.",
       url="https://proprietes.lefigaro.fr/annonces/maison-var-provence+alpes+cote+d+azur-france/98255163/?priceMin=1000000&priceMax=1700000",
       photos=[
         "https://lh3.googleusercontent.com/ESOUrEtEydSjN3jSTyrDFeFRjivpHTK7I1l36pBVFIj5op3GjvnXfYOIXQLp5DT1my6ymSSenjh1s3A7ld9aL3VWsxGe6HQcb2_jSQ=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/1cKOxlaefReZurqGxUlTrw3_SBLJc_9j4TAQb8FCEh121H-LXjmNeb2aeGZ6RYHP_jmPZs7FQypnvCpSXs4zVDpv0RYW1vstePX4Z0Q=rj-w900-h675-n-l80",
         "https://lh3.googleusercontent.com/bF3USt9iRsADWDZDOdHY2w1NYjElHMPHVSuDF-ZowFpTU9Ujmfb9d4p4s1ZJKYJWP3vO85jrgR2ix79J-ey8JABkaBabnU0WtoVF6A=rj-w900-h675-n-l80",
       ],
       photo_fichier=None),
  dict(ref="82558858", titre="Bastide de charme avec vue mer panoramique",
       commune="Saint-Raphaël — Boulouris", secteur="Var (83)",
       agence="BIRD Saint-Raphaël", source="Côte d'Azur Estate",
       prix=1990000, prixM2="7 625 € / m²", negociation=None,
       surface="261 m²", terrain="1 330 m²", pieces="7", chambres="4",
       piscine="Oui, chauffée et à débordement", dpe=None,
       vue="Mer panoramique et collines, plein sud",
       commentaire="Dépasse le budget initial.",
       url="https://cotedazurestate.com/fr/propriete/vente+maison+saint-raphael+saint-raphael-boulouris-villa-de-charme-vue-mer-7-pieces-a-vendre+82558858",
       photos=[
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/88e2381670ee6be9ad553f6c77e1bbaf.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/f1ed2e3eae1b6f26703e41d705cf777d.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/e1c69c008c6a33f9f3553463d4dc3178.webp",
       ],
       photo_fichier=None),
  dict(ref="86141231", rouge=True, titre="Appartement-villa sur le toit, vue mer",
       commune="Saint-Raphaël", secteur="Var (83)",
       agence="Azur Astoria — Groupe BIRD", source="Côte d'Azur Estate",
       prix=1690000, prixM2="11 655 € / m²", negociation=None,
       surface="145 m² carrez (185 m² utiles)", terrain="540 m² privatifs",
       pieces="4", chambres="3",
       piscine="Oui, privée", dpe=None, vue="Mer panoramique, plein sud",
       commentaire="Appartement « villa sur le toit ».",
       url="https://cotedazurestate.com/fr/propriete/vente+appartement+saint-raphael+appartement-villa-4-pieces-vue-mer-d-exception-a-saint-raphael+86141231",
       photos=[
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/c36fdafa4ca03e5f5914fcbb621142f9.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/f35f966493d73486138695ef0988b5ff.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/a2e54b5eb0cbbb31a53c4803149981af.webp",
       ],
       photo_fichier=None),
  dict(ref="87185556", rouge=True, titre="Villa contemporaine rénovée, vue mer",
       commune="Saint-Aygulf", secteur="Var (83)",
       agence="BIRD Saint-Raphaël", source="Côte d'Azur Estate",
       prix=1490000, prixM2="9 141 € / m²", negociation=None,
       surface="163 m²", terrain="1 309 m²", pieces="4", chambres="3",
       piscine="Oui, au sel et chauffée (8 x 4 m)", dpe=None,
       vue="Mer et verdure, sud-est",
       commentaire="Vue mer limitée.",
       url="https://cotedazurestate.com/fr/propriete/vente+maison+saint-aygulf+87185556",
       photos=[
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/d7c7000c175498a878bc6c6fd167c854.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/5940ebc90589ef423ed26c9a67758db4.webp",
         "https://d36vnx92dgl2c5.cloudfront.net/prod/Elone/3414/media/6586e2b9b0a68391b2313fbd39f8dcca.webp",
       ],
       photo_fichier=None),
  dict(ref="26164VWGRV7G", titre="Villa rénovée avec piscine et vue mer",
       commune="Saint-Raphaël — Boulouris", secteur="Var (83)",
       agence="3% Immobilier Prestige", source="SeLoger",
       prix=870000, prixM2="6 591 € / m²", negociation=None,
       surface="132 m²", terrain="950 m²", pieces="5", chambres="4",
       piscine="Oui, chauffée", dpe="C / GES B", vue="Mer, terrasse plein sud",
       commentaire="Peut-être pas de vue mer.",
       url="https://www.seloger.com/annonce/achat/provence-alpes-cote-d-azur/var-83/saint-raphael-83700/26164VWGRV7G",
       photos=[
         "https://mms.seloger.com/3/4/f/8/34f8e695-17a3-4ee9-b45b-c94d81e79f9f.jpg?ci_seal=23c2659421c1e64efb3ac42c4e054e3b1009d40a",
         "https://mms.seloger.com/6/a/0/b/6a0bb2a7-a8e7-4571-8b20-f3e86abadd7d.jpg?ci_seal=824e12acf07a248f5fc600e3a2a9f9802537104e",
         "https://mms.seloger.com/1/d/b/a/1dbac27f-86fa-46d1-bc4c-73b525cf21b4.jpg?ci_seal=03f602d7555c56b53b0cf93f2ae1c42d7d16b2d2",
       ],
       photo_fichier=None),
]

MAJ = "10 septembre 2026"

# Adresse publique de la page. Sert aux balises de partage (WhatsApp,
# iMessage, Slack…) qui exigent des URLs absolues.
URL_SITE = "https://chakybou.github.io/maisons-sud/"
