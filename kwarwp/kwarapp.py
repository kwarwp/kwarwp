# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

    .. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

    Classes neste módulo:
        - :py:class:`Kwarwp` Jogo para ensino de programação.
        - :py:class:`Indio` Personagem principal do jogo.
        - :py:class:`Taba` Arena onde os desafios ocorrem.

    Changelog
    ---------
    .. versionadded::    20.08
        Usa um mapa de caracteres para colocar os elementos.
        classe Indio.
            
    .. versionadded::    20.07
        classe Kwarwp.

"""
from collections import namedtuple as nt

IMGUR = "https://imgur.com/"
"""Prefixo do site imgur."""
MAPA_INICIO = """
@....&
......
......
.#.^..
"""
"""Mapa com o posicionamento inicial dos elementos."""


class Indio():
    """ Personagem principal do jogo.
        
        .. image:: https://i.imgur.com/wghTu6y.png
            :height: 100
            :width: 400
            :alt: X X X - E M ---  C O N S T R U Ç Ã O - X X X
            :align: center

    """
    ...


class Taba():
    """ Arena onde os desafios ocorrem.
    
        Na taba cada casa se relaciona com quatro outras, ao 
        **Norte, Sul, Leste e Oeste**

        .. mermaid::

            graph TD
                Casa --> Oeste & Norte & Leste & Sul 
   
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.

    
    """
    def __init__(self, cena, taba=None, mapa=MAPA_INICIO):
        self.v = Kwarwp.VITOLLINO
        self.taba = taba if taba else self.cria(mapa)
        self.norte = self.sul = self.leste = self.oeste = self

    def cria(self, mapa):
        """ Fábrica de componentes.
        
            :param mapa: Um texto representando o mapa do desafio.
        """
        Fab = nt("Fab", "action image")
        fabrica = {
        "&": Fab(self.coisa, "{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, "{IMGUR}8jMuupz.png"), # INDIO
        ".": Fab(self.vazio, "{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, "{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.coisa, "{IMGUR}ldI7IbK.png"), # TORA
        "@": Fab(self.coisa, "{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, "{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, "{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, "{IMGUR}uwYPNlz.png")  # CERCA       
        }

class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
        :param medidas: Um dicionário usado para redimensionar a tela.
    """
    VITOLLINO = None
    """Referência estática para obter o engenho de jogo."""
    GLIFOS = {
    "&": "{IMGUR}dZQ8liT.jpg", # OCA
    "^": "{IMGUR}8jMuupz.png",   # INDIO
    ".": "{IMGUR}npb9Oej.png", # VAZIO
    "_": "{IMGUR}sGoKfvs.jpg", # SOLO
    "#": "{IMGUR}ldI7IbK.png",   # TORA
    "@": "{IMGUR}tLLVjfN.png",   # PICHE
    "~": "{IMGUR}UAETaiP.gif", # CEU
    "*": "{IMGUR}PfodQmT.gif", # SOL
    "|":" {IMGUR}uwYPNlz.png"  # CERCA
    }
    """Dicionário contendo as imagens dos elementos."""
    
    def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
        Kwarwp.VITOLLINO = self.v = vitollino()
        """Cria um matriz com os elementos descritos em cada linha de texto"""
        self.mapa = mapa.split()
        """Largura da casa da arena dos desafios, número de colunas no mapa"""
        self.lado, self.col, self.lin = 100, len(self.mapa[0]), len(self.mapa)+1
        w, h = self.col *self.lado, self.lin *self.lado
        medidas.update(width=w, height=f"{h}px")
        self.cena = self.cria(mapa=self.mapa) if vitollino else None
        
    def cria(self, mapa=""):
        """ Cria o ambiente de programação Kwarwp.

            :param mapa: Um texto representando o mapa do desafio.
        """
        """Cria um cenário com imagem de terra de chão batido, céu e sol"""
        mapa = mapa if mapa != "" else self.mapa
        mapa = self.mapa
        lado = self.lado
        print(f"cria(self, mapa={mapa}, col={len(self.mapa[0])}")
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
        return self.v.a(self.GLIFOS[imagem], w=lado, h=lado, x=x, y=y, cena=cena)

def main(vitollino, medidas={}):
    """ Rotina principal que invoca a classe Kwarwp.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param medidas: Um dicionário usado para redimensionar a tela.
    """
    # print(f"main(vitollino={vitollino} medidas={medidas}")
    Kwarwp(vitollino, medidas=medidas)
        
    
if __name__ == "__main__":
    from _spy.vitollino.main import Jogo, STYLE
    STYLE.update(width=600, height="500px")
    main(Jogo, STYLE)
