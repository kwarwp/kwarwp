.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _adicionando_indio:

Adicionando o Indio
===================

Para melhorar o nosso jogo kwarwp, teremos que fazer o índio executar coisas guiadas pela programação.
Precisamos agora ter uma classe Indio, para que ela possa executar os comandos.
Neste exercício só iremos separar a construção do índio, usando uma classe para isso.
No momento o índio não apresenta nenhum comportamento especial, foi somente uma refatoração.
Este código é uma modificação do código descrito em :ref:`usando_mapa`

.. note ::

 Refatoração (do inglês Refactoring) é o processo de modificar um sistema de software para melhorar a estrutura interna do código sem alterar seu comportamento externo.

 O uso desta técnica aprimora a concepção (design) de um software e evita a deterioração tão comum durante o ciclo de vida de um código. Esta deterioração é geralmente causada por mudanças com objetivos de curto prazo ou por alterações realizadas sem a clara compreensão da concepção do sistema.

 Outra consequência é a melhora no entendimento do código, o que facilita a manutenção e evita a inclusão de defeitos. Esta melhora no entendimento vem da constante alteração do código com objetivo de facilitar a comunicação de motivações, intenções e objetivos por parte do programador. 

 A refatoração é comumente feita quando se vai criar novas funcionalidades no código. 
 O código é preparado para que as novidades sejam incorporadas da melhor maneira,
 sem perturbar ou incluir códigos confusos.

 Wikipedia_

.. _Wikipedia : https://pt.wikipedia.org/wiki/Refatoração


Classe Indio
------------

Com esta classe vamos separar o índio dos outros elementos da tela.
Com isso poderemos colocar funcionalidades nela que os outros não tem.

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

Classe Kwarwp
-------------

Vamos começar melhorando a classe Kwarwp, aplicando nela o conceito de fábrica.
A fábrica constrói um componente segundo a especicificação dada.
No nosso caso temos um símbolo que identifica o componenete no mapa.
Este símbolo nos diz que tipo de objeto tem ali e também qual é a imagem
que deve representar este objeto.

Jogo para ensino de programação.
      
   :param vitollino: Empacota o engenho de jogo Vitollino.
   :param mapa: Um texto representando o mapa do desafio.
   :param medidas: Um dicionário usado para redimensionar a tela.

.. code :: python

   class Kwarwp():
      VITOLLINO = None
      """Referência estática para obter o engenho de jogo."""
      LADO = None
      """Referência estática para definir o lado do piso da casa."""
      
      def __init__(self, vitollino=None, mapa=MAPA_INICIO, medidas={}):
         Kwarwp.VITOLLINO = self.v = vitollino()
         """Cria um matriz com os elementos descritos em cada linha de texto"""
         self.mapa = mapa.split()
         """Largura da casa da arena dos desafios, número de colunas no mapa"""
         self.lado, self.col, self.lin = 100, len(self.mapa[0]), len(self.mapa)+1
         Kwarwp.LADO = self.lado
         w, h = self.col *self.lado, self.lin *self.lado
         self.taba = {}
         """Dicionário que a partir de coordenada (i,J) localiza um piso da taba"""
         medidas.update(width=w, height=f"{h}px")
         self.cena = self.cria(mapa=self.mapa) if vitollino else None

Método Cria
-------------

Este método define uma fábrica de componentes.
         
   :param mapa: Um texto representando o mapa do desafio.

.. code :: python

      def cria(self, mapa=""):

.. note ::

 O Python suporta um tipo de contêiner como dicionários chamado “namedtuples ()” presente no módulo, “coleções”.
 Como dicionários, eles contêm chaves com hash para um valor específico.
 Mas, pelo contrário, suporta o acesso a partir do valor-chave e da iteração, a funcionalidade que falta nos dicionários.
 Uma tupla nomeada assume o formato **nome_tupla = namedtuple("nome_tupla", "nome dos campos separados por branco")**

 Operações em namedtuple ():
   Operações de acesso

      1. Acesso por índice: os valores de atributo de namedtuple () são ordenados e podem ser acessados usando o número do índice, diferentemente dos dicionários que não são acessíveis pelo índice.

      2. Acesso por nome da chave: O acesso por nome da chave também é permitido como nos dicionários.

      3. usando getattr (): - Essa é outra maneira de acessar o valor, fornecendo o valor nomeado de parâmetro e chave como argumento.

 GeeksForGeeks-Namedtuple_

.. _GeeksForGeeks-Namedtuple: https://www.geeksforgeeks.org/namedtuple-in-python/

Esta tupla nomeada serve para definir o objeto construido e sua imagem.
    :nome Fab: O nome da tupla que descreve a fábrica.
    :campo objeto: O tipo de objeto que vai ser criado.
    :campo imagem: A imagem que representa o objeto que vai ser criado.

.. code :: python

         from collections import namedtuple as nt
         Fab = nt("Fab", "objeto imagem")

O atributo **fabrica** é um dicionário que relaciona o símbolo no mapa com a fábrica necessária para criar o componente.

Dicionário que define o tipo e a imagem do objeto para cada elemento.

.. code :: python

         fabrica = {
         "&": Fab(self.coisa, f"{IMGUR}dZQ8liT.jpg"), # OCA
         "^": Fab(self.indio, f"{IMGUR}8jMuupz.png"), # INDIO
         ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
         "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
         "#": Fab(self.coisa, f"{IMGUR}ldI7IbK.png"), # TORA
         "@": Fab(self.coisa, f"{IMGUR}tLLVjfN.png"), # PICHE
         "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
         "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
         "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA
         }

Cria um cenário com imagem de terra de chão batido, céu e sol.
O mapa pode pode ser o definido no argumento ou atributo da instância do Kwarwp.

.. code :: python

         mapa = mapa if mapa != "" else self.mapa

         mapa = self.mapa
         lado = self.lado
         cena = self.v.c(fabrica["_"].imagem)
         ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado, x=0, y=0, cena=cena)
         sol = self.v.a(fabrica["*"].imagem, w=60, h=60, x=0, y=40, cena=cena)

Cria um cenário com imagem de terra de chão batido, céu e sol.
O mapa pode pode ser o definido no argumento ou atributo da instância do Kwarwp.
Esta construção é uma compreensão de dicionário que posiciona os elementos
segundo suas posições i, j na matriz mapa

.. note ::

 Como a compreensão de lista, o **Python** permite a compreensão de dicionário.
 Podemos criar dicionários  usando expressões simples.
 Uma compreensão de dicionário assume o formato **{key: value for (key, value) em iterável}**

 GeeksForGeeks_Dict_Comprenension_

.. _`GeeksForGeeks_Dict_Comprenension`: https://www.geeksforgeeks.org/python-dictionary-comprehension/

.. code :: python

         self.taba = {(i, j): fabrica[imagem].objeto(
               fabrica[imagem].imagem, x=i*lado, y=j*lado+lado, cena=cena)
               for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)}

         cena.vai()
         return cena
         
Métodos Fabricantes - Coisa
-----------------------------

Este método define uma fábrica para coisas que estão no cenário.
         
               :param imagem: imagem que representa o elemento que será posicionado.
               :param x: coluna em que o elemento será posicionado.
               :param y: linha em que o elemento será posicionado.
               :param cena: cena em que o elemento será posicionado.

Cria um elemento na arena do Kwarwp na posição definida.

.. code :: python

      def coisa(self, imagem, x, y, cena):
         lado = self.lado
         return self.v.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)

Métodos Fabricantes - Indio
-----------------------------

Este método define uma fábrica criando o índio o personagem principal.
         
               :param imagem: imagem que representa o elemento que será posicionado.
               :param x: coluna em que o elemento será posicionado.
               :param y: linha em que o elemento será posicionado.
               :param cena: cena em que o elemento será posicionado.

Cria o personagem principal na arena do Kwarwp na posição definida.
Em vez de criar diretamente um elemento do Vitollino, cria uma classe
para lidar com o componente e seu comportamento distinto.

.. code :: python

      def indio(self, imagem, x, y, cena):
         lado = self.lado
         return Indio(imagem, x=x, y=y, cena=cena)

