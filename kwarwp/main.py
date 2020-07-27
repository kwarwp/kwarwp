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


class Vitollino(Jogo):
    """ Empacota o engenho de jogo Vitollino """
    pass
    
    
if __name__ == "__main__":
    Vitollino()
