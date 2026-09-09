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


def champ(label, valeur):
    if valeur:
        return f"<div><dt>{escape(label)}</dt><dd>{escape(valeur)}</dd></div>"
    return f'<div><dt>{escape(label)}</dt><dd class="vide">—</dd></div>'


def fiche(b):
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

        <a class="lien" href="{u}" target="_blank" rel="noopener noreferrer">Voir l'annonce</a>
      </div>
    </article>"""


# Les biens marqués `rouge` passent en fin de page, ordre relatif conservé.
BIENS = sorted(BIENS, key=lambda b: bool(b.get("rouge")))

prix = [b["prix"] for b in BIENS]
# Les communes affichées suivent les données : rien à mettre à jour à la main.
communes = ", ".join(dict.fromkeys(b["commune"].split(" — ")[0] for b in BIENS))
# Résumé d'une ligne, réutilisé par les messageries dans l'aperçu du lien.
description = (f"{len(BIENS)} biens retenus, de {million(min(prix))} à "
               f"{million(max(prix))} M€ — {communes}.")

resume = (f'<span><b>{len(BIENS)}</b> biens retenus</span>'
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

  .fiche{display:grid;grid-template-columns:minmax(0,340px) minmax(0,1fr);
    gap:36px;padding:44px 0;border-bottom:1px solid var(--trait);}
  .media{display:grid;grid-template-columns:1fr 1fr;gap:8px;align-content:start;}
  .photo{display:block;background:var(--craie-fonce);border-radius:2px;overflow:hidden;
    aspect-ratio:4/3;grid-column:1 / -1;}
  .photo.mini{grid-column:auto;aspect-ratio:4/3;}
  .photo img{width:100%;height:100%;object-fit:cover;display:block;}

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

  .ailleurs{margin:-14px 0 22px;font-size:.86rem;color:var(--gris);}
  .ailleurs a{color:var(--mer);text-decoration:none;border-bottom:1px solid var(--trait);}
  .ailleurs a:hover,.ailleurs a:focus-visible{border-bottom-color:var(--mer);}

  footer{padding-top:40px;color:var(--gris);font-size:.85rem;max-width:58ch;}

  @media (max-width:760px){
    .page{padding:0 20px 64px;}
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

  <main>{"".join(fiche(b) for b in BIENS)}
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
