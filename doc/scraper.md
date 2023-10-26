# Scraper

Le repertoire par défaut des scrapper est:  `cert_bulletin_gen/parser/scraper`

## PageParser

[PageParser](../parser/page_parser.py)

## Custom parser

- Un parser doit **obligatoirement hérité** de PageParser
- Doit **être importé** dans le fichier __init__.py de sont modules
- Doit avoir le **même nom** que dans le fichier de configuration

### 1. Python Parser

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..page_parser import PageParser
from cert_bulletin_gen.models import Event

class CustomParser(PageParser):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_event(self, data, **kwargs):
        """ Parse the alert page """
        return ...
```

### 2. Modification __init__.py

Il faut maintenant modifier le fichier `cert_bulletin_gen/parser/__init__.py`.

### 3. Ajout dans le fichier de configuration

Un parseur doit avoir le même nom que le *nom.py* du parser.

- `url` (obligatoire) : liste des urls à utiliser
- `title` (obligatoire) : nom du cert
- `description`  (obligatoire): description du cert
- ext (optionel): extension des urls pour effectuer d'autres recherches

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
        },
        "customparser":{
            "url":[
                "mon_url"
            ],
            "ext": "ext",
            "title": "Custom Parser",
            "description": "Une description"
        }
    }
```