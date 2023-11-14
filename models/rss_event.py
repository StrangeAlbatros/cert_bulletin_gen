#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class RssEvent:
    """ Represent a RSS event """
    def __init__(self, **kwargs) -> None:
        self.data = kwargs.get('data')
        self.title = kwargs.get('title')
        self.link = kwargs.get('link', [])
        self.published = kwargs.get('published', None)

    @classmethod
    def from_feedparser(cls, **kwargs):
        """ Create an RssEvent from feedparser entry """
        return cls(
            data = kwargs.get('data'),
            title = kwargs.get('title'),
            link = kwargs.get('link', []),
            published = kwargs.get('published', None)
        )
    
    def latex_support_format(self):
        """ Return the latex format of the events """
        latex_format = self.__dict__()
        latex_format['data'] = self.remove_unicode(latex_format['data'])
        # manage the link
        latex_format['link'] =  str(r"\url{" + latex_format['link'] + "}")

        return latex_format

    def remove_unicode(self, list_str):
        """ Remove unicode caracter from a list of string """
        return [ elt.encode("utf-8").decode().replace("​​​​", ' ')  for elt in list_str if elt]

    def __dict__(self) -> str:
        """ Return a dict of the object """
        return {
            "data": self.data,
            "title": self.title,
            "link": self.link,
            "published": self.published
        }