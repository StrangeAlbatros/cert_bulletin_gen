#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, GuessedAtParserWarning

import warnings

from ..page_parser import PageParser
from cert_bulletin_gen.models import Event

from cert_bulletin_gen.logger import LOGGER

class Certfr(PageParser):
    """ Parse the certfr bulletin """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        warnings.filterwarnings("ignore", category=GuessedAtParserWarning, module='bs4')
        self.urls = kwargs.get('url')
        self.ind_page = 1
        self.ext = kwargs.get('ext') # extension of the url for the next page
        self.events = []
        self.start_treament()

    def start_treament(self):
        """ Start the treatment """
        LOGGER.info("Start treatment of certfr")
        for url in self.urls:
            content = self.send_request(url)

            # if centent is int, 
            # it means that the date is not in the range
            if isinstance(content, int):
                continue

            # get all cve from the first page
            all_cve = []
            if "avis" in url:
                all_cve = self.main_page(content, type="avis")
            else:
                all_cve = self.main_page(content, type="alerte")
            
            # if all_cve is 1, it means that the date is not in the range 
            # (date is too old)
            while all_cve !=1 :
                # get all cve from the next page
                research = self.main_page(
                    self.send_request(self.next_page(url))
                )
                if research == 0:
                    break
                all_cve.extend(research)
            
            if isinstance(all_cve, int):
                LOGGER.warning(f"No events found for: {url}")
                continue
            for cve in all_cve:
                LOGGER.debug(f"Treatment of {cve}")
                r_data = self.send_request(
                    f"{url}{cve}"
                )
                if r_data != 404 or 403:
                    self.events.append(self.get_event(r_data))

            self.ind_page = 1

        if self.events:
            LOGGER.debug(f"{len(self.events)} event(s) found for certfr")
        else:
            LOGGER.warning("No events found for certfr")
        LOGGER.info("End treatment of certfr")

    def next_page(self, url):
        """ Return the next page with the extension """
        self.ind_page += 1
        return f"{url}{self.ext}/{self.ind_page}/"

    def main_page(self, data, **kwargs):
        """ Parse the main page of the bulletin """
        all_cve = []

        soup = BeautifulSoup(data, "html.parser", from_encoding="utf-8")

        if kwargs.get("type", "alerte") == "alerte":
            articles = soup.find_all("article", {'class':'cert-alert'})
        else:
            articles = soup.find_all("article", {'class':'cert-avis'})  

        check_date = 0  
        for article in articles:
            # Find the publication date
            pub_date = article.find('span', class_='item-date').text.strip()
            pub_date = pub_date.replace('Publié le ', '')
            # Check if the publication date is in the range
            check_date = self.check_date(pub_date)
            if check_date == 0 :
                # Find the CVE URL
                cve_url = article.find('a', href=True)
                if cve_url:
                    all_cve.append(cve_url['href'].replace('/alerte/', '').replace('/avis/', ''))
            elif check_date == 1:
                break

        return all_cve if all_cve else check_date


    def get_event(self, data, **kwargs):
        """ Parse the alert page """
        soup = BeautifulSoup(data, "html.parser", from_encoding="utf-8")
        content = soup.find('div', {'class' : 'content'})
        return Event.from_certfr(content)