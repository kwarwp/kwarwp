.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _melhora_indio:

Melhorando o Índio
===================

O movimento do índio pode melhorar, podendo dobrar à esquerda e direita.

Para direcionar o índio, modificamos o método **anda ()** para considerar a direção.
Adicionamos `Os Métodos Direcionais e a Fala`_


.. seealso::
 Este código é uma modificação do código descrito em :ref:`organiza_taba`

Classe Indio - Com Direção 
-----------------------------

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

Os Métodos Direcionais e a Fala
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **mostra** modifica a exibição da *folha de sprites*, posicionando o canto
superior esquerdo (origem) em uma coordenada negativa em relação à janela
de exibição. Desta forma, a posição correta do índio vai aparecer na tela.

.. image:: http://imgur.com/UCWGCKR.png
   :height: 180px
   :width: 240 px
   :alt: folha de sprites do índio
   :align: center

.. note ::
   O termo Sprite vem do latim spiritus que significa “Espíritos”, mas também pode significar "fada" ou "duende".
   No âmbito da computação gráfica (Quer seja em games ou não) são os quadros de movimento que são desenhados
   individualmente com uma pequena variação entre si, mas obedecendo um padrão sequencial que quando disposto
   numa ordem coerente acaba gerando uma animação de movimento quando exibidas em sucessão.
   Ver externamente `Definição de Sprite Sheet`_

.. _`Definição de Sprite Sheet`: https://gamerdesconstrutor.blogspot.com/2014/12/sprite-sheets-definicao.html

Os métodos **esquerda** e **direita** trocam a direção (azimute) para o qual o índio
está olhando. Eles usam uma propriedade das listas em Python de circularidade
dos índices negativos. Quando se tenta acessar uma posição de uma lista com um
índice negativo, a posição é contada do fim da lista para o princípio.

.. mermaid ::

    graph LR

        subgraph Positivos
            s0[0]--> s1[1]--> s2[2]--> s3[3]
        end

        subgraph Lista
            l0[n]--> l1[l]--> l2[s]--> l3[o]
        end

        subgraph Negativos
            n4[-4]--> n3[-3]--> n2[-2]--> n1[-1]
        end       

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
       
    def fala(self, texto=""):
        """ O índio fala um texto dado.
        
        :param texto: O texto a ser falado.
        """
        self.taba.fala(texto)


Os Protocolos de Saída
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O ìndio teve que ser modificado para incorporar um novo `duplo despacho`_ de saída.
Ele terá que consultar primeiro a vaga onde está para saber se pode sair

Ao receber de um evento o comando **anda ()**, ele terá que consultar com um **sair ()** a vaga onde está.
Em uma vaga normal ele recebe o **siga ()**, segue em frente e executa o seu **_anda ()** original.
Se ele entrou numa vaga que tinha uma armadilha, agora a vaga onde está é a armadilha.
Em uma armadilha leniente, segue normalmente. Numa armadilha rígida, o seu pedido de
**sair ()** é ignorado e ele não recebe a resposta **siga ()**.

.. mermaid ::

    sequenceDiagram
        participant Evento
        participant Indio
        participant Origem
        participant Ocupante
        Evento->>Indio: anda # pede para entrar
        Indio->>Origem: sair # pede para sair
        Origem->>Indio: siga
        Note left of Origem: Origem vago <br/>autoriza a saída
        Indio->>Indio: _anda
        Note left of Indio: Autorizado pela vaga <br/>executa o anda
        Indio->>Ocupante: sair
        Note right of Origem: Origem é ocupante <br/>consulta ocupante
        Ocupante->>Indio: siga
        Note left of Ocupante: Ocupante autoriza <br/>indio a seguir
        Indio->>Indio: _anda
        Note left of Indio: Autorizado a sair <br/>executa o anda
        Ocupante->>Ocupante: pass
        Note left of Ocupante: Ocupante armadilha <br/>indio não segue

.. code :: python

    def anda(self):
        """Objeto tenta sair, tem que consultar a vaga onde está"""
        self.vaga.sair()      

    def sair(self):
        """Objeto de posse do índio tenta sair e é autorizado"""
        self.vaga.ocupante.siga()      

    def siga(self):
        """Objeto tentou sair e foi autorizado"""
        self._anda()       

    def _anda(self):
        """ Faz o índio caminhar na direção em que está olhando.
        """
        destino = (self.posicao[0]+self.azimute.x, self.posicao[1]+self.azimute.y)
        """Assumimos que o índio está olhando para cima, decrementamos a posição **y**"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            vaga.acessa(self)


Kwarwp - Oca e Piche
--------------------

A classe Kwarwp vai ser modificada para agregar novas fábricas.
Além do `Classe Indio - Com Direção`_ e do vazio teremos a
`Oca - O Destino`_ e o `Piche - A Armadilha`_

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
 Veja o código anterior da classe no tutorial :ref:`organiza_taba`    

Dicionário com Oca e Piche
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **cria ()** define as fábricas de componentes.

No dicionário pode se ver que **"&"** agora remete a **maloc**
e **"@"** remete a **barra**. Uma outra alteração é que a
construção do **sol** agora se liga ao tratador de evento **esquerda**.
Isto permite que se experimente andar com o índio no cenário.
Note que agora o **ceu** foi convertido em atributo de instância.
Por isso agora ele é referido como **self.ceu**.
       
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
        "#": Fab(self.coisa, f"{IMGUR}ldI7IbK.png"), # TORA
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
        self.ceu = self.v.a(fabrica["~"].imagem, w=lado*self.col, h=lado-10, x=0, y=0, cena=cena, vai=self.executa,
                       style={"padding-top": "10px", "text-align": "center"})
        """No argumento *vai*, associamos o clique no céu com o método **executa ()** desta classe.
           O *ceu* agora é um argumento de instância e por isso é referenciado como **self.ceu**.
        """
        sol = self.v.a(fabrica["*"].imagem, w=60, h=60, x=0, y=40, cena=cena, vai=self.esquerda)
        """No argumento *vai*, associamos o clique no sol com o método **esquerda ()** desta classe."""
        self.taba = {(i, j): fabrica[imagem].objeto(fabrica[imagem].imagem, x=i*lado, y=j*lado+lado, cena=cena)
            for j, linha in enumerate(mapa) for i, imagem in enumerate(linha)}
        """Posiciona os elementos segundo suas posições i, j na matriz mapa"""
        cena.vai()
        return cena

Comandos para o Índio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **fala ()** é usado por objetos que emitem mensagens.
Ele instrumentaliza o céu para que um texto em html seja escrito nele.

O método **esquerda ()** invoca sua contrapartida na instância de **Indio**.
O método **executa ()** invoca sua contrapartida na instância de **Indio**.

.. code :: python
        
    def fala(self, texto=""):
        """ O Kwarwp é aqui usado para falar algo que ficará escrito no céu.
        """
        self.ceu.elt.html = texto
        pass
        
    def esquerda(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        self.o_indio.esquerda()
        
    def executa(self, *_):
        """ Ordena a execução do roteiro do índio.
        """
        self.o_indio.executa()

Fabricando a Oca e o Piche
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O método **maloc ()** invoca a criação da `Oca - O Destino`_.
O método **barra ()** invoca a criação do `Piche - A Armadilha`_.

.. code :: python
        
    def maloc(self, imagem, x, y, cena):
        """ Cria uma maloca na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Oca(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        return vaga
        
    def barra(self, imagem, x, y, cena):
        """ Cria uma armadilha na arena do Kwarwp na posição definida.

        :param x: coluna em que o elemento será posicionado.
        :param y: linha em que o elemento será posicionado.
        :param cena: cena em que o elemento será posicionado.
        
        Cria uma vaga vazia e coloca o componente dentro dela.
        """
        coisa = Piche(imagem, x=0, y=0, cena=cena, taba=self)
        vaga = Vazio("", x=x, y=y, cena=cena, ocupante=coisa)
        return vaga

Ocupante e Vaga Nulos
^^^^^^^^^^^^^^^^^^^^^

O Kwarwp é aqui usado como um ocupante `objeto nulo`_, usado ao fabricar espaços vazios
O pedido de ocupar é ignorado.

.. code :: python
       
        
    def sai(self, *_):
        """ O Kwarwp é aqui usado como uma vaga falsa, o pedido de sair é ignorado.
        """
        pass
        
    def ocupa(self, *_):
        """ O Kwarwp é aqui usado como um ocupante falso, o pedido de ocupar é ignorado.
        """
        pass

.. _`objeto nulo`: https://www.thiengo.com.br/padrao-de-projeto-objeto-nulo

Vazio - A Vaga
-------------------

O Vazio vai ser atualizado aqui para funcionar como uma vaga leniente,
ou seja, deixa sair quem quiser abandonar a vaga.

A principar ideia aqui vai ser usar o **Vazio** como *classe base* de uma
linhagem de herança, onde outras classes vão herdar o seu comportamento.
No diagrama abaixo vemos que **Piche** herda de **Vazio** e por sua vez **Oca**
herda de **Piche**

.. mermaid ::

 classDiagram
      Vazio <|-- Piche
      Piche <|-- Oca
      Vazio : +Vaga vaga
      Vazio : +Coisa ocupante
      Vazio : +Elemento vazio
      Vazio: _acessa()
      Vazio: _valida_acessa()
      Vazio: _sair()
      Vazio: _pede_sair()
      class Piche{
        +Vaga vaga
        +Coisa ocupante
        +Kwarwp taba
        +Elemento vazio
        _acessa()
        _pede_sair()
      }
      class Oca{
        _acessa()
        _pede_sair()
      }

.. note ::
 O principal mecanismo do recurso da herança é permitir que uma classe possa
 ser derivada de uma classe base, permitindo que um comportamento mais especifico
 seja implementado na subclasse. A herança, é também uma importante característica 
 para ao reuso de algoritmos e evitar códigos redundantes que possam tornar difícil 
 a manutenção da base de códigos. Ver externamente `O Uso da Herança`_

.. _`O Uso da Herança`: https://professormarcolan.com.br/como-utilizar-a-heranca-em-python/

.. code :: python

    class Vazio():
        """ Cria um espaço vazio na taba, para alojar os elementos do desafio.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
        """
        
        def __init__(self, imagem, x, y, cena, ocupante=None):
            self.lado = lado = Kwarwp.LADO
            self.posicao = (x//lado,y//lado-1)
            self.vazio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=x, y=y, cena=cena)
            self._nada = Kwarwp.VITOLLINO.a()
            self.acessa = self._acessa
            """O **acessa ()** é usado como método dinâmico, variando com o estado da vaga.
            Inicialmente tem o comportamento de **_acessa ()** que é o estado vago, aceitando ocupantes"""
            self.ocupante = ocupante or self
            """O ocupante se não for fornecido é encenado pelo próprio vazio, agindo como nulo"""
            self.acessa(ocupante)
            self.sair = self._sair
            """O **sair ()** é usado como método dinâmico, variando com o estado da vaga.
            Inicialmente tem o comportamento de **_sair ()** que é o estado leniente, aceitando saidas"""
            
O Objeto de Estado Sair
^^^^^^^^^^^^^^^^^^^^^^^

O `Vazio - A Vaga`_ tem um outro `objeto de estado`_ além do **acessa ()**.
Este objeto é o **sair ()**, que assume os estados **_sair** quando a vaga
está livre ou **_pede_sair ()** quando está ocupada.

.. code :: python

        def _sair(self):
            """Objeto tenta sair e secebe autorização para seguir"""
            self.ocupante.siga()      
        
        def _pede_sair(self):
            """Objeto tenta sair e secebe autorização para seguir"""
            self.ocupante.sair()      

Piche - A Armadilha
-------------------

O piche vai funcionar como uma forma especializada do `Vazio - A Vaga`_ 

.. code :: python

    class Piche(Vazio):
        """ Poça de Piche que gruda o ńdio se ele cair nela.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
        
        def __init__(self, imagem, x, y, cena, taba):
            self.taba = taba
            self.vaga = taba
            self.lado = lado = Kwarwp.LADO
            self.posicao = (x//lado,y//lado-1)
            self.vazio = Kwarwp.VITOLLINO.a(imagem, w=lado, h=lado, x=0, y=0, cena=cena)
            self._nada = Kwarwp.VITOLLINO.a()
            self.acessa = self._acessa
            """O **acessa ()** é usado como método dinâmico, variando com o estado da vaga.
            Inicialmente tem o comportamento de **_acessa ()** que é o estado vago, aceitando ocupantes"""
            self.sair = self._sair
            """O **sair ()** é usado como método dinâmico, variando com o estado da vaga.
            Inicialmente tem o comportamento de **_sair ()** que é o estado vago, aceitando ocupantes"""

        @property        
        def elt(self):
            """ A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .

            No caso do piche, retorna o elt do elemento do atributo **self.vazio**.
            """
            return self.vazio.elt
            
        def ocupa(self, vaga):
            """ Pedido por uma vaga para que ocupe a posição nela.
            
            :param vaga: A vaga que será ocupada pelo componente.

            No caso do piche, requisita que a vaga seja ocupada por ele.
            """
            self.vaga.sai()
            self.posicao = vaga.posicao
            vaga.ocupou(self)
            self.vaga = vaga
        
        def _pede_sair(self):
            """Objeto tenta sair mas não é autorizado"""
            self.taba.fala("Você ficou preso no piche")       
            
        def _acessa(self, ocupante):
            """ Atualmente a posição está vaga e pode ser acessada pelo novo ocupante.
            
            A responsabilidade de ocupar definitivamente a vaga é do candidato a ocupante
            Caso ele esteja realmente apto a ocupar a vaga deve cahamar de volta ao vazio
            com uma chamada **ocupou (ocupante)**.

                :param ocupante: O canditato a ocupar a posição corrente.
            """
            ocupante.ocupa(self)

Oca - O Destino
-------------------

A Oca vai funcionar como uma forma especializada do `Piche - A Armadilha`_ 

.. code :: python

    class Oca(Piche):
        """ A Oca é o destino final do índio, não poderá sair se ele entrar nela.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
        
        def _pede_sair(self):
            """Objeto tenta sair mas não é autorizado"""
            self.taba.fala("Você chegou no seu objetivo")       
            
        def _acessa(self, ocupante):
            """ Atualmente a posição está vaga e pode ser acessada pelo novo ocupante.
            
            A responsabilidade de ocupar definitivamente a vaga é do candidato a ocupante
            Caso ele esteja realmente apto a ocupar a vaga e deve cahamar de volta ao vazio
            com uma chamada ocupou.

                :param ocupante: O canditato a ocupar a posição corrente.
            """
            self.taba.fala("Você chegou no seu objetivo")       
            ocupante.ocupa(self)

.. _`duplo despacho`: http://www.dpi.ufv.br/projetos/apri/?page_id=726
