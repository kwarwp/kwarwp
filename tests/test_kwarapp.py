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
from kwarwp.kwarapp import Kwarwp, Indio
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
