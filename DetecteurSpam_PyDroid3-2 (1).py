# ============================================================
# DETECTEUR DE SPAM - PYDROID 3 / ANDROID
# 100 % GRATUIT - AUCUNE API - AUCUNE CONNEXION INTERNET
# Bibliothèque standard Python uniquement.
# ============================================================

import math
import random
import re
import unicodedata
from collections import Counter

# ------------------------------------------------------------
# DONNÉES DU PROJET
# ------------------------------------------------------------
SPAM = ['felicitations vous avez gagne un iphone gratuit', 'vous avez gagne un prix exceptionnel', 'un gain important vous attend', 'vous etes le gagnant de notre loterie', 'votre lot est pret a etre reclame', 'reclamez votre cadeau gratuit maintenant', 'vous avez ete selectionne pour recevoir un bonus', 'felicitations votre numero a ete tire', 'gagnez un telephone gratuitement', 'gagnez un iphone sans frais', 'telephone gratuit pour les premiers inscrits', 'smartphone gratuit disponible maintenant', 'gagnez un voyage grace a notre promotion', 'votre jackpot est disponible', 'felicitations jackpot gagne', 'participez a notre loterie et gagnez', 'une fortune peut devenir la votre', 'gagnez des millions rapidement', 'votre chance de gagner commence aujourd hui', 'obtenez un gain exceptionnel', 'argent gratuit disponible pour vous', 'recevez de l argent gratuitement', 'argent facile depuis chez vous', 'gagnez de l argent sans experience', 'gains rapides sans investissement', 'revenu garanti depuis votre telephone', 'salaire garanti sans experience', 'gagnez depuis chez vous', 'travail facile disponible maintenant', 'emploi facile avec revenu garanti', 'travail en ligne tres bien remunere', 'double votre argent des aujourd hui', 'argent multiplie en quelques heures', 'votre argent peut etre double', 'investissez maintenant pour gagner rapidement', 'investissez sans risque et obtenez une fortune', 'bitcoin et gains garantis', 'gagnez avec la cryptomonnaie', 'crypto avec revenu garanti', 'profitez de notre offre forex', 'trading facile avec gains garantis', 'ethereum disponible pour les nouveaux investisseurs', 'usdt et bonus exclusif', 'votre wallet peut recevoir un bonus', 'offre exclusive pour nouveaux clients', 'promotion speciale disponible maintenant', 'promo exceptionnelle pour vous', 'reduction incroyable pour les membres', 'cadeau gratuit reserve pour vous', 'offre speciale valable aujourd hui', 'dernieres places disponibles', 'profitez maintenant avant la fermeture', 'ne ratez pas cette offre', 'ne perdez pas votre chance', 'agissez maintenant pour recevoir votre cadeau', 'dernier delai pour recuperer votre prix', 'derniere chance de gagner', 'offre disponible immediatement', 'votre recompense vous attend', 'recuperez votre recompense rapidement', 'vous avez gagne un bonus', 'bonus exceptionnel pour vous', 'bonus gratuit pour les nouveaux membres', 'prix gagne disponible maintenant', 'vous avez gagne une importante somme', 'vous avez gagne un lot surprise', 'felicitations votre gain est confirme', 'felicitation vous avez ete selectionne', 'felicitations vous etes notre gagnant', 'urgence votre compte doit etre verifie', 'urgent confirmez votre compte', 'compte bloque verifiez votre identite', 'compte suspendu confirmez vos informations', 'votre compte sera bloque si vous ne reagissez pas', 'verifier votre compte immediatement', 'confirmer votre compte pour eviter la suspension', 'confirmez votre identite maintenant', 'connectez vous pour recevoir votre bonus', 'cliquez ici pour confirmer votre compte', 'clique ici pour recuperer votre gain', 'cliquez pour ouvrir le lien', 'visitez ce lien pour recevoir votre cadeau', 'inscrivez vous pour obtenir votre bonus', 'inscris toi pour gagner un prix', 'ouvrez le lien avant le dernier delai', 'payez les frais de livraison pour recevoir votre cadeau', 'payez les frais de retrait pour obtenir votre gain', 'envoyez de largent pour recevoir votre recompense', 'envoyez argent pour confirmer le transfert', 'envoie argent maintenant pour debloquer votre compte', 'envoyez votre code pour recevoir le gain', 'donnez votre mot de passe pour confirmer', 'donnez votre code pin immediatement', 'envoyez le code recu par sms', 'donnez votre numero de carte pour recevoir le prix', 'entrez votre carte bancaire pour obtenir le bonus', 'donnez votre numero de compte pour recevoir votre argent', 'votre date de naissance est necessaire pour gagner', 'envoyez votre piece didentite pour recevoir le lot', 'donnez vos informations personnelles pour participer']

NON_SPAM = ['bonjour comment vas tu', 'on se voit demain matin', 'bonsoir peux tu venir chez moi', 'ma grand mere m a garde du chocolat', 'n oublie pas notre rendez vous', 'la reunion commence a dix heures', 'merci pour ton aide', 'merci pour le message', 'je suis bien arrive a la maison', 'je serai la dans quelques minutes', 'peux tu m envoyer le document', 'peux tu me donner le devoir', 'as tu termine le travail', 'le professeur a donne un exercice', 'n oublie pas ton cahier', 'apporte ton livre demain', 'on travaille ensemble ce soir', 'rendez vous demain apres midi', 'je vais arriver un peu tard', 'appelle moi quand tu arrives', 'envoie moi ton adresse', 'quel est ton numero', 'peux tu me rappeler', 'merci pour ce cadeau', 'bonne journee a toi', 'bonne chance pour ton examen', 'bon courage pour demain', 'a demain au lycee', 'on se retrouve apres les cours', 'les cours commencent a huit heures', 'le professeur est deja arrive', 'le devoir est difficile', 'peux tu expliquer cet exercice', 'je ne comprends pas cette question', 'aide moi avec les mathematiques', 'on peut travailler ensemble', 'je vais faire le devoir ce soir', 'as tu compris la lecon', 'la lecon commence maintenant', 'n oublie pas de reviser', 'il faut reviser pour le controle', 'le controle est demain', 'le professeur a annonce un controle', 'je vais etudier ce soir', 'je suis fatigue aujourd hui', 'je rentre a la maison', 'je vais manger maintenant', 'on mange ensemble ce soir', 'viens manger avec nous', 'le repas est pret', 'maman demande de rentrer', 'papa est deja a la maison', 'ma soeur est a l ecole', 'mon frere arrive demain', 'nous partons samedi', 'on voyage pendant les vacances', 'les vacances commencent bientot', 'je vais visiter ma famille', 'nous allons chez nos grands parents', 'tu peux acheter du pain', 'n oublie pas le lait', 'il faut acheter du riz', 'peux tu faire les courses', 'je vais au magasin', 'le magasin ferme a dix neuf heures', 'la voiture est devant la maison', 'le bus arrive bientot', 'je suis dans le bus', 'le taxi est deja arrive', 'on se retrouve a la gare', 'le train arrive a midi', 'mon professeur a envoye un message', 'le directeur a parle aux eleves', 'la classe commence demain', 'nous avons cours de physique', 'nous avons cours de chimie', 'le devoir de mathematiques est long', 'j ai fini mon exercice', 'peux tu verifier mon travail', 'merci beaucoup pour ton explication', 'je comprends maintenant', 'c est beaucoup plus clair', 'on continuera demain', 'je vais dormir maintenant', 'bonne nuit', 'a demain', 'a bientot', 'prends soin de toi', 'comment va ta famille', 'tout va bien ici', 'je voulais prendre de tes nouvelles', 'merci pour ta reponse', 'desole pour le retard', 'je n avais pas vu ton message', 'je viens de voir ton message', 'je te reponds plus tard', 'peux tu m envoyer la photo', 'envoie moi les informations', 'j ai besoin de ton aide', 'on en parlera demain']

# ------------------------------------------------------------
# NORMALISATION
# ------------------------------------------------------------
def nettoyer(texte):
    texte = str(texte).lower().strip()
    texte = re.sub(r"https?://\S+|www\.\S+", " URL ", texte)
    texte = re.sub(r"\S+@\S+", " EMAIL ", texte)
    texte = unicodedata.normalize("NFKC", texte)
    texte = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", " ", texte)
    texte = re.sub(r"\d+", " NOMBRE ", texte)
    texte = re.sub(r"\s+", " ", texte).strip()
    return texte

def mots(texte):
    return nettoyer(texte).split()

# ------------------------------------------------------------
# APPRENTISSAGE NAIVE BAYES
# ------------------------------------------------------------
class DetecteurSpam:
    def __init__(self, spam, non_spam):
        self.spam = spam
        self.non_spam = non_spam
        self.nb_spam = Counter()
        self.nb_normal = Counter()
        self.n_spam = 0
        self.n_normal = 0
        self.vocabulaire = set()
        self.total_spam = 0
        self.total_normal = 0
        self.train()

    def train(self):
        # seed fixe = résultats reproductibles
        data = [(x, "spam") for x in self.spam] + [(x, "non_spam") for x in self.non_spam]
        random.Random(42).shuffle(data)

        for texte, classe in data:
            tokens = mots(texte)
            self.vocabulaire.update(tokens)
            if classe == "spam":
                self.n_spam += 1
                self.nb_spam.update(tokens)
            else:
                self.n_normal += 1
                self.nb_normal.update(tokens)

        self.total_spam = sum(self.nb_spam.values())
        self.total_normal = sum(self.nb_normal.values())

    def _log_prob(self, tokens, classe):
        # Laplace smoothing.
        alpha = 1.0
        vocab = max(1, len(self.vocabulaire))

        if classe == "spam":
            compte = self.nb_spam
            total = self.total_spam
            classe_n = self.n_spam
        else:
            compte = self.nb_normal
            total = self.total_normal
            classe_n = self.n_normal

        prior = classe_n / max(1, self.n_spam + self.n_normal)
        score = math.log(max(prior, 1e-12))

        denom = total + alpha * vocab
        for mot in tokens:
            score += math.log((compte.get(mot, 0) + alpha) / denom)

        return score

    def predire(self, texte):
        tokens = mots(texte)

        if not tokens:
            return "non_spam", 50.0, 50.0

        s_spam = self._log_prob(tokens, "spam")
        s_normal = self._log_prob(tokens, "non_spam")

        # Conversion stable des scores logarithmiques en probabilités.
        m = max(s_spam, s_normal)
        e_spam = math.exp(s_spam - m)
        e_normal = math.exp(s_normal - m)
        total = e_spam + e_normal

        p_spam = e_spam / total * 100
        p_normal = e_normal / total * 100

        if p_spam >= p_normal:
            return "spam", p_spam, p_normal
        return "non_spam", p_spam, p_normal

    def analyser(self, texte):
        resultat, p_spam, p_normal = self.predire(texte)
        return {
            "resultat": resultat,
            "spam": p_spam,
            "non_spam": p_normal,
            "mots": len(mots(texte)),
            "confiance": max(p_spam, p_normal),
        }

# ------------------------------------------------------------
# ÉVALUATION SIMPLE
# ------------------------------------------------------------
def evaluation(modele):
    data = [(x, "spam") for x in SPAM] + [(x, "non_spam") for x in NON_SPAM]
    rnd = random.Random(42)
    rnd.shuffle(data)

    split = int(len(data) * 0.80)
    test = data[split:]

    if not test:
        return 0.0, 0, 0

    correct = 0
    for texte, vraie in test:
        pred, _, _ = modele.predire(texte)
        if pred == vraie:
            correct += 1

    return correct / len(test) * 100, len(test), correct

# ------------------------------------------------------------
# INTERFACE GRAPHIQUE ANDROID / PYDROID 3
# ------------------------------------------------------------
# Kivy est optionnel. Le moteur fonctionne sans Kivy.
# Sur PyDroid 3, installer Kivy depuis Pydroid repository
# si vous voulez l'interface graphique.

def lancer_interface():
    try:
        from kivy.app import App
        from kivy.metrics import dp
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.label import Label
        from kivy.uix.textinput import TextInput
        from kivy.uix.scrollview import ScrollView
        from kivy.graphics import Color, RoundedRectangle
    except ImportError:
        print("\nKivy n'est pas installé.")
        print("Le moteur fonctionne quand même.")
        print("Pour l'interface Android, installez Kivy dans PyDroid 3.")
        lancer_mode_console()
        return

    modele = DetecteurSpam(SPAM, NON_SPAM)
    precision, ntest, correct = evaluation(modele)

    class Fond(BoxLayout):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            with self.canvas.before:
                Color(0.96, 0.97, 0.99, 1)
                self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
            self.bind(pos=self._update_rect, size=self._update_rect)

        def _update_rect(self, *args):
            self.rect.pos = self.pos
            self.rect.size = self.size

    class SpamApp(App):
        def build(self):
            self.title = "Détecteur de Spam"
            root = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(10))

            title = Label(
                text="🛡️ DÉTECTEUR DE SPAM",
                font_size=dp(24),
                bold=True,
                size_hint_y=None,
                height=dp(55),
                color=(0.08, 0.10, 0.16, 1)
            )
            root.add_widget(title)

            subtitle = Label(
                text="Analyse locale • Gratuit • Sans Internet",
                font_size=dp(14),
                size_hint_y=None,
                height=dp(30),
                color=(0.25, 0.28, 0.34, 1)
            )
            root.add_widget(subtitle)

            self.input = TextInput(
                hint_text="Écrivez ou collez votre message ici...",
                multiline=True,
                font_size=dp(18),
                padding=[dp(12), dp(12)],
                size_hint_y=None,
                height=dp(180)
            )
            root.add_widget(self.input)

            buttons = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))

            analyse = Button(
                text="🔎 ANALYSER",
                font_size=dp(17),
                bold=True
            )
            effacer = Button(
                text="🧹 EFFACER",
                font_size=dp(17)
            )

            buttons.add_widget(analyse)
            buttons.add_widget(effacer)
            root.add_widget(buttons)

            self.resultat = Label(
                text="Résultat : en attente...",
                font_size=dp(20),
                bold=True,
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=dp(90),
                color=(0.08, 0.10, 0.16, 1)
            )
            self.resultat.bind(size=self._wrap_label)
            root.add_widget(self.resultat)

            scroll = ScrollView()
            self.details = Label(
                text="Entrez un message puis appuyez sur ANALYSER.",
                font_size=dp(16),
                halign="left",
                valign="top",
                size_hint_y=None
            )
            self.details.bind(texture_size=self._details_height)
            scroll.add_widget(self.details)
            root.add_widget(scroll)

            stats = Label(
                text=f"Modèle : Naive Bayes local | Test : {precision:.1f}% "
                     f"({correct}/{ntest}) | {len(SPAM)+len(NON_SPAM)} messages",
                font_size=dp(12),
                size_hint_y=None,
                height=dp(35),
                color=(0.30, 0.32, 0.38, 1)
            )
            root.add_widget(stats)

            analyse.bind(on_press=self.analyser)
            effacer.bind(on_press=self.effacer)

            return root

        def _wrap_label(self, instance, value):
            instance.text_size = (instance.width - dp(10), instance.height)

        def _details_height(self, instance, value):
            instance.height = max(dp(80), value[1] + dp(10))
            instance.text_size = (self.details.width - dp(10), None)

        def analyser(self, *args):
            texte = self.input.text.strip()

            if not texte:
                self.resultat.text = "⚠️ Écrivez un message."
                self.details.text = "Aucun texte à analyser."
                return

            r = modele.analyser(texte)

            if r["resultat"] == "spam":
                self.resultat.text = "🚨 SPAM DÉTECTÉ"
            else:
                self.resultat.text = "✅ NON-SPAM"

            self.details.text = (
                f"Probabilité spam : {r['spam']:.1f}%\n"
                f"Probabilité non-spam : {r['non_spam']:.1f}%\n"
                f"Confiance du modèle : {r['confiance']:.1f}%\n"
                f"Nombre de mots analysés : {r['mots']}\n\n"
                "ℹ️ Ce résultat est une estimation automatique."
            )

        def effacer(self, *args):
            self.input.text = ""
            self.resultat.text = "Résultat : en attente..."
            self.details.text = "Entrez un message puis appuyez sur ANALYSER."

    SpamApp().run()

# ------------------------------------------------------------
# MODE CONSOLE DE SECOURS
# ------------------------------------------------------------
def lancer_mode_console():
    modele = DetecteurSpam(SPAM, NON_SPAM)
    print("\n=== DÉTECTEUR DE SPAM ===")
    print("Tapez 'quitter' pour arrêter.\n")

    while True:
        texte = input("Message : ").strip()
        if texte.lower() == "quitter":
            break

        r = modele.analyser(texte)
        print(
            f">>> {r['resultat'].upper()} | "
            f"spam={r['spam']:.1f}% | non-spam={r['non_spam']:.1f}%"
        )

if __name__ == "__main__":
    lancer_interface()
