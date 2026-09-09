# Short-list maisons — Var & Côte d'Azur

## Structure

| Fichier | Rôle |
|---|---|
| `biens.py` | **Source de vérité.** Les données des biens. C'est le seul fichier à éditer pour ajouter, modifier ou retirer un bien. |
| `generer-page-maisons.py` | Génère `index.html`, la page publiée. |
| `generer-pdf-maisons.py` | Génère `maisons-var-cote-azur.pdf` (une seule page A4, à envoyer en pièce jointe). |
| `photos/` | Une photo par bien, nommée `<ref>.webp`. Nécessaire au PDF, qui doit embarquer les images. |

Les deux générateurs lisent les mêmes données : pas de risque que le HTML et le PDF divergent.

```bash
python3 generer-page-maisons.py    # → index.html
python3 generer-pdf-maisons.py     # → maisons-var-cote-azur.pdf
```

## Publier

Le site est servi directement depuis la branche `main` (Settings → Pages →
Deploy from a branch → main / root). Rien n'est construit côté GitHub :

```bash
python3 generer-page-maisons.py    # régénère index.html
git add -A && git commit -m "maj" && git push
```

La page est en ligne une minute plus tard sur
https://chakybou.github.io/maisons-sud/ — adresse inchangée à chaque fois.

## Contraintes à ne pas casser

- **Zéro JavaScript dans le HTML.** Quick Look sur iPhone ne l'exécute pas : la page apparaîtrait vide. Les deux scripts ont un garde-fou (`assert "<script" not in page`) qui échoue si du JS s'y glisse.
- **Ne jamais éditer le HTML ni le PDF à la main** — ils sont écrasés à chaque génération.
- **Les annonces (proprietes.lefigaro.fr, leboncoin.fr) bloquent l'accès automatisé.** Pour relever les données d'une annonce, il faut passer par le navigateur.
- **Les photos ne sont pas téléchargeables automatiquement non plus.** Pour un nouveau bien : enregistrer la photo dans `photos/<ref>.webp` (ou .jpg) et renseigner `photo_fichier` dans `biens.py`. Sans photo locale, le PDF affiche un cadre vide mais se génère quand même.

## Partage du lien

La vignette qui s'affiche dans WhatsApp et consorts est `preview.jpg`, un
fichier fixe à la racine du dépôt (1200 x 630). Les balises Open Graph de la
page y renvoient en URL absolue, construite depuis `URL_SITE` dans `biens.py` :
si l'adresse du site change un jour, c'est la seule ligne à modifier.

La vignette n'est pas régénérée automatiquement — elle montre le titre et un
échantillon de photos, pas les chiffres du moment. À refaire à la main
seulement si la sélection change beaucoup.

Les messageries mettent l'aperçu en cache pendant plusieurs jours. Après une
mise à jour, un lien déjà partagé continuera d'afficher l'ancienne vignette —
ajouter `?v=2` à la fin de l'URL force un nouvel aperçu.

## Photos

Chaque bien porte un champ `photos` : de 1 à 3 URLs. La première s'affiche en grand, les deux suivantes en vignettes sous elle. Avec une ou deux photos seulement, la mise en page s'adapte.

**Ces URLs expirent.** Les agences remplacent leurs photos et les anciens liens meurent sans prévenir — c'est arrivé à l'annonce 107859973. Si une image est cassée dans la page, il faut relever les nouvelles URLs sur l'annonce (via le navigateur, les serveurs bloquant l'accès direct) et les remplacer dans `biens.py`.

## Ajouter un bien

Copier un bloc `dict(...)` dans `biens.py`, remplir les champs, mettre à jour `MAJ`, déposer la photo dans `photos/`, relancer les deux scripts. Les champs inconnus se mettent à `None` : ils sont simplement omis du PDF et affichés « — » dans le HTML.
