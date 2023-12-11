# cert bulletin gennerator

[![made-with-python](https://img.shields.io/badge/Made%20with-Python%203.10-1f425f.svg?logo=python)](https://www.python.org/)
![GitHub License](https://img.shields.io/github/license/StrangeAlbatros/cert_bulletin_gen)
![GitHub repo size](https://img.shields.io/github/repo-size/StrangeAlbatros/cert_bulletin_gen)

![img certfr](./doc/img/certfr_full_logo.png)

Application qui génère un bulletin de veille informatique à partir des alertes du [certfr](https://www.cert.ssi.gouv.fr/alerte/)

---

## Sommaire

[1. Specification technique](#1-specification-technique)

[2. Installation](#2-installation)

[3. Paramétrage](#3-paramétrage)

[4. Utilisation](#4-utilisation)

---

## 1. Specification technique

### Support

- Linux
- MacOS X

### Prérequis

- latex
- python

#### Linux debian like

```
sudo apt install -y python3 texlive texlive-formats-extra texlive-lang-french
```
#### Linux red hat like
```
sudo yum install -y python3 texlive texlive-formats-extra texlive-lang-french
```

## 2. Installation

### Linux
```
python3 -m venv .venv
source .venv
pip3 install -r requirements.txt
```
## 3. Paramétrage

Pour la configuration allez sur la [documention de paramètre](./doc/setting.MD)

## 4. Utilisation
Ce situer dans le dossier parent de la racine de cert_bulletin_gen.
```
python3 -m cert_bulletin_gen
```

```
usage: Cert Bulletin Generator [-h] [-c CONFIG] [--no-compil] [-v] [--pdf-name PDF_NAME] [--version]

Generate a bulletin of vulnerabilities from cert

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config file
  --no-compil           no latex compilation, only latex file generation
  -v, --verbose         Increase output verbosity
  --pdf-name PDF_NAME   name of the pdf file
  --version             show program's version number and exit

An application wich generate a bulletin of vulnerabilities from cert
```
