
# Jeu du Pendu avec BeeWare

Bienvenue dans le **jeu du pendu**, une application éducative et ludique développée avec le framework BeeWare. Ce projet met en avant des fonctionnalités interactives, des sons, une gestion d'affichage dynamique et la possibilité d'expliquer les mots joués via une WebView.

---

## Fonctionnalités

- **Jeu interactif** : Entrez des lettres pour deviner un mot secret choisi aléatoirement.
- **Affichage graphique** : Une potence s'affiche progressivement avec chaque mauvaise tentative.
- **Historique des lettres** : Visualisez les lettres déjà essayées.
- **Explication des mots** : Consultez une définition en ligne via une WebView intégrée.
- **Sons immersifs** : Sons différents pour les bonnes réponses, mauvaises réponses, et fin de partie (victoire ou défaite).

---

## Installation

### Prérequis
- Python 3.10 ou une version supérieure.
- BeeWare (Briefcase, Toga).
- Android Studio ou un environnement de développement Android (pour les builds mobiles).

### Étapes
1. Clonez le projet :
   ```
   git clone git@github.com:kattouba/pendu.git
   cd pendu
   ```

2. Installez les dépendances BeeWare :
   ```
   pip install briefcase
   ```

3. Exécutez le projet en local :
   ```
   briefcase dev
   ```

---

## Build pour Android

Pour générer une version mobile de l'application :
1. Configurez les dépendances Android avec Briefcase :
   ```
   briefcase create android
   ```

2. Compilez le projet :
   ```
   briefcase build android
   ```

3. Installez et exécutez sur un appareil connecté ou un émulateur :
   ```
   briefcase run android
   ```

---

## Contributeurs

**Créateur** : Le Studio **KATEB & Papa**  
📧 Email : [kateb.et.papa@zohomail.com](mailto:kateb.et.papa@zohomail.com)  

Contributions, idées et retours sont les bienvenus !

---

## Licence

Ce projet est sous licence **GNU General Public License v2.0**. Consultez le fichier `LICENSE` pour plus d'informations.

---

## Capture d'écran

![Aperçu du jeu du pendu](resources/pendu_etape10.png)

---

## Remerciements

Un grand merci à la communauté BeeWare pour son excellent framework facilitant le développement multiplateforme.
