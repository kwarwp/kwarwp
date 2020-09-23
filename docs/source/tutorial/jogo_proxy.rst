.. Jogo para ensino de programação Python.
    Changelog
    ---------
    .. versionadded::    20.09.a1
        Proxy e Command.

.. _jogo_proxy:

Proxy - Passo a Passo
======================

Ao se colocar mais de um comando no método **Indio.executa ()**, todos executam
de imediato e não se observa o que acontece entre a primeira posição do índio e
a última. Para que a execução dos comandos não seja imediata, temos que intermediar
o fornecimento de comandos entre o indio e o vitollino. Para isso usaremos dois padrões
o Proxy e o Command. O Proxy será o intemediário que vai regular o fornecimento dos
comandos ao Vitollino. O Command vai tratar cada comando como um objeto que poderá
ser manipulado pelo Proxy.

Nesta parte do tutorial mostramos uma nova classe e seus comportamentos, a **Tora**.
Ela tem comportamento que se assemelham ao **Vazio** e mais especificamente
ao do seu descendente **Piche** e para isso usaremos a herança.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`tora_partes`.


.. _classe_proxy:

JogoProxy - Intermediando Comandos
-----------------------------------

A classe **JogoProxy** foi criada para estabelecer um controle no uso do **Jogo**
Vitollino. Em vez de enviar os comandos diretamente para o Vitollino, esta classe tem um
buffer que vai armazenando todos os comandos. Quando se quer executar um comando, um clique
retira um comando do buffer e o executa.

Como a classe **Jogo** no vitolino implementa o padrão fábrica, **JogoProxy** també é uma fábrica
criando proxies para **Cena** e **Elemento** invocados por **Jogo.c** e **Jogo.a**. Para facilitar
a implementação da fila de comandos foi acrescentado um **JogoProxy.e** que sinaliza que este será
o dono da fila de comandos.

A fila de comandos guarda uma coleção de objetos do padrão command. No entanto, devido ao fato
de que toda função ou método no Python é um objeto, nenhuma infraestrutura extra é nescessária,
o pŕoprio método é guardado na fila de comandos.

.. mermaid ::

    sequenceDiagram
        participant Kwarwp
        participant Indio
        participant JogoProxy
        participant [JP].comandos
        Kwarwp->>Indio: Indio() 
        Indio->>JogoProxy: JogoProxy.e # pede para sair
        Note left of JogoProxy: Proxy de <br/>Elemento
        Kwarwp->>Indio: executa
        Indio->>JogoProxy: ocupa
        JogoProxy->>[JP].comandos: enfileira
        Note right of JogoProxy: Enfileira <br/>um comando
        Kwarwp->>Indio: passo 
        Indio->>JogoProxy: passo
        Note right of JogoProxy: pop comando <br/>e executa
        JogoProxy->>[JP].comandos: pop

.. seealso::
 O proxy, fábrica e comando são padrões descritos no livro `Gang of Four`_. Veja os link externos `O Padrão Proxy`_, `Factory Method`_ e `Command`_

.. _`O Padrão Proxy`: https://pt.wikipedia.org/wiki/Proxy_(padr%C3%B5es_de_projeto)
.. _`Factory Method`: https://pt.wikipedia.org/wiki/Factory_Method
.. _`Command`: https://pt.wikipedia.org/wiki/Command
.. _`Gang of Four`: https://pt.wikipedia.org/wiki/Padr%C3%A3o_de_projeto_de_software

.. code :: python

    class JogoProxy():
    """ Proxy que enfileira comandos gráficos.
    
    :param vitollino: Empacota o engenho de jogo Vitollino.
    :param elt: Elemento que vai ser encapsulado pelo proxy.
    :param proxy: Referência para o objeto proxy parente.
    :param master: Determina se este elemento vai ser mestre de comandos.
    """
   
    def __init__(self, vitollino=None, elt=None, proxy=None, master=False):
        class AdaptaElemento(vitollino.a):
            """ Adapta um Elemento do Vitollino para agrupar ocupa e pos.

            """
                
            def ocupa(self, ocupante=None, pos=(0, 0)):
                # super().elt.pos = pos
                #vitollino.a.pos.fset(self, pos)
                ocupante = ocupante or NULO
                ocupante.pos = pos
                # print(f"AdaptaElemento pos: {self.pos}")
                super().ocupa(ocupante) if ocupante else None

        self.v = vitollino
        self.proxy = proxy or self
        self.master = master # or NULO
        self._corrente = self
        self.comandos = []
        self._ativa = False
        """Cria um referência para o jogo do vitollino"""
        self.ae = AdaptaElemento
        """Cria um referência o Adapador de Eelementos"""
        self.elt = elt
        
    @property    
    def siz(self):
        """Propriedade tamanho"""
        return self.elt.siz
        
    def a(self, *args, **kwargs):
        """Método fábrica - Encapsula a criação de elementos
        
        :param args: coleção de argumentos posicionais.
        :param kwargs: coleção de argumentos nominais.
        :return: Proxy para um Elemento construído com estes argumentos.
        
        """
        return JogoProxy(elt=self.ae(*args, **kwargs), vitollino=self.v, proxy=self)
        
    def e(self, *args, **kwargs):
        """Método fábrica - Encapsula a criação de elementos ativos, que executam scripts
        
        :param args: coleção de argumentos posicionais.
        :param kwargs: coleção de argumentos nominais.
        :return: Proxy para um Elemento construído com estes argumentos.
        
        """
        return JogoProxy(elt=self.ae(*args, **kwargs), vitollino=self.v, proxy=self, master=True)
        
    def cria(self):
        """Fábrica do JogoProxy"""
        return self
    
    @property    
    def corrente(self):
        """Retorna o proxy master acertado no parente"""
        return self.proxy._corrente

    @corrente.setter
    def corrente(self, mestre):
        """Estabelece o proxy master"""
        self._corrente = mestre
        
    def ativa(self):
        """Ativa bufferização do JogoProxy"""
        # JogoProxy.ATIVA = True
        self._ativa = True
        self.proxy.corrente = self
        
    def lidar(self, metodo_command):
        """Lida com modo de operação do JogoProxy - bufferizado ou não"""
        self.ativa() if self.master else None
        print(self._ativa, self.proxy._ativa, metodo_command)
        self.corrente._enfileira(metodo_command) if self.proxy._ativa else self._executa(metodo_command)
        
    def c(self, *args, **kwargs):
        """Método fábrica - Encapsula a criação de cenas - apenas delega.
        
        :param args: coleção de argumentos posicionais.
        :param kwargs: coleção de argumentos nominais.
        :return: Uma Cena do Vitollino construída com estes argumentos.
        
        """
        return self.v.c(*args, **kwargs)
        
    @siz.setter    
    def siz(self, value):
        """Propriedade tamanho"""
        self.elt.siz = value
        
    @property    
    def pos(self):
        """Propriedade posição"""
        return self.elt.pos
        
    @property    
    def x(self):
        """Propriedade posição x"""
        return self.elt.x
        
    @property    
    def y(self):
        """Propriedade posição y"""
        return self.elt.y
        
    @pos.setter    
    def pos(self, value):
        """Propriedade posição"""
        def _command(val=value):
            self.elt.pos = val
        self.lidar(_command)

    def ocupa(self, ocupante=None, pos=(0, 0)):
        """Muda a posição e atitude de um elemento"""
        def _command(val=ocupante):
            destino = val.elt if val else None
            self.elt.ocupa(destino, pos)
        self.lidar(_command)

    def _enfileira(self, metodo_command):
        """Coloca um comando na fila"""
        self.comandos.append(metodo_command)

    def _executa(self, metodo_command):
        """Executa imediamente um comando, não põe na fila"""
        metodo_command()

    def executa(self, *_):
        """Tira e executa um comando na fila"""
        self.comandos.pop(0)() if self.comandos else None


Kwarwp Com Proxy
----------------------

O Kwarwp é melhorado para suportar novos desenhos de índio, incluindo a Índia e o Pajé*.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`tora_partes`.

.. code :: python



    class Kwarwp():
    """ Jogo para ensino de programação.
    
        :param vitollino: Empacota o engenho de jogo Vitollino.
        :param mapa: Um texto representando o mapa do desafio.
        :param medidas: Um dicionário usado para redimensionar a tela.
        :param indios: Uma coleção com outros índios e outros comportamentos.
    """
    
    def __init__(self, vitollino=None, mapa=None, medidas={}, indios=()):
        Vazio.VITOLLINO = self.v = vitollino()
        self.vitollino = vitollino
        """Referência estática para obter o engenho de jogo."""
        self.mapa = (mapa or MAPA_INICIO).split()
        """Cria um matriz com os elementos descritos em cada linha de texto"""
        self.taba = {}
        """Cria um dicionário com os elementos traduzidos a partir da interpretação do mapa"""
        self.o_indio = NULO
        self.os_indios = []
        """Instância do personagem principal, o índio, vai ser atribuído pela fábrica do índio"""
        self.lado, self.col, self.lin = 100, len(self.mapa[0]), len(self.mapa)+1
        """Largura da casa da arena dos desafios, número de colunas e linhas no mapa"""
        Vazio.LADO = self.lado
        """Referência estática para definir o lado do piso da casa."""
        w, h = self.col *self.lado, self.lin *self.lado
        medidas.update(width=w, height=f"{h}px")
        self.indios = deque(indios or [Indio])
        self.cena = self.cria(mapa=self.mapa) if vitollino else None

    def cria(self, mapa=""):
        """ Fábrica de componentes.
        
        :param mapa: Um texto representando o mapa do desafio.
        """
        Fab = nt("Fab", "objeto imagem")
        """Esta tupla nomeada serve para definir o objeto construido e sua imagem."""

        fabrica = {
        "&": Fab(self.maloc, f"{IMGUR}dZQ8liT.jpg"), # OCA
        "^": Fab(self.indio, f"{IMGUR}UCWGCKR.png"), # INDIO
        "$": Fab(self.indio, f"{IMGUR}nvrwu0r.png"), # INDIA
        "p": Fab(self.indio, f"{IMGUR}HeiupbP.png"), # PAJE
        ".": Fab(self.vazio, f"{IMGUR}npb9Oej.png"), # VAZIO
        "_": Fab(self.coisa, f"{IMGUR}sGoKfvs.jpg"), # SOLO
        "#": Fab(self.atora, f"{IMGUR}0jSB27g.png"), # TORA
        "@": Fab(self.barra, f"{IMGUR}tLLVjfN.png"), # PICHE
        "~": Fab(self.coisa, f"{IMGUR}UAETaiP.gif"), # CEU
        "*": Fab(self.coisa, f"{IMGUR}PfodQmT.gif"), # SOL
        "|": Fab(self.coisa, f"{IMGUR}uwYPNlz.png")  # CERCA       
        }
        """Dicionário que define o tipo e a imagem do objeto para cada elemento."""
        mapa = mapa if mapa != "" else self.mapa
        """Cria um cenário com imagem de terra de chão batido, céu e sol"""
        mapa = self.mapa
        lado = self.lado
        cena = self.v.c(fabrica["_"].imagem)
        self.ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado-10, x=0, y=0, cena=cena, vai=self.passo,
                       style={"padding-top": "10px", "text-align": "center"})
        """No argumento *vai*, associamos o clique no céu com o método **executa ()** desta classe.
           O *ceu* agora é um argumento de instância e por isso é referenciado como **self.ceu**.
        """
        sol = self.v.a(fabrica["*"].imagem, w=60, h=60, x=0, y=40, cena=cena, vai=self.executa)
        """No argumento *vai*, associamos o clique no sol com o método **esquerda ()** desta classe."""
        self.taba = {(i, j): fabrica[imagem].objeto(fabrica[imagem].imagem, x=i*lado, y=j*lado+lado, cena=cena)
            for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)}
        """Posiciona os elementos segundo suas posições i, j na matriz mapa"""
        cena.vai()
        return cena

    def passo(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        # self.o_indio.esquerda()
        # self.v.executa()
        # self.o_indio.passo()

        [indio.passo() for indio in self.os_indios]

        
    def executa(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        # self.v.ativa()
        # JogoProxy.ATIVA = True
        # self.o_indio.ativa()
        # self.o_indio.executa()
        # [indio.ativa() and indio.executa() for indio in self.os_indios]
        self.os_indios[0].ativa()
        self.v.ativa()
        self.os_indios[0].executa()
        
    def indio(self, imagem, x, y, cena):
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        """
        self.o_indio = self.indios[0](imagem, x=1, y=0, cena=cena, taba=self, vitollino=self.v)
        """ O índio tem deslocamento zero, pois é relativo à vaga.
            O **x=1** serve para distinguir o indio de outros derivados.
        """
        self.o_indio.indio.vai = lambda *_: self.o_indio.pega()
        """o índio.vai é associado ao seu próprio metodo pega"""
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=self.o_indio)
        self.os_indios.append(self.o_indio)
        self.indios.rotate()
        """recebe a definição do próximo índio"""
        return vaga



Indio Com Proxy
----------------------

O Indio é melhorado para operar com o JogoProxy.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`tora_partes`.

.. code :: python


    class Indio():
    """ Cria o personagem principal na arena do Kwarwp na posição definida.

        :param imagem: A figura representando o índio na posição indicada.
        :param x: Coluna em que o elemento será posicionado.
        :param y: Cinha em que o elemento será posicionado.
        :param cena: Cena em que o elemento será posicionado.
        :param taba: Representa a taba onde o índio faz o desafio.
        :param vitollino: Recebe referência para o vitollino ou proxy.
    """
    AZIMUTE = Rosa(Ponto(0, -1),Ponto(1, 0),Ponto(0, 1),Ponto(-1, 0),)
    """Constante com os pares ordenados que representam os vetores unitários dos pontos cardeais."""
    
    def __init__(self, imagem, x, y, cena, taba, vitollino=None):
        self.vitollino = vitollino or Vazio.VITOLLINO
        self.lado = lado = Vazio.LADO
        self.azimute = self.AZIMUTE.n
        """índio olhando para o norte"""
        self.taba = taba
        self.vaga = self
        self.ocupante = NULO
        self.posicao = (x//lado,y//lado) 
        self.indio = self.vitollino.e(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
        self.x = x
        """Este x provisoriamente distingue o índio de outras coisas construídas com esta classe"""
        if x:
            self.indio.siz = (lado*3, lado*4)
            """Define as proporções da folha de sprites"""
            self.gira()
       
    def ativa(self):
        """ Ativa o proxy do índio para enfileirar comandos.
        """
        #self.vitollino.ativa()
        self.indio.ativa()
       
        
    def passo(self):
        self.indio.executa()
