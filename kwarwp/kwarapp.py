# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Classes neste módulo:
    :py:class:`Taba` Arena onde os desafios ocorrem.
    :py:class:`Kwarwp` Jogo para ensino de programação.

Changelog
---------
.. versionadded::    20.07
        classe Taba.
        classe Kwarwp.

"""
MAPA_INICIO = """
@...&
.....
.....
.#.^.
"""


class Taba():
    """ Arena onde os desafios ocorrem.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
    """
    GLIFOS = {
    "&": "https://i.imgur.com/dZQ8liT.jpg",  # OCA
    "^": "https://imgur.com/8jMuupz.png",  # INDIO
    ".": "https://i.imgur.com/sGoKfvs.jpg",  # SOLO
    "#": "https://imgur.com/ldI7IbK.png",  # TORA
    "@": "https://imgur.com/tLLVjfN.png",  # PICHE
    "~": "https://i.imgur.com/UAETaiP.gif",  # CEU
    "*": "https://i.imgur.com/PfodQmT.gif"  # SOL
    }
    
    def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
        self.v = vitollino()
        self.cena = self.cria(cenario=cenario) if vitollino else None
        
    def cria(self, cenario="default"):
        """ Cria o ambiente de programação Kwarwp."""
        cena = self.v.c(self.SOLO)
        indio = self.v.a(self.INDIO, w=100, h=100, x=300, y=400, cena=cena)
        oca = self.v.a(self.OCA, w=100, h=100, x=500, y=100, cena=cena)
        tora = self.v.a(self.TORA, w=100, h=100, x=100, y=400, cena=cena)
        piche = self.v.a(self.PICHE, w=100, h=100, x=100, y=100, cena=cena)
        piche = self.v.a(self.CEU, w=600, h=100, x=0, y=0, cena=cena)
        sol = self.v.a(self.SOL, w=60, h=60, x=0, y=40, cena=cena)
        cena.vai()
        return cena


class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
    """
    OCA = "https://i.imgur.com/dZQ8liT.jpg"
    INDIO = "https://imgur.com/8jMuupz.png"
    SOLO = "https://i.imgur.com/sGoKfvs.jpg"
    TORA = "https://imgur.com/ldI7IbK.png"
    PICHE = "https://imgur.com/tLLVjfN.png"
    CEU = "https://i.imgur.com/UAETaiP.gif"
    SOL = "https://i.imgur.com/PfodQmT.gif"
    
    def __init__(self, vitollino=None, cenario="default"):
        self.v = vitollino()
        self.cena = self.cria(cenario=cenario) if vitollino else None
        
    def cria(self, cenario="default"):
        """ Cria o ambiente de programação Kwarwp."""
        cena = self.v.c(self.SOLO)
        indio = self.v.a(self.INDIO, w=100, h=100, x=300, y=400, cena=cena)
        oca = self.v.a(self.OCA, w=100, h=100, x=500, y=100, cena=cena)
        tora = self.v.a(self.TORA, w=100, h=100, x=100, y=400, cena=cena)
        piche = self.v.a(self.PICHE, w=100, h=100, x=100, y=100, cena=cena)
        piche = self.v.a(self.CEU, w=600, h=100, x=0, y=0, cena=cena)
        sol = self.v.a(self.SOL, w=60, h=60, x=0, y=40, cena=cena)
        cena.vai()
        return cena
        

def main(vitollino):
    Kwarwp(vitollino)
        
    
if __name__ == "__main__":
    from _spy.vitollino.main import Jogo, STYLE
    STYLE.update(width=600, height="500px")
    main(Jogo)
