.. Jogo para ensino de programação Python.
    Changelog
    ---------
    .. versionadded::    20.09.a0
        Testes Unitários.

.. _teste_unitario:

Testes Unitários
======================

Os testes unitários procuram aferir a corretude do código, em sua menor fração. 
Em linguagens orientadas a objetos, essa menor parte do código pode ser um método de uma classe. 
Sendo assim, os testes unitários são aplicados a esses métodos, a partir da criação de classes de testes.

.. seealso::
 Você pode aprender mais um pouco em :

 - `Testes Unitários e Python`_
 - `Framework de Testes Unitários`_
 - `Primeiros passos com testes unitários`_

.. _`Testes Unitários e Python`: https://medium.com/mercos-engineering/tutorial-testes-unit%C3%A1rios-e-python-parte-i-bb77182db93f

.. _`Framework de Testes Unitários`: https://docs.python.org/pt-br/3/library/unittest.html

.. _`Primeiros passos com testes unitários`: http://devfuria.com.br/python/tdd-primeiros-passos-com-testes-unitarios/

.. _test_case:

Test Case - Uma Classe com Testes
---------------------------------

Para criar um testcase basta criar uma classe que estende de **unittest.TestCase**.
Os três testes individuais são definidos com métodos cujos nomes começam com as letras test.
Esta convenção na nomenclatura informa o runner a respeitos de quais métodos são, na verdade, testes.

Criando a Classe de Teste
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Basta criar um classe que herde de **unittest.TestCase**

.. code :: python


    from _spy.vitollino.main import Jogo
    from unittest import TestCase
    # from unittest.mock import MagicMock
    from kwarwp.kwarapp import Kwarwp, Indio
    from kwarwp.kwarwpart import Piche, Vazio, Oca, Tora, NULO
    #sys.path.insert(0, os.path.abspath('../../libs'))

    class Test_Kwarwp(TestCase):
        """ Teste do Jogo para ensino de programação.
        
        Vamos aqui definir um conjunto de URLs identificadoras das peças.
        """
        ABERTURA = "https://i.imgur.com/dZQ8liT.jpg"
        INDIO = "https://imgur.com/UCWGCKR.png"
        OCA = "https://imgur.com/dZQ8liT.jpg"
        PICHE = "https://imgur.com/tLLVjfN.png"
        TORA = "https://imgur.com/0jSB27g.png"


Criando o Procedimento de Preparação
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O procedimento de preparação é executado antes de cada teste. Neste procedimento podemos
preparar as condições iniciais que serão resetadas em cada teste. Também podemos criar
objetos instrumentalizados que nos ajude a observar o comportamento do programa.


.. code :: python
    

    class Test_Kwarwp(TestCase):
    # ...
        def setUp(self):
            elts = self.elts = {}
            class FakeTaba:
                """ Permite capturar as chamadas de fala """
                def __init__(self):
                    self.falou = ""
                def sai(self,*_):
                    pass
                def fala(self, falou):
                    self.falou = falou
                    
            self.k = Kwarwp(Jogo)
            self.t = FakeTaba()
            self.LADO = Vazio.LADO


Instrumentalizando Objetos
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Podemos criar objetos instrumentalizados que nos ajude a observar o comportamento do programa.
Contruimos uma classe modificada que permie coletar informações de acontecimentos durante o teste.
Basta injetar este objeto no lugar do verdadeiro e ele se torna um espião.


.. code :: python
    
        
        def set_fake(self):
            """Cria objetos doublê que irão espionar o que estaria sendo feito com os originais."""
            elts = self.elts = {}
            """Coleção de imagens que indicam os Elementos Vitollino que são criados"""
            class FakeCena:
                """Usado para substituir a Cena original do Vitollino"""
                def __init__(self, *_, **__):
                    pass
                def vai(self, *_, **__):
                    pass
                
            class FakeElemento:
                """Usado para substituir o Elemento original do Vitollino
                
                Captura a imagem recebida e coloca na coleção de imagens **self.elts**.
                Também coleta os diversos parâmetros recebidos para que possam ser averiguados.
                """
                def __init__(self, img=0, x=0, y=0, w=0, h=0, vai=None, elts=elts, **kwargs):
                    elts[img] = self
                    """Insere este FakeElemento no dicionário, no verbete indicado pela imagem"""
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
            """Troca o Elemento original pelo fake, na "maternidade""""
            Vazio.VITOLLINO.c = FakeCena
            """Troca a Cena original pelo fake, na "maternidade""""

Aproveitando os Doublês
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vamos criar agora dois testes simples que usarão os objetos instrumentalizados.
Sabemos que se o **FakeElemento** for chamado ele vai registra sua imagem no dicionário **elts**.
Quando o Kwarwp for criado é só checar se as imagens foram parar no dicionário


.. code :: python

    def testa_cria(self):
        """ Cria o ambiente de programação Kwarwp."""
        self.set_fake()
        """instrumentaliza os objetos Vitollino"""
        cena = self.k.cria()
        self.assertIn(self.INDIO, self.elts)
        """Aqui perguntamos se a imagem do índio foi parar no dicionário elts"""

    def testa_cria_indio(self):
        """ Cria o índio com a fábrica."""
        self.set_fake()
        cena = self.k.cria()
        coisa = self.k.taba[3,3]
        """Nesta posição da taba está colocada a vaga que tem o índio.

        É esperado que coisa.ocupante aponte para o índio criado.
        """
        self.assertIsInstance(coisa.ocupante,  Indio, f"but ocupante was {coisa.ocupante}")
        """Queremos saber se o objeto que está nesta vaga é uma instância da classe Indio.

        O terceiro parâmetro é uma mensagem que será enviada se o teste falhar.
        """
        self.assertEqual(100, coisa.lado, f"but coisa.lado was {coisa.lado}")
        indio = self.elts[self.INDIO]
        self.assertEqual(coisa.ocupante.indio, indio, f"but coisa.ocupante.indio was {coisa.ocupante.indio}")
        self.assertEqual((0, 0), indio.pos, f"but indio.pos was {indio.pos}")

Um Teste Mais Elaborado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vamos dispensar os doublês e agora os atores irão atuar na cena de ação.
Testaremos o caso de empurrar a tora contra a parede para ver se ainda
funciona quando tentar empurrar de novo.


.. code :: python
        
    def testa_empurra_tora(self):
        """ Vai até a tora e empurra. O método set_fake não é usado."""
        cena = self.k.cria()
        vaga_tora = self.k.taba[1, 3]
        self.assertEqual(vaga_tora.taba,  self.k, f"but taba was {vaga_tora.taba}")
        tora = vaga_tora.ocupante
        pos = tora.posicao
        self.assertEqual((1, 3),  pos, f"but last pos was {pos}")
        indio = self.k.o_indio
        indio.esquerda()
        indio.anda()  # se posiciona diante da tora
        pos = indio.posicao
        self.assertEqual((2, 3),  pos, f"but indio pos was {pos}")
        vaga = indio.vaga  #  a vaga que o índio estava antes
        indio.empurra()  # agora empurra a tora
        pos = tora.posicao  # a tora estava em (1,3), checar se foi para (0,3)
        self.assertEqual((0, 3),  pos, f"but tora pos was {pos}")
        self.assertEqual(vaga.ocupante,  NULO, f"but vaga ocupante was {vaga.ocupante}")
        """Garantir que a vaga onde o índio estava foi desocupada"""
        vaga = indio.vaga
        indio.empurra()
        pos = tora.posicao #  a tora estava contra a parede, deve permanecer em (0,3)
        self.assertEqual((0, 3),  pos, f"but tora new pos was {pos}")
        self.assertEqual(vaga.ocupante,  indio, f"but vaga new  ocupante {vaga.ocupante}")
        """Garantir que o índio não se mexeu e continua na mesma vaga"""
        vaga = tora.vaga
        indio.pega()
        pos = tora.posicao
        self.assertEqual((1, 3),  pos, f"but tora taken pos was {pos}")
        self.assertEqual(vaga.ocupante,  NULO, f"but vaga taken  ocupante {vaga.ocupante}")
        self.assertEqual(tora.vaga,  indio, f"but tora vaga {tora.vaga}")
        indio.larga()  # larga a tora para ver se não deu um erro
        pos = tora.posicao  # verifica se as posições e as vagas estão ok
        self.assertEqual((0, 3),  pos, f"but tora drop pos was {pos}")
        self.assertEqual(vaga.ocupante,  tora, f"but vaga drop  ocupante {vaga.ocupante}")
        self.assertEqual(tora.vaga,  vaga, f"but tora drop vaga {tora.vaga}")


Executando o Teste
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Vamos construir uma suite de testes com esta classe. 
Para observar os resultados vamos usar o HTMTestRunner.
Esta classe vai apresentar os resultados dos testes em uma tabela.


.. code :: python


    def main():
        import unittest
        import kwarwp.htmlrunner as htmlrun
        suite = unittest.TestLoader().loadTestsFromTestCase(Test_Kwarwp)
        htmlrun.HTMLTestRunner().run(suite)        
        
    if __name__ == "__main__":
        main()

Crie os Seus Próprios Testes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Neste desafio vamos criar uma cobertura para todas as operações do índio no Kwarwp.
Acrescente um teste de cada vez e experimente.


.. code :: python
        
    def testa_cria_piche_oca(self):
        """ Cria o piche e a oca com a fábrica."""
        ...
        
    def testa_cria_tora(self):
        """ Cria a tora com a fábrica."""
        ...

    def testa_pega_tora_elimina_piche(self):
        """ Vai até a tora e pega e usa para eliminar o piche."""
        ...
        
    def testa_pega_tora(self):
        """ Vai até a tora e pega."""
        cena = self.k.cria()
        self._pega_tora()
        
    def testa_larga_tora(self):
        """ Vai até a tora pega e larga."""
        ...
        
      
    def testa_pega_vazio_oca_piche(self):
        """ Vai até a piche, oca e vazio e tenta pegar."""
        ...

    def testa_move_indio(self):
        """ Move o índio, andando em frente."""
        ...

    def testa_prende_indio(self):
        """ Tenta mover o índio, mas fica preso."""
        ...

    def testa_chega_taba_indio(self):
        """ Chega no seu destino, tenta mover o índio, mas fica preso."""
        ...

    def testa_esquerda_indio(self):
        """ Move o índio, andando em frente, esquerda, frente."""
        ...

    def testa_volta_indio(self):
        """ Move o índio, andando em frente, meia volta, frente."""
        ...
