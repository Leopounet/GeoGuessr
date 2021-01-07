# GeoGuessr challenge generator

With this simple app you can generate as many GeoGuessr challenges as you want (given you have a premium account).

## Dependencies

Python:
- Version >= 3.6
- Discord `pip3 install discord`
- Selenium `pip3 install selenium`
- [geckodiver](https://github.com/mozilla/geckodriver/releases) somewhere in your path (for example /usr/bin)

Discord:
- An [app](https://discord.com/developers/applications) (and a bot).
- A server ready to welcome your Bot.

GeoGuessr:
- A premium account (only 25€/yr).

Documentation (optional):
- sphinx `pip3 install sphinx`
- a nice theme `pip3 install sphinx_rtd_theme`

To generate the documentation type `make doc` at the root of the project.

## Commands

A command is the combination of two methods `handle` and `usage` (see CommandExample.py).
To add a new command, add a new `MyCommand.py` in the commands directory with the same format
as the one described in CommandExample.py.

## Issues

### Properly setting your bot TOKEN

In `BotGeoguessr.py` you can find a line reading `TOKEN = os.environ["GEOGUESSR_TOKEN"]`. 
For this line to make any sense, you have to have an environment variable with this name.
If you don't want to use an environment variable, just set `TOKEN = "your_token"`. You can find it
[here](https://discord.com/developers/applications).

### Linking your GeoGuessr account

In `Utils.py` there are two lines `mail = os.environ["MAIL"]` and `password = os.environ["PASSWD"]`.
Same idea as with the TOKEN, either set environment variables, or just replace both fields with both your
mail and password.

### Browsing context has been discarded

If you ever encounter this error, reboot the bot and wait a bit (like 30 seconds) before using it.

### Another issue?

Make sure everything is up-to-date and then raise it!

# Générateur de challenges GeoGuessr

Permet de générer facilement des parties GeoGuessr (nécessite GeoGuessr premium).

## Dépendances

Python:
- Version >= 3.6
- Discord `pip3 install discord`
- Selenium `pip3 install selenium`

Discord:
- Une [application](https://discord.com/developers/applications) (et un bot).
- Un serveur pour l'utiliser.

GeoGuessr:
- Un compte premium.

Documentation:
- sphinx `pip3 install sphinx`
- un thème sympa `pip3 install sphinx_rtd_theme`

Pour générer la documentation `make doc` à la racine du projet.

## Commandes

Une commande est la combinaison d'une fonction `handle` et d'une fonction `usage` (voir CommandExample.py).
Pour ajouter une nouvelle commande il suffit de créer un fichier `MyCommand.py` dans le dossier commands en
respectant le format donné dans CommandExample.py.

## Problèmes

### Définir son TOKEN

Dans `BotGeoguessr.py` il y a la ligne `TOKEN = os.environ["GEOGUESSR_TOKEN"]`. 
Pour qu'elle fonctionne il faut créer une variable d'environement avec ce nom.
Si vous ne voulez pas utiliser de variables d'environement, remplacez la ligne par
`TOKEN = "your_token"`. Votre TOKEN se trouve [ici](https://discord.com/developers/applications).

### Lier votre compte geoGuessr

Dans `Utils.py` il ya ces deux lignes `mail = os.environ["MAIL"]` et `password = os.environ["PASSWD"]`.
Comme pour le TOKEN, soit définissez des variables d'environement, ou remplacez les deux champs par votre 
mail et votre mot de passe.

### Browsing context has been discarded

Si vous avez cette erreur, relancez le bot et attendez quelques secondes avant de l'utiliser (~30 secondes).

### Un autre problème?

Assurez-vous que tout est à jour puis signalez le!