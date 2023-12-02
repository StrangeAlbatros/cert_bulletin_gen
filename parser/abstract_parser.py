#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from datetime import datetime, date

from cert_bulletin_gen.logger import LOGGER

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

class AbstractParser(ABC):

    def __init__(self, **kwargs) -> None:
        self.events = []
        self.min_date = kwargs.get('start_date') # min date of the range
        self.max_date = kwargs.get('end_date') # max date of the range

    @property
    def events(self):
        """ Get the events """
        return self._events
    
    @events.setter
    def events(self, events):
        """ Set the events """
        if not isinstance(events, list):
            raise TypeError("events must be a list")

        self._events = events

    def check_date(self, date_event):
        """ Check if the date is in the range (like compare to)"""
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
        if date_event <= self.min_date:
            return 1
        if date_event > self.max_date:
            return -1
        return 0