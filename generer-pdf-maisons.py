# -*- coding: utf-8 -*-
"""Génère le PDF une page de la short-list immobilière.

Données : biens.py (source de vérité). Ne jamais éditer le PDF.
Rendu : Chromium headless. Les photos sont lues dans photos/ et embarquées
en base64 — indispensable, les serveurs des annonces bloquent l'accès direct.

Usage : python3 generer-pdf-maisons.py [dossier_de_sortie]
"""
import base64
import mimetypes
import pathlib
import subprocess
import sys
import tempfile
from html import escape

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from biens import BIENS, MAJ  # noqa: E402

ICI = pathlib.Path(__file__).resolve().parent
PHOTOS = ICI / "photos"
SORTIE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ICI
NOM = "maisons-var-cote-azur.pdf"

CHROME = next(
    (c for c in ("/opt/pw-browsers/chromium",
                 "/usr/bin/chromium", "/usr/bin/chromium-browser",
                 "/usr/bin/google-chrome",
                 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
     if pathlib.Path(c).exists()),
    None,
)


def euros(n):
    return f"{n:,}".replace(",", " ") + " €"


def million(n):
    return f"{n/1e6:.2f}".replace(".", ",")


def image_data_uri(nom):
    """Renvoie la photo en data: URI, ou None si le fichier manque."""
    if not nom:
        return None
    p = PHOTOS / nom
    if not p.exists():
        print(f"  ! photo absente : photos/{nom}")
        return None
    mime = mimetypes.guess_type(p.name)[0] or "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def fiche(b):
    u = escape(b["url"], quote=True)
    lieu = " · ".join(x for x in (b["commune"], b["secteur"]) if x)

    # Caractéristiques en une ligne dense : on n'affiche que ce qui est renseigné.
    bits = []
    if b["surface"]:
        bits.append(f'<b>{escape(b["surface"])}</b>')
    if b["terrain"]:
        bits.append(f'terrain {escape(b["terrain"])}')
    if b["pieces"]:
        bits.append(f'{escape(b["pieces"])} pièces')
    if b["chambres"]:
        bits.append(f'{escape(b["chambres"])} chambres')
    if b["piscine"]:
        bits.append(f'piscine : {escape(b["piscine"].lower())}')
    if b["dpe"]:
        bits.append(f'DPE {escape(b["dpe"])}')
    if b["vue"]:
        bits.append(f'vue {escape(b["vue"][0].lower() + b["vue"][1:])}')
    carac = '<span class="sep">·</span>'.join(bits)

    nego = (f'<span class="nego">{escape(b["negociation"])}</span>'
            if b["negociation"] else "")

    src = image_data_uri(b.get("photo_fichier"))
    photo = (f'<img src="{src}" alt="">' if src
             else '<span class="sans-photo">photo —</span>')

    return f"""
  <article class="fiche">
    <a class="photo" href="{u}">{photo}</a>
    <div class="infos">
      <p class="ref">{escape(b["agence"])} <span class="sep">·</span> {escape(b["source"])} <span class="sep">·</span> réf. {escape(b["ref"])}</p>
      <div class="tete">
        <h2><a href="{u}">{escape(b["titre"])}</a></h2>
        <p class="prix"><span class="montant">{euros(b["prix"])}</span><span class="m2">{escape(b["prixM2"])}</span></p>
      </div>
      <p class="lieu">{escape(lieu)}</p>
      <p class="carac">{carac}</p>
      {nego}
      <p class="mot">{escape(b["commentaire"])}</p>
    </div>
  </article>"""


prix = [b["prix"] for b in BIENS]
resume = (f'<span><b>{len(BIENS)}</b> biens retenus</span>'
          f'<span>de <b>{million(min(prix))}</b> à <b>{million(max(prix))} M€</b></span>'
          f'<span>Agay <span class="sep">·</span> Saint-Aygulf <span class="sep">·</span> Saint-Raphaël</span>')

CSS = """
  @page { size: A4; margin: 0; }
  :root{
    --craie:#FCFDFB; --craie-fonce:#EFF1ED; --encre:#1B2A23;
    --pin:#33594A; --mer:#2C6577; --gris:#6E7A73; --trait:#E3E7E0;
  }
  *{box-sizing:border-box;margin:0;}
  body{
    width:210mm;height:297mm;overflow:hidden;
    padding:12mm 13mm 9mm;background:var(--craie);color:var(--encre);
    font-family:"Carlito","Helvetica Neue",Arial,sans-serif;
    font-size:8.4pt;line-height:1.4;
    display:flex;flex-direction:column;
    -webkit-print-color-adjust:exact;print-color-adjust:exact;
  }
  a{color:inherit;text-decoration:none;}
  .sep{color:var(--trait);padding:0 .38em;}

  header{border-bottom:1.6pt solid var(--encre);padding-bottom:3.6mm;}
  .bandeau{display:flex;align-items:baseline;justify-content:space-between;gap:8mm;}
  h1{font-family:"Lora",Georgia,serif;font-weight:500;font-size:23pt;
     line-height:1;letter-spacing:-0.012em;}
  .sous-titre{color:var(--gris);font-size:8pt;text-align:right;max-width:62mm;line-height:1.35;}
  .resume{display:flex;flex-wrap:wrap;gap:0 9mm;margin-top:2.6mm;
          font-size:8pt;color:var(--gris);}
  .resume b{color:var(--encre);font-weight:700;}

  main{flex:1;display:flex;flex-direction:column;}
  .fiche{flex:1;display:grid;grid-template-columns:44mm 1fr;gap:6mm;
         align-items:center;padding:3.6mm 0;border-bottom:.5pt solid var(--trait);}
  .fiche:last-child{border-bottom:none;}

  .photo{display:block;width:44mm;height:33mm;background:var(--craie-fonce);
         border-radius:1pt;overflow:hidden;}
  .photo img{width:100%;height:100%;object-fit:cover;display:block;}
  .sans-photo{display:block;padding:14mm 0;text-align:center;
              color:var(--gris);font-size:7pt;}

  .ref{font-size:6.6pt;color:var(--gris);letter-spacing:.015em;
       text-transform:uppercase;}
  .tete{display:flex;align-items:baseline;justify-content:space-between;
        gap:5mm;margin-top:.6mm;}
  h2{font-family:"Lora",Georgia,serif;font-weight:500;font-size:12.6pt;
     line-height:1.15;}
  .prix{text-align:right;white-space:nowrap;}
  .prix .montant{font-family:"Lora",Georgia,serif;font-size:14pt;
                 font-variant-numeric:tabular-nums;}
  .prix .m2{display:block;color:var(--gris);font-size:7.2pt;margin-top:.3mm;}
  .lieu{color:var(--pin);font-size:8.6pt;font-weight:700;margin-top:.4mm;}
  .carac{margin-top:1.8mm;font-size:8pt;color:var(--encre);}
  .carac b{font-weight:700;}
  .nego{display:block;margin-top:1.2mm;color:var(--mer);font-size:7.8pt;font-weight:700;}
  .mot{margin-top:1.8mm;padding-left:2.6mm;border-left:1.6pt solid var(--pin);
       font-family:"Lora",Georgia,serif;font-style:italic;font-size:8.6pt;
       line-height:1.35;color:var(--encre);}

  footer{border-top:.5pt solid var(--trait);padding-top:2.4mm;
         display:flex;justify-content:space-between;gap:6mm;
         color:var(--gris);font-size:6.8pt;}
"""

page = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Maisons — Var &amp; Côte d'Azur</title>
<style>{CSS}</style>
</head>
<body>
  <header>
    <div class="bandeau">
      <h1>Maisons — Var &amp; Côte d'Azur</h1>
      <p class="sous-titre">Sélection en cours pour une résidence secondaire.<br>
      Chaque fiche renvoie à l'annonce d'origine.</p>
    </div>
    <div class="resume">{resume}</div>
  </header>

  <main>{"".join(fiche(b) for b in BIENS)}</main>

  <footer>
    <span>Données relevées sur les annonces le {MAJ}. Prix et disponibilités évoluent&nbsp;: vérifier auprès de l'agence avant tout déplacement.</span>
    <span>Photos et titres cliquables&nbsp;→&nbsp;annonce</span>
  </footer>
</body>
</html>
"""

assert "<script" not in page, "aucun JavaScript ne doit entrer dans la page"

SORTIE.mkdir(parents=True, exist_ok=True)
cible = SORTIE / NOM

if CHROME is None:
    raise SystemExit("Chromium/Chrome introuvable — impossible de produire le PDF.")

with tempfile.TemporaryDirectory() as tmp:
    src = pathlib.Path(tmp) / "page.html"
    src.write_text(page, encoding="utf-8")
    subprocess.run(
        [CHROME, "--headless", "--disable-gpu", "--no-sandbox",
         f"--user-data-dir={tmp}/profil",
         "--no-pdf-header-footer",
         f"--print-to-pdf={cible}", src.as_uri()],
        check=True, capture_output=True,
    )

print(f"écrit : {cible} — {cible.stat().st_size:,} octets".replace(",", " "))
