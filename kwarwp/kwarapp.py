# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Changelog
---------
.. versionadded::    20.07
        classe Kwarwp.

"""


class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
    """
    ABERTURA = "https://i.imgur.com/dZQ8liT.jpg"
    
    def __init__(self, vitollino=None, cenario="default"):
        self.v = vitollino()
        self.cena = self.cria(cenario=cenario) if vitollino else None
        
    def cria(self, cenario="default"):
        """ Cria o ambiente de programação Kwarwp."""
        cena = self.v.c(self.ABERTURA)
        cena.vai()
        return cena
        

def main(vitollino):
    Kwarwp(vitollino)
        
    
if __name__ == "__main__":
    from _spy.vitollino.main import Jogo
    main(Jogo)
