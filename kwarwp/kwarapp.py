# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Jogo para ensino de programação Python.

    .. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

    Classes neste módulo:
        - :py:class:`Kwarwp` Jogo para ensino de programação.
        - :py:class:`Indio` Personagem principal do jogo.

    Changelog
    ---------
    .. versionadded::    20.08.a1
        Classe Indio que executa roteiro e anda.
            
    .. versionadded::    20.08.a0
        Fábrica de componentes
        classe Indio.
        Usa um mapa de caracteres para colocar os elementos.
            
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
Ponto = nt("Ponto", "x y")
"""Par de coordenadas na direção horizontal (x) e vertiacal (y)."""
Rosa = nt("Rosa", "n l s o")
"""Rosa dos ventos com as direções norte, leste, sul e oeste."""


class Indio():
    """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param imagem: A figura representando o índio na posição indicada.
        :param x: Coluna em que o elemento será posicionado.
        :param y: Cinha em que o elemento será posicionado.
        :param cena: Cena em que o elemento será posicionado.
    """
    
    def __init__(self, imagem, x, y, cena):
        self.lado = lado = Kwarwp.LADO
        self.posicao = (x//lado,y//lado)
        self.indio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        
    def anda(self):
        """ Faz o índio caminhar na direção em que está olhando.
        """
        self.posicao = (self.posicao[0], self.posicao[1]-1)
        """Assumimos que o índio está olhando para cima, decrementamos a posição **y**"""
        self.indio.y = self.posicao[1]*self.lado
        self.indio.x = self.posicao[0]*self.lado
         
    def executa(self):
        """ Roteiro do índio. Conjunto de comandos para ele executar.
        """
        self.anda()


class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
        :param medidas: Um dicionário usado para redimensionar a tela.
    """
    VITOLLINO = None
    """Referência estática para obter o engenho de jogo."""
    LADO = None
    """Referência estática para definir o lado do piso da casa."""
    
    def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
        Kwarwp.VITOLLINO = self.v = vitollino()
        self.mapa = mapa.split()
        """Cria um matriz com os elementos descritos em cada linha de texto"""
        self.o_indio = None
        """Instância do personagem principal, o índio, vai ser atribuído pela fábrica do índio"""
        self.lado, self.col, self.lin = 100, len(self.mapa[0]), len(self.mapa)+1
        """Largura da casa da arena dos desafios, número de colunas e linhas no mapa"""
        Kwarwp.LADO = self.lado
        w, h = self.col *self.lado, self.lin *self.lado
        self.taba = {}
        """Dicionário que a partir de coordenada (i,J) localiza um piso da taba"""
        medidas.update(width=w, height=f"{h}px")
        self.cena = self.cria(mapa=self.mapa) if vitollino else None
        
    # def cria(self, mapa):

    def cria(self, mapa=""):
        """ Fábrica de componentes.
        
            :param mapa: Um texto representando o mapa do desafio.
        """
        Fab = nt("Fab", "objeto imagem")
        """Esta tupla nomeada serve para definir o objeto construido e sua imagem."""

        fabrica = {
        "&": Fab(self.coisa, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}8jMuupz.png"), # INDIO
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.coisa, f"{IMGUR}ldI7IbK.png"), # TORA
        "@": Fab(self.coisa, f"{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA       
        }
        """Dicionário que define o tipo e a imagem do objeto para cada elemento."""
        mapa = mapa if mapa != "" else self.mapa
        """Cria um cenário com imagem de terra de chão batido, céu e sol"""
        mapa = self.mapa
        lado = self.lado
        print(f"cria(self, mapa={mapa}, col={len(self.mapa[0])}")
        cena = self.v.c(fabrica["_"].imagem)
        ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado, x=0, y=0, cena=cena, vai=self.executa)
        """No argumento *vai*, associamos o clique no céu com o método **ececuta ()** desta classe"""
        sol = self.v.a(fabrica["*"].imagem, w=60, h=60, x=0, y=40, cena=cena)
        self.taba = {(i, j): fabrica[imagem].objeto(fabrica[imagem].imagem, x=i*lado, y=j*lado+lado, cena=cena)
            for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)}
        """Posiciona os elementos segundo suas posições i, j na matriz mapa"""
        cena.vai()
        return cena
        
    def executa(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        self.o_indio.executa()
        
    def coisa(self, imagem, x, y, cena):
        """ Cria um elemento na arena do Kwarwp na posição definida.

            :param x: coluna em que o elemento será posicionado.
            :param y: linha em que o elemento será posicionado.
            :param cena: cena em que o elemento será posicionado.
        """
        lado = self.lado
        return self.v.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        
    def vazio(self, imagem, x, y, cena):
        """ Cria um espaço vazio na arena do Kwarwp na posição definida.

            :param x: coluna em que o elemento será posicionado.
            :param y: linha em que o elemento será posicionado.
            :param cena: cena em que o elemento será posicionado.
        """
        lado = self.lado
        return self.v.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        
    def indio(self, imagem, x, y, cena):
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

            :param x: coluna em que o elemento será posicionado.
            :param y: linha em que o elemento será posicionado.
            :param cena: cena em que o elemento será posicionado.
        """
        self.o_indio = Indio(imagem, x=x, y=y, cena=cena)
        return self.o_indio

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
