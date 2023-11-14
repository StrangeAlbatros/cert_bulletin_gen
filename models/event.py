#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from re import findall

class Event:

    def __init__(self, **kwargs) -> None:
        self.type = kwargs.get('type', "Alerte")

        self.subject = kwargs.get("objet")
        self.metadata = {
            "Référence": kwargs.get('référence'),
            "Titre": kwargs.get('titre'),
            "Date de la première version": kwargs.get('date_de_la_première_version'),
            "Date de la dernière version": kwargs.get('date_de_la_dernière_version', None),
            'Source(s)': kwargs.get('source(s)', None),
        }
        # h2 tags
        self.risks = kwargs.get('risque(s)', [])
        self.system_affected = kwargs.get('systèmes_affectés', [])
        self.resume = kwargs.get('résumé')
        self.solutions = kwargs.get('solution', [])
        self.documentations = kwargs.get('documentation', [])
        self.detal_doc_manage = kwargs.get('gestion_détaillée_du_document', {})

    @classmethod
    def from_certfr(cls, html, type='Alerte'):
        """ Create an alert from bs4.element.tag html"""
        # h2 is all informations in the h2 tags
        h2 = {
            "ul": [
                "Risque(s)",
                "Systèmes affectés",
                "Documentation"
            ],
            "ol": ["Gestion détaillée du document"],
            "p":[
                "Solution",
                "Résumé"
            ]
        }
        # metadata
        args = {"type":type}
        tmp = html.find('table', {'class': 'table table-condensed'}).get_text().split('\n')
        tmp = [data.lower() for data in tmp if data]

        for i in range(0, len(tmp)-1, 2):
            args[tmp[i].replace(" ", "_")] = tmp[i+1]

        args['objet'] = html.find('h1').get_text().strip("Objet: ")

        for type,lst_title in h2.items():
            for title in lst_title:
                h2_tags = html.find_all('h2', string=title)
                if not h2_tags:
                    continue
                title = title.lower().replace(" ", "_")
                if type == 'ul' or type == 'ol':
                    args[title] = [ 
                        elt for elt in h2_tags[0].find_next(type).get_text().replace("\u00e0", "\n").split('\n') if elt
                    ]
                elif type == 'p':
                    args[title] = h2_tags[0].find_next(type).get_text()

        args['systèmes_affectés'] = args['systèmes_affectés'][0].split('-')
        return cls(**args)
    
    def latex_support_format(self):
        """ Return a dict with the latex support format """
        latex_format = self.__dict__().copy()
        #TODO fair la meme chose en mieu
        ind = 0
        for doc in self.documentations:
            urls = findall(r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))", doc)
            for url in urls:
                latex_format['documentations'][ind] = doc.replace(url[0], str(r"\url{" + url[0] + "}"))
            ind  += 1

        # remove some unicode caracter
        latex_format['system_affected'] = self.remove_unicode(self.system_affected)
        latex_format['system_affected'] = [ elt.replace("_", "\_") for elt in latex_format['system_affected'] ]

        # remove empty item (bug with parser)
        if latex_format['documentations'][-1] == " ":
            latex_format['documentations'].pop(-1)

        return latex_format
    
    def remove_unicode(self, list_str):
        """ Remove unicode caracter from a list of string """
        return [ elt.encode("utf-8").decode().replace(" ", ' ').replace(' ', ' ')  for elt in list_str if elt]
    
    def __dict__(self):
        """ Return a dict with all the attributes """
        return {
            "subject": self.subject,
            "metadata": self.metadata,
            "risks": self.risks,
            "system_affected": self.system_affected,
            "resume": self.resume,
            "solutions": self.solutions,
            "documentations": self.documentations,
            "detal_doc_manage": self.detal_doc_manage,
        }