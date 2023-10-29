#!/usr/bin/env python3

import requests
from abc import ABC, abstractmethod

from json import dumps
from datetime import datetime, date

MONTHS = {
    "janvier": "January",
    "février": "February",
    "mars": "March",
    "avril": "April",
    "mai": "May",
    "juin": "June",
    "juillet": "July",
    "août": "August",
    "septembre": "September",
    "octobre": "October",
    "novembre": "November",
    "décembre": "December",
}

class PageParser(ABC):

    def __init__(self, **kwargs) -> None:
        self.event = []
        self.logger = kwargs.get('logger')
        self.url = kwargs.get('url')
        self.min_date = kwargs.get('start_date')
        self.max_date = kwargs.get('end_date')

    @abstractmethod
    def get_event(self):
        pass

    def check_date(self, date_event):
        """ Check if the date is in the range """
        date_trim = date_event
        for month in MONTHS:
            if month in date_event:
                date_trim = date_event.replace(month, MONTHS[month])
                break
        datetime_obj = datetime.strptime(date_trim, "%d %B %Y")
        date_event = date(
            datetime_obj.year,
            datetime_obj.month,
            datetime_obj.day
        )
        if date_event < self.min_date:
            return 1
        if date_event >= self.max_date:
            return -1
        return 0
    
    def send_request(self, url):
        """ Send a request to the url and return the content """
        resp = requests.get(url)
        if resp.status_code != 200:
            return resp.status_code
        
        return resp.content.decode('utf-8')
