.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _melhora_indio:

Melhorando o Índio
===================

O movimento do índio pode melhorar, podendo dobrar à esquerda e direita.

Para direcionar o índio, modificamos o método **anda ()** para considerar a direção.
Adicionamos `Os Métodos Esquerda, Direita e Mostra`_


.. seealso::
 Este código é uma modificação do código descrito em :ref:`organiza_taba`

Classe Indio - Novos Comandos 
=============================

Cria o personagem principal na arena do Kwarwp na posição definida.

   :param imagem: A figura representando o índio na posição indicada.
   :param x: Coluna em que o elemento será posicionado.
   :param y: Linha em que o elemento será posicionado.
   :param cena: Cena em que o elemento será posicionado.

.. code :: python

    class Indio():
      
        def __init__(self, imagem, x, y, cena):
            self.lado = lado = Kwarwp.LADO
            self.indio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
            self.vaga = self
            self.posicao = (x//lado,y//lado)
            self.indio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)

Os Métodos Esquerda, Direita e Mostra
-------------------------------------

Este método foi modificado para procurar na taba um vazio adjacente

.. code :: python
       
    def mostra(self):
        """ Modifica a figura (Sprite) do índio mostrando para onde está indo.
        """
        sprite_col = sum(self.posicao) % 3
        """Faz com que três casas adjacentes tenha valores diferentes para a coluna do sprite"""
        sprite_lin = self.AZIMUTE.index(self.azimute)
        """A linha do sprite depende da direção dque índio está olhando"""
        self.indio.pos = (-self.lado*sprite_col, -self.lado*sprite_lin)
       
    def esquerda(self):
        """ Faz o índio mudar de na direção em que está olhando para a esquerda.
        """
        self.azimute = self.AZIMUTE[self.AZIMUTE.index(self.azimute)-1]
        self.mostra()
       
    def direita(self):
        """ Faz o índio mudar de na direção em que está olhando para a direita.
        """
        self.azimute = self.AZIMUTE[self.AZIMUTE.index(self.azimute)-3]
        self.mostra()

Kwarwp - Fabricando Vagas
=========================

A classe Kwarwp vai ser modificada para que na fábrica seja sempre criado um **Vazio**.
Neste vazio, o objeto a ser posicionado é alocado nesta vaga do local vazio.

Jogo para ensino de programação.
      
   :param vitollino: Empacota o engenho de jogo Vitollino.
   :param mapa: Um texto representando o mapa do desafio.
   :param medidas: Um dicionário usado para redimensionar a tela.

.. code :: python

   class Kwarwp():
      VITOLLINO = None
      ...
      self.o_indio = None
      """Instância do personagem principal, o índio, vai ser atribuído pela fábrica do índio"""
      ...

.. seealso::
 Veja o código anterior da classe no tutorial :ref:`movendo_indio`    

Vagas nas Fábricas de Componentes
---------------------------------

Estes método definen fábricas de componentes.
         
    :param x: coluna em que o elemento será posicionado.
    :param y: linha em que o elemento será posicionado.
    :param cena: cena em que o elemento será posicionado.

.. code :: python
        
    def coisa(self, imagem, x, y, cena):
        """ Cria um elemento na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Indio(imagem, x=0, y=0, cena=cena, taba=self)
        """o índio tem deslocamento zero, pois é relativo à vaga"""
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        """Aqui o índio está sendo usado para qualquer objeto, enquanto não tem o próprio"""
        return vaga
        
    def vazio(self, imagem, x, y, cena):
        """ Cria um espaço vazio na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        vaga = Vazio(imagem, x=x, y=y, cena=cena, ocupante=self)
        """ O Kwarwp é aqui usado como um ocupante nulo, que não ocupa uma vaga vazia."""
        return vaga
        
    def indio(self, imagem, x, y, cena):
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        # self.o_indio = Indio(imagem, x=x, y=y, cena=cena)
        self.o_indio = Indio(imagem, x=0, y=0, cena=cena, taba=self)
        """o índio tem deslocamento zero, pois é relativo à vaga"""
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=self.o_indio)
        return vaga

Ocupante nulo
-------------

O Kwarwp é aqui usado como um ocupante `objeto nulo`_, usado ao fabricar espaços vazios
O pedido de ocupar é ignorado.

.. code :: python
       
    def ocupa(self, *_):
        """ O Kwarwp é aqui usado como um ocupante falso, o pedido de ocupar é ignorado.
        """
        pass

.. _`objeto nulo`: https://www.thiengo.com.br/padrao-de-projeto-objeto-nulo

