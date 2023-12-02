#!/usr/bin/env python3


import importlib
from inspect import getmembers, isclass
from json import dumps, load

from .parser.scraper import *
from .models.config import Config
from .models.translator import Translator
from .export import Exporter

from .logger import LOGGER

class Bulletin:

    def __init__(self, args) -> None:
        self.conf = None
        if args.config:
            self.load_conf(args.config)
        else:
            self.load_conf()

        if args.debug:
            LOGGER.set_debug()

        if not self.conf:
            raise Exception("ERREUR: Impossible de charger la configuration")

        self.translator = Translator(lang=self.conf.lang)
        self.start_treatment(args)

    def start_treatment(self, args):
        """ Start the treatment """
        conf_cert = { k:v for k,v in self.conf.parser.items()}

        self.parser = []
        for obj,name in self.get_scraper():
            if name.lower() in conf_cert:
                conf_cert[name.lower()].update(self.conf.timeframe)
                conf_cert[name.lower()].update({"translator":self.translator})
                self.parser.append(obj(**(conf_cert[name.lower()])))

        # export the data to the latex template
        self.exporter = Exporter(
            data={elt.__class__.__name__.lower(): elt.events for elt in self.parser},
            conf={
                "output":self.conf.output,
                "template":self.conf.template,
                "parser":self.conf.parser,
            }
        )

        # latex compile the bulletin
        compile_args = {
            'data': {elt.__class__.__name__.lower(): elt.events for elt in self.parser},
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

