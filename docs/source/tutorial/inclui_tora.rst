.. Jogo para ensino de programação Python.
    Changelog
    ---------
    .. versionadded::    20.08.b0
        Inclui fabricação da Tora e protocolo pega e larga no Indio.



.. _inclui_tora:

Incluindo a Tora
===================

Para incluir a Tora, decidimos repartir o módulo com um outro, o **kwarwp.kwarwpart**


Neste tutorial incuímos uma nova classe e seus comportamentos, a **Tora**.
Ela tem comportamento que se assemelham ao **Vazio** e usaremos a herança.


.. seealso::
 Este código é uma modificação do código descrito em :ref:`melhora_indio`.
 O código da classe Tora pode ser visto em :ref:`tora_partes`.

Importando o Módulo Kwarwpart
-----------------------------

As várias partes do jogo foram transferidas  para outro módulo.
Para podermos usar neste módulo teremos que importar.

.. code :: python

    from collections import namedtuple as nt
    from kwarwp.kwarwpart import Vazio, Piche, Oca, Tora, NULO

    IMGUR = "https://imgur.com/"
    """Prefixo do site imgur."""
    MAPA_INICIO = """
    @....&
    ......
    ......
    .#.^..
    """

Classe Indio - Pega e Larga 
-----------------------------

Cria o personagem principal na arena do Kwarwp na posição definida.

   :param imagem: A figura representando o índio na posição indicada.
   :param x: Coluna em que o elemento será posicionado.
   :param y: Linha em que o elemento será posicionado.
   :param cena: Cena em que o elemento será posicionado.
   :param taba: Representa a taba onde o índio faz o desafio.

.. code :: python

    AZIMUTE = Rosa(Ponto(0, -1),Ponto(1, 0),Ponto(0, 1),Ponto(-1, 0),)
    """Constante com os pares ordenados que representam os vetores unitários dos pontos cardeais."""
    
    def __init__(self, imagem, x, y, cena, taba):
        self.lado = lado = Kwarwp.LADO
        self.azimute = self.AZIMUTE.n
        """índio olhando para o norte"""
        self.taba = taba
        self.vaga = self
        self.posicao = (x//lado,y//lado)
        self.indio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        self.x = x
        """Este x provisoriamente distingue o índio de outras coisas construídas com esta classe"""
        if x:
            self.indio.siz = (lado*3, lado*4)
            """Define as proporções da folha de sprites"""
            self.mostra()


Interação do Índio com a Tora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **pega ()** é usado pelo índio para adquirir  e carregar a tora.
O método **pega ()** invoca sua contrapartida **pegar ()** na instância de **Tora**.
A tora responde à requisição invocando **ocupar ()** no **Indio**.

O método **larga ()** invoca **acessa ()** na instância de **Vaga** onde
a Tora deve ser colocada, mas passa como parâmetro o ocupante em vez
de si próprio. De resto é executado o double dispatch como no anda,
sendo que "andarilho" é a **Tora**.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`melhora_indio`.
 O código da classe **Tora** e o diagrama do protocolo podem ser visto em :ref:`tora_tronco`.

.. code :: python

    def pega(self):
        """tenta pegar o objeto que está diante dele"""
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """A posição para onde o índio vai depende do vetor de azimute corrente"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            vaga.pegar(self)

    def larga(self):
        """tenta largar o objeto que está segurando"""
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """A posição para onde o índio vai depende do vetor de azimute corrente"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            # self.ocupante.largar(vaga)
            vaga.acessa(self.ocupante)
 
    def ocupou(self, ocupante):
        """ O candidato à vaga decidiu ocupá-la e efetivamente entra neste espaço.
        
        :param ocupante: O canditato a ocupar a posição corrente.
        
        Este ocupante vai entrar no elemento do Vitollino e definitivamente se tornar
        o ocupante da vaga. Com isso ele troca o estado do método acessa para primeiro
        consultar a si mesmo, o ocupante corrente usando o protocolo definido em
        **_valida_acessa ()**

        """
        self.indio.ocupa(ocupante)
        self.ocupante = ocupante


Kwarwp - Tora
--------------------

A classe Kwarwp vai ser modificada para agregar novas fábricas.
Teremos a construção de instância de :ref:`tora_tronco` como uma
nova fábrica definida em `Fabricando a Tora`_.


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
 Veja o código anterior da classe no tutorial :ref:`melhora_indio`    

Dicionário com Tora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **cria ()** define as fábricas de componentes.

No dicionário pode se ver que **"#"** agora remete ao 
método fábrica **atora ()** que é explicado em `Fabricando a Tora`_.

       
    :param mapa: Um texto representando o mapa do desafio.

.. code :: python
        

    def cria(self, mapa=""):
        """ Fábrica de componentes.
        
        :param mapa: Um texto representando o mapa do desafio.
        """
        Fab = nt("Fab", "objeto imagem")
        """Esta tupla nomeada serve para definir o objeto construido e sua imagem."""

        fabrica = {
        "&": Fab(self.maloc, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}UCWGCKR.png"), # INDIO
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.atora, f"{IMGUR}0jSB27g.png"), # TORA
        "@": Fab(self.barra, f"{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA       
        }
        ... # ver tutorial anterior

Fabricando a Tora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **atora ()** invoca a criação da :ref:`tora_tronco`.
No **Vitollino**, um clique no elemento invoca o seu  método **vai ()**.
Neste método mostramos a associação do clique da tora com o **larga ()**
do **Indio**, associando uma função **lambda** com o vai do índio.
O **lambda** é um método anônimo para encapsular a
chamada do larga sem que ele seja invocado imediatamente.

A mesma manobra foi feita com o índio associando o clique nele
com o seu próprio método **pega ()**

.. code :: python
        
    def atora(self, imagem, x, y, cena):
        """ Cria uma tora na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Tora(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        coisa.vazio.vai = lambda *_: self.o_indio.larga()
        """o vazio.vai é associado ao método larga do índio"""
        return vaga
        
    def indio(self, imagem, x, y, cena):
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        self.o_indio = Indio(imagem, x=1, y=0, cena=cena, taba=self)
        """ O índio tem deslocamento zero, pois é relativo à vaga.
            O **x=1** serve para distinguir o indio de outros derivados.
        """
        self.o_indio.indio.vai = lambda *_: self.o_indio.pega()
        """o índio.vai é associado ao seu próprio metodo pega"""
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=self.o_indio)
        return vaga

.. _`duplo despacho`: http://www.dpi.ufv.br/projetos/apri/?page_id=726
.. _`estado de objeto`: http://www.dpi.ufv.br/projetos/apri/?page_id=745
