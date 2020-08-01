# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
""" Kwarapp portando o kwarwp para o Vitollino.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

- Como associar um evento a uma imagem
- Como combinar cenas em salas diferentes
- Como capturar o teclado

Sem Classes neste modulo:

Changelog
---------
.. versionadded::    20.08
        Adiciona o gerenciador de chamadas http via bottle.

"""
from bottle import default_app, route, static_file, run  # , debug
from kwarwp import __version__
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))
PARDIR = os.path.abspath(os.path.join(BASEDIR, os.pardir))
HTMLDIR = os.path.abspath(os.path.join(PARDIR, "docs", "build", "html"))
@route('/')
def game_world():
    """Roteia o caminho / para o jogo do kwarwp."""
    print("game_world", BASEDIR, PARDIR, HTMLDIR)
    return static_file('index.html', root=BASEDIR, mimetype='text/html')

@route('/vs')
def vs_mundo():
    """Roteia o caminho /vs para retornar a versão do sistema."""
    return f'Kwarwp - Versão do sistema: {__version__}'

@route('/<filename:re:.*[.]py>')
def py_mundo(filename):
    """Roteia o caminho /<nome>.py para retornar arquivos python.
    
    	:param filename: O nome do arquivo.
    """
    print("py_mundo", PARDIR, filename)
    return static_file(filename, root=PARDIR, mimetype='text/python')

@route('/doc')
def docroot_mundo():
    """Roteia o caminho /doc para a documentação."""
    print ("docroot_mundo",HTMLDIR)
    return static_file("index.html", root=HTMLDIR, mimetype='text/html')

@route('/doc/<filename:re:.*[.]html>')
def doc_mundo(filename):
    """Roteia o caminho /<nome>.html para retornar arquivos htmls.
    
    	:param filename: O nome do arquivo.
    """
    print ("doc_mundo",HTMLDIR)
    return static_file(filename, root=HTMLDIR, mimetype='text/html')

@route('/doc/<filename:re:.*[.]css>')
def css_mundo(filename):
    """Roteia o caminho /<nome>.css para retornar arquivos css.
    
    	:param filename: O nome do arquivo.
    """
    return static_file(filename, root=HTMLDIR, mimetype='text/css')

   
# debug(True)

application = default_app()


if __name__ == "__main__":
    #print(BASEDIR, os.path.abspath(BASEDIR), PARDIR, HTMLDIR)
    run(host='localhost', port=8000)
