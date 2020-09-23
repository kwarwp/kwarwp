# kwarwp.kwarwp.main.py
# SPDX-License-Identifier: GPL-3.0-or-later
""" Teste do Jogo para ensino de programação Python.

.. codeauthor:: Carlo Oliveira <carlo@ufrj.br>

Changelog
---------
.. versionadded::    20.08.b1
        Testa fila e execução passo a passo.
        
.. versionadded::    20.07
        classe Test_Kwarwp.

        "&": Fab(self.maloc, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}UCWGCKR.png"), # INDIO
        "`": Fab(self.indio, f"{IMGUR}nvrwu0r.png"), # INDIA
        "p": Fab(self.indio, f"{IMGUR}HeiupbP.png"), # PAJE
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.atora, f"{IMGUR}0jSB27g.png"), # TORA
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
from kwarwp.kwarapp import Kwarwp, Indio, JogoProxy, main
from kwarwp.kwarwpart import Piche, Vazio, Oca, Tora
from kwarwp.main import main as mn, Kaiowa
#sys.path.insert(0, os.path.abspath('../../libs'))

class Test_Kwarwp(TestCase):
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
    """
    ABERTURA = "https://i.imgur.com/dZQ8liT.jpg"
    INDIO = "https://imgur.com/UCWGCKR.png"
    INDIA = "https://imgur.com/nvrwu0r.png"
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
            def __init__(self, img=0, x=0, y=0, w=0, h=0, vai=None, elts=elts, cena=None, **kwargs):
                elts[img] = self
                self.cena = cena
                cena.ocupa(self) if cena else None
                self.img, self.x, self.y, self.w, self.h, self.vai = img, x, y, w, h, vai
                self.destino, self._pos, self._siz = [None]*3
            def ocupa(self, destino=None, pos=(0, 0)):
                self.pos = pos
                # print(f"FakeElemento ocupa {destino} {self.pos}")
                self.destino = destino.elt if destino else None
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
        self.v().a = self.v().e = self.e = FakeElemento
        self.k = Kwarwp(self.v)
        Vazio.VITOLLINO.a = FakeElemento
        self.t = FakeTaba()
        self.LADO = Vazio.LADO
        
    def _testa_cria_dois_indios(self):
        """ Cria o ambiente com dois índio."""
        krw = mn(self.v, {})
        self.assertIn(self.INDIO, self.elts)
        self.assertIn(self.INDIA, self.elts)
        self.assertIn(Kaiowa, [type(i) for i in krw.os_indios])
        io, ia = krw.os_indios
        krw.executa()
        self.assertTrue(ia.vitollino._ativa, f"but india cmd: {ia.vitollino._ativa}")
        self.assertEquals(krw.v._corrente, io.vitollino, f"but indio cmd: {krw.v._corrente}")
        self.assertEquals(0, len(krw.v.comandos), f"but indio cmd: {krw.v.comandos}")
        self.assertEquals(10, len(io.vitollino.comandos), f"but indio cmd: {io.vitollino.comandos}")
        self.assertEquals(10, len(ia.vitollino.comandos), f"but india cmd: {ia.vitollino.comandos}")
        
    def testa_executa_proxy_indio(self):
        """ Cria o ambiente proxy com um índio."""
        krw = mn(self.v, {})
        self.assertIn(self.INDIO, self.elts)
        self.assertIn(self.INDIA, self.elts)
        self.assertIn(Kaiowa, [type(i) for i in krw.os_indios])
        self.assertIsInstance(krw.os_indios[1], Kaiowa)
        self.assertIsInstance(krw.os_indios[0].indio, JogoProxy)
        io, ia = krw.os_indios
        krw.executa()
        self.assertTrue(io.indio._ativa, f"but indio ativa: {io.indio._ativa}")
        #self.assertTrue(ia.vitollino._ativa, f"but india cmd: {ia.vitollino._ativa}")
        #self.assertEquals(krw.v._corrente, io.vitollino, f"but indio cmd: {krw.v._corrente}")
        self.assertEquals(0, len(krw.v.comandos), f"but indio cmd: {krw.v.comandos}")
        #self.assertEquals(10, len(io.vitollino.comandos), f"but indio cmd: {io.vitollino.comandos}")
        self.assertEquals(10, len(io.indio.comandos), f"but indio cmd: {io.indio.comandos}")
        
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
        self.k = main(self.v)
        self.assertIsInstance(Vazio.VITOLLINO,  JogoProxy, f"but self.k.VITOLLINO was {Vazio.VITOLLINO}")
        cena = self.k.cria()
        coisa = self.k.taba[3,3]
        self.assertIsInstance(coisa.ocupante,  Indio, f"but coisa was {coisa}")
        self.assertEquals(100, coisa.lado, f"but coisa.lado was {coisa.lado}")
        indio = self.k.o_indio
        self.assertIsInstance(indio.indio,  JogoProxy, f"but indio was {indio.indio}")
        indio = self.elts[self.INDIO]
        self.assertEquals(coisa.ocupante.indio.elt, indio, f"but coisa.ocupante.indio was {coisa.ocupante.indio.elt}")
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
    
    def testa_cria_jogo_proxy_from_main(self):
        """Cria um proxy para o Elemento Jogo usando o main"""
        # JogoProxy.COMANDOS, JogoProxy.ATIVA = [], False
        krp = main(self.v)
        cena = krp.cria()
        self.assertEquals(0, len(JogoProxy.COMANDOS), f"mas a pilha era {JogoProxy.COMANDOS}")
        vaga_oca = krp.taba[5, 0]
        oca = self.elts[self.OCA]
        self.assertIsInstance(vaga_oca.ocupante,  Oca, f"but vaga_oca was {vaga_oca.ocupante}")
        self.assertEquals(vaga_oca.vazio.elt.destino, oca, f"but vaga_oca.vazio was {vaga_oca.vazio.elt.destino}")
        vaga_piche = krp.taba[0, 0]
        piche = self.elts[self.PICHE]
        self.assertIsInstance(vaga_piche.ocupante,  Piche, f"but vaga_piche was {vaga_piche.ocupante}")
        self.assertEquals(vaga_piche.vazio.elt.destino, piche, f"but vaga_piche.vazio was {vaga_piche.vazio.elt.destino}")
    
    def testa_cria_jogo_proxy(self):
        """Cria um proxy para o Elemento Jogo"""
        x = JogoProxy(vitollino=self.v())
        cena = x.c("_IMAGEM_")
        self.assertIn("Vitollino_cria", str(cena.name))
        elt = x.a("_IMAGEM_ELT_", x=999, cena=cena)
        self.assertIsInstance(elt.elt, self.e)
        self.assertEquals(999, self.elts["_IMAGEM_ELT_"].x)
        self.assertEquals(cena, self.elts["_IMAGEM_ELT_"].cena)
    
    def testa_kwarwp_com_jogo_proxy(self):
        """Cria kwarwp com um proxy para o Elemento Jogo"""
        x = JogoProxy(vitollino=self.v())
        krp = Kwarwp(x.cria)
        cena = krp.cria()
        self.assertIn("Vitollino_cria",  str(cena), cena)
        self.assertIn(self.INDIO, self.elts)
        
    def testa_cria_piche_oca_proxy(self):
        """ Cria o piche e a oca com a fábrica e jogo proxy."""
        JogoProxy.COMANDOS, JogoProxy.ATIVA = [], False
        x = JogoProxy(vitollino=self.v())
        z = len(x.COMANDOS)
        # [x.COMANDOS.pop() for _ in range(z)]
        krp = Kwarwp(x.cria)
        cena = krp.cria()
        self.assertEquals(0, len(x.COMANDOS), f"mas a pilha era {x.COMANDOS}")
        vaga_oca = krp.taba[5, 0]
        oca = self.elts[self.OCA]
        self.assertIsInstance(vaga_oca.ocupante,  Oca, f"but vaga_oca was {vaga_oca.ocupante}")
        self.assertEquals(vaga_oca.vazio.elt.destino, oca, f"but vaga_oca.vazio was {vaga_oca.vazio.elt.destino}")
        vaga_piche = krp.taba[0, 0]
        piche = self.elts[self.PICHE]
        self.assertIsInstance(vaga_piche.ocupante,  Piche, f"but vaga_piche was {vaga_piche.ocupante}")
        self.assertEquals(vaga_piche.vazio.elt.destino, piche, f"but vaga_piche.vazio was {vaga_piche.vazio.elt.destino}")
        JogoProxy.COMANDOS = []

    def testa_empilha_ocupa_jogo_proxy(self):
        """Empilha um comando de ocupa no proxy para o Elemento Jogo"""
        x = JogoProxy(vitollino=self.v())
        y = JogoProxy(vitollino=self.v(), proxy=x)
        # x.COMANDOS = x.comandos
        z = len(x.comandos)
        [x.comandos.pop() for _ in range(z)]
        y.ativa()
        # self.assertEquals(x.lidar, x._enfileira, f"mas o lidar era {x.lidar}")
        # x.COMANDOS = []
        # x.COMANDOS = x.comandos
        cena = x.c("_IMAGEM_")
        self.assertIn("Vitollino_cria", str(cena.name))
        vag = y.a("_IMAGEM_VAGA_", x=998, cena=cena)
        el0 = y.e("_IMAGEM_OCUPA0_", x=997, cena=cena)
        el1 = y.a("_IMAGEM_OCUPA1_", x=997, cena=cena)
        self.assertIsInstance(vag.elt, self.e)
        # y.executa()
        vag.ocupa(el0)
        self.assertIsInstance(vag, JogoProxy)
        self.assertEquals(1, len(y.comandos), f"mas a pilha era {y.comandos}")
        self.assertEquals(vag.corrente, y, f"mas x corrente era {vag.corrente}")
        vag.ocupa(el1)
        self.assertEquals(2,  len(y.comandos))
        y.executa()
        self.assertEquals(1, len(y.comandos), f"mas a pilha ficou {y.comandos}")
        self.assertEquals(el0.elt,  vag.elt.destino)
        y.executa()
        self.assertEquals(0, len(y.comandos), f"mas a pilha ficou ainda {y.comandos}")
        self.assertEquals(el1.elt,  vag.elt.destino)
        
    def testa_avanca_passo_a_passo(self):
        """Avança a execução do roteiro do índio passo a passo."""
        num_comandos = 10
        krp = mn(self.v, {})
        self.assertIn(self.INDIO, self.elts)
        self.assertIn(self.INDIA, self.elts)
        io, ia = krp.os_indios
        x = io.indio
        self.assertEquals(0, len(x.COMANDOS), f"mas a pilha era {x.COMANDOS}")
        indio = io #krp.o_indio
        self.assertIsInstance(indio.indio, JogoProxy)
        pos = indio.posicao
        self.assertEquals((3, 3),  pos, f"but original pos was {pos}")
        cena = krp.executa()
        self.assertEquals(num_comandos, len(x.comandos), f"mas a pilha era {x.comandos}")
        self.assertIn("JogoProxy.pos.", str(x.comandos[0]), f"mas a pilha tinha {x.comandos[0]}")
        vaga = krp.taba[3, 3]
        self.assertEquals(vaga.vazio.elt.destino,  indio.indio.elt, f"but vaga was {vaga.vazio.elt.destino}")
        sprite = indio.indio.pos
        self.assertIsInstance(indio.indio.elt.elt, self.e, f"mas a indio2.elt2 era {indio.indio.elt.elt}")
        self.assertEquals(indio.indio.pos, (0, 0), f"mas a vaga era {indio.indio.pos}")
        self.assertEquals((0, 0),  sprite, f"but previous pos was {sprite}")
        krp.passo()
        self.assertEquals(num_comandos-1, len(x.comandos), f"mas a pilha era {len(x.comandos)}")
        pos = indio.posicao
        self.assertEquals((1, 0),  pos, f"but last pos was {pos}")
        self.assertEquals(vaga.vazio.elt.destino,  indio.indio.elt, f"but vaga was {vaga.vazio.elt.destino}")
        krp.passo()
        pos = indio.posicao
        vaga = krp.taba[2, 3]
        self.assertEquals((1, 0),  pos, f"but last pos was {pos}")
        self.assertEquals(vaga.vazio.elt.destino,  indio.indio.elt, f"but vaga was {vaga.vazio.elt.destino}")

if __name__ == "__main__":
    from unittest import main
    main()
