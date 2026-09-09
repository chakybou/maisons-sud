# Short-list maisons — Var & Côte d'Azur

## Structure

| Fichier | Rôle |
|---|---|
| `biens.py` | **Source de vérité.** Les données des biens. C'est le seul fichier à éditer pour ajouter, modifier ou retirer un bien. |
| `generer-page-maisons.py` | Génère `maisons-var-cote-azur.html` (page web, à partager par lien). |
| `generer-pdf-maisons.py` | Génère `maisons-var-cote-azur.pdf` (une seule page A4, à envoyer en pièce jointe). |
| `photos/` | Une photo par bien, nommée `<ref>.webp`. Nécessaire au PDF, qui doit embarquer les images. |

Les deux générateurs lisent les mêmes données : pas de risque que le HTML et le PDF divergent.

```bash
python3 generer-page-maisons.py    # → maisons-var-cote-azur.html
python3 generer-pdf-maisons.py     # → maisons-var-cote-azur.pdf
```

## Contraintes à ne pas casser

- **Zéro JavaScript dans le HTML.** Quick Look sur iPhone ne l'exécute pas : la page apparaîtrait vide. Les deux scripts ont un garde-fou (`assert "<script" not in page`) qui échoue si du JS s'y glisse.
- **Ne jamais éditer le HTML ni le PDF à la main** — ils sont écrasés à chaque génération.
- **Les annonces (proprietes.lefigaro.fr, leboncoin.fr) bloquent l'accès automatisé.** Pour relever les données d'une annonce, il faut passer par le navigateur.
- **Les photos ne sont pas téléchargeables automatiquement non plus.** Pour un nouveau bien : enregistrer la photo dans `photos/<ref>.webp` (ou .jpg) et renseigner `photo_fichier` dans `biens.py`. Sans photo locale, le PDF affiche un cadre vide mais se génère quand même.

## Photos

Chaque bien porte un champ `photos` : de 1 à 3 URLs. La première s'affiche en grand, les deux suivantes en vignettes sous elle. Avec une ou deux photos seulement, la mise en page s'adapte.

**Ces URLs expirent.** Les agences remplacent leurs photos et les anciens liens meurent sans prévenir — c'est arrivé à l'annonce 107859973. Si une image est cassée dans la page, il faut relever les nouvelles URLs sur l'annonce (via le navigateur, les serveurs bloquant l'accès direct) et les remplacer dans `biens.py`.

## Ajouter un bien

Copier un bloc `dict(...)` dans `biens.py`, remplir les champs, mettre à jour `MAJ`, déposer la photo dans `photos/`, relancer les deux scripts. Les champs inconnus se mettent à `None` : ils sont simplement omis du PDF et affichés « — » dans le HTML.
