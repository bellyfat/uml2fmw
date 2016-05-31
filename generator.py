# -*- coding: utf-8 -*-
"""
    Módulo do gerador de códigos.

    Possui as classes e métodos que geram o código da aplicação Pyramid a partir de um scaffold localizado na pasta
    'template' e dos dados objectificados do arquivo XML exportado do modelo UML.
"""

import glob
from distutils.dir_util import copy_tree
from chameleon import PageTemplate
from os import walk, remove
from os.path import abspath, dirname, join
from datamodels import *

SCAFFOLD_FOLDER = 'scaffold'
GENERATED_FOLDER = 'generated'


class Generator(object):
    """Classe geradora de código."""

    def __init__(self, xml_file):
        self.project = Project.from_xml(xml_file)

    def generate(self):
        """Gera o código da aplicação Pyramid a partir do XML."""

        # Definição de diretótios de origem e destino.
        here = abspath(dirname(__file__))
        from_folder, to_folder = (join(here, SCAFFOLD_FOLDER), join(here, GENERATED_FOLDER))

        # Faz a cópia de todos os arquivos na pasta de templates para a pasta de destino.
        copy_tree(from_folder, to_folder)

        # Mapeia os templates nas pastas copiadas, usando-os como chave para os arquivos de código python.
        templates_and_genfiles = {tf: tf.replace('.u2p', '') for root, _, __ in walk(join(to_folder, 'u2p'))
                                  for tf in glob.glob(join(root, '*.u2p'))}

        # Dicionário de arquivos python e seus respectivos códigos.
        genfiles_and_codes = dict()
        for template_file, python_file in templates_and_genfiles.items():
            # Gera o código a partir do template e adiciona ao dicionário de arquivos python e códigos.
            code = Template(template_file).render(self.project)
            genfiles_and_codes[python_file] = code

            # Escreve o código num arquivo.
            with open(python_file, 'w') as pf:
                pf.write(code.encode('utf-8'))

            # Exlui o arquivo do template na pasta de destino.
            remove(template_file)

        return genfiles_and_codes


class Template(object):
    """Classe que representa um template."""
    def __init__(self, template):
        self.__template = template

    def render(self, project):
        """Gera a aplicação a partir do arquivo XML exportado de um modelo UML."""
        with open(self.__template) as tf:
            template_code = tf.read()
        template = PageTemplate(template_code)
        rendered = template(project=project)
        return rendered
