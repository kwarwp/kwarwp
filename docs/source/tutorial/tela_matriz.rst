.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Usando um Mapa
===============

Nesta tela vamos montar um simulacro do primeiro desafio kwarwp.
O desafio será montado a partir de um mapa com símbolos.

.. note::
    Nesta versão estamos usando um componente especial do vitollino o **Jogo**. 
    O Jogo é uma fábrica de componentes **Vitollino**, retorna um componente construído 
    com os mesmos parâmetros de chamada de um compnente original. Veja alguns métodos
    usados no exemplo abaixo
    
    
Chamadas do Jogo
----------------

Jogo.c:
  Equivale a chamar uma Cena importada do Vitollino

Jogo.a: 
  Equivale a chamar um Elemento importado do Vitollino

Código Fonte
------------

Aqui especificamos um mapa que orienta a construção da arena. 
Cada símbolo representa um elemento, definido a seguir
num dicionário de imagens dos elementos.



.. code:: python

  MAPA_INICIO = """
  @....&
  ......
  ......
  .#.^..
  """


Arena onde os desafios ocorrem.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Esta versão recebe como parâmetro um mapa que define a montagem da arena.

   :param vitollino: Empacota o engenho de jogo Vitollino.
   :param mapa: Um texto representando o mapa do desafio.


.. code:: python

  class Kwarwp():
    ...

Esta versão usa um dicionário para guardar as imagens dos elementos.

.. code:: python

      GLIFOS = {
      "&": "https://i.imgur.com/dZQ8liT.jpg",  # OCA ⛺
      "^": "https://imgur.com/8jMuupz.png",  # INDIO 🧍
      ".": "https://i.imgur.com/npb9Oej.png",  # VAZIO 🗌
      "_": "https://i.imgur.com/sGoKfvs.jpg",  # SOLO 🛏️
      "#": "https://imgur.com/ldI7IbK.png",  # TORA 💈
      "@": "https://imgur.com/tLLVjfN.png",  # PICHE 🕳️
      "~": "https://i.imgur.com/UAETaiP.gif",  # CEU 🌌
      "*": "https://i.imgur.com/PfodQmT.gif"  # SOL ☀️
      }


A arena é construída a partir da matriz textual **mapa** dada. O atributo **lado** define a largura e altura .

.. code:: python

      def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
          self.v = vitollino()
          """Cria um matriz com os elementos descritos em cada linha de texto"""
          mapa = mapa.split()
          """Largura da casa da arena dos desafios, número de colunas no mapa"""
          self.lado, self.col = 100, len(mapa[0]) 
          self.cena = self.cria(mapa=mapa) if vitollino else None


A arena é construída a partir da matriz usando uma **list comprehension** .

.. code:: python

      def cria(self, mapa="  "):
      
Cria o ambiente de programação Kwarwp.

  :param mapa: Um texto representando o mapa do desafio.

.. code:: python

          """Cria um cenário com imagem de terra de chão batido, céu e sol"""
          lado = self.lado
          cena = self.v.c(self.GLIFOS["_"])
          ceu = self.v.a(self.GLIFOS["~"], w=lado*self.col, h=lado, x=0, y=0, cena=cena)
          sol = self.v.a(self.GLIFOS["*"], w=60, h=60, x=0, y=40, cena=cena)
      
A construção entre chaves **[]** é chamada **list comprehension**.
Neste caso usamos intenamente duas iterações, uma para as linhas e outras para as colunas.
Tabém estamos usando a função embutida **enumerate()**. Esta função pega uma lista e retorna
outra lista, mas contendo tuplas onde o primeiro elemento é o índice do elemento original
e o outro é o elemento original.
.
Posiciona os elementos segundo suas posições i, j na matriz mapa

.. code:: python
          
          [self.cria_elemento( x=i*lado, y=j*lado+lado, cena=cena)
              for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)]
          cena.vai()
          return cena
          
Cria um elemento na arena do Kwarwp na posição definida.

  :param x: coluna em que o elemento será posicionado.
  :param y: linha em que o elemento será posicionado.
  :param cena: cena em que o elemento será posicionado.

.. code:: python

      def cria_elemento(self, x, y, cena):
          lado = self.lado
          return self.v.a(self.GLIFOS[imagem], w=lado, h=lado, x=i*lado, y=j*lado+lado, cena=cena)

Tela Gerada
------------

.. image:: https://i.imgur.com/iRaafk8.png
   :height: 600
   :width: 600
   :scale: 50
   :alt: Tela inicial do Kwarwp
   :align: center

