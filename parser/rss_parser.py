#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .abstract_parser import AbstractParser

import requests
import feedparser

class RssParser(AbstractParser):

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.data = []
        self.logger = kwargs.get('logger')
        self.url = kwargs.get('url')
        self.min_date = kwargs.get('start_date')
        self.max_date = kwargs.get('end_date')

        self.parse_url()

    def parse_url(self):
        """ Parse the url and return the content """
        for url in self.url:
            feed_content = requests.get(url)
            feed = feedparser.parse(feed_content.text)
            self.data.append(feed)