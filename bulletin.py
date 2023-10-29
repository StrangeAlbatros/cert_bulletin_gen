#!/usr/bin/env python3


import importlib
from inspect import getmembers, isclass
from json import dumps, load

from .parser.scraper import *
from .models.config import Config
from .models.logger import Log
from .export import Exporter

class Bulletin:

    def __init__(self, args) -> None:
        self.conf = None
        if args.config:
            self.load_conf(args.config)
        else:
            self.load_conf()

        self.log = Log(debug=args.debug)

        if not self.conf:
            raise Exception("ERREUR: Impossible de charger la configuration")

        conf_cert = { k:v for k,v in self.conf.parser.items()}

        self.parser = []
        for obj,name in self.get_scraper():
            if name.lower() in conf_cert:
                conf_cert[name.lower()].update(self.conf.timeframe)
                conf_cert[name.lower()].update({"logger":self.log})
                self.parser.append(obj(**(conf_cert[name.lower()])))

        self.exporter = Exporter(
            data={elt.__class__.__name__.lower(): elt.alertes for elt in self.parser},
            logger=self.log,
            conf={
                "output":self.conf.output,
                "template":self.conf.template,
            }
        )

        compile_args = {
            'data': {elt.__class__.__name__.lower(): elt.alertes for elt in self.parser},
            'compile': args.no_compil,
        }

        if args.pdf_name:
            compile_args['pdf_name'] = args.pdf_name
        self.exporter.export(**compile_args)

    def get_scraper(self):
        """ Get the list of the available scrapers """
        try:
            package = importlib.import_module("cert_bulletin_gen.parser.scraper")
            return [ (obj,name) for name, obj in vars(package).items() if isclass(obj)]
        except ModuleNotFoundError as e:
            print(f"Error: {e}")
            return []

    def load_conf(self, path="cert_bulletin_gen/settings.json"):
        """ load the configuration file """
        with open(path) as json_file:
            data = load(json_file)

        if data:
            self.conf = Config(**data)

