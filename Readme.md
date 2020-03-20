# Claims checking

Extraction et structuration d'informations venant de quelques site web de fact-checking

## À propos du projet

Les fausses nouvelles (fake news) sont devenues un problème de plus en plus important, tant du point de vue de la société que de celui de la recherche. Le [LIRMM](http://www.lirmm.fr/ "Laboratoire d’Informatique, de Robotique et de Microélectronique de Montpellier") en collaboration avec 2 équipes allemandes a construit et mis à disposition la base de connaissance ClaimsKG qui recueillit les informations et méta-données provenant d’un grand nombre de sites journalistiques de fact checking. Le sujet de ce projet consiste en l’enrichissement de cette base de connaissances avec des nouvelles données provenant des sites web suivants (liste soumise à évolution) :

- [Vishvas.news](https://www.vishvasnews.com/english/) ~~> Un site Internet de vérification des faits multilingue (en hindi, anglais ...) qui s'engage à combattre la désinformation et les informations erronées.
- [Fatabyyano](https://fatabyyano.net/) ~~> Jordani, en Arabe, Fatabyyano ("فتبينوا" veut dire "Alors montrez-le" en arabe) est la première et la seule plateforme arabe certifiée par l'[IFCN](https://ifcncodeofprinciples.poynter.org/).

### Prérequis

#### Python

Vous devez avoir Python3 installer sur votre machine

```
# On ubuntu for example
sudo apt install python3 python3-pip

```

#### Yandex translator API

Avoir une clé api yandex pour la traduction

```
google it
```

#### TagMe API

Avoir une clé api TagMe pour extraire les entités

```
google it
```

### Installation

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```

# install all python requirements
pip3 install -r requirements.txt

python3 __init__.py

```

End with an example of getting some data out of the system or using it for a little demo

## Technologie utilisée

- [Python](https://www.python.org/) - The principal language
- [Beautiful Soup](https://fr.wikipedia.org/wiki/Beautiful_Soup) - Python package for parsing HTML and XML documents
- [Yandex translator](http://translate.yandex.com/) - The translation is Powered by Yandex.Translate
- [TagMe](https://sobigdata.d4science.org/web/tagme/tagme-help) - A powerful tool that identifies on-the-fly meaningful substrings (called "spots") in an unstructured text and link each of them to a pertinent Wikipedia page in an efficient and effective way
- [Python TagMe api](https://github.com/marcocor/tagme-python) - TagMe API wrapper for Python

## Auteurs

- **Bouzidi Belkassim** ~~> [BOuzidiBElkassim](https://github.com/BOuzidiBElkassim)
- **Elhouiti Chakib** ~~> [chakibreds](https://github.com/chakibreds/)
- **Kezzoul Massili** ~~> [massyKezzoul](https://github.com/massykezzoul)
- **Nedjari Abdelkader** ~~> [abdelkader-nedjari](https://github.com/nedjariabdelkader)
- **Zeroual Ramzi** ~~> [RamziZer](https://github.com/RamziZer)

* Encadrement : **Konstantin Todorov** ​[todorov@lirmm.fr​](mailto:todorov@lirmm.fr​)

## Remerciements

- Hat tip to anyone whose code was used
- Inspiration
- etc
