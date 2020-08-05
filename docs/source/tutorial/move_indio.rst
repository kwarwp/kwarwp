.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _movendo_indio:

Movendo o Indio
===================

Para mover o índio, adicionamos o método **anda ()** na sua classe. No Kwarwp original,
havia um método que executava o roteiros de comandos programado pelo usuário. 
Colocamos então um método **executa ()** que vai conter estes comandos.
Também no jogo original bastava clicar no céu para executar os comandos.
Programamos então um enlace do evento clique com método executa.
No caso, o **ceu** pertence à classe Kwarwp então criamos um método **executa ()**
na classe Kwarwp e chamamos o respectivo método do índio, **self.o_indio.executa ()**.
No momento o índio só apresenta o comportamento de andar.
Este código é uma modificação do código descrito em :ref:`adicionando_indio`

Classe Indio
------------

Com esta classe vamos separar o índio dos outros elementos da tela.
Com isso poderemos colocar funcionalidades nela que os outros não tem.
No momento o índio tem o método :py:meth:`kwarwp.kwarapp.Indio.anda` que movimenta
o personagem na direção que está olhando. O método :py:meth:`kwarwp.kwarapp.Indio.executa`
contém o conjunto de comandos que dever ser executados para resolver 
o desafio.

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

Método Anda
-------------

Este método define um comportamento que faz o personagem andar
na direção para onde está olhando.

.. code :: python

        
   def anda(self):
      """ Faz o índio caminhar na direção em que está olhando.
      """
      self.posicao = (self.posicao[0], self.posicao[1]-1)
      """Assumimos que o índio está olhando para cima, decrementamos a posição **y**"""
      self.indio.y = self.posicao[1]*self.lado
      self.indio.x = self.posicao[0]*self.lado

Método Executa
--------------

Este método define um roteiro do comportamento que o personagem
vai executar.

.. code :: python

   def executa(self):
      """ Roteiro do índio. Conjunto de comandos para ele executar.
      """
      self.anda()


Kwarwp - Enlace do Céu
----------------------

A classe Kwarwp vai ter um enlace que liga o clique no céu
com o chamado do roteiro de execuções do indio.

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

Veja o código completo no tutorial :ref:`adiciona_cria_indio`    


Enlace no Método Cria
---------------------

Este método define uma fábrica de componentes.
         
   :param mapa: Um texto representando o mapa do desafio.

.. code :: python

      def cria(self, mapa=""):
      ...
      ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado, x=0, y=0, cena=cena, vai= self.executa)
      """No argumento *vai*, associamos o clique no céu com o método **executa ()** desta classe"""
      ...

Delegando a Execução
--------------------

Este método recebe o evento .
         
   :param _: este argumento recebe a estrutura oriunda do evento, o **_** indica que não será usado.

.. code :: python
    
   def executa(self, *_):
      """ Ordena a execução do roteiro do índio.
      """
      self.o_indio.executa()


Atribuindo o Indio na Fábrica
-----------------------------

Este método define uma fábrica criando o índio o personagem principal.
         
   :param imagem: imagem que representa o elemento que será posicionado.
   :param x: coluna em que o elemento será posicionado.
   :param y: linha em que o elemento será posicionado.
   :param cena: cena em que o elemento será posicionado.

Cria o personagem principal na arena do Kwarwp na posição definida.
Em vez de criar diretamente um elemento do Vitollino, cria uma classe
para lidar com o componente e seu comportamento distinto.
O atributo da instância **o_indio** passa a ser uma referência para
uma instância da classe :py:class:`kwarwp.kwarapp.Indio`

.. code :: python

      def indio(self, imagem, x, y, cena):
         self.o_indio = Indio(imagem, x=x, y=y, cena=cena)
         return self.o_indio



