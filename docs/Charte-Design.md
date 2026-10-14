# Charte de design de l'application

Les règles d'apparence appliquées aux écrans d'édition, au rapport et à la fiche d'une
non-conformité. Elles ont été fixées écran par écran, à partir de retours sur le rendu réel.

**Le but : une compréhension au premier coup d'œil.** Un écran doit se lire sans commentaire.

## 1. Les sept règles — chacune vient d'un retour de Sébastien

1. **Moins de texte.** Aucun paragraphe d'aide à l'écran. Supprimés et jamais regrettés : « Déposer
   le PDF signé revenu de l'approbateur… », « Basculer le sélecteur sur Tous les fichiers… »,
   « L'aperçu reste vide pour un PDF… », « Rattachement — déduit de la section d'origine, non
   saisi ». Une règle qui doit rester accessible devient l'**infobulle** (`Tooltip`) du libellé
   concerné.
2. **Montrer plutôt que dire.** Une icône remplace une étiquette : `[document] NC-26-004`, pas
   « Non-conformité : NC-26-004 ». Les numéros d'étape (« ① Joindre le PDF… ») ont été **refusés** :
   l'icône d'import suffit.
3. **Segmenter l'information.** Trois blocs lisibles d'un regard, dans cet ordre : **contexte**
   (de quoi parle-t-on), **saisie** (ce que je dois fournir), **actions** (ce que je peux faire).
   Un état d'attente ou de verrou se dit dans un **bandeau** d'une ligne.
4. **Une seule action principale par état**, grisée tant que l'obligatoire manque — ce qui dispense
   des astérisques et des mentions « obligatoire ». Les contrôles de cohérence restent au clic.
5. **Le chemin d'exception est en retrait** (replié, ou à côté de l'objet qu'il touche), jamais
   au même rang que le chemin nominal. Le bouton « Retirer » vit sur la ligne de l'action qu'il
   détache, pas dans la barre d'actions.
6. **Trois couleurs d'objets au plus par écran** (§ 2). La hiérarchie se marque par la couleur.
7. **Tout bouton a un fond de couleur.** `Subtle`, `Outline`, `Transparent` et fond blanc sont
   **refusés** : « ce n'est pas très lisible ».

## 2. La palette — trois couleurs d'objets, un signal

| Rôle | Couleur | Où |
|---|---|---|
| **Bleu** — agir, structurer | bouton `Primary` par défaut ; icônes et titres `RGBA(16, 60, 92, 1)` ; fond de bandeau `ThemeEtiqBleuFond` | action principale, icônes de contexte, bandeau d'état |
| **Rouge** — détruire, refuser, détacher | `RGBA(168, 0, 0, 1)` | Supprimer, Retirer, « Signature refusée ? » |
| **Gris ardoise** — revenir, neutre | `RGBA(96, 94, 92, 1)` | Retour, Annuler, bascule de filtre |
| *Vert — signal « c'est fait »* | `RGBA(16, 124, 16, 1)` | icône d'import, document coché, nom du fichier choisi. **Jamais un bouton.** |

Texte : sombre `RGBA(32, 31, 30, 1)` ; secondaire `RGBA(105, 103, 101, 1)`.
**Refusés** : l'ambre / marron sur un bouton (« pas de marron ») ; toute quatrième couleur d'objet.
**À faire trancher** : Sébastien demande « pas plus de deux ou trois couleurs dans les objets » ;
le vert est tenu ici pour un signal d'état, pas pour une couleur d'objet. S'il le compte, le
retirer d'abord des écrans où le rouge et le gris sont tous deux présents.

## 3. Les motifs — à recopier tels quels

**Bandeau d'état** (`ecrRapport`, `conSigneBandeau`) : conteneur AutoLayout horizontal, fond
`ThemeEtiqBleuFond`, rayons 8, hauteur 56, une icône 32 px et **un** libellé semi-gras de 15.
Le sous-titre de détail a été supprimé à la demande de Sébastien : une ligne, pas deux.

**Ligne de contexte** (`ecrEditionPreuve`, `ecrEditionSuivi`) : icône 20 px bleu foncé à X, valeur
à X + 28, hauteur 28, une ligne par information, **sans clé écrite**.

**Dépôt d'un fichier** (`conSigneFichier`, puis `ecrEditionPreuve`) — le motif préféré :

```
[flèche d'import verte]  [Choisir le fichier]        ← avant le choix : rien d'autre
[flèche d'import verte]  [Choisir le fichier]  [document coché vert] nom-du-fichier.pdf
```

`ArrowDownload` 28 px · `AddMedia` · l'`Image` d'aperçu **réduite à 1 × 1 px, jamais supprimée ni
masquée** (c'est `Image.Image` qui porte le contenu envoyé au flux) · `DocumentCheckmark` et libellé vert semi-gras, visibles
seulement si `!IsBlank(add….FileName)`.

**Verrou** : cadenas gris 20 px + trois ou quatre mots (« Fichier verrouillé », « Suivi approuvé,
figé sauf la description »), la règle complète en infobulle.

**Libellé de champ** : icône 20 px + libellé court semi-gras sombre, à X + 28 ; pas d'astérisque.
Une date = l'icône calendrier.

**Barre d'actions** : principale bleue avec `Checkmark` ; retour gris avec `ArrowLeft` ;
destructive rouge avec `Delete`. Toujours `Appearance: =ButtonAppearance.Primary` **écrit en
toutes lettres** + `BasePaletteColor` — le serveur fusionne le YAML, retirer `Appearance` ne
ramène pas le défaut.
