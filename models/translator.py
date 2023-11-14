#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from deep_translator import GoogleTranslator

class Translator:
    """ Translate the text with Google translate """
    def __init__(self, **kwargs) -> None:
        self.conf =kwargs.get('conf')
        self.logger = kwargs.get('logger')
        self.tr = GoogleTranslator(
            source='auto',
            target=kwargs.get('lang', 'fr')
        )

    def translate(self, text):
        """ translate the text """
        if type(text) == str:
            return self.tr.translate(text)
        elif type(text) == list:
            return [self.tr.translate(t) for t in text]
        else:
            raise Exception(f"Not supported type, must be str or list not {type(text)}")