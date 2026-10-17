# Chronologie du projet

Cette chronologie est reconstituée à partir du journal de développement : 243 commits en six
semaines, du 3 septembre au 12 octobre 2026, c'est-à-dire autant d'enregistrements datés d'une
modification. Ce dépôt public repart d'un historique neuf ; ce document en garde l'essentiel.

Le projet a été conduit avec un agent de programmation, Claude Code.

## Avant le premier commit

Le cadrage date du 8 août 2026. Trois itérations ont précédé le dépôt : un modèle de données
validé, un script de création des listes SharePoint, puis le chargement d'un jeu de données. Au
3 septembre, 11 listes existaient et 5 critères d'acceptation étaient vérifiés. La conversion en
PDF par un connecteur standard était prouvée, ce qui levait le seul critère d'abandon du projet.

## Les étapes

| Période (2026) | Commits | Ce qui a été livré |
|---|---|---|
| 3 sept. | 7 | Première version en lecture seule : 9 sources connectées, navigation, liste des NC avec recherche et filtre, fiche détaillée, compteurs d'accueil. |
| 9–11 sept. | 32 | Accessibilité mesurée (90 écarts ramenés à 70), fiche en 8 sections repliables. Retour arrière sur la liste des NC, cause racine trouvée, plan de redressement en 6 jalons et garde-fou de compilation. |
| 14–16 sept. | 14 | L'application écrit : création d'une NC, d'une analyse causale, d'une action, puis d'un suivi d'efficacité rattaché à ses actions. |
| 18–22 sept. | 21 | Modification des quatre entités, numérotation automatique des NC, inventaire des outils et de leur coût réel. |
| 23 sept. | 23 | Preuves : dépôt d'un fichier dans SharePoint par un flux piloté depuis l'application, modification, suppression, attribution à une action. Six critères tenus. |
| 24–25 sept. | 45 | Rapport de NC en PDF généré par un flux, puis circuit de signature : envoi, dépôt du rapport signé, refus, clôture. Douze critères tenus. Correction des dates affichées la veille. |
| 28–30 sept. | 43 | Trois listes de pilotage et accueil refondu (onze critères tenus). Statuts des NC, des actions et des suivis calculés d'après les faits, et non plus saisis. |
| 1ᵉʳ–8 oct. | 32 | Jeu de douze NC fictives, diagrammes du processus en français et en anglais. Site de démonstration monté par script : 11 listes, 3 flux, 10 sources, jeu fictif chargé et relu (1 416 champs, 0 écart). |
| 9–12 oct. | 26 | Téléversement par un contrôle plus récent : suspendu. Rapports du jeu fictif générés, signés et déposés. Refonte visuelle des écrans d'édition, du rapport et de la fiche, avec une charte de design. Projet déclaré terminé le 12 octobre. |

Après la clôture, deux vidéos de démonstration ont été tournées sur le jeu fictif et publiées le
16 octobre : une présentation et un scénario d'utilisation.

## Ce que l'historique montre

**Un incident a changé la méthode.** Le 9 septembre, cinq modifications faites d'un coup cassent
la liste des NC, sans qu'aucune soit isolable : retour arrière à l'état connu bon. La cause
racine est trouvée le jour même : le service d'édition fusionne le fichier envoyé avec
l'existant au lieu de le remplacer, et la compilation affiche pourtant zéro erreur. Deux jours
plus tard, le projet repart sur un plan de redressement en six jalons, avec une règle de gel et
un garde-fou de compilation écrit avant toute autre tâche et couvert par 25 tests.

**Un contrôle doit être indépendant de ce qu'il contrôle.** Le garde-fou a lui-même rendu un
faux feu vert, corrigé le 11 septembre. La règle a ensuite été appliquée partout : le
comparateur de textes PDF ne partage aucun code avec le flux qui génère le rapport, et la règle
des statuts existe en deux implémentations, celle de l'application et celle d'un script, qui se
contrôlent l'une l'autre.

**La mesure prime sur la supposition.** Le 24 septembre, les dates chargées s'affichent la
veille. Le défaut est décrit, une convention unique est posée, les dates sont réécrites, et un
contrôle confirme qu'aucune ne reste décalée. Le coût d'une invocation de sous-agent, estimé à
20 000 jetons, est mesuré à 540 000 ; remplacer l'agent générique par un agent spécialisé
réduit ensuite la facture de 62 %.

**Les décisions renversées sont tracées.** Le volet d'analyse de données sous Power BI, prévu
comme cinquième jalon, est abandonné le 28 septembre. Le téléversement par le contrôle moderne
est suspendu le 9 octobre, après avoir mesuré que ce contrôle n'existe pas encore dans le
catalogue de l'environnement. Chaque message de commit dit aussi ce qui n'est pas validé.

**Le déploiement par script prouve la documentation.** Le 8 octobre, le site de démonstration
est monté en une journée par script : listes, gabarit du rapport, flux, sources de
l'application, jeu fictif.

## Ce qui n'est pas fait

- Le volet Power BI n'a pas été réalisé.
- Le téléversement par le contrôle moderne attend la disponibilité de ce contrôle.
- Depuis la refonte visuelle, le dépôt d'un rapport signé n'a pas été rejoué depuis
  l'application. Il avait été éprouvé de bout en bout le 25 septembre. Le dépôt d'une preuve,
  lui, a été rejoué le 14 octobre, pendant le tournage de la seconde vidéo.
