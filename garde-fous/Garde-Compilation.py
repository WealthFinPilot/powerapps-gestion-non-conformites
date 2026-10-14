"""Garde-fou de compilation canvas : refuse une compilation qui detruirait l'app.

Usage :
  python Garde-Compilation.py avant --synchro <dir-sync>  --cible <dir-a-compiler> [--attendu ecrX ...]
  python Garde-Compilation.py apres --avant   <dir-sync-1> --apres <dir-sync-2>    [--attendu ecrX ...]

POURQUOI CE SCRIPT EXISTE. Deux destructions de l'app en deux jours, meme outil, meme
absence de signal :
  - 2026-09-11 : le dossier donne a compile_canvas DEVIENT l'app. Un dossier ne
    contenant qu'un ecran a fait tomber la session de 6 fichiers a 3 — App.pa.yaml
    reduit a son Theme, ses 20 jetons et son OnStart evapores, trois ecrans disparus.
    compile_canvas a rendu « 0 erreur ».
  - 2026-09-10 : une compilation depuis des fichiers PERIMES a reapplique un etat
    ancien. Les 6 fichiers etaient pourtant bien la. La aussi, « 0 erreur ».
compile_canvas valide la GRAMMAIRE du YAML qu'on lui donne. Il ne verifie jamais que ce
YAML est bien l'app en cours. C'est ce trou-la que ce script bouche, et rien d'autre.

DEUX NIVEAUX DE REFUS, parce qu'un seul ne couvre qu'un seul des deux incidents :
  1. L'ENSEMBLE DES FICHIERS doit etre identique. Binaire, sans bruit. (incident 2)
  2. L'ARBRE DES CONTROLES de chaque ecran doit etre identique, sauf pour les fichiers
     declares par --attendu. (incident 1, qui passait sous le niveau 1)

POURQUOI L'ARBRE, ET PAS LE TEXTE. Le serveur normalise les colonnes en noms
d'AFFICHAGE : on ecrit Search(NC, x, Title, Intitule), il relit
Search(NC, x, 'N° de NC', Intitule). Un diff texte local/serveur n'est donc JAMAIS
vide, et un controle qui crie a chaque passage n'est plus lu. L'arbre des controles —
noms, types, imbrication, ORDRE — ne subit pas cette normalisation : c'est le seul
niveau ou une divergence veut dire quelque chose. Le diff texte reste affiche du cote
« avant », pour information, jamais bloquant.

CE QU'IL NE FAIT PAS. Il n'appelle ni compile_canvas ni sync_canvas : ce sont des outils
MCP, pilotes par l'agent. Le script est un juge, pas un pilote. La sequence complete :
  1. sync_canvas   -> <dir-sync-1>        (synchro fraiche, depuis la session vivante)
  2. garde avant   -> feu vert, ou refus motive
  3. compile_canvas sur <dir-a-compiler>  (a la main, par l'agent)
  4. sync_canvas   -> <dir-sync-2>
  5. garde apres   -> les ecrans qui ont bouge sans qu'on le demande

CE QUE CE SCRIPT NE PEUT PAS VOIR. Une divergence qui ne touche qu'une formule, sur un
fichier non declare : elle est signalee du cote « avant », pas bloquee, parce que la
normalisation du serveur produit exactement la meme signature. Et aucun defaut de
RENDU — cadre noir, texte tronque, section vide : ceux-la ne se voient que sur une
capture d'ecran.

CODES DE SORTIE : 0 = feu vert. 1 = refus, motif nomme. Un garde-fou qui n'a jamais dit
non n'a rien prouve : voir test_garde_compilation.py, temoin negatif et temoin positif.

Lance par : python Garde-Compilation.py avant --synchro ... --cible ...
Tests      : python -m unittest test_garde_compilation -v
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# La console Windows par defaut est en cp1252. Un motif de refus qui cite une
# formule contenant un caractere hors de cette page -- les cases a cocher de
# lblSuiActCoche, par exemple -- faisait planter le rapport EN COURS
# D'ENUMERATION, apres quelques motifs et avant les autres. Un garde-fou qui
# meurt en enumerant ses raisons peut en TAIRE une : c'est exactement l'angle
# mort qu'il est cense ne pas avoir. Mesure du 2026-09-22 : UnicodeEncodeError
# sur U+2611 apres 11 motifs sur 30, code de sortie fausse par le pipe.
for _flux in (sys.stdout, sys.stderr):
    try:
        _flux.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

# Une cle dont la valeur est un scalaire en bloc : « Text: | », « OnSelect: |- », « Width: |+ ».
# Ces blocs portent des formules Power Fx multi-lignes : une ligne de formule peut
# ressembler a une declaration de controle. Les sauter est la seule facon de ne pas
# compter des controles fantomes.
RE_BLOC = re.compile(r"^(\s*)[^\s#][^:]*:\s*[|>][-+0-9]*\s*$")
# Un controle : un item de liste dont la cle est un identificateur, seul sur sa ligne.
RE_CONTROLE = re.compile(r"^(\s*)- ([A-Za-z_][A-Za-z0-9_]*):\s*$")
# Un ecran : une cle a l'indentation 2, sous « Screens: ».
RE_ECRAN = re.compile(r"^  ([A-Za-z_][A-Za-z0-9_]*):\s*$")
RE_TYPE = re.compile(r"^\s+Control:\s*(\S+)\s*$")
RE_VARIANT = re.compile(r"^\s+Variant:\s*(\S+)\s*$")
# Une propriete sur UNE ligne : « Fill: =RGBA(...) ». Les proprietes multi-lignes sont
# des scalaires en bloc, donc deja sautees : voir propietes_simples().
RE_PROPRIETE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(\S.*)$")
STRUCTURE = {"Control", "Variant", "Properties", "Children", "Screens", "App", "EditorState"}
# Une formule nommee dans le bloc « Formulas » de App.pa.yaml : « NOM = valeur; ».
RE_FORMULE = re.compile(r"^\s*=?\s*([A-Za-z_][A-Za-z0-9_]*)\s*=")
RE_PROP_APP = re.compile(r"^    ([A-Za-z_][A-Za-z0-9_]*):")


def sauter_blocs(lignes: list[str]) -> list[str]:
    """Rend les lignes hors scalaires en bloc, en gardant leur numero d'origine.

    Regle YAML : un bloc se termine a la premiere ligne NON VIDE dont l'indentation
    est inferieure ou egale a celle de sa cle.
    """
    gardees: list[str] = []
    i = 0
    while i < len(lignes):
        ligne = lignes[i]
        m = RE_BLOC.match(ligne)
        gardees.append(ligne)
        i += 1
        if not m:
            continue
        indent = len(m.group(1))
        while i < len(lignes):
            suite = lignes[i]
            if suite.strip() and (len(suite) - len(suite.lstrip())) <= indent:
                break
            i += 1
    return gardees


def arbre_controles(texte: str) -> dict[str, list[str]]:
    """Rend { nom d'ecran : [chemin de chaque controle, DANS L'ORDRE] }.

    Le chemin encode l'imbrication (« conMain/galActions/lblTitre ») et le type entre
    crochets. Deux arbres sont identiques si et seulement si les listes le sont : cela
    couvre d'un coup l'ordre, la presence et la hierarchie — les trois choses que le
    serveur deplace en silence.
    """
    lignes = sauter_blocs(texte.splitlines())
    arbre: dict[str, list[str]] = {}
    ecran: str | None = None
    pile: list[tuple[int, str]] = []
    dernier: str | None = None  # chemin du controle ouvert, en attente de son type
    types: dict[str, str] = {}

    for ligne in lignes:
        m = RE_ECRAN.match(ligne)
        if m:
            ecran = m.group(1)
            if ecran in ("Properties", "Children"):
                ecran = None
                continue
            arbre.setdefault(ecran, [])
            pile, dernier = [], None
            continue
        if ecran is None:
            continue
        m = RE_CONTROLE.match(ligne)
        if m:
            indent, nom = len(m.group(1)), m.group(2)
            while pile and pile[-1][0] >= indent:
                pile.pop()
            chemin = "/".join([p[1] for p in pile] + [nom])
            pile.append((indent, nom))
            arbre[ecran].append(chemin)
            dernier = chemin
            continue
        if dernier is not None:
            m = RE_TYPE.match(ligne)
            if m:
                types[dernier] = m.group(1)
                continue
            m = RE_VARIANT.match(ligne)
            if m and dernier in types:
                types[dernier] += "/" + m.group(1)

    return {
        e: [f"{c} [{types.get(c, '?')}]" for c in chemins]
        for e, chemins in arbre.items()
    }


def proprietes_simples(texte: str) -> dict[tuple[str, str], str]:
    """Rend { (chemin du controle, propriete) : valeur } pour les proprietes d'UNE ligne.

    POURQUOI CE TROISIEME NIVEAU EXISTE. Mesure du 2026-09-11, premier usage reel du
    garde-fou : le depot canvas/ et l'app divergeaient sur 90, 9, 332 et 231 lignes de
    TEXTE — et l'arbre etait pourtant intact des deux cotes. Compiler le depot aurait
    ecrase des retouches faites a la main dans Studio : menus passes au bleu, coins de
    boutons a 10 px, jetons de theme remplaces par des litteraux. Feu vert sur une
    destruction : exactement le defaut que ce script existe pour empecher.

    POURQUOI LE TEXTE NE SUFFISAIT PAS, ET POURQUOI CECI SUFFIT. Le diff texte melange
    trois choses : l'ordre des proprietes, celles que le serveur AJOUTE en les explicitant
    (DisabledColor, IconStyle...), et les valeurs reellement differentes. Mesure sur les
    4 ecrans : 332 lignes de diff texte se reduisent a 16 proprietes de valeur differente,
    dont ZERO imputable a la normalisation en noms d'affichage. Une propriete ajoutee d'un
    seul cote reste une information ; une propriete presente des deux cotes avec deux
    valeurs, c'est un choix qu'on ecraserait.

    CE QU'IL NE VOIT PAS, ET C'EST VOULU : les proprietes multi-lignes — Items, OnSelect,
    Text de galerie — sont des scalaires en bloc, donc sautees. C'est la que vit la
    normalisation des noms de colonnes (Title relu 'N° de NC'), et c'est la seule raison
    pour laquelle ce controle peut etre bloquant sans crier a chaque passage.
    """
    lignes = sauter_blocs(texte.splitlines())
    valeurs: dict[tuple[str, str], str] = {}
    pile: list[tuple[int, str]] = []
    chemin: str | None = None
    for ligne in lignes:
        m = RE_CONTROLE.match(ligne)
        if m:
            indent, nom = len(m.group(1)), m.group(2)
            while pile and pile[-1][0] >= indent:
                pile.pop()
            pile.append((indent, nom))
            chemin = "/".join(p[1] for p in pile)
            continue
        m = RE_PROPRIETE.match(ligne)
        if m and chemin and m.group(1) not in STRUCTURE:
            valeurs[(chemin, m.group(1))] = m.group(2).strip()
    return valeurs


def profil_app(texte: str) -> dict[str, list[str]]:
    """Rend les proprietes de App et le nom de ses formules nommees.

    C'est la signature exacte de l'incident du 2026-09-10 : App.pa.yaml revenu reduit a
    son Theme, ses 20 jetons et son OnStart evapores. L'arbre des controles ne dit rien
    de App — il n'y a pas d'ecran dedans.
    """
    lignes = texte.splitlines()
    proprietes = [m.group(1) for m in (RE_PROP_APP.match(l) for l in lignes) if m]
    formules: list[str] = []
    dans_formules = False
    for ligne in lignes:
        if RE_PROP_APP.match(ligne):
            dans_formules = ligne.strip().startswith("Formulas:")
            continue
        if dans_formules and ligne.strip():
            m = RE_FORMULE.match(ligne)
            if m:
                formules.append(m.group(1))
    return {"proprietes": sorted(proprietes), "formules": formules}


def fichiers_pa(dossier: Path, etiquette: str) -> dict[str, Path]:
    if not dossier.is_dir():
        raise SystemExit(f"REFUS : {etiquette} introuvable — {dossier}")
    trouves = {
        p.relative_to(dossier).as_posix(): p for p in sorted(dossier.rglob("*.pa.yaml"))
    }
    if not trouves:
        raise SystemExit(f"REFUS : {etiquette} ne contient aucun .pa.yaml — {dossier}")
    return trouves


def est_ecran(nom: str) -> bool:
    return not Path(nom).name.startswith(("App.", "_"))


def normaliser_attendus(attendus: list[str]) -> set[str]:
    """« ecrDetailNC », « ecrDetailNC.pa.yaml » et « canvas/ecrDetailNC.pa.yaml » : meme chose."""
    return {Path(a).name.replace(".pa.yaml", "") for a in attendus}


def comparer_arbres(
    avant: dict[str, list[str]], apres: dict[str, list[str]]
) -> list[str]:
    """Rend la liste des ecarts, en clair. Liste vide = arbres identiques."""
    ecarts: list[str] = []
    for ecran in sorted(set(avant) | set(apres)):
        a, b = avant.get(ecran), apres.get(ecran)
        if a is None:
            ecarts.append(f"ecran apparu : {ecran}")
            continue
        if b is None:
            ecarts.append(f"ecran disparu : {ecran}")
            continue
        sa, sb = set(a), set(b)
        for c in sorted(sa - sb):
            ecarts.append(f"{ecran} : controle disparu — {c}")
        for c in sorted(sb - sa):
            ecarts.append(f"{ecran} : controle apparu — {c}")
        if sa == sb and a != b:
            rang = next(i for i, (x, y) in enumerate(zip(a, b)) if x != y)
            ecarts.append(
                f"{ecran} : ORDRE different au rang {rang} — {a[rang]} devient {b[rang]}"
            )
    return ecarts


def lire(dossier: Path, etiquette: str):
    """Rend (fichiers, arbres, profils App, textes, proprietes d'une ligne)."""
    fichiers = fichiers_pa(dossier, etiquette)
    arbres, profils, textes, props = {}, {}, {}, {}
    for nom, chemin in fichiers.items():
        texte = chemin.read_text(encoding="utf-8")
        textes[nom] = texte
        props[nom] = proprietes_simples(texte)
        if est_ecran(nom):
            arbre = arbre_controles(texte)
            if not arbre or not any(arbre.values()):
                # Fail-closed : un fichier d'ecran qu'on ne sait pas lire n'est pas un
                # fichier conforme. Ne jamais rendre « rien a signaler » sur un silence.
                raise SystemExit(
                    f"REFUS : aucun controle lu dans {nom} ({etiquette}). "
                    "Fichier vide, tronque, ou format inattendu — ne pas compiler."
                )
            arbres[nom] = arbre
        elif Path(nom).name.startswith("App."):
            profils[nom] = profil_app(texte)
    return fichiers, arbres, profils, textes, props


def cmd_avant(args: argparse.Namespace) -> int:
    synchro, cible = Path(args.synchro), Path(args.cible)
    attendus = normaliser_attendus(args.attendu)
    f_syn, a_syn, p_syn, t_syn, v_syn = lire(synchro, "dossier de synchro")
    f_cib, a_cib, p_cib, t_cib, v_cib = lire(cible, "dossier a compiler")

    print(f"synchro : {synchro}  ({len(f_syn)} fichier(s))")
    print(f"cible   : {cible}  ({len(f_cib)} fichier(s))")
    print(f"attendu : {', '.join(sorted(attendus)) if attendus else '(aucun ecart tolere)'}")
    print()

    refus: list[str] = []
    nouveaux: list[str] = []

    manquants = sorted(set(f_syn) - set(f_cib))
    surnumeraires = sorted(set(f_cib) - set(f_syn))
    if manquants:
        refus.append(
            "fichier(s) ABSENT(S) du dossier a compiler : "
            + ", ".join(manquants)
            + " — le dossier donne a compile_canvas DEVIENT l'app : "
            "ces ecrans seraient supprimes."
        )
    # Un fichier ABSENT reste un refus inconditionnel : c'est l'incident du 2026-09-11,
    # ou compiler un dossier ampute a supprime trois ecrans. Un fichier AJOUTE, lui, est
    # legitime des lors qu'il est declare — sans quoi aucun ecran neuf ne peut jamais
    # entrer dans l'app. Non declare, il reste un refus.
    if surnumeraires:
        declares = [
            n for n in surnumeraires
            if Path(n).name.replace(".pa.yaml", "") in attendus
        ]
        non_declares = [n for n in surnumeraires if n not in declares]
        if non_declares:
            refus.append(
                "fichier(s) inconnu(s) de la synchro : "
                + ", ".join(non_declares)
                + " — ils seraient ajoutes a l'app."
            )
        for n in declares:
            nouveaux.append(f"  {n} : ecran NEUF declare — il sera ajoute a l'app.")

    for nom in sorted(set(a_syn) & set(a_cib)):
        if Path(nom).name.replace(".pa.yaml", "") in attendus:
            continue
        ecarts = comparer_arbres(a_syn[nom], a_cib[nom])
        for e in ecarts:
            refus.append(f"{nom} non declare, et son arbre DIVERGE — {e}")

    for nom in sorted(set(p_syn) & set(p_cib)):
        if Path(nom).name.replace(".pa.yaml", "") in attendus:
            continue
        for cle in ("proprietes", "formules"):
            if p_syn[nom][cle] != p_cib[nom][cle]:
                perdus = sorted(set(p_syn[nom][cle]) - set(p_cib[nom][cle]))
                refus.append(
                    f"{nom} non declare, et ses {cle} divergent"
                    + (f" — perdu(s) : {', '.join(perdus)}" if perdus else " — ordre ou ajout")
                )

    # Troisieme niveau : une propriete presente des DEUX cotes avec deux valeurs est un
    # choix qu'on ecraserait en compilant. Les proprietes ajoutees d'un seul cote ne sont
    # qu'une information : le serveur explicite des valeurs par defaut a chaque synchro.
    ajouts: list[str] = []
    for nom in sorted(set(v_syn) & set(v_cib)):
        if Path(nom).name.replace(".pa.yaml", "") in attendus or Path(nom).name.startswith("_"):
            continue
        a, b = v_syn[nom], v_cib[nom]
        divergentes = sorted(k for k in set(a) & set(b) if a[k] != b[k])
        for k in divergentes[:6]:
            refus.append(
                f"{nom} : {k[0]}.{k[1]} vaut {b[k]} dans la cible et {a[k]} dans l'app "
                "— compiler ECRASERAIT la valeur de l'app."
            )
        if len(divergentes) > 6:
            refus.append(f"{nom} : ... et {len(divergentes) - 6} autre(s) propriete(s) divergente(s)")
        n_ajout, n_perdu = len(set(a) - set(b)), len(set(b) - set(a))
        if n_ajout or n_perdu:
            ajouts.append(
                f"  {nom} : {n_ajout} propriete(s) explicitee(s) par le serveur, "
                f"{n_perdu} absente(s) de l'app"
            )
    if nouveaux:
        print("Ecran(s) neuf(s) declare(s) — verifier l'ordre des enfants apres compilation :")
        print("\n".join(nouveaux))
        print()

    if ajouts:
        print("Pour information — ecarts de forme, sans valeur contradictoire :")
        print("\n".join(ajouts))
        print()

    if refus:
        print(f"REFUS — {len(refus)} motif(s). NE PAS LANCER compile_canvas.")
        for r in refus:
            print(f"  !! {r}")
        print()
        print("Reprendre depuis une synchro fraiche, ou declarer le fichier vise par --attendu.")
        return 1

    print("FEU VERT : le dossier a compiler est l'app en cours, aux ecarts declares pres.")
    return 0


def cmd_apres(args: argparse.Namespace) -> int:
    av, ap = Path(args.avant), Path(args.apres)
    attendus = normaliser_attendus(args.attendu)
    f_av, a_av, p_av, t_av, v_av = lire(av, "synchro d'avant")
    f_ap, a_ap, p_ap, t_ap, v_ap = lire(ap, "synchro d'apres")

    print(f"avant : {av}  ({len(f_av)} fichier(s))")
    print(f"apres : {ap}  ({len(f_ap)} fichier(s))")
    print(f"attendu : {', '.join(sorted(attendus)) if attendus else '(aucun mouvement tolere)'}")
    print()

    anomalies: list[str] = []
    mouvements: list[str] = []
    disparus = sorted(set(f_av) - set(f_ap))
    apparus = sorted(set(f_ap) - set(f_av))
    if disparus:
        anomalies.append("fichier(s) DISPARU(S) de l'app : " + ", ".join(disparus))
    # Symetrique du cas traite dans cmd_avant : un ecran qui APPARAIT alors qu'il etait
    # declare est le resultat attendu d'un ajout. Non declare, il reste une anomalie.
    if apparus:
        declares_ap = [
            n for n in apparus
            if Path(n).name.replace(".pa.yaml", "") in attendus
        ]
        non_declares_ap = [n for n in apparus if n not in declares_ap]
        if non_declares_ap:
            anomalies.append(
                "fichier(s) apparu(s) dans l'app : " + ", ".join(non_declares_ap)
            )
        for n in declares_ap:
            mouvements.append(f"  {n} : ecran NEUF declare, bien ajoute a l'app.")

    bouges: list[str] = []
    for nom in sorted(set(a_av) & set(a_ap)):
        ecarts = comparer_arbres(a_av[nom], a_ap[nom])
        declare = Path(nom).name.replace(".pa.yaml", "") in attendus
        if ecarts and not declare:
            bouges.append(nom)
            for e in ecarts:
                anomalies.append(f"{nom} a BOUGE sans etre declare — {e}")
        elif ecarts:
            print(f"{nom} (declare) — {len(ecarts)} changement(s) d'arbre :")
            for e in ecarts[:15]:
                print(f"    {e}")
            if len(ecarts) > 15:
                print(f"    ... et {len(ecarts) - 15} autre(s)")
            print()
        elif declare:
            if t_av.get(nom) != t_ap.get(nom):
                print(f"{nom} (declare) — arbre inchange, texte modifie : formule seule.")
            else:
                print(f"{nom} (declare) — RIEN n'a bouge. Le changement n'a pas ete applique.")
            print()

    for nom in sorted(set(p_av) & set(p_ap)):
        if p_av[nom] != p_ap[nom]:
            perdues = sorted(set(p_av[nom]["formules"]) - set(p_ap[nom]["formules"]))
            anomalies.append(
                f"{nom} a change : "
                + (f"formule(s) perdue(s) — {', '.join(perdues)}" if perdues else "profil different")
            )

    for nom in sorted(set(t_av) & set(t_ap)):
        if Path(nom).name.startswith("_"):
            continue  # _EditorState varie avec la navigation dans Studio, pas avec l'app.
        declare = Path(nom).name.replace(".pa.yaml", "") in attendus
        if not declare and t_av[nom] != t_ap[nom] and nom not in bouges:
            a, b = v_av.get(nom, {}), v_ap.get(nom, {})
            divergentes = sorted(k for k in set(a) & set(b) if a[k] != b[k])
            detail = (
                "; ".join(f"{k[0]}.{k[1]} : {a[k]} -> {b[k]}" for k in divergentes[:4])
                if divergentes
                else f"{sum(1 for x, y in zip(t_av[nom].splitlines(), t_ap[nom].splitlines()) if x != y)} ligne(s), aucune valeur contradictoire"
            )
            anomalies.append(
                f"{nom} a change sans etre declare — {detail}. Les deux cotes viennent du "
                "serveur : ce diff n'a pas d'excuse de normalisation."
            )

    if mouvements:
        print("Ecran(s) neuf(s) entre(s) dans l'app, comme declare :")
        print("\n".join(mouvements))
        print()

    if anomalies:
        print(f"ANOMALIE — {len(anomalies)} constat(s). L'app a bouge ailleurs que la ou on l'a demande.")
        for a in anomalies:
            print(f"  !! {a}")
        return 1

    print("CONFORME : seuls les ecrans declares ont bouge.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Garde-fou de compilation canvas (jalon 0 du plan de redressement)."
    )
    sous = p.add_subparsers(dest="etape", required=True)

    a = sous.add_parser("avant", help="avant compile_canvas : la cible est-elle l'app en cours ?")
    a.add_argument("--synchro", required=True, help="dossier d'un sync_canvas frais")
    a.add_argument("--cible", required=True, help="dossier qui sera donne a compile_canvas")
    a.add_argument("--attendu", action="append", default=[], help="ecran autorise a diverger")
    a.set_defaults(fn=cmd_avant)

    b = sous.add_parser("apres", help="apres compile_canvas : qu'est-ce qui a bouge ?")
    b.add_argument("--avant", required=True, help="dossier du sync_canvas d'avant")
    b.add_argument("--apres", required=True, help="dossier du sync_canvas d'apres")
    b.add_argument("--attendu", action="append", default=[], help="ecran autorise a bouger")
    b.set_defaults(fn=cmd_apres)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
