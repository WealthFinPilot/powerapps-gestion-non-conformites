"""Tests du garde-fou de compilation canvas.

Lance par : python -m unittest test_garde_compilation -v
pytest n'est PAS installe sur ce poste : on s'en tient a unittest, bibliotheque standard.

CE QUE CES TESTS PROUVENT, et pourquoi ils sont ecrits dans cet ordre :

  1. Le parseur saute les scalaires en bloc. TestPiegeDuBloc etablit d'abord que la ligne
     piege EST un faux positif naturel — sans ce temoin, le test « 3 controles » passerait
     aussi avec un parseur qui ne compte rien du tout.
  2. Le garde dit NON. Temoin negatif du jalon 0 : un dossier ampute d'un fichier est
     refuse. Un garde-fou qui n'a jamais dit non n'a rien prouve.
  3. Le garde dit OUI. Temoin positif : un dossier complet, un seul fichier modifie et
     declare, passe — et le rapport d'apres ne signale que cet ecran.

Les deux derniers sont les deux criteres d'acceptation du jalon 0, mot pour mot.
"""

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

# Le livrable s'appelle « Garde-Compilation.py », avec un tiret : le nom vient du plan de
# redressement et les scripts du projet sont nommes ainsi. Un tiret n'est pas importable
# par « import », d'ou le chargement explicite. Renommer le fichier serait plus simple,
# mais le nom du livrable est celui du plan.
_spec = importlib.util.spec_from_file_location(
    "garde_compilation", Path(__file__).parent / "Garde-Compilation.py"
)
garde = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(garde)

RE_CONTROLE = garde.RE_CONTROLE
arbre_controles = garde.arbre_controles
comparer_arbres = garde.comparer_arbres
main = garde.main
profil_app = garde.profil_app
sauter_blocs = garde.sauter_blocs

APP = """App:
  Properties:
    Formulas: |-
      =ThemeUn = RGBA(255, 241, 232, 1);
      ThemeDeux = RGBA(250, 249, 248, 1);
      SeuilJours = 180;
    OnStart: =Set(gblNC, Defaults(NC))
    Theme: =PowerAppsTheme
"""

APP_AMPUTEE = """App:
  Properties:
    Theme: =PowerAppsTheme
"""

# Le piege : dans le bloc « Tooltip: | », deux lignes ont la forme exacte d'un controle.
ECRAN_UN = """Screens:
  ecrUn:
    Properties:
      Fill: =RGBA(255, 255, 255, 1)
    Children:
      - conA:
          Control: GroupContainer
          Variant: AutoLayout
          Properties:
            Tooltip: |
              ="Sections :
              - faux:
              - egalementFaux:
              fin"
          Children:
            - lblUn:
                Control: Label
                Properties:
                  Text: ="un"
            - lblDeux:
                Control: Label
                Properties:
                  Text: ="deux"
"""

ECRAN_DEUX = """Screens:
  ecrDeux:
    Properties:
      Fill: =RGBA(255, 255, 255, 1)
    Children:
      - conB:
          Control: GroupContainer
          Properties:
            Height: =200
          Children:
            - lblTrois:
                Control: Label
                Properties:
                  Text: ="trois"
"""

# Meme ecran, lblUn et lblDeux inverses : ensemble identique, ORDRE different. C'est le
# defaut que compile_canvas rend avec « 0 erreur » et que seul un sync relu fait voir.
ECRAN_UN_ORDRE_INVERSE = ECRAN_UN.replace(
    """            - lblUn:
                Control: Label
                Properties:
                  Text: ="un"
            - lblDeux:
                Control: Label
                Properties:
                  Text: ="deux"
""",
    """            - lblDeux:
                Control: Label
                Properties:
                  Text: ="deux"
            - lblUn:
                Control: Label
                Properties:
                  Text: ="un"
""",
)

ECRAN_UN_CONTROLE_AJOUTE = ECRAN_UN.replace(
    """            - lblDeux:""",
    """            - lblNouveau:
                Control: Label
                Properties:
                  Text: ="nouveau"
            - lblDeux:""",
)

# Valeur de propriete modifiee : l'arbre est identique, la valeur non. C'est le cas
# mesure le 2026-09-11 — des retouches Studio absentes du depot, qu'une compilation du
# depot aurait ecrasees.
ECRAN_UN_FORMULE = ECRAN_UN.replace('Text: ="un"', 'Text: ="un modifie"')

# Propriete explicitee par le serveur, presente d'un seul cote : forme, pas contradiction.
ECRAN_UN_PROPRIETE_EXPLICITEE = ECRAN_UN.replace(
    """                Properties:
                  Text: ="un\"""",
    """                Properties:
                  DisabledColor: =RGBA(0, 0, 0, 1)
                  Text: ="un\"""",
)


def monter(dossier: Path, fichiers: dict[str, str]) -> Path:
    dossier.mkdir(parents=True, exist_ok=True)
    for nom, contenu in fichiers.items():
        (dossier / nom).write_text(contenu, encoding="utf-8")
    return dossier


APP_COMPLETE = {
    "App.pa.yaml": APP,
    "ecrUn.pa.yaml": ECRAN_UN,
    "ecrDeux.pa.yaml": ECRAN_DEUX,
}


def lancer(argv: list[str]) -> tuple[int, str]:
    """Rend (code de sortie, sortie texte). SystemExit leve par lire() vaut refus."""
    tampon = io.StringIO()
    try:
        with contextlib.redirect_stdout(tampon):
            code = main(argv)
    except SystemExit as e:
        return 1, tampon.getvalue() + str(e.code)
    return code, tampon.getvalue()


class TestPiegeDuBloc(unittest.TestCase):
    """Les formules Power Fx multi-lignes contiennent des lignes en forme de controle."""

    def test_la_ligne_piege_est_bien_un_faux_positif(self):
        # Sans ce temoin, le test suivant passerait aussi avec un parseur qui ne compte rien.
        self.assertIsNotNone(RE_CONTROLE.match("              - faux:"))

    def test_le_bloc_est_saute(self):
        restantes = sauter_blocs(ECRAN_UN.splitlines())
        self.assertNotIn("              - faux:", restantes)
        self.assertIn("            Tooltip: |", restantes)

    def test_le_bloc_se_termine_a_la_desindentation(self):
        # La ligne qui suit le bloc, moins indentee, doit etre gardee.
        self.assertIn("          Children:", sauter_blocs(ECRAN_UN.splitlines()))


class TestArbre(unittest.TestCase):
    def test_compte_et_ordre(self):
        arbre = arbre_controles(ECRAN_UN)
        self.assertEqual(list(arbre), ["ecrUn"])
        self.assertEqual(
            arbre["ecrUn"],
            [
                "conA [GroupContainer/AutoLayout]",
                "conA/lblUn [Label]",
                "conA/lblDeux [Label]",
            ],
        )

    def test_l_imbrication_est_dans_le_chemin(self):
        self.assertTrue(
            all("/" in c for c in arbre_controles(ECRAN_UN)["ecrUn"][1:])
        )

    def test_une_inversion_d_ordre_est_vue(self):
        ecarts = comparer_arbres(
            arbre_controles(ECRAN_UN), arbre_controles(ECRAN_UN_ORDRE_INVERSE)
        )
        self.assertEqual(len(ecarts), 1)
        self.assertIn("ORDRE different", ecarts[0])

    def test_une_modification_de_formule_seule_ne_bouge_pas_l_arbre(self):
        self.assertEqual(arbre_controles(ECRAN_UN), arbre_controles(ECRAN_UN_FORMULE))

    def test_app_n_a_pas_d_arbre(self):
        self.assertEqual(arbre_controles(APP), {})


class TestProfilApp(unittest.TestCase):
    def test_releve_les_formules_nommees_et_les_proprietes(self):
        p = profil_app(APP)
        self.assertEqual(p["formules"], ["ThemeUn", "ThemeDeux", "SeuilJours"])
        self.assertEqual(p["proprietes"], ["Formulas", "OnStart", "Theme"])

    def test_voit_l_amputation_du_2026_09_10(self):
        # Theme seul conserve, jetons et OnStart evapores : la signature exacte.
        p = profil_app(APP_AMPUTEE)
        self.assertEqual(p["formules"], [])
        self.assertEqual(p["proprietes"], ["Theme"])


class TestTemoinNegatif(unittest.TestCase):
    """Critere d'acceptation 1 du jalon 0 : un dossier ampute est REFUSE."""

    def test_dossier_ampute_d_un_ecran(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            ampute = {k: v for k, v in APP_COMPLETE.items() if k != "ecrDeux.pa.yaml"}
            cible = monter(racine / "cible", ampute)
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("REFUS", sortie)
        self.assertIn("ecrDeux.pa.yaml", sortie)

    def test_dossier_a_un_seul_ecran_le_cas_du_2026_09_11(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(racine / "cible", {"ecrUn.pa.yaml": ECRAN_UN})
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 1)
        self.assertIn("App.pa.yaml", sortie)
        self.assertIn("ecrDeux.pa.yaml", sortie)

    def test_un_ecran_perime_non_declare_le_cas_du_2026_09_10(self):
        # Les 6 fichiers sont la : la comparaison des NOMS ne voit rien. L'arbre, si.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            perime = dict(APP_COMPLETE)
            perime["ecrDeux.pa.yaml"] = ECRAN_DEUX.replace(
                """            - lblTrois:
                Control: Label
                Properties:
                  Text: ="trois"
""",
                "",
            )
            cible = monter(racine / "cible", perime)
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 1)
        self.assertIn("ecrDeux", sortie)

    def test_app_amputee_de_ses_jetons(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(racine / "cible", dict(APP_COMPLETE, **{"App.pa.yaml": APP_AMPUTEE}))
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("ThemeUn", sortie)

    def test_un_fichier_d_ecran_vide_est_refuse_pas_ignore(self):
        # Fail-closed : ne jamais rendre « rien a signaler » sur un fichier illisible.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(racine / "cible", dict(APP_COMPLETE, **{"ecrDeux.pa.yaml": ""}))
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("aucun controle lu", sortie)


class TestTemoinPositif(unittest.TestCase):
    """Critere d'acceptation 2 du jalon 0 : un dossier complet, un fichier declare, PASSE."""

    def test_dossier_identique(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(racine / "cible", APP_COMPLETE)
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 0)
        self.assertIn("FEU VERT", sortie)

    def test_un_seul_ecran_modifie_et_declare(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible",
                dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_CONTROLE_AJOUTE}),
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 0)
        self.assertIn("FEU VERT", sortie)

    def test_le_meme_ecran_modifie_mais_NON_declare_est_refuse(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible",
                dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_CONTROLE_AJOUTE}),
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("lblNouveau", sortie)

    def test_une_valeur_de_propriete_divergente_est_REFUSEE(self):
        # Le faux vert du 2026-09-11 : arbre intact des deux cotes, valeurs differentes,
        # et compiler la cible aurait ecrase les retouches faites dans Studio.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible", dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_FORMULE})
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("ECRASERAIT", sortie)
        self.assertIn("conA/lblUn.Text", sortie)

    def test_la_meme_divergence_declaree_passe(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible", dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_FORMULE})
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 0)

    def test_une_propriete_explicitee_par_le_serveur_ne_bloque_pas(self):
        # A chaque synchro le serveur ajoute des valeurs par defaut explicites
        # (DisabledColor, IconStyle...). Bloquer la-dessus, c'est crier a chaque passage.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(
                racine / "sync",
                dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_PROPRIETE_EXPLICITEE}),
            )
            cible = monter(racine / "cible", APP_COMPLETE)
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 0)
        self.assertIn("Pour information", sortie)
        self.assertIn("1 propriete(s) explicitee(s)", sortie)


class TestRapportDApres(unittest.TestCase):
    """Second volet du critere 2 : le rapport d'apres ne signale QUE l'ecran declare."""

    def test_seul_l_ecran_declare_a_bouge(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap",
                dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_CONTROLE_AJOUTE}),
            )
            code, sortie = lancer(
                ["apres", "--avant", str(av), "--apres", str(ap), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 0)
        self.assertIn("CONFORME", sortie)
        self.assertIn("lblNouveau", sortie)
        self.assertNotIn("ecrDeux.pa.yaml a BOUGE", sortie)

    def test_un_ecran_declare_qui_n_a_pas_bouge_du_tout_est_dit(self):
        # Cas utile : une creation de controle exige DEUX compile_canvas, parfois trois.
        # Si le fichier declare est identique des deux cotes, le changement n'a pas pris.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(racine / "ap", APP_COMPLETE)
            code, sortie = lancer(
                ["apres", "--avant", str(av), "--apres", str(ap), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 0)
        self.assertIn("RIEN n'a bouge", sortie)

    def test_un_autre_ecran_a_bouge_en_silence(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap",
                dict(
                    APP_COMPLETE,
                    **{
                        "ecrUn.pa.yaml": ECRAN_UN_CONTROLE_AJOUTE,
                        "ecrDeux.pa.yaml": ECRAN_DEUX.replace("lblTrois", "lblAutre"),
                    },
                ),
            )
            code, sortie = lancer(
                ["apres", "--avant", str(av), "--apres", str(ap), "--attendu", "ecrUn"]
            )
        self.assertEqual(code, 1)
        self.assertIn("ANOMALIE", sortie)
        self.assertIn("ecrDeux.pa.yaml a BOUGE", sortie)

    def test_l_ordre_reempile_a_la_fin_est_vu(self):
        # Le symptome du 2026-09-03 : le serveur reattache les enfants A LA FIN, et
        # compile_canvas rend « 0 erreur » sur un ecran dont l'ordre est faux.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap", dict(APP_COMPLETE, **{"ecrUn.pa.yaml": ECRAN_UN_ORDRE_INVERSE})
            )
            code, sortie = lancer(["apres", "--avant", str(av), "--apres", str(ap)])
        self.assertEqual(code, 1)
        self.assertIn("ORDRE different", sortie)

    def test_un_ecran_disparu_de_la_session(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap",
                {k: v for k, v in APP_COMPLETE.items() if k != "ecrDeux.pa.yaml"},
            )
            code, sortie = lancer(["apres", "--avant", str(av), "--apres", str(ap)])
        self.assertEqual(code, 1)
        self.assertIn("DISPARU", sortie)

    def test_une_formule_perdue_dans_App_est_vue(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(racine / "ap", dict(APP_COMPLETE, **{"App.pa.yaml": APP_AMPUTEE}))
            code, sortie = lancer(["apres", "--avant", str(av), "--apres", str(ap)])
        self.assertEqual(code, 1)
        self.assertIn("ThemeUn", sortie)


class TestEcranNeuf(unittest.TestCase):
    """Ajouter un ecran, cas non couvert jusqu'au 2026-09-14 : le garde-fou refusait tout
    fichier surnumeraire, meme declare, ce qui interdisait d'ajouter le moindre ecran."""

    def test_un_ecran_neuf_declare_passe(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible",
                dict(APP_COMPLETE, **{"ecrTrois.pa.yaml": ECRAN_DEUX}),
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible),
                 "--attendu", "ecrTrois"]
            )
        self.assertEqual(code, 0)
        self.assertIn("FEU VERT", sortie)
        self.assertIn("ecrTrois", sortie)
        self.assertIn("NEUF", sortie)

    def test_un_ecran_neuf_NON_declare_reste_refuse(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            cible = monter(
                racine / "cible",
                dict(APP_COMPLETE, **{"ecrTrois.pa.yaml": ECRAN_DEUX}),
            )
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible)]
            )
        self.assertEqual(code, 1)
        self.assertIn("ecrTrois", sortie)

    def test_apres_un_ecran_neuf_declare_est_conforme(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap",
                dict(APP_COMPLETE, **{"ecrTrois.pa.yaml": ECRAN_DEUX}),
            )
            code, sortie = lancer(
                ["apres", "--avant", str(av), "--apres", str(ap), "--attendu", "ecrTrois"]
            )
        self.assertEqual(code, 0)
        self.assertIn("CONFORME", sortie)
        self.assertIn("ecrTrois", sortie)

    def test_apres_un_ecran_neuf_NON_declare_est_une_anomalie(self):
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            av = monter(racine / "av", APP_COMPLETE)
            ap = monter(
                racine / "ap",
                dict(APP_COMPLETE, **{"ecrTrois.pa.yaml": ECRAN_DEUX}),
            )
            code, sortie = lancer(["apres", "--avant", str(av), "--apres", str(ap)])
        self.assertEqual(code, 1)
        self.assertIn("ecrTrois", sortie)

    def test_une_suppression_reste_refusee_MEME_declaree(self):
        # La tolerance ouverte ci-dessus ne doit PAS s'etendre a la disparition d'un
        # ecran : c'est l'incident du 2026-09-11, ou compiler a supprime trois ecrans.
        with tempfile.TemporaryDirectory() as t:
            racine = Path(t)
            synchro = monter(racine / "sync", APP_COMPLETE)
            ampute = {k: v for k, v in APP_COMPLETE.items() if k != "ecrDeux.pa.yaml"}
            cible = monter(racine / "cible", ampute)
            code, sortie = lancer(
                ["avant", "--synchro", str(synchro), "--cible", str(cible),
                 "--attendu", "ecrDeux"]
            )
        self.assertEqual(code, 1)
        self.assertIn("ecrDeux", sortie)


if __name__ == "__main__":
    unittest.main()
