#!/usr/bin/env python3

from datetime import datetime
from json import dumps

from cert_bulletin_gen.utils import get_week_timeframe, get_month_timeframe, get_year_timeframe

DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

class Config:

    def __init__(self, **kwargs) -> None:
        self.output = kwargs.get("output")
        self.template = kwargs.get("template")
        self.timeframe = kwargs.get("timeframe")
        self.parser = kwargs.get("parser")

    @property
    def output(self):
        return self._output
    
    @output.setter
    def output(self, value):
        if not isinstance(value, dict):
            raise TypeError("Le parametre doit etre un dictionnaire")
        self._output = value

    @property
    def template(self):
        return self._template
    
    @template.setter
    def template(self, value):
        if not isinstance(value, dict):
            raise TypeError("Le parametre doit etre un dictionnaire")
        
        primary_keys = frozenset(["path", "data", "type"])

        if not primary_keys.issubset(value.keys()):
            raise KeyError("Il manque des cles dans le dictionnaire")
        
        if not isinstance(value['path'], dict):
            raise TypeError("Le parametre doit \"path\" etre une liste")
        
        sub_keys = frozenset(["title", "author"])

        if not sub_keys.issubset(value['data'].keys()):
            raise KeyError("Il manque des cles dans le dictionnaire")

        self._template = value

    @property
    def timeframe(self):
        return self._timeframe
    
    @timeframe.setter
    def timeframe(self, value):
        if not isinstance(value, dict):
            raise TypeError("Le parametre doit etre un dictionnaire")
        
        fixed_date = frozenset(["start", "end"])
        range_date = frozenset(["begin", "range"])

        if not fixed_date.issubset(value.keys()) and not range_date.issubset(value.keys()):
            raise KeyError("Il manque des cles dans le dictionnaire")
        
        self._timeframe = {}

        if value.get("start", None) and value.get("end", None):
            try:
                self._timeframe['start_date'] = datetime.strptime(value.get("start"), "%Y-%m-%d")
                self._timeframe['end_date'] = datetime.strptime(value.get("end"), "%Y-%m-%d")
            except ValueError:
                raise ValueError("Les dates doivent etre au format YYYY-MM-DD")
            
        if value.get("begin", None) and value.get("range", None):
            if value.get("range") not in ["day", "week", "month"]:
                raise ValueError("La valeur de \"range\" doit etre \"day\", \"week\" ou \"month\"")
            #TODO: ajouter la gestion des dates relatives
            if value.get("range") == "week":
                self._timeframe['start_date'], self._timeframe['end_date'] = get_week_timeframe(
                    DAYS.index(value.get("begin"))
                )
            elif value.get("range") == "month":
                #TODO : a faire
                pass
            elif value.get("range") == "year":
                #TODO : a faire
                pass
        
        if not self._timeframe:
            raise Exception("ERREUR: Impossible de charger la configuration")
        
        # update title
        self.parse_title(self.template['data']['title'])

    @property
    def parser(self):
        return self._parser
    
    @parser.setter
    def parser(self, value):
        if not isinstance(value, dict):
            raise TypeError("Le parametre doit etre un dictionnaire")
        
        #TODO: faire qqc de plus précis
        self._parser = value

    def parse_title(self, title):
        """ Parse the title """

        title_keywords = {
            "$week$": f"{self.timeframe['start_date']} au {self.timeframe['end_date']}",
            "$month$": f"{self.timeframe['start_date'].strftime('%B %Y')}",
            "$week_of_year$": f"{self.timeframe['start_date'].strftime('%W')}",
        }

        for keyword, value in title_keywords.items():
            title = title.replace(keyword, value)
        
        return title
