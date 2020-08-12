# GeoGuessr challenge generator

With this simple app you can generate as many GeoGuessr challenges as you want (given you have a premium account).

## Dependencies

Python:
- Version >= 3.6
- Discord `pip3 install discord`
- Selenium `pip3 install selenium`

Discord:
- An [app](https://discord.com/developers/applications) (and a bot).
- A server ready to welcome your Bot.

GeoGuessr:
- A premium account (only 25€/yr).

## Commands

A command is the combination of two methods `handle` and `usage` (see cmdExample.py).
To add a new command, add a new `MyCommand.py` file, then add the file to the list of modules in
`BotGeoguessr.py` (don't forget to import your file!).

## Issues

### Properly setting your bot TOKEN

In `BotGeoguessr.py` you can find a line reading `TOKEN = os.environ["GEOGUESSR_TOKEN"]`. 
For this line to have any sense, you have to have an environment variable with this name.
If you don't want to use an environment variable, just set `TOKEN = "your_token"`. You can find it
[here](https://discord.com/developers/applications).

### Linking your GeoGuessr account

In `Generate.py` there are two lines `mail = os.environ["MAIL"]` and `password = os.environ["PASSWD"]`.
Same idea as with the TOKEN, either set environment variables, or just replace both fields with both your
mail and password.

### Documentation?

Nope, gl hf (to be fair this README is clear enough).

### Another issue?

Raise it!

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

## Commandes

Une commande est la combinaison d'une fonction `handle` et d'une fonction `usage` (voir cmdExample.py).
Pour ajouter une nouvelle commande il suffit de créer un fichier `MyCommand.py` et d'ajouter le fichier 
dans la liste de modules du fichier `BotGeoguessr.py` (pensez à importer le module!).

## Problèmes

### Définir son TOKEN

Dans `BotGeoguessr.py` il y a la ligne `TOKEN = os.environ["GEOGUESSR_TOKEN"]`. 
Pour qu'elle fonctionne il faut créer une variable d'environement avec ce nom.
Si vous ne voulez pas utiliser de variables d'environement, remplacez la ligne par
`TOKEN = "your_token"`. Votre TOKEN se trouve [ici](https://discord.com/developers/applications).

### Lié votre compte geoGuessr

Dans `Generate.py` il ya ces deux lignes `mail = os.environ["MAIL"]` et `password = os.environ["PASSWD"]`.
Comme pour le TOKEN, soit définissez des variables d'environement, ou remplacez les deux champs par votre 
mail et votre mot de passe.

### Documentation?

Non (le README est suffisament clair).

### Un autre problème?

Signalez le.