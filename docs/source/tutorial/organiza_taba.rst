.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


.. _organiza_taba:

Organizando a Taba
===================

O movimento do índio ainda está errático pois ele não sonda o ambiente, não respeita
os limites da taba e atropela os objetos. Vamos povoar a taba com espaços vazios
predeterminados. As coisas e o índio serão colocados nestes espaços e o índio só poderá
ir para um vazio se ele estiver dentro dos limites da taba e estiver desocupado.

Para mover o índio, modificamos o método **anda ()** na sua classe.
Na versão anterior, ele mudava a coordenada do elemento.
Nesta ele muda o elemento para um **Vazio** adjacente.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`movendo_indio`

Padrões de projeto
------------------

Padrões de projeto são a linguagem culta do programador.
Eles são soluções típicas para problemas comuns em projeto de software. 
Cada padrão é como uma planta de construção que você pode customizar para
resolver um problema de projeto particular em seu código.

.. seealso ::
 Neste site `Padrões de Projeto`_, veja também na `Apresentação de Slides Padrões de Projeto`_

.. _`Padrões de Projeto`: https://refactoring.guru/pt-br/design-patterns
.. _`Apresentação de Slides Padrões de Projeto`: http://www.inf.ufpr.br/andrey/ci163/PadroesdeProjeto.pdf

O protocolo duplo despacho
^^^^^^^^^^^^^^^^^^^^^^^^^^

Neste protocolo é estabelecido um diálogo entre um objeto que quer entrar,
o **Imigrante** e a vaga que quer ocupar, o **Destino**. O destino estando
vago, pede para o imigrante ocupar imediatamente e recebe o pedido **ocupou ()**
do imigrante. Caso odestino esteja ocupado, ele delega a decisão ao **Ocupante**
que decide ignorar ou acatar o pedido de acesso enviando o pedido de **ocupa**
no últino caso. Neste exemplo, o protocolo está implementado em `Classe Indio - Duplo Despacho`_
e na `Classe Vazio`_

.. seealso::
 Ver uma explicação externa em `duplo despacho`_

.. mermaid ::

    sequenceDiagram
        participant Imigrante
        participant Origem
        participant Destino
        participant Ocupante
        Imigrante->>Destino: acessa(imigrante) # pede para entrar
        Destino->>Imigrante: ocupa(destino)
        Note left of Destino: Destino vago <br/>autoriza o ocupa
        Destino->>Ocupante: acessa(imigrante)
        Note right of Destino: Destino ocupado <br/>consulta ocupante
        Ocupante->>Imigrante: ocupa(destino)
        Note left of Ocupante: Ocupante autoriza <br/>ser substituído
        Imigrante->>Destino: ocupou(imigrante) # entra definitivamente
        Imigrante->>Origem: sai() # sai da origem
    

O protocolo objeto de estado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Neste protocolo o objeto **Vazio** pode estar em um `Estado Ocupado`_ ou `Estado Vago`_.
Nesta implementação usaremos um jeito `Pythônico`_ para fazer uma modificação dinâmica de comportamento.
Como métodos são objetos de primeira ordem no Python, em vez de criarmos classes para
representar os estados, simplesmente trocamos a operação do método **acessa ()** quando o estado
é chaveado.

.. seealso::
 Ver uma explicação externa em `estado de objeto`_

.. _`Pythônico`: https://pt.stackoverflow.com/questions/192343/o-que-%C3%A9-c%C3%B3digo-pyth%C3%B4nico

.. mermaid ::

    stateDiagram
        vago: Vazio está vago
        ocupado: Vazio tem um ocupante
        [*] -->  vago : inicia vago
        Note left of vago: acessa autoriza <br/>diretamente o imigrante
        vago --> ocupado : acessa = _valida_acessa
        Note left of ocupado: acessa delega <br/>autorização ao ocupante
        ocupado --> vago : acessa = _acessa  


.. _`duplo despacho`: http://www.dpi.ufv.br/projetos/apri/?page_id=726

.. _`estado de objeto`: http://www.dpi.ufv.br/projetos/apri/?page_id=745


Classe Vazio
-------------

Com esta classe vamos separar locais onde coisas e o índio podem ser alocados.
Vamos organizar a maneira como objetos se deslocam nesta taba usando `o protocolo
duplo despacho`_. Para entrar em um vazio o objeto pede **acessa ()** e só entra
se receber um convite **ocupa ()**. Um outro protocolo que vamos usar é `o protocolo objeto de estado`_
Neste protocolo o objeto assume comportamentos diferentes caso esteja vago ou ocupado.

Cria um espaço vazio na taba, para alojar os elementos do desafio.

    :param imagem: A figura representando o espaço vazio (normalmente transparente).
    :param x: Coluna em que o elemento será posicionado.
    :param y: Cinha em que o elemento será posicionado.
    :param cena: Cena em que o elemento será posicionado.

.. code :: python

    class Vazio():
        """ Cria um espaço vazio na taba, para alojar os elementos do desafio.

            :param imagem: A figura representando o espaço vazio (normalmente transparente).
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
            self.ocupante = ocupante or self
            """O ocupante será definido pelo acessa, por default é o vazio"""
            self.acessa(ocupante)

Estado Ocupado
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
Consulta o ocupante atual se há permissão para substituí-lo pelo novo ocupante.
Veja o `O protocolo objeto de estado`_.

    :param ocupante: O canditato a ocupar a posição corrente.

.. code :: python

        def _valida_acessa(self, ocupante):
            """ Consulta o ocupante atual se há permissão para substituí-lo pelo novo ocupante.

                :param ocupante: O canditato a ocupar a posição corrente.
            """
            self.ocupante.acessa(ocupante)

Estado Vago
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
Atualmente a posição está vaga e pode ser acessada pelo novo ocupante.
            
    A responsabilidade de ocupar definitivamente a vaga é do candidato a ocupante
    Caso ele esteja realmente apto a ocupar a vaga e deve cahamar de volta ao vazio
    com uma chamada ocupou.

    :param ocupante: O canditato a ocupar a posição corrente.

.. seealso::
 Veja o `O protocolo objeto de estado`_.

.. code :: python

        def _acessa(self, ocupante):
            """ Atualmente a posição está vaga e pode ser acessada pelo novo ocupante.
            
            A responsabilidade de ocupar definitivamente a vaga é do candidato a ocupante
            Caso ele esteja realmente apto a ocupar a vaga e deve cahamar de volta ao vazio
            com uma chamada ocupou.

                :param ocupante: O canditato a ocupar a posição corrente.
            """
            ocupante.ocupa(self)

Confirmando a Ocupação
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
O candidato à vaga decidiu ocupá-la e efetivamente entra neste espaço.
            
    Este ocupante vai entrar no elemento do Vitollino e definitivamente se tornar
    o ocupante da vaga. Com isso ele troca o estado do método acessa para primeiro
    consultar a si mesmo, o ocupante corrente usando o protocolo definido em
    **_valida_acessa ()**

    :param ocupante: O canditato a ocupar a posição corrente.

.. code :: python
            
        def ocupou(self, ocupante):
            """ O candidato à vaga decidiu ocupá-la e efetivamente entra neste espaço.
            
            :param ocupante: O canditato a ocupar a posição corrente.
            
            Este ocupante vai entrar no elemento do Vitollino e definitivamente se tornar
            o ocupante da vaga. Com isso ele troca o estado do método acessa para primeiro
            consultar a si mesmo, o ocupante corrente usando o protocolo definido em
            **_valida_acessa ()**

            """
            self.vazio.ocupa(ocupante)
            self.ocupante = ocupante
            self.acessa = self._valida_acessa

Pedido para Ocupar
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
Pedido por uma vaga para que ocupe a posição nela.

    Neste caso, um objeto Vazio nunca vai ocupar nenhuma vaga. Este método
    está definido aqui para efeito de `objeto nulo`_

    :param vaga: A vaga a ser ocupada.

.. code :: python

        def ocupa(self, vaga):
            """ Pedido por uma vaga para que ocupe a posição nela.

            No caso do espaço vazio, não faz nada.
            """
            pass

Pedido para Sair
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
Pedido por um ocupante para que desocupe a posição nela.

    Quando um ocupante deixa a vaga, ele envia este comando para desfazer a ocupação.
    Ver `O protocolo duplo despacho`_

.. code :: python
            
        def sai(self):
            """ Pedido por um ocupante para que desocupe a posição nela.
            """
            self.ocupante = self
            self.acessa = self._acessa
            
Propriedade Elemento (elt).

    A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .
    No caso do espaço vazio, vai retornar um elemento que não contém nada.

.. code :: python

        @property        
        def elt(self):
            """ A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .

            No caso do espaço vazio, vai retornar um elemento que não contém nada.
            """
            return self._nada.elt

Classe Indio - Duplo Despacho 
------------------------------

Vamos modificar esta classe para ela suportar `O protocolo duplo despacho`_

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

Método Anda - Acessa uma Vaga
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Este método foi modificado para procurar na taba um vazio adjacente
e realizar `O protocolo duplo despacho`_.

.. code :: python
        
    def anda(self):
        """ Faz o índio caminhar na direção em que está olhando.
        """
        destino = (self.posicao[0], self.posicao[1]-1)
        """Assumimos que o índio está olhando para cima, decrementamos a posição **y**"""
        taba = self.taba.taba
        if destino in taba:
            vaga = taba[destino]
            """Recupera na taba a vaga para a qual o índio irá se transferir"""
            vaga.acessa(self)
            """Inicia o protocolo duplo despacho, pedindo para acessar a vaga"""
         
    def executa(self):
        """ Roteiro do índio. Conjunto de comandos para ele executar.
        """
        self.anda()

Indio como Vaga Nula
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O índio é usado como  `objeto nulo`_, representando uma vaga.

.. code :: python
         
    def sai(self):
        """ Rotina de saída falsa, o objeto Indio é usado como uma vaga nula.
        """
        pass

Indio no Despacho Duplo
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O índio implementa  `O protocolo duplo despacho`_, no papel de ocupante de uma vaga.
O índio també pode funcionar como um objeto intransponível, poi quando a vaga
que ele ocupa delega a ele o pedido **acessa ()**, ele não responde nada, negando acesso.

.. code :: python

    @property        
    def elt(self):
        """ A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .

        No caso do índio, retorna o elt do elemento do atributo **self.indio**.
        """
        return self.indio.elt
        
    def ocupa(self, vaga):
        """ Pedido por uma vaga para que ocupe a posição nela.
        
        :param vaga: A vaga que será ocupada pelo componente.

        No caso do índio, requisita que a vaga seja ocupada por ele.
        """
        self.vaga.sai()
        self.posicao = vaga.posicao
        vaga.ocupou(self)
        self.vaga = vaga
        
    def acessa(self, ocupante):
        """ Pedido de acesso a essa posição, delegada ao ocupante pela vaga.
        
        :param ocupante: O componente candidato a ocupar a vaga já ocupada pelo índio.

        No caso do índio, ele age como um obstáculo e não prossegue com o protocolo.
        """
        pass

Kwarwp - Fabricando Vagas
---------------------------

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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O Kwarwp é aqui usado como um ocupante `objeto nulo`_, usado ao fabricar espaços vazios
O pedido de ocupar é ignorado.

.. code :: python
       
    def ocupa(self, *_):
        """ O Kwarwp é aqui usado como um ocupante falso, o pedido de ocupar é ignorado.
        """
        pass

.. _`objeto nulo`: https://www.thiengo.com.br/padrao-de-projeto-objeto-nulo

