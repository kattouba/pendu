from os.path import dirname, join
import random
import unicodedata
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, CENTER
from android.media import AudioManager, SoundPool


def enlever_accents(texte):
    """
    Remplace les caractères accentués par leurs équivalents non accentués.
    """
    return ''.join(
        c for c in unicodedata.normalize('NFD', texte)
        if unicodedata.category(c) != 'Mn'
    )


def charger_fichier_txt(nom_fichier):
    """
    Charge un fichier texte depuis le dossier resources avec un encodage spécifique.
    """
    fichier_path = join(dirname(__file__), "resources", nom_fichier)
    with open(fichier_path, "r", encoding="latin1") as f:
        return f.read().splitlines()


class Pendu(toga.App):
    def startup(self):
        # Initialisation de SoundPool pour les sons
        self.sound_pool = SoundPool(5, AudioManager.STREAM_MUSIC, 0)
        self.sound1 = self.sound_pool.load(join(dirname(__file__), "resources/son1.mp3"), 1)
        self.sound2 = self.sound_pool.load(join(dirname(__file__), "resources/son2.mp3"), 1)
        self.sound3 = self.sound_pool.load(join(dirname(__file__), "resources/son3.mp3"), 1)

        # Initialisation des variables de jeu
        self.mot_secret = ""
        self.mot_secret_normalise = ""
        self.essais_restants = 10
        self.lettres_trouvees = set()
        self.lettres_essayees = set()

        # Conteneur principal pour le jeu
        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=10, alignment=CENTER))

        # Widgets de l'interface principale
        self.resultat_label = toga.Label("Bienvenue dans le jeu du pendu !", style=Pack(padding=(0, 5), text_align=CENTER))
        self.image_label = toga.ImageView(style=Pack(height=200, alignment=CENTER, padding=(0, 5)))
        self.image_label.image = join(dirname(__file__), "resources/pendu_etape0.png")
        self.lettres_label = toga.Label("Mot : ", style=Pack(padding=(0, 5), text_align=CENTER))
        self.historique_label = toga.Label("Lettres utilisées : ", style=Pack(padding=(0, 5), text_align=CENTER))
        self.entry_lettre = toga.TextInput(placeholder="Entrez une lettre", style=Pack(padding=(0, 5), alignment=CENTER))
        self.verifier_button = toga.Button("Essayer", on_press=self.verifier_lettre, style=Pack(padding=(0, 5), alignment=CENTER))
        self.rejouer_button = toga.Button("Rejouer", on_press=self.rejouer, style=Pack(padding=(0, 5), alignment=CENTER))
        self.expliquer_button = toga.Button("Expliquer le mot", on_press=self.expliquer_mot, style=Pack(padding=(0, 5), alignment=CENTER))

        # Ajouter les widgets au conteneur principal
        self.main_box.add(self.resultat_label)
        self.main_box.add(self.image_label)
        self.main_box.add(self.lettres_label)
        self.main_box.add(self.historique_label)
        self.main_box.add(self.entry_lettre)
        self.main_box.add(self.verifier_button)
        self.main_box.add(self.rejouer_button)
        self.main_box.add(self.expliquer_button)

        # Conteneur pour la WebView
        self.webview = toga.WebView(style=Pack(flex=1))
        self.webview_box = toga.Box(children=[self.webview], style=Pack(direction=COLUMN, padding=10))
        self.webview_box.visible = False

        self.retour_button = toga.Button(
            "Retour", on_press=self.afficher_principal, style=Pack(padding=(0, 5), alignment=CENTER)
        )
        self.webview_box.add(self.retour_button)

        # Fenêtre principale
        self.main_window = toga.MainWindow(title="Pendu")
        self.main_window.content = toga.Box(
            children=[self.main_box, self.webview_box],
            style=Pack(direction=COLUMN)
        )
        self.main_window.show()

        # Commencer un nouveau jeu
        self.rejouer()

    def jouer_son(self, sound):
        """
        Joue un son à l'aide de SoundPool.
        """
        self.sound_pool.play(sound, 1.0, 1.0, 0, 0, 1.0)

    def verifier_lettre(self, widget):
        """
        Vérifie la lettre entrée par l'utilisateur.
        """
        lettre = self.entry_lettre.value.lower()
        self.entry_lettre.value = ""

        if not lettre or len(lettre) != 1 or not lettre.isalpha():
            self.resultat_label.text = "Entrez une lettre valide."
            return

        if lettre in self.lettres_essayees:
            self.resultat_label.text = f"Vous avez déjà essayé la lettre '{lettre}'."
            return

        self.lettres_essayees.add(lettre)

        # Mettre à jour l'historique des lettres utilisées
        self.historique_label.text = "Lettres utilisées : " + ", ".join(sorted(self.lettres_essayees))

        if lettre in self.mot_secret_normalise:
            self.lettres_trouvees.add(lettre)
            self.resultat_label.text = f"Bonne réponse : '{lettre}' est dans le mot !"
        else:
            self.essais_restants -= 1
            self.jouer_son(self.sound1)
            self.resultat_label.text = f"Mauvaise réponse. Essais restants : {self.essais_restants}"
            self.image_label.image = join(dirname(__file__), f"resources/pendu_etape{10 - self.essais_restants}.png")

        mot_affiche = " ".join([lettre if lettre in self.lettres_trouvees else "-" for lettre in self.mot_secret_normalise])
        self.lettres_label.text = f"Mot : {mot_affiche}"

        if set(self.mot_secret_normalise) == self.lettres_trouvees:
            self.jouer_son(self.sound2)
            self.resultat_label.text = f"Bravo ! Vous avez trouvé le mot : {self.mot_secret}"
        elif self.essais_restants == 0:
            self.jouer_son(self.sound3)
            self.resultat_label.text = f"Perdu ! Le mot était : {self.mot_secret}"

    def expliquer_mot(self, widget):
        """
        Charge l'explication du mot dans une WebView intégrée, en affichant uniquement les définitions pertinentes.
        """
        self.main_box.visible = False
        self.webview_box.visible = True

        base_url = "https://www.littre.org/search/definitions?_hasdata=&f1="
        mot_a_expliquer = self.mot_secret
        url = f"{base_url}{mot_a_expliquer}"

        try:
            custom_script = """
            document.addEventListener('DOMContentLoaded', function() {
                document.body.innerHTML = '';
                var matchingDefinitions = document.querySelector('ol.matching-definitions');
                if (matchingDefinitions) {
                    document.body.appendChild(matchingDefinitions);
                } else {
                    document.body.innerHTML = '<p>Aucune définition trouvée.</p>';
                }
            });
            """
            self.webview.url = url
            self.webview.on_load = lambda _: self.webview.evaluate_javascript(custom_script)
        except Exception as e:
            self.resultat_label.text = "Erreur : Impossible de charger l'explication."
            print(f"Erreur lors du chargement de l'URL : {e}")

    def afficher_principal(self, widget):
        """
        Retourne à l'écran principal.
        """
        self.main_box.visible = True
        self.webview.set_content("", "<html><body></body></html>")
        self.webview_box.visible = False

    def rejouer(self, widget=None):
        """
        Réinitialise le jeu et assure que la WebView est bien masquée.
        """
        self.essais_restants = 10
        self.lettres_trouvees.clear()
        self.lettres_essayees.clear()

        # Choisir un nouveau mot
        longueur_mot = random.randint(5, 9)
        fichier_mots = f"data{longueur_mot}.txt"
        mots = charger_fichier_txt(fichier_mots)

        self.mot_secret = random.choice(mots).strip().lower()
        self.mot_secret_normalise = enlever_accents(self.mot_secret)

        # Réinitialiser les composants de l'interface
        self.image_label.image = join(dirname(__file__), "resources/pendu_etape0.png")
        self.resultat_label.text = "Nouveau jeu lancé ! Bonne chance."
        self.lettres_label.text = "Mot : " + "-" * len(self.mot_secret_normalise)
        self.historique_label.text = "Lettres utilisées : "

        # Masquer la WebView et afficher l'écran principal
        self.webview.set_content("", "<html><body></body></html>")
        self.webview_box.visible = False
        self.main_box.visible = True


def main():
    return Pendu()
