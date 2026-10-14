# Contrat narratif — histoires de non-conformités

> Fiche de contexte pour le modèle qui rédige les histoires. Elle fixe le décor, le vocabulaire et
> les faits que chaque histoire doit rendre explicites. L'intrigue t'appartient.

## 1. Ta mission

Tu écris de courtes histoires vraisemblables. Chacune raconte la vie d'une non-conformité (NC) dans
une entreprise fictive : la découverte de l'écart, ce qu'on a fait sur le moment, ce qu'on a
compris de sa cause, ce qu'on a corrigé, comment on a vérifié que la correction tenait, et comment
le dossier s'est conclu.

Un traitement ultérieur transformera chaque histoire en enregistrements d'une application de
gestion des NC et des CAPA (actions correctives et préventives). Il fabrique lui-même les numéros,
les codes et les liens entre enregistrements. Toi, tu racontes **ce qui s'est passé dans
l'entreprise**. Ce traitement ne doit rien inventer : un fait absent de ton récit restera absent
du dossier.

Rédige en français, dans une langue sobre.

## 2. L'entreprise

Une PME fictive d'une vingtaine de personnes : un laboratoire d'essais sur matériaux métalliques,
accrédité ISO/IEC 17025. Il réalise des essais mécaniques (traction, résilience, dureté), de la
métallographie, de l'analyse chimique et des essais sur assemblages soudés. Un atelier d'usinage
prépare les éprouvettes ; un département de contrôle non destructif (NDT) complète l'offre. Les
fonctions de soutien : achats, administration, ventes, ressources humaines, ingénierie. La
clientèle est industrielle.

Le système qualité vit au rythme d'un laboratoire accrédité : procédures et formulaires maîtrisés,
étalonnages et vérifications intermédiaires, contrôles qualité internes, essais d'aptitude, audits
internes, évaluations par l'organisme d'accréditation, revue de direction.

## 3. Le parcours d'une NC

L'application connaît sept étapes. Leurs noms servent à ta compréhension, pas à ton récit :

1. **Ouverte** — l'écart est signalé, le dossier est ouvert.
2. **En analyse** — on cherche la cause.
3. **CAPA définie** — au moins une action corrective est décidée.
4. **CAPA en cours** — au moins une action corrective a commencé.
5. **En vérif efficacité** — les actions correctives sont toutes tranchées (réalisées et
   approuvées, ou rejetées), au moins une approuvée ; on vérifie qu'elles ont produit l'effet
   attendu.
6. **En signature** — le rapport de NC est soumis à l'approbateur.
7. **Close** — l'approbateur a signé, le responsable a clos le dossier.

À savoir :

- Les actions immédiates ne font pas avancer le dossier ; seules les actions correctives le font.
- Une NC peut se passer d'action corrective : l'analyse conclut à un événement isolé, la
  correction immédiate suffit, et le dossier passe directement au rapport.
- Le dossier peut reculer : une vérification non concluante appelle une nouvelle action
  corrective ; l'approbateur peut refuser de signer, et le rapport est alors repris dans une
  nouvelle version, motif à l'appui.
- **Le statut découle des faits, jamais d'une déclaration.** Écris « l'action est terminée le
  12 mai et le responsable qualité l'approuve », pas « la NC passe en CAPA en cours ».

## 4. Le vocabulaire de l'application

### 4.1 Département concerné — un seul par NC

Laboratoire · Atelier (usinage, préparation des éprouvettes) · NDT (contrôle non destructif) ·
Achat · Administration · Marketing (ventes) · RH · Ingénierie

Il n'existe pas de département « Qualité » : un écart du système qualité se rattache au
département où il se produit.

### 4.2 Source de détection — une seule par NC : le canal par lequel l'écart a été découvert

- **Opérations et essais** : Contrôle opérationnel (pendant l'essai) · Revue technique des
  résultats · Revue du rapport (avant ou après émission) · Réception / gestion des échantillons ·
  Incident imprévu (bris, coupure de courant, contamination, perte de données, erreur de
  manipulation)
- **Assurance qualité** : Contrôle qualité interne (matériau de référence, duplicata, carte de
  contrôle) · Essai d'aptitude / interlaboratoires · Indicateur de performance (hausse des
  reprises, retards répétés)
- **Équipements et métrologie** : Vérification métrologique · Maintenance · Surveillance des
  conditions environnementales
- **Audits et gouvernance** : Audit interne · Audit externe (organisme d'accréditation, client,
  fournisseur) · Revue de direction
- **Clients et parties externes** : Réclamation client · Partie externe (fournisseur,
  sous-traitant, organisme réglementaire, laboratoire partenaire)
- **Personnel et compétences** : Surveillance du personnel (supervision, témoin de compétence) ·
  Signalement spontané (déclaration volontaire d'un employé)
- **Documentation et exigences** : Revue documentaire · Revue de contrat / demande client
- **Données et systèmes numériques** : Systèmes informatiques (transfert de données, formule,
  LIMS, fichier corrompu)
- **Gestion du changement** : Changement organisationnel (écart apparu après un changement de
  méthode, de logiciel, d'équipement, de personnel ou de fournisseur)
- **Autre** : Autre source, exceptionnelle

### 4.3 Causes — seize familles

Décris la cause concrètement, dans les mots du terrain : le traitement suivant la rattachera à
l'une des 256 causes de la taxonomie. Les exemples ci-dessous en sont tirés.

- **Gouvernance et ressources** — responsabilités non définies, ressources humaines
  insuffisantes, pression opérationnelle excessive, gestion du changement absente
- **Compétence du personnel** — formation initiale insuffisante, supervision insuffisante,
  transfert de connaissances insuffisant, habilitation accordée sans preuve suffisante
- **Revue de la demande et du contrat** — exigence client non clarifiée, révision normative non
  identifiée, délai irréaliste accepté, statut d'accréditation mal déterminé
- **Méthodes et instructions techniques** — version incorrecte utilisée, instruction de travail
  incomplète, paramètre technique non défini, unité de mesure incorrecte
- **Échantillonnage et réception** — identification ambiguë, traçabilité interrompue, vérification
  à la réception insuffisante, échantillon endommagé accepté
- **Préparation des éprouvettes** — géométrie d'entaille incorrecte, orientation de prélèvement
  incorrecte, échauffement durant l'usinage, mélange d'éprouvettes
- **Équipements et traçabilité métrologique** — étalonnage expiré, vérification intermédiaire
  absente, dérive métrologique non détectée, usure mécanique non détectée
- **Exécution de l'essai** — vitesse d'essai incorrecte, température d'essai incorrecte, mise à
  zéro omise, anomalie technique non signalée
- **Conditions environnementales** — température hors limites, alimentation électrique instable,
  ventilation insuffisante, alarme environnementale inefficace
- **Données, calculs et systèmes informatiques** — transcription incorrecte, formule de calcul
  incorrecte, cellule de calcul modifiable, sauvegarde inefficace
- **Assurance de la validité des résultats** — fréquence de contrôle insuffisante, tendance
  défavorable non détectée, résultat suspect non investigué
- **Revue technique et rapport d'essai** — revue technique incomplète, résultat mal retranscrit,
  exigence client omise, rapport émis avant approbation
- **Fournisseurs et prestations externes** — consommable expiré, certificat fournisseur absent,
  substitution de produit non maîtrisée, compétence du sous-traitant non démontrée
- **Documentation et enregistrements** — document obsolète disponible, formulaire incomplet,
  enregistrement absent, modification documentaire non maîtrisée
- **Processus du système de management** — travail non conforme non isolé, impact sur les
  résultats antérieurs non évalué, action corrective limitée au symptôme, vérification
  d'efficacité insuffisante
- **Communication et coordination** — transmission d'information incomplète, consigne ambiguë,
  relève de poste inadéquate, coordination interservice insuffisante

Une NC porte le plus souvent une seule cause racine ; une NC sérieuse peut en porter deux. Quand
une analyse est menée, elle prend la forme d'une chaîne de « pourquoi » — de deux à cinq niveaux,
souvent trois — qui s'arrête quand la cause est atteinte. Une hypothèse examinée puis écartée a
toute sa place dans le récit.

### 4.4 Actions

Deux types :

- **Action immédiate** — contenir ou corriger l'effet : isoler des éprouvettes, mettre un
  équipement hors service, refaire un essai, corriger et réémettre un rapport, prévenir le
  client, accuser réception d'une réclamation. Elle ne fait pas l'objet d'une vérification
  d'efficacité.
- **Action corrective** — supprimer la cause pour éviter la récurrence : réviser une instruction,
  former, protéger un fichier de calcul, ajouter un contrôle, changer de fournisseur, resserrer
  la fréquence des vérifications intermédiaires.

Chaque action a **un** pilote, une date de début, souvent une échéance, une date de réalisation et
ce qui la prouve. Elle est planifiée, puis en cours, puis **approuvée** une fois réalisée — jamais
avant. Elle peut aussi être **rejetée** à tout moment, même avant d'être exécutée : jugée
disproportionnée, trop coûteuse, remplacée par une meilleure option. Une action rejetée reste au
dossier : dis qui l'a écartée et pourquoi.

### 4.5 Vérification d'efficacité

Elle porte sur une ou plusieurs actions correctives. C'est un contrôle planifié, **pas un journal
d'avancement** : un critère mesurable (un seuil, une période), un responsable, une date prévue,
une échéance ; puis une date de vérification et une conclusion — **approuvée** (efficace),
**rejetée** (inefficace : une nouvelle action corrective suit) ou **en surveillance** (on prolonge
l'observation). Avant la conclusion, elle est planifiée, puis en cours dès que les premiers
éléments sont réunis.

Exemples de critères : aucune erreur de transcription sur les 20 rapports suivants ; trois
vérifications intermédiaires mensuelles conformes ; score z satisfaisant au prochain essai
d'aptitude ; technicien observé sans écart sur deux essais ; aucune réclamation du même type
pendant six mois ; les deux livraisons suivantes conformes à la réception.

### 4.6 Preuves

Une preuve est toujours un fichier, rattaché au dossier, à une action ou à une vérification.
Quatorze types :

Communication (courriel, avis au client, accusé de réception) · Document technique (procédure,
instruction, norme, organigramme, version révisée) · Formulaire contrôlé (formulaire du système
qualité rempli) · Rapport (rapport d'essai erroné, corrigé ou réémis ; rapport d'audit) · Donnée
brute d'essai · Calcul et analyse (calcul d'incertitude, analyse d'impact, tendance) · Preuve
métrologique (certificat d'étalonnage, vérification intermédiaire) · Preuve liée au personnel
(attestation de formation, prise de connaissance signée, habilitation) · Preuve informatique
(capture d'écran, journal système, droits d'accès) · Preuve matérielle (achat ou objet : outil
adapté, équipement de protection) · Certificat et preuve externe (certificat fournisseur, rapport
de sous-traitant) · Photo · Vidéo · Preuve d'efficacité (relevé qui démontre le résultat d'une
vérification)

Nomme les documents produits comme on en parle : « la photo de l'éprouvette », « la version 3 de
l'instruction », « le courriel au client ». Les citer suffit : inutile de préciser qu'ils sont
« joints ».

### 4.7 Rapport et clôture

Le responsable du dossier rédige le rapport de NC, qui résume les actions immédiates, les actions
correctives et leur efficacité. Le rapport passe de brouillon à « en signature » ; l'approbateur
le signe. Le responsable clôt ensuite le dossier, le jour de la signature ou après. L'approbateur peut refuser de signer — synthèse imprécise, vérification jugée trop courte :
la version refusée est remplacée par une nouvelle, avec le motif.

### 4.8 Coûts — facultatifs

En dollars canadiens : le coût immédiat de la NC (essai repris, éprouvettes refaites, transport) ;
pour une action, les heures passées avec un taux horaire, un coût interne, un coût externe.
Chiffre seulement quand c'est naturel.

## 5. Rôles et responsabilités

L'application ne tient pas de matrice RACI : chaque élément a **une** personne responsable,
nommée.

- **Lanceur d'alerte** — qui signale l'écart : un employé, ou une personne externe (client,
  auditeur, fournisseur) nommée avec son organisation.
- **Responsable du dossier** — porte la NC de l'ouverture à la clôture et rédige le rapport. Le
  plus souvent la personne chargée de la qualité ; parfois un directeur, quand l'écart relève
  entièrement de son secteur.
- **Approbateur** — un membre de la direction, distinct du responsable ; il signe le rapport.
- **Pilote d'action** — un par action : technicien, machiniste, acheteur, directeur…
- **Responsable de la vérification** — un par vérification, de préférence indépendant de l'action
  vérifiée.
- Les personnes consultées ou informées — client prévenu, équipe formée — apparaissent dans le
  récit, sans rôle formel.

Une liste d'employés fictifs t'est fournie : pour les rôles internes, n'emploie que ces personnes
et n'en invente aucune autre. Si la liste précise qui peut porter une responsabilité formelle,
respecte cette indication. Dans une entreprise de cette taille, les mêmes personnes reviennent
d'une histoire à l'autre.

## 6. L'impact — aucun champ ne le porte

L'application n'enregistre pas de niveau d'impact : il doit se lire dans les faits — ce qui est
arrivé, et l'ampleur du traitement.

| Impact | Ce qui s'est passé | Traitement proportionné |
|---|---|---|
| Faible ou limité | Écart isolé ou constat mineur d'audit ; arrêté avant le client, ou sans effet sur un résultat transmis | Correction immédiate ; analyse courte ou constat d'événement isolé ; zéro ou une action corrective simple ; clos en 2 à 8 semaines |
| Moyen | Un client ou plusieurs résultats touchés (essais repris, rapport réémis, retard notable), ou faiblesse d'une méthode ou d'un équipement | Analyse complète ; une à trois actions correctives ; vérification sur quelques semaines à trois mois |
| Sérieux | Validité de résultats déjà émis en cause, constat majeur de l'organisme d'accréditation, ou risque réel pour la santé et la sécurité | Impact évalué sur les rapports antérieurs, clients notifiés ; plusieurs actions, dont une première réponse souvent insuffisante ; vérification sur six à douze mois |

## 7. Ce que chaque histoire doit rendre explicite

Sans alourdir le style, fais apparaître :

1. **Quand** — la date de détection (jour et mois). Pour la suite, une date ou un délai relatif
   (« deux jours plus tard », « fin avril »), pourvu que l'enchaînement se calcule.
2. **Comment et par qui** — la circonstance de la découverte et le lanceur d'alerte.
3. **Où** — le département concerné et le contexte : essai, équipement, document, client,
   fournisseur.
4. **Quoi** — le fait observé et sa conséquence visible.
5. **Qui porte le dossier** — ses gestes suffisent souvent à le montrer ; l'approbateur peut
   n'apparaître qu'à la signature.
6. **Le confinement**, s'il y en a un : quoi, qui, quand.
7. **La cause** — ce qui a été examiné, ce qui a été écarté, ce qui a été retenu ; la chaîne des
   « pourquoi » quand une analyse est menée.
8. **Chaque action corrective** — qui, quoi, quand, ce qui la prouve. Une action réalisée est
   réputée approuvée : ne le dis que si l'approbation tarde ou fait débat. Une action rejetée se
   raconte toujours, avec la raison.
9. **La vérification d'efficacité** — le critère, le responsable, la date prévue, puis la date et
   la conclusion.
10. **La fin** — la signature et la clôture ; ou, pour un dossier inachevé, où il en est à la date
    de référence.

Une NC mineure n'a pas à tout remplir : les points 1 à 6, une cause en une phrase et la clôture
suffisent.

Cette liste n'est pas un plan. Ne la suis pas phrase par phrase et ne fige aucune formule : deux
histoires ne doivent ni commencer ni finir de la même façon.

## 8. Réalisme

- Évite la ligne droite « problème → cause évidente → action parfaite → résolu ». Selon les cas :
  une première hypothèse écartée, une mesure provisoire avant la solution définitive, une action
  en retard (fournisseur, absence, charge de travail), une action rejetée, une vérification qui
  montre que la correction ne suffit pas.
- Reste proportionné : un incident mineur ne déclenche ni analyse lourde ni CAPA en cascade.
- Penche du côté du laboratoire : dans un laboratoire réel, la plupart des NC y naissent, et les
  audits et les réclamations clients en sont des sources fréquentes. Varie le reste sans chercher
  à tout couvrir.
- Donne des détails techniques concrets : normes d'essai (ASTM, ISO), équipements décrits sans
  marque (machine de traction, mouton-pendule, duromètre, four, polisseuse, spectromètre).
- Aucun nom d'entreprise, de marque ou d'organisme existant : clients, fournisseurs et auditeurs
  portent des noms fictifs.
- Le ton d'un compte rendu de terrain, pas d'un exercice scolaire : la norme n'est pas un décor,
  et ses articles ne sont cités que par un auditeur dans son constat.
- La chronologie tient : rien n'est réalisé avant d'avoir commencé ; la vérification suit les
  actions, la signature suit la vérification, la clôture suit la signature. Signatures, clôtures
  et autres gestes administratifs ont lieu un jour ouvrable.
- Une histoire de 2026 peut être la récidive d'une histoire de 2025 dont l'action corrective s'est
  révélée insuffisante ; dis-le en langage naturel.

## 9. Ce que tu ne fais pas

- Aucun numéro ni code : ni n° de NC, d'action, de vérification, de preuve ou de rapport, ni code
  de catégorie.
- Aucune structure technique : ni tableau, ni JSON, ni nom de champ.
- Aucune étiquette de statut dans le récit (§3).
- Aucune mention de l'application, du système ou de la saisie : tu racontes l'entreprise, pas
  l'outil.
- Aucun événement postérieur à la date de référence.
- Aucun employé absent de la liste fournie.

Si une règle de ce document te paraît rendre une histoire invraisemblable, respecte-la et
signale-le en une ligne sous l'histoire.

## 10. Le lot à produire

- **Date de référence** — « aujourd'hui » pour les histoires : **1ᵉʳ octobre 2026**.
- **10 histoires** : 5 détectées en 2025, 5 en 2026.
- **Impact** : 8 faibles ou limités, 1 moyen, 1 sérieux — de préférence pas la même année pour ces
  deux derniers.
- **Avancement** : les histoires de 2025 sont en principe closes ; l'une peut encore être en
  vérification si son suivi est long. Deux ou trois histoires de 2026 s'arrêtent en cours de
  route, à des étapes différentes : analyse en cours, action corrective en retard, vérification
  planifiée, rapport en signature.
- **Accrocs** : au moins trois histoires comportent un accroc réel — mesure provisoire, action
  rejetée, retard, vérification non concluante, refus de signature —, dont l'histoire sérieuse.
- **Diversité** : client, rapport, équipement, étalonnage, erreur opérationnelle, traçabilité,
  audit interne ou externe, compétence, documentation, fournisseur ou achat, environnement de
  travail, santé-sécurité liée à l'activité, informatique, écart arrêté avant le client. Choisis ;
  ne parcours pas la liste.

Format de chaque histoire :

```
## Histoire <n> — <année de détection> — impact <faible | moyen | sérieux>
Titre : <le problème, en 60 caractères au plus>

<le récit : 80 à 150 mots pour un impact faible, 150 à 250 pour moyen, 250 à 350 pour sérieux>
```

Le niveau de détail attendu, sur une action :

- Trop vague : « Une action corrective a été mise en place et le problème a été résolu. »
- Juste : « Le 3 juin, le responsable de l'atelier révise l'instruction de préparation pour
  imposer un contrôle de l'entaille au projecteur de profil avant chaque essai ; les deux
  techniciens signent la prise de connaissance le 10 juin. »
