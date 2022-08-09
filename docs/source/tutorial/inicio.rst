.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tela Inicial
===============

Nesta tela vamos montar um simulacro do primeiro desafio kwarwp.

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

Este tutorial ensina passo a passo a criação de um Ambiente de desenvolvimento na WEB, o qual funcionará no navegador Firefox. 
O código abaixo montará a cena inicial com os elementos: Índio, Oca, Tora e Piche.

.. code:: python
  
  class Kwarwp():
      """ Jogo para ensino de programação.

          :param vitollino: Empacota o engenho de jogo Vitollino.
      """
      OCA = "https://i.imgur.com/dZQ8liT.jpg"
      INDIO = "https://imgur.com/8jMuupz.png"
      SOLO = "https://i.imgur.com/sGoKfvs.jpg"
      TORA = "https://imgur.com/ldI7IbK.png"
      PICHE = "https://imgur.com/tLLVjfN.png"
      CEU = "https://i.imgur.com/UAETaiP.gif"
      SOL = "https://i.imgur.com/PfodQmT.gif"

      def __init__(self, vitollino=None, cenario="default"):
          self.v = vitollino()
          self.cena = self.cria(cenario=cenario) if vitollino else None

      def cria(self, cenario="default"):
          """ Cria o ambiente de programação Kwarwp."""
          cena = self.v.c(self.SOLO)
          indio = self.v.a(self.INDIO, w=100, h=100, x=300, y=400, cena=cena)
          oca = self.v.a(self.OCA, w=100, h=100, x=500, y=100, cena=cena)
          tora = self.v.a(self.TORA, w=100, h=100, x=100, y=400, cena=cena)
          piche = self.v.a(self.PICHE, w=100, h=100, x=100, y=100, cena=cena)
          piche = self.v.a(self.CEU, w=600, h=100, x=0, y=0, cena=cena)
          sol = self.v.a(self.SOL, w=60, h=60, x=0, y=40, cena=cena)
          cena.vai()
          return cena

  
Tela Gerada
------------

.. image:: https://i.imgur.com/iRaafk8.png
   :height: 200
   :width: 200
   :scale: 50
   :alt: Tela inicial do Kwarwp
   :align: center


Complementação do Código
------------------------

Se usado outro navegador, a cena só aparecerá com o acréscimo da linha abaixo 
antes da declaração da classe Kwarwp.

.. code:: python

  from _spy.vitollino.main import Cena, STYLE
  """Importa os compenentes Cena e STYLE do Vitollino""" 

  class Kwarwp():
  . . .

E também com o acréscimo das linhas abaixo no final do código, com indentação alinhada à declaração da classe Kwarwp.

.. code:: python  
  
  if __name__ == "__main__":
    from _spy.vitollino.main import Jogo
    STYLE["width"]=600
    STYLE["height"]=500
    Kwarwp(Jogo) 

