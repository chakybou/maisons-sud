# -*- coding: utf-8 -*-
"""Génère index.html, la page publiée.

Données : biens.py (source de vérité). Ne jamais éditer le HTML directement :
il est écrasé à chaque exécution.

Contrainte : ZÉRO JavaScript — Quick Look sur iPhone ne l'exécute pas et la
page apparaîtrait vide. Un assert en fin de fichier le vérifie.

Le site est servi directement depuis la branche main : on génère en local,
on commit index.html, on pousse. Pas de construction côté GitHub.

Usage : python3 generer-page-maisons.py [dossier_de_sortie]
"""
import pathlib
import sys
from html import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from biens import BIENS, MAJ, URL_SITE  # noqa: E402

SORTIE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent


def euros(n):
    return f"{n:,}".replace(",", " ") + " €"


def million(n):
    return f"{n/1e6:.2f}".replace(".", ",")


def lien_tel(numero):
    """Numéro cliquable : sur iPhone, un appui suffit à appeler."""
    brut = numero.replace(" ", "").replace(".", "").replace("-", "")
    if brut.startswith("0"):
        brut = "+33" + brut[1:]
    return (f'<a href="tel:{escape(brut, quote=True)}">{escape(numero)}</a>')


def bloc_visite(b):
    """Encadré rendez-vous : n'affiche que ce qui est renseigné."""
    rdv, lieu = b.get("rdv"), b.get("rdv_lieu")
    contact, tels = b.get("contact"), b.get("tel") or []
    if not (rdv or lieu or contact or tels):
        return ""

    lignes = []
    if rdv:
        alerte = "" if b.get("rdv_confirme", True) else '<span class="apre">à confirmer</span>'
        lignes.append(f'<p class="quand">{escape(rdv)}{alerte}</p>')
    else:
        lignes.append('<p class="quand sans">Pas encore de rendez-vous</p>')
    if lieu:
        lignes.append(f'<p class="ou">{escape(lieu)}</p>')
    qui = [escape(contact)] if contact else []
    qui += [lien_tel(x) for x in tels]
    if qui:
        lignes.append('<p class="qui">' + " · ".join(qui) + "</p>")
    return '<div class="rdv">' + "".join(lignes) + "</div>"


def champ(label, valeur):
    if valeur:
        return f"<div><dt>{escape(label)}</dt><dd>{escape(valeur)}</dd></div>"
    return f'<div><dt>{escape(label)}</dt><dd class="vide">—</dd></div>'


def fiche(b, repere):
    lieu = " · ".join(x for x in (b["commune"], b["secteur"]) if x)
    u = escape(b["url"], quote=True)
    carac = "".join([
        champ("Prix / m²", b["prixM2"]),
        champ("Surface", b["surface"]),
        champ("Terrain", b["terrain"]),
        champ("Pièces", b["pieces"]),
        champ("Chambres", b["chambres"]),
        champ("Piscine", b["piscine"]),
        champ("DPE", b["dpe"]),
        champ("Vue", b["vue"]),
    ])
    # 1re photo en grand, les suivantes en vignettes ; s'adapte à 1, 2 ou 3 photos.
    photos = b.get("photos") or []
    vignettes = "".join(
        f'<a class="photo{"" if i == 0 else " mini"}" href="{u}" target="_blank" rel="noopener noreferrer">'
        f'<img src="{escape(p, quote=True)}" alt="{escape(b["titre"]) if i == 0 else ""}" loading="lazy"></a>'
        for i, p in enumerate(photos[:3]))

    nego = (f'<span class="negociation">{escape(b["negociation"])}</span>'
            if b["negociation"] else "")

    autres = b.get("autres_annonces") or []
    ailleurs = ""
    if autres:
        liens = " · ".join(
            f'<a href="{escape(u, quote=True)}" target="_blank" rel="noopener noreferrer">{escape(lbl)}</a>'
            for lbl, u in autres)
        ailleurs = f'<p class="ailleurs">Aussi publié&nbsp;: {liens}</p>' 
    classe = "fiche rouge" if b.get("rouge") else "fiche"
    return f"""
    <article class="{classe}">
      <div class="media">{vignettes}</div>
      <div class="infos">
        <p class="repere">{escape(repere)}</p>
        <p class="ref">{escape(b["agence"])} — {escape(b["source"])}, réf. {escape(b["ref"])}</p>
        <h2><a href="{u}" target="_blank" rel="noopener noreferrer">{escape(b["titre"])}</a></h2>
        <p class="lieu">{escape(lieu)}</p>

        <p class="prix">
          <span class="montant">{euros(b["prix"])}</span>
          <span class="note">{escape(b["prixM2"])}</span>
          {nego}
        </p>

        <dl class="carac">{carac}</dl>

        <blockquote>{escape(b["commentaire"])}</blockquote>
        {ailleurs}
        {bloc_visite(b)}

        <a class="lien" href="{u}" target="_blank" rel="noopener noreferrer">Voir l'annonce</a>
      </div>
    </article>"""


# Les biens marqués `rouge` passent en fin de page, ordre relatif conservé —
# sauf ceux qui portent aussi `en_place`, qui gardent leur rang.
BIENS = sorted(BIENS, key=lambda b: bool(b.get("rouge")) and not b.get("en_place"))

# Le bandeau ne décrit que les biens réellement retenus : les fiches rouges
# restent affichées en fin de page mais ne comptent ni dans le total, ni dans
# la fourchette de prix, ni dans la liste des communes.
retenus = [b for b in BIENS if not b.get("rouge")] or BIENS

prix = [b["prix"] for b in retenus]
communes = ", ".join(dict.fromkeys(b["commune"].split(" — ")[0] for b in retenus))
# Résumé d'une ligne, réutilisé par les messageries dans l'aperçu du lien.
description = (f"{len(retenus)} biens retenus, de {million(min(prix))} à "
               f"{million(max(prix))} M€ — {communes}.")

import re as _re  # noqa: E402
from datetime import date as _date  # noqa: E402

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
FENETRE = [21, 22, 23, 24]      # du lundi 21 au jeudi 24 septembre 2026
MOIS_FENETRE, AN_FENETRE = 9, 2026


def calendrier(biens, reperes):
    """Planning des visites sur la fenêtre, construit depuis les champs `rdv`."""
    par_jour = {j: [] for j in FENETRE}
    for rang, (b, rep) in enumerate(zip(biens, reperes)):
        rdv = b.get("rdv")
        if not rdv:
            continue
        m = _re.search(r"(\d{1,2})\s+septembre,\s*(\d{1,2})\s*h\s*(\d{2})?", rdv)
        if not m or int(m.group(1)) not in par_jour:
            continue
        jour, heure, minute = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
        # le rang départage deux visites à la même heure (ordre de la liste)
        par_jour[jour].append((heure * 60 + minute, rang,
                               f"{heure}h{minute:02d}" if minute else f"{heure}h",
                               rep, b))

    colonnes = []
    for j in FENETRE:
        libelle = JOURS[_date(AN_FENETRE, MOIS_FENETRE, j).weekday()]
        entrees = []
        for _, _rang, hhmm, rep, b in sorted(par_jour[j]):
            lieu = b.get("rdv_lieu") or b["commune"].split(" — ")[0]
            apre = "" if b.get("rdv_confirme", True) else '<span class="apre">à confirmer</span>'
            rouge = " rouge" if b.get("rouge") else ""
            entrees.append(
                f'<li class="visite{rouge}"><span class="h">{escape(hhmm)}</span>'
                f'<span class="no">{escape(rep)}</span>'
                f'<span class="lieu">{escape(lieu)}{apre}</span></li>')
        corps = ("<ul>" + "".join(entrees) + "</ul>") if entrees else \
                '<p class="rien">—</p>'
        colonnes.append(f'<div class="jour"><h3>{libelle} {j}</h3>{corps}</div>')
    return '<section class="planning"><h2>Visites</h2>' \
           '<div class="jours">' + "".join(colonnes) + "</div></section>"


# Repères : chiffres pour les biens retenus, lettres pour les rouges.
# Ils suivent l'ordre d'affichage, donc ils changent si un bien bascule.
from string import ascii_uppercase  # noqa: E402
reperes, n, r = [], 0, 0
for b in BIENS:
    # Lettre pour les rouges relégués en fin de page ; une fiche rouge restée
    # `en_place` garde son rang dans la numérotation.
    if b.get("rouge") and not b.get("en_place"):
        reperes.append(ascii_uppercase[r]); r += 1
    else:
        n += 1; reperes.append(str(n))

resume = (f'<span><b>{len(retenus)}</b> biens retenus</span>'
          f'<span>De <b>{million(min(prix))}</b> à <b>{million(max(prix))} M€</b></span>'
          f'<span>{escape(communes)}</span>')

CSS = """
  :root{
    --craie:#FCFDFB; --craie-fonce:#EFF1ED; --encre:#1B2A23;
    --pin:#33594A; --mer:#2C6577; --gris:#6E7A73; --trait:#E3E7E0; --blanc:#F6F7F3;
  }
  *{box-sizing:border-box;}
  html{-webkit-text-size-adjust:100%;}
  body{margin:0;background:var(--craie);color:var(--encre);
    font-family:"Archivo","Helvetica Neue",Arial,sans-serif;
    font-size:16px;line-height:1.55;-webkit-font-smoothing:antialiased;}
  .page{max-width:1060px;margin:0 auto;padding:0 28px 96px;}

  header{padding:72px 0 40px;border-bottom:2px solid var(--encre);}
  h1{font-family:"Fraunces",Georgia,serif;font-optical-sizing:auto;font-weight:500;
    font-size:clamp(2.4rem,6vw,3.9rem);line-height:1.02;letter-spacing:-0.015em;margin:0 0 14px;}
  .sous-titre{max-width:52ch;margin:0;color:var(--gris);font-size:1.02rem;}
  .resume{display:flex;flex-wrap:wrap;gap:8px 34px;margin-top:30px;font-size:.9rem;color:var(--gris);}
  .resume b{color:var(--encre);font-weight:600;}

  .planning{padding:34px 0 6px;border-bottom:1px solid var(--trait);}
  .planning h2{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:1.3rem;
    margin:0 0 18px;}
  .jours{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;}
  .jour{background:var(--blanc);border-radius:2px;padding:14px 16px 16px;}
  .jour h3{margin:0 0 10px;font-size:.82rem;font-weight:600;color:var(--gris);
    letter-spacing:.03em;text-transform:uppercase;}
  .jour ul{list-style:none;margin:0;padding:0;}
  .visite{display:flex;align-items:baseline;flex-wrap:wrap;gap:0 8px;
    padding:7px 0;border-top:1px solid var(--trait);font-size:.9rem;}
  .visite:first-child{border-top:none;padding-top:0;}
  .visite .h{font-weight:600;font-variant-numeric:tabular-nums;min-width:3.2em;}
  .visite .no{font-family:"Fraunces",Georgia,serif;font-size:1.05rem;
    color:var(--pin);min-width:1.1em;}
  .visite.rouge .no{color:#A32E28;}
  .visite .lieu{color:var(--gris);flex:1 1 100%;margin-left:3.2em;
    font-size:.84rem;line-height:1.3;}
  .jour .rien{margin:0;color:var(--trait);font-size:1rem;}

  .fiche{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);
    gap:36px;padding:44px 0;border-bottom:1px solid var(--trait);}
  .media{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-content:start;}
  .photo{display:block;background:var(--craie-fonce);border-radius:2px;overflow:hidden;
    aspect-ratio:4/3;grid-column:1 / -1;}
  .photo.mini{grid-column:auto;aspect-ratio:4/3;}
  .photo img{width:100%;height:100%;object-fit:cover;display:block;}

  .repere{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:1.5rem;
    line-height:1;color:var(--pin);margin:0 0 10px;}

  .ref{font-size:.76rem;color:var(--gris);letter-spacing:.02em;margin:0 0 6px;}
  h2{font-family:"Fraunces",Georgia,serif;font-weight:500;font-size:1.62rem;
    line-height:1.15;margin:0 0 4px;}
  h2 a{color:inherit;text-decoration:none;text-underline-offset:4px;}
  h2 a:hover,h2 a:focus-visible{text-decoration:underline;text-decoration-thickness:1px;}
  .lieu{margin:0 0 22px;color:var(--pin);font-size:.98rem;}

  .prix{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;
    margin:0 0 24px;padding-bottom:20px;border-bottom:1px solid var(--trait);}
  .prix .montant{font-family:"Fraunces",Georgia,serif;font-weight:400;font-size:2.35rem;
    line-height:1;font-variant-numeric:tabular-nums;letter-spacing:-0.01em;}
  .prix .note{color:var(--gris);font-size:.88rem;}
  .negociation{display:block;width:100%;margin:0;color:var(--mer);font-size:.9rem;font-weight:500;}

  dl.carac{display:grid;grid-template-columns:repeat(auto-fit,minmax(112px,1fr));
    gap:18px 20px;margin:0 0 24px;}
  dl.carac dt{font-size:.75rem;color:var(--gris);margin-bottom:2px;}
  dl.carac dd{margin:0;font-size:1.02rem;font-weight:500;}
  dl.carac dd.vide{color:var(--trait);font-weight:400;}

  blockquote{margin:0 0 26px;padding:2px 0 2px 20px;border-left:3px solid var(--pin);
    font-family:"Fraunces",Georgia,serif;font-style:italic;font-weight:300;
    font-size:1.12rem;line-height:1.5;max-width:56ch;}

  .lien{display:inline-block;color:var(--blanc);background:var(--pin);text-decoration:none;
    padding:11px 20px;border-radius:2px;font-size:.92rem;font-weight:500;}
  .lien:hover,.lien:focus-visible{background:var(--encre);}
  a:focus-visible{outline:2px solid var(--mer);outline-offset:3px;}

  /* Fiches écartées : tout le texte bascule en rouge via les variables. */
  .fiche.rouge{--encre:#A32E28;--pin:#A32E28;--mer:#A32E28;--gris:#C2736D;
    color:var(--encre);}

  .rdv{margin:0 0 24px;padding:14px 18px;background:var(--blanc);
    border-left:3px solid var(--mer);border-radius:2px;max-width:56ch;}
  .rdv p{margin:0;}
  .rdv .quand{font-weight:600;font-size:1.02rem;color:var(--encre);}
  .rdv .quand.sans{font-weight:500;color:var(--gris);}
  .apre{display:inline-block;margin-left:10px;padding:2px 8px;border-radius:2px;
    background:#A32E28;color:var(--blanc);font-size:.72rem;font-weight:600;
    letter-spacing:.02em;vertical-align:1px;white-space:nowrap;}
  .rdv .ou{margin-top:4px;font-size:.92rem;color:var(--encre);}
  .rdv .qui{margin-top:8px;font-size:.9rem;color:var(--gris);}
  .rdv .qui a{color:var(--mer);text-decoration:none;
    border-bottom:1px solid var(--trait);}
  .rdv .qui a:hover,.rdv .qui a:focus-visible{border-bottom-color:var(--mer);}
  .fiche.rouge .rdv{background:#FBF4F3;border-left-color:#A32E28;}

  .ailleurs{margin:-14px 0 22px;font-size:.86rem;color:var(--gris);}
  .ailleurs a{color:var(--mer);text-decoration:none;border-bottom:1px solid var(--trait);}
  .ailleurs a:hover,.ailleurs a:focus-visible{border-bottom-color:var(--mer);}

  footer{padding-top:40px;color:var(--gris);font-size:.85rem;max-width:58ch;}

  @media (max-width:760px){
    .page{padding:0 20px 64px;}
    .jours{grid-template-columns:1fr;gap:10px;}
    .visite .lieu{margin-left:0;flex:1 1 auto;}
    header{padding:48px 0 32px;}
    .fiche{grid-template-columns:1fr;gap:24px;padding:36px 0;}
    .prix .montant{font-size:2rem;}
  }
"""

page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Maisons — Var &amp; Côte d'Azur</title>
<meta name="description" content="{escape(description, quote=True)}">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Maisons — Var &amp; Côte d'Azur">
<meta property="og:title" content="Maisons — Var &amp; Côte d'Azur">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:url" content="{escape(URL_SITE, quote=True)}">
<meta property="og:image" content="{escape(URL_SITE + 'preview.jpg', quote=True)}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Maisons — Var &amp; Côte d'Azur">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600&family=Fraunces:ital,opsz,wght@0,9..144,300..700;1,9..144,300..600&display=swap" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
<div class="page">

  <header>
    <h1>Maisons&nbsp;— Var<br>&amp; Côte d'Azur</h1>
    <p class="sous-titre">Sélection en cours pour une résidence secondaire. Chaque fiche renvoie à l'annonce d'origine.</p>
    <div class="resume">{resume}</div>
  </header>

  {calendrier(BIENS, reperes)}

  <main>{"".join(fiche(b, rep) for b, rep in zip(BIENS, reperes))}
  </main>

  <footer>
    <p>Données relevées sur les annonces le {MAJ}. Les prix et disponibilités évoluent&nbsp;: vérifier auprès de l'agence avant tout déplacement.</p>
  </footer>

</div>
</body>
</html>
"""

assert "<script" not in page, "aucun JavaScript ne doit entrer dans la page"

SORTIE.mkdir(parents=True, exist_ok=True)
cible = SORTIE / "index.html"
cible.write_text(page, encoding="utf-8")
print(f"écrit : {cible} — {len(page)} octets, 0 <script>")
