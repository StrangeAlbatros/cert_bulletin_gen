# Flux RSS

<img src="./img/rss_feed.png" width="300">

# Scraper

Le repertoire par défaut des lecteur de flux rss est:  `cert_bulletin_gen/parser/scraper`

## RssParser

[RssParser](../parser/rss_parser.py)

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
```

Les evenement doivent être stocker dans herité de PageParser `self.events` qui est une liste d'event.

Les objet **RssEvent** sont prévu pour stocker des information de flux rss.

lien de du fichier python de [RssEvent](../models/rss_event.py)

### 2. Modification __init__.py

Il faut maintenant modifier le fichier `cert_bulletin_gen/parser/__init__.py`.

### 3. Ajout dans le fichier de configuration

Un parseur doit avoir le même nom que le *nom.py* du parser.

- `template_name`(obligatoire): nom du template à utilisé
- `url` (obligatoire) : liste des urls à utiliser
- `title` (obligatoire) : nom du cert
- `description`  (obligatoire): description du cert
- ext (optionel): extension des urls pour effectuer d'autres recherches

```json
    "parser":{
        "cyware":{
            "translate": true,
            "template_name":"rss",
            "url":[
                "https://cyware.com/allnews/feed"
            ],
            "title":"Cyware",
            "description":"Cyware is the industry's only Virtual Cyber Fusion platform provider, offering secure collaboration, threat intelligence sharing, and integrated solutions to seamlessly fuse intelligence across the cybersecurity ecosystem"
        },
        "customparser":{
            "template_name": "mon template",
            "url":[
                "mon_url"
            ],
            "title": "Custom Parser",
            "description": "Une description"
        }
    }
```