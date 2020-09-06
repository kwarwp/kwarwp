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
from unittest import TestCase
# from unittest.mock import MagicMock
from kwarwp.kwarapp import Kwarwp, Indio
from kwarwp.kwarwpart import Piche, Vazio, Oca, Tora, NULO
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
                
        self.k = Kwarwp(Jogo)
        self.t = FakeTaba()
        self.LADO = Vazio.LADO
    
    def set_fake(self):
        elts = self.elts = {}
        class FakeCena:
            def __init__(self, *_, **__):
                pass
            def vai(self, *_, **__):
                pass
            
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
        Vazio.VITOLLINO.a = FakeElemento
        Vazio.VITOLLINO.c = FakeCena
        
    def testa_cria(self):
        """ Cria o ambiente de programação Kwarwp."""
        self.set_fake()
        cena = self.k.cria()
        # self.assertIn("Vitollino_cria",  str(cena), cena)
        self.assertIn(self.INDIO, self.elts)

    def testa_cria_indio(self):
        """ Cria o índio com a fábrica."""
        self.set_fake()
        cena = self.k.cria()
        coisa = self.k.taba[3,3]
        self.assertIsInstance(coisa.ocupante,  Indio, f"but ocupante was {coisa.ocupante}")
        self.assertEquals(100, coisa.lado, f"but coisa.lado was {coisa.lado}")
        indio = self.elts[self.INDIO]
        self.assertEquals(coisa.ocupante.indio, indio, f"but coisa.ocupante.indio was {coisa.ocupante.indio}")
        self.assertEquals((0, 0), indio.pos, f"but indio.pos was {indio.pos}")
        
    def testa_empurra_tora(self):
        """ Vai até a tora e empurra."""
        cena = self.k.cria()
        vaga_tora = self.k.taba[1, 3]
        self.assertEquals(vaga_tora.taba,  self.k, f"but taba was {vaga_tora.taba}")
        tora = vaga_tora.ocupante
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but last pos was {pos}")
        indio = self.k.o_indio
        indio.esquerda()
        indio.anda()
        pos = indio.posicao
        self.assertEquals((2, 3),  pos, f"but indio pos was {pos}")
        vaga = indio.vaga
        indio.empurra()
        pos = tora.posicao
        self.assertEquals((0, 3),  pos, f"but tora pos was {pos}")
        self.assertEquals(vaga.ocupante,  NULO, f"but vaga ocupante was {vaga.ocupante}")
        vaga = indio.vaga
        indio.empurra()
        pos = tora.posicao
        self.assertEquals((0, 3),  pos, f"but tora new pos was {pos}")
        self.assertEquals(vaga.ocupante,  indio, f"but vaga new  ocupante {vaga.ocupante}")
        vaga = tora.vaga
        indio.pega()
        pos = tora.posicao
        self.assertEquals((1, 3),  pos, f"but tora taken pos was {pos}")
        self.assertEquals(vaga.ocupante,  NULO, f"but vaga taken  ocupante {vaga.ocupante}")
        self.assertEquals(tora.vaga,  indio, f"but tora vaga {tora.vaga}")
        # vaga = tora.vaga
        indio.larga()
        pos = tora.posicao
        self.assertEquals((0, 3),  pos, f"but tora drop pos was {pos}")
        self.assertEquals(vaga.ocupante,  tora, f"but vaga drop  ocupante {vaga.ocupante}")
        self.assertEquals(tora.vaga,  vaga, f"but tora drop vaga {tora.vaga}")
        return indio, tora


class Vitollino(Jogo):
    """ Empacota o engenho de jogo Vitollino """
    pass

def main():
    # from unittest import main
    # main()

    import unittest
    import kwarwp.htmlrunner as htmlrun
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Kwarwp)
    htmlrun.HTMLTestRunner().run(suite)        
    
if __name__ == "__main__":
    main()
