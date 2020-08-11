# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Teste do Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Changelog
---------
.. versionadded::    20.07
        classe Test_Kwarwp.

"""
import os
import sys
sys.path.insert(0, os.path.abspath('../'))
from unittest import TestCase
from unittest.mock import MagicMock
from kwarwp.kwarapp import Kwarwp, Indio, Piche, Vazio, Oca
#sys.path.insert(0, os.path.abspath('../../libs'))

class Test_Kwarwp(TestCase):
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
    """
    ABERTURA = "https://i.imgur.com/dZQ8liT.jpg"
    
    def setUp(self):
        self.v = MagicMock(name="Vitollino")
        self.v().c = MagicMock(name="Vitollino_cria")
        self.k = Kwarwp(self.v)
        
    def testa_cria(self):
        """ Cria o ambiente de programação Kwarwp."""
        cena = self.k.cria()
        self.assertIn("Vitollino_cria",  str(cena), cena)
        
    def testa_cria_indio(self):
        """ Cria o índio com a fábrica."""
        cena = self.k.cria()
        coisa = self.k.taba[3,3]
        self.assertIsInstance(coisa.ocupante,  Indio, f"but coisa was {coisa}")
        self.assertEquals(100, coisa.lado, f"but coisa.lado was {coisa.lado}")
        
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
        class FakeTaba:
            def __init__(self):
                self.falou = ""
            def sai(self,*_):
                pass
            def fala(self, falou):
                self.falou = falou
        ftaba = FakeTaba()
        cena = self.k.cria()
        l = self.k.LADO
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
        class FakeTaba:
            def __init__(self):
                self.falou = ""
            def sai(self,*_):
                pass
            def fala(self, falou):
                self.falou = falou
        ftaba = FakeTaba()
        cena = self.k.cria()
        l = self.k.LADO
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
