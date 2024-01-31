# Parametre

## Paramètre globale

- `lang`(obligatoire): langue cible utilisé pour le traducteur

Exemple:
```json
{
    "lang": "fr"
}
```

## Template

- `path` (obligatoire) :  chemins des templates
- `data` (obligatoire) : données du templates
    - `title` (obligatoire):  titre du document
    - `author` (obligatoire) : auteur du document

Exemple:
```json
"template":{
    "path":[ 
        "cert_bulletin_gen/templates/main.tex",
        "cert_bulletin_gen/templates/events/event.tex"
    ],
    "data": {
        "title":"Bulletin de veille semaine $week$",
        "author":"Cert bulletin generator"
    }
}
```

## Parser

Configuration des différents Parser.

Un parseur doit avoir le même nom que le *nom.py* du parser.

- `template_name`(obligatoire): nom du template à utiliser
- `url` (obligatoire) : liste des urls à utiliser
- `title` (obligatoire) : nom du cert
- `description`  (obligatoire): description du cert
- ext (optionel): extension des urls pour effectuer d'autres recherches

exemple pour **Certfr** et **cyware**:
```json
"parser":{
    "certfr":{
        "template_name": "cert",
        "url":[
            "https://www.cert.ssi.gouv.fr/alerte/",
            "https://www.cert.ssi.gouv.fr/avis/"
        ],
        "ext": "page",
        "title":"CERT-FR",
        "description":"Centre gouvernemental de veille, d'alerte et de réponse aux attaques informatiques"
    },
     "cyware":{
            "template_name":"rss",
            "url":[
                "https://cyware.com/allnews/feed"
            ],
            "title":"Cyware",
            "description":"Cyware is the industry's only Virtual Cyber Fusion platform provider, offering secure collaboration, threat intelligence sharing, and integrated solutions to seamlessly fuse intelligence across the cybersecurity ecosystem"
        }
}
```

## Timeframe

Paramétrage deA l'intervalle temporel de CVE à mettre dans le bulletin
```json
"timeframe": {
    "range": "week",
    "begin": "friday"
}
```
### Range

l'option `range` est obligatoire, elle spécifie l'intervalle temporel relatif
choix disponible:
- week: toutes les semaines
- month: tous les mois (pas encore opérationnel)
- year: tous les ans (pas encore opérationnel)

Exemple:
```json
"timeframe": {
    "range": "week",
    "begin": "friday"
}
```

## Output

Configuration de la sortie des livrables.

- `path`: chemin du repertoire de sortie
- `name` (optionel): nom du fichier de sortie

configuration par défaut:
```json
"output":{
    "path": "cert_bulletin_gen/aout",
    "name": "nom de fichier"
}
```
