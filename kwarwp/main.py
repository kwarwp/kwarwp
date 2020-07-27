# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Changelog
---------
.. versionadded::    20.07
        classe Vitollino.

"""
from _spy.vitollino.main import Jogo
from kwarwp.kwarapp import main as kwarup_main


class Vitollino(Jogo):
    """ Empacota o engenho de jogo Vitollino """
    pass

def main():
    kwarwp_main(Vitollino)
        
    
if __name__ == "__main__":
    main()
