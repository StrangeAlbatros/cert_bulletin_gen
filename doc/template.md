# Templates

Les templates sont aux format **LaTeX** dans le repertoire `cert_bulletin_gen/templates`

## Fichier report.tex

`report.tex` est le fichier principale du template.

Voici les structures des données injecter sous forme de dictionnaire dans le template :

- content
    - title : titre du rapport
    - author: auteur du rapport
    - chapters: chapitre du documents

## Fichiers secondaires

Les autres fichier sont les chapitre du document **LaTeX**


Voici les structures des données injecter sous forme de dictionnaire dans le template :

- content
    - title : titre du chapitre
    - events : list de CVE
        - subject: nom de la CVE
        - riks: liste de risques de la CVE
        - system_affected: liste des système affecttés
        - resume: résumé de la CVE
        - solutions: solution de la CVE
        - documentations: liste des documentations
        - etal_doc_manage: gestion détaillé de la CVE