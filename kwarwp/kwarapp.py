# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Classes neste módulo:
    :py:class:`Kwarwp` Jogo para ensino de programação.
    :py:class:`Taba` Arena onde os desafios ocorrem.

Changelog
---------
.. versionadded::    20.07
        Usa um mapa de caracteres para colocar os elementos.
        classe Kwarwp.

"""
from collections import namedtuple as nt

MAPA_INICIO = """
@....&
......
......
.#.^..
"""


class Taba():
    """ Arena onde os desafios ocorrem.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.

    Na taba cada casa se relaciona com quatro outras, ao 
    **Norte, Sul, Leste e Oeste**

    .. mermaid::

        graph TD
            Casa --> Oeste & Norte & Leste & Sul 
    
    """
def __init__(self, cena, taba=None, mapa=MAPA_INICIO):
    self.v = Kwarwp.VITOLLINO
    self.taba = taba if taba else self.cria(mapa)
    self.norte = self.sul = self.leste = self.oeste = self

def cria(self, mapa):
    Fab = nt("Fab", "action image")
    fabrica = {
    "&": Fab(self.coisa, "https://i.imgur.com/dZQ8liT.jpg"), # OCA
    "^": Fab(self.indio, "https://imgur.com/8jMuupz.png"),   # INDIO
    ".": Fab(self.vazio, "https://i.imgur.com/npb9Oej.png"), # VAZIO
    "_": Fab(self.coisa, "https://i.imgur.com/sGoKfvs.jpg"), # SOLO
    "#": Fab(self.coisa, "https://imgur.com/ldI7IbK.png"),   # TORA
    "@": Fab(self.coisa, "https://imgur.com/tLLVjfN.png"),   # PICHE
    "~": Fab(self.coisa, "https://i.imgur.com/UAETaiP.gif"), # CEU
    "*": Fab(self.coisa, "https://i.imgur.com/PfodQmT.gif"), # SOL
    "|": Fab(self.coisa, " https://i.imgur.com/uwYPNlz.png")  # CERCA       
    }

class Kwarwp():
    """ Jogo para ensino de programação.

        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
    """
    VITOLLINO = None
    GLIFOS = {
    "&": "https://i.imgur.com/dZQ8liT.jpg", # OCA
    "^": "https://imgur.com/8jMuupz.png",   # INDIO
    ".": "https://i.imgur.com/npb9Oej.png", # VAZIO
    "_": "https://i.imgur.com/sGoKfvs.jpg", # SOLO
    "#": "https://imgur.com/ldI7IbK.png",   # TORA
    "@": "https://imgur.com/tLLVjfN.png",   # PICHE
    "~": "https://i.imgur.com/UAETaiP.gif", # CEU
    "*": "https://i.imgur.com/PfodQmT.gif", # SOL
    "|":" https://i.imgur.com/uwYPNlz.png"  # CERCA
    }
    
    def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
        Kwarwp.VITOLLINO = self.v = vitollino()
        """Cria um matriz com os elementos descritos em cada linha de texto"""
        mapa = mapa.split()
        """Largura da casa da arena dos desafios, número de colunas no mapa"""
        self.lado, self.col = 100, len(mapa[0]) 
        self.cena = self.cria(mapa=mapa) if vitollino else None
        
    def cria(self, mapa="  "):
        """ Cria o ambiente de programação Kwarwp.

            :param mapa: Um texto representando o mapa do desafio.
        """
        """Cria um cenário com imagem de terra de chão batido, céu e sol"""
        lado = self.lado
        cena = self.v.c(self.GLIFOS["_"])
        ceu = self.v.a(self.GLIFOS["~"], w=lado*self.col, h=lado, x=0, y=0, cena=cena)
        sol = self.v.a(self.GLIFOS["*"], w=60, h=60, x=0, y=40, cena=cena)
        """Posiciona os elementos segundo suas posições i, j na matriz mapa"""
        [self.cria_elemento(imagem, x=i*lado, y=j*lado+lado, cena=cena)
            for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)]
        cena.vai()
        return cena
        
    def cria_elemento(self, imagem, x, y, cena):
        """ Cria um elemento na arena do Kwarwp na posição definida.

            :param x: coluna em que o elemento será posicionado.
            :param y: linha em que o elemento será posicionado.
            :param cena: cena em que o elemento será posicionado.
        """
        lado = self.lado
        return self.v.a(self.GLIFOS[imagem], w=lado, h=lado, x=x*lado, y=y*lado+lado, cena=cena)

def main(vitollino):
    Kwarwp(vitollino)
        
    
if __name__ == "__main__":
    from _spy.vitollino.main import Jogo, STYLE
    STYLE.update(width=600, height="500px")
    main(Jogo)
