#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ..rss_parser import RssParser

from cert_bulletin_gen.models import RssEvent

from json import dumps
from bs4 import BeautifulSoup

class Cyware(RssParser):
    """ Parse the Cyware RSS feed """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.translate = kwargs.get('translate', False)
        self.translator = kwargs.get('translator', None)
        if self.translate and self.translator:
            self.logger.info("Translation enabled for Cyware RSS feed")

        self.start_treament()

    def start_treament(self):
        """ Start the treatment of the RSS feed """
        for entry in [ elt.entries for elt in  self.data]:
            for event in entry:
                self.events.append(self.get_event(event))

        if self.events:
            self.logger.success(f"{len(self.events)} event(s) found in Cyware RSS feed")
        else:
            self.logger.info("No events found in the RSS feed")

    def get_event(self, element):
        """ parse one rss event """
        summary = BeautifulSoup(element.summary, "html.parser", from_encoding="utf-8").get_text().split("\n")
        summary = [ line.strip() for line in summary if line.strip() ]

        title = element.title

        # Translate the event
        if self.translate and self.translator:
            summary = [ self.translator.translate(line) for line in summary ]
            title = self.translator.translate(title)

        return RssEvent.from_feedparser(
            data=summary,
            title=title,
            link=element.link,
            published=element.published
        )