# Parametre

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

- `url` (obligatoire) : liste des urls à utiliser
- `title` (obligatoire) : nom du cert
- `description`  (obligatoire): description du cert
- ext (optionel): extension des urls pour effectuer d'autres recherches

exemple pour Certfr:
```json
"parser":{
    "certfr":{
        "url":[
            "https://www.cert.ssi.gouv.fr/alerte/",
            "https://www.cert.ssi.gouv.fr/avis/"
        ],
        "ext": "page",
        "title":"CERT-FR",
        "description":"Centre gouvernemental de veille, d'alerte et de réponse aux attaques informatiques"
    }
}
```

## Timeframe

Paramétrage des l'intervalle temporel de CVE à mettre dans le bulletin
```json
"timeframe": {
    "range": "week",
    "begin": "friday"
}
```
### Range

l'option `range` est obligatoire pour spécifer que l'intervalle temporel est realtif
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

### begin and end date

format YYYY-MM-DD

pas encore fait

## Output

Configuration de la sortie des livrables.

configuration par défaut:
```json
"output":{
    "path": "cert_bulletin_gen/aout"
}
```