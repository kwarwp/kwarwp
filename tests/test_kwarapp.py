# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Teste do Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Changelog
---------
.. versionadded::    20.07
        classe Test_Kwarwp.

        "&": Fab(self.maloc, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}UCWGCKR.png"), # INDIO
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.coisa, f"{IMGUR}ldI7IbK.png"), # TORA
        "@": Fab(self.barra, f"{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA       


"""
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from unittest import TestCase
from unittest.mock import MagicMock
from kwarwp.kwarapp import Kwarwp, Indio
from kwarwp.kwarwpart import Piche, Vazio, Oca, Tora
#sys.path.insert(0, os.path.abspath('../../libs'))

class Test_Kwarwp(TestCase):
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
    """
    ABERTURA = "https://i.imgur.com/dZQ8liT.jpg"
    INDIO = "https://imgur.com/UCWGCKR.png"
    OCA = "https://imgur.com/dZQ8liT.jpg"
    PICHE = "https://imgur.com/tLLVjfN.png"
    TORA = "https://imgur.com/0jSB27g.png"
    
    def setUp(self):
        elts = self.elts = {}
        class FakeTaba:
            def __init__(self):
                self.falou = ""
            def sai(self,*_):
                pass
            def fala(self, falou):
                self.falou = falou
                
        class FakeElemento:
            def __init__(self, img=0, x=0, y=0, w=0, h=0, vai=None, elts=elts, **kwargs):
                elts[img] = self
                self.img, self.x, self.y, self.w, self.h, self.vai = img, x, y, w, h, vai
                self.destino, self._pos, self._siz = [None]*3
            def ocupa(self, destino):
                self.destino = destino.elt
            @property
            def elt(self):
                return self
            @property
            def siz(self):
                return self._siz
            @property
            def pos(self):
                return self._pos
            @siz.setter
            def siz(self, value):
                self._siz = value
            @pos.setter
            def pos(self, value):
                self._pos = value
        self.v = MagicMock(name="Vitollino")
        self.v().c = MagicMock(name="Vitollino_cria")
        self.v().a = FakeElemento
        self.k = Kwarwp(self.v)
        Vazio.VITOLLINO.a = FakeElemento
        self.t = FakeTaba()
        self.LADO = Vazio.LADO
        
    def testa_cria(self):
        """ Cria o ambiente de programação Kwarwp."""
        cena = self.k.cria()
        self.assertIn("Vitollino_cria",  str(cena), cena)
        self.assertIn(self.INDIO, self.elts)
        
    def testa_cria_piche_oca(self):
        """ Cria o piche e a oca com a fábrica."""
        cena = self.k.cria()
        vaga_oca = self.k.taba[5, 0]
        oca = self.elts[self.OCA]
        self.assertIsInstance(vaga_oca.ocupante,  Oca, f"but vaga_oca was {vaga_oca.ocupante}")
        self.assertEquals(vaga_oca.vazio.destino, oca)
        vaga_piche = self.k.taba[0, 0]
        piche = self.elts[self.PICHE]
        self.assertIsInstance(vaga_piche.ocupante,  Piche, f"but vaga_piche was {vaga_piche.ocupante}")
        self.assertEquals(vaga_piche.vazio.destino, piche)
        
    def testa_cria_tora(self):
        """ Cria a tora com a fábrica."""
        cena = self.k.cria()
        vaga_tora = self.k.taba[1, 3]
        tora = self.elts[self.TORA]
        self.assertIsInstance(vaga_tora.ocupante,  Tora, f"but vaga_tora was {vaga_tora.ocupante}")
        self.assertEquals(vaga_tora.vazio.destino, tora)
        
    def _pega_tora(self):
        """ Vai até a tora e pega."""
        vaga_tora = self.k.taba[1, 3]
        tora = vaga_tora.ocupante
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but last pos was {pos}")
        indio = self.k.o_indio
        indio.esquerda()
        indio.anda()
        pos = indio.posicao
        self.assertEquals((2, 3),  pos, f"but indio pos was {pos}")
        indio.pega()
        pos = tora.posicao
        self.assertEquals((2, 3),  pos, f"but tora pos was {pos}")
        return indio, tora
        
    def _pega_tora_elimina_piche(self):
        """ Vai até a tora e pega e usa para eliminar o piche."""
        cena = self.k.cria()
        l = self.LADO
        indio = self.k.o_indio
        vaga_tora = self.k.taba[2, 3]
        tora = Tora("", x=0, y=0, cena=cena, taba=self.k)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=tora)
        vaga_tora = self.k.taba[(2, 3)] = vaga
        indio.pega()
        indio.direita()
        piche = Piche("", x=0, y=0, cena=cena, taba=self.k)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=piche)
        vaga_piche = self.k.taba[(3,2)] = vaga
        indio.larga()
        indio.pega()
        self.assertEquals(vaga_piche.vazio,  vaga_piche, f"but vazio was {vaga_piche.vazio}")
        
    def testa_pega_tora(self):
        """ Vai até a tora e pega."""
        cena = self.k.cria()
        self._pega_tora()
        
    def testa_larga_tora(self):
        """ Vai até a tora pega e larga."""
        cena = self.k.cria()
        self.k.o_indio.larga()
        l = self.LADO
        indio, tora = self._pega_tora()
        indio.larga()
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but tora pos was {pos}")
        coisa = Tora("", x=0, y=0, cena=cena, taba=self.k)
        vaga = Vazio("", x=0*l, y=3*l, cena=cena, ocupante=coisa)
        vazio = self.k.taba[(0,3)] = vaga
        indio.pega()
        pos = tora.posicao
        self.assertEquals((2, 3),  pos, f"but tora pos was {pos}")
        indio.anda()
        pos = indio.posicao
        self.assertEquals((1, 3),  pos, f"but indio andou pos was {pos}")
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but tora andou pos was {pos}")
        indio.anda()
        indio.larga()
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but tora not drop pos was {pos}")
        
      
    def testa_pega_vazio_oca_piche(self):
        """ Vai até a piche, oca e vazio e tenta pegar."""
        cena = self.k.cria()
        ftaba = self.t
        l = self.LADO
        indio = self.k.o_indio
        indio.pega()
        coisa = Oca("", x=0, y=0, cena=cena, taba=self.k)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=coisa)
        vazio = self.k.taba[(3,2)] = vaga
        indio.pega()
        coisa = Piche("", x=0, y=0, cena=cena, taba=self.k)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=coisa)
        vazio = self.k.taba[(3,2)] = vaga
        indio.pega()
        indio.esquerda()
        indio.esquerda()
        indio.pega()
        
    def testa_cria_indio(self):
        """ Cria o índio com a fábrica."""
        cena = self.k.cria()
        coisa = self.k.taba[3,3]
        self.assertIsInstance(coisa.ocupante,  Indio, f"but coisa was {coisa}")
        self.assertEquals(100, coisa.lado, f"but coisa.lado was {coisa.lado}")
        indio = self.elts[self.INDIO]
        self.assertEquals(coisa.ocupante.indio, indio, f"but coisa.ocupante.indio was {coisa.ocupante.indio}")
        self.assertEquals((0, 0), indio.pos, f"but indio.pos was {indio.pos}")
        
    def testa_usa_indio(self):
        """ Obtem o índio como atributo Kwarwp."""
        cena = self.k.cria()
        indio = self.k.o_indio
        self.assertIsInstance(indio,  Indio, f"but coisa was {indio}")

    def testa_move_indio(self):
        """ Move o índio, andando em frente."""
        cena = self.k.cria()
        indio = self.k.o_indio
        pos = indio.posicao
        self.assertEquals((3, 3),  pos, f"but previous pos was {pos}")
        indio.anda()
        pos = indio.posicao
        self.assertEquals((3, 2),  pos, f"but last pos was {pos}")
        # self.assertIsInstance(indio,  Indio, f"but coisa was {indio}")

    def testa_prende_indio(self):
        """ Tenta mover o índio, mas fica preso."""
        ftaba = self.t
        cena = self.k.cria()
        l = self.LADO
        indio = self.k.o_indio
        piche = Piche("", x=0, y=0, cena=cena, taba=ftaba)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=piche)
        vazio = self.k.taba[(3,1)] = vaga
        self.assertIsInstance(vazio.ocupante, Piche, f"but vaga was {type(vazio.ocupante)}")
        pos = piche.posicao
        self.assertEquals((3, 1),  pos, f"but piche pos was {pos}")
        indio.anda()
        indio.anda()
        self.assertIsInstance(indio.vaga, Piche, f"but vaga was {type(indio.vaga)}")
        self.assertEquals(piche, indio.vaga, f"but vaga was {indio.vaga}")
        indio.anda()
        pos = indio.posicao
        self.assertEquals((3, 1),  pos, f"but last pos was {pos}")
        self.assertIn("preso", ftaba.falou, f"but fala was {ftaba.falou}")

    def testa_chega_taba_indio(self):
        """ Chega no seu destino, tenta mover o índio, mas fica preso."""
        ftaba = self.t
        cena = self.k.cria()
        l = self.LADO
        indio = self.k.o_indio
        oca = Oca("", x=0, y=0, cena=cena, taba=ftaba)
        vaga = Vazio("", x=3*l, y=2*l, cena=cena, ocupante=oca)
        vazio = self.k.taba[(3,1)] = vaga
        self.assertIsInstance(vazio.ocupante, Oca, f"but vaga was {type(vazio.ocupante)}")
        pos = oca.posicao
        self.assertEquals((3, 1),  pos, f"but oca pos was {pos}")
        indio.anda()
        indio.anda()
        self.assertIsInstance(indio.vaga, Oca, f"but vaga was {type(indio.vaga)}")
        self.assertEquals(oca, indio.vaga, f"but vaga was {indio.vaga}")
        self.assertIn("chegou", ftaba.falou, f"but fala was {ftaba.falou}")
        indio.anda()
        pos = indio.posicao
        self.assertEquals((3, 1),  pos, f"but last pos was {pos}")
        # self.assertIsInstance(indio,  Indio, f"but coisa was {indio}")

    def testa_esquerda_indio(self):
        """ Move o índio, andando em frente, esquerda, frente."""
        cena = self.k.cria()
        indio = self.k.o_indio
        pos = indio.posicao
        self.assertEquals((3, 3),  pos, f"but previous pos was {pos}")
        indio.anda()
        indio.esquerda()
        indio.anda()
        pos = indio.posicao
        self.assertEquals((2, 2),  pos, f"but last pos was {pos}")
        # self.assertIsInstance(indio,  Indio, f"but coisa was {indio}")

    def testa_volta_indio(self):
        """ Move o índio, andando em frente, meia volta, frente."""
        cena = self.k.cria()
        indio = self.k.o_indio
        pos = indio.posicao
        self.assertEquals((3, 3),  pos, f"but previous pos was {pos}")
        indio.anda()
        indio.esquerda()
        indio.esquerda()
        indio.anda()
        pos = indio.posicao
        self.assertEquals((3, 3),  pos, f"but last pos was {pos}")
        # self.assertIsInstance(indio,  Indio, f"but coisa was {indio}")
    
if __name__ == "__main__":
    from unittest import main
    main()
