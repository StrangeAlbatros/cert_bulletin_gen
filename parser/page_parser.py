#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

from .abstract_parser import AbstractParser

class PageParser(AbstractParser):

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.url = kwargs.get('url')
    
    def send_request(self, url):
        """ Send a request to the url and return the content """
        resp = requests.get(url)
        if resp.status_code != 200:
            return resp.status_code
        
        return resp.content.decode('utf-8')
