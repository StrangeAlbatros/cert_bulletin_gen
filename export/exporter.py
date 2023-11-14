#!/usr/bin/env python3

from jinja2 import Template

from os.path import exists,isfile
from os import remove, listdir
from platform import system
from subprocess import call
from shutil import copytree
from json import dumps

from cert_bulletin_gen.utils import read_file, write_file, snake_case, rename_file

from cert_bulletin_gen.models.event import Event
from cert_bulletin_gen.models.rss_event import RssEvent

LATEX_INTER_FILE = [
    "aux",
    "out",
    "toc"
]

class Exporter:

    def __init__(self, **kwargs) -> None:
        self.conf =kwargs.get('conf')
        self.logger = kwargs.get('logger')
        self.templates = None
        self.contents = {}

        self.load_template()

        if not self.templates:
            print("Pas de template trouvé")
            return

    def template_render(self, template, data=None):
        """ render the template with the data """
        tm = Template(template)
        return tm.render(content=data)
    
    def load_template(self):
        """ load the template from the config file """
        paths  = self.conf['template'].get('path', None)
        if not paths:
            raise Exception(
                "Pas de champs \"path\" dans le fichier de configurations (dans \"templates\")"
            )
        
        for type,path in paths.items():
            if not exists(path):
                raise FileNotFoundError(f"Le fichier {path} est introuvable")

        self.templates = {tpl: (type,read_file(tpl)) for type,tpl in paths.items() if isfile(tpl)}

    def export(self, **kwargs):
        """ export the data to the template """
        self.logger.indication("Start export")
        data = kwargs.get('data')
        out_folder = self.conf['output'].get('path')
        tpl_conf = self.conf['template'].get('data')
        files = {}

        # copy the template folder images
        if not exists(f"{out_folder}/img"):
            copytree("cert_bulletin_gen/templates/img", f"{out_folder}/img")

        self.logger.info("Generating latex files")

        # match the name of the template to the name of the parser
        match_name_tpl =  self.match_name_to_template()

        for name,t_data in self.templates.items():
            if t_data[0] == "main":
                # main template
                files[f"{out_folder}/main.tex"] = self.template_render(
                    t_data[1],
                    {
                        "title": tpl_conf.get('title'),
                        "author":tpl_conf.get('author'),
                        "chapters": [snake_case(cert) for cert,events in data.items()]
                    }
                )
            else:
                for elt in match_name_tpl[t_data[0]]:
                    cert = elt[0].upper() + elt[1:]
                    if elt in data:
                        files[f"{out_folder}/{elt}.tex"] = self.template_render(
                            t_data[1],
                            {
                                "title": cert,
                                "events": [event.latex_support_format() for event in data[elt]]
                            }
                        )

        if files:
            self.logger.success("Latex files generated")
        else:
            self.logger.warning("No data to export")
            return

        for f_name, content in files.items():
            write_file(f_name,content)

        if kwargs.get('compile', False):
            self.logger.info("No compile option activated")
            return

        self.compile()

        if self.conf['output'].get('name', False):
            rename_file(
                f"{out_folder}/main.pdf",
                f"{out_folder}/{self.conf['output'].get('name')}.pdf"
            )

        self.logger.info(f"Report generated : {self.conf['output'].get('path')}/{kwargs.get('pdf_name', 'report')}.pdf")

    def match_name_to_template(self):
        """ match the name of the template to the name of the parser """
        match = {}

        for name, data in self.conf['parser'].items():
            if match.get(data.get('template_name'), True):
                match[data.get('template_name')] = []
            match[data.get('template_name')].append(name)
        return match

    def compile(self):
        """ compile the latex file to pdf """
        self.logger.indication("Start compilation")
        os = system().lower()

        if os.startswith('linux') or os.startswith('darwin'):
            resp = self.execute_unix_command("cd cert_bulletin_gen/aout && pdflatex main.tex")
        else:
            pass
            #TODO : manage windows
        if resp == 0:
            self.logger.success("Compilation done")
        else:
            self.logger.error("Compilation failed see latex logs for more details")
        
        self.rm_inter_file()

    def rm_inter_file(self):
        """ remove the intermediate files """
        self.logger.indication("Removing intermediate files")
        
        for f in listdir(self.conf['output'].get('path')):
            if f.split(".")[-1] in LATEX_INTER_FILE:
                try:
                    remove(f"{self.conf['output'].get('path')}/{f}")
                except Exception as e:
                    self.logger.error(f"Error while removing {f} : {e}")

    def execute_unix_command(self, command):
        """ execute the command and retrieve its output """
        return call(command, shell=True)
