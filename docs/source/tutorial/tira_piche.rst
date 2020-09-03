.. Jogo para ensino de programação Python.
    Changelog
    ---------
    .. versionadded::    20.08.b0
        Tira o Piche.

.. _tira_piche:

Remove o Piche
======================

Nesta parte do tutorial mudamos o comportamento do **Piche**.
para que ele seja removido pela **Tora**.
O código da classe **Piche** deve ser adaptado para interagir com o **Vazio**
de modo que ele seja elimidado quando a **Tora** sair dele

.. seealso::
 Este código é uma modificação do código descrito em :ref:`tora_partes`.
 
.. _tora_piche:

Tora - Saindo do Piche
-----------------------------

O objeto **Piche** vai ser eliminado quendo a **Tora** sair.
Para isso temos que mudar o protocolo do **Piche** com o **Vazio.**
Teremos que também mexer na **Oca** para evitar que ela seja
eliminada caso se remova uma **Tora** largada nela.

Interação do Piche com o Vazio
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O **Piche** agora usa um novo método sai, pedindo para o **Vazio.** para ser eliminado.
O **Vazio.** usa um objeto _nada que não aparece no jogo para abrigar a figura eliminada do **Piche**.

.. mermaid ::

    sequenceDiagram
        participant Indio
        participant Tora
        participant Piche
        participant Vazio
        Indio->>Tora: largar # pede para sair
        Note left of Tora: Tora largada <br/>no Piche
        Indio->>Tora: pegar # pede para sair
        Note left of Tora: Tora removida <br/>do Piche
        Tora->>Piche: sai
        Note right of Piche: Piche agora <br/>requer remoção
        Piche->>Vazio: limpa
        Vazio->>Vazio: _nada.ocupa(ocupante)
        Note left of Vazio: Piche anexado <br/>ao nada some

.. seealso ::
 O resto do código do Piche e do Vazio estão em :ref:`tora_partes`


.. code :: python


    class Piche(Vazio):
        """ Poça de Piche que gruda o índio se ele cair nela.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
    
        def __init__(self, imagem, x, y, cena, taba):
            ...
            # não muda nada
            
        # Agora Piche implementa sai:
        def sai(self):
            """ Pedido por um ocupante para que desocupe a posição nela.
            """
            ... # faz as coisas normais que fazia quando usava o sai do Vazio
            self.vaga.limpa()
                


    class Vazio():
        """ Cria um espaço vazio na taba, para alojar os elementos do desafio.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
        """
        VITOLLINO, LADO = None, None
        
        def __init__(self, imagem, x, y, cena, ocupante=None):
            ...
            # não muda nada

        # Agora tem este método limpa, para eliminar o elemento ocupante do jogo.
        def limpa(self):
            """ Pedido por um ocupante para ele seja eliminado do jogo.
            """
            self._nada.ocupa(self.ocupante)
            """a figura do ocupante vai ser anexada ao elemento nada, que não é apresentado"""
            ... # faz as coisas normais que o método sai faz


    class Oca(Piche):
        """  A Oca é o destino final do índio, não poderá sair se ele entrar nela.
        
            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
        def sai(self):
            ... # O que devemos fazer aqui para que a oca não seja removida?

Empurra a Tora
======================

Agora vamos mudamos o comportamento da **Tora** para que o **Indio** possa empurrar.
O código da classe **Vazio** deve ser adaptado para que execute um protocolo com
a **Tora** e o **Indio**. A **Tora** quando recebe o comando empurra, tem que saber
em que direção está sendo empurrada.


.. seealso::
 Este código é uma modificação do código descrito em :ref:`tora_partes`.
 
.. _tora_empurra:

Tora - Empurrando
-----------------------------

O objeto **Indio** pede para empurrar a **Tora**.
Ele precisa passar o azimute para que a **Tora** saiba para qual **Vazio** vai mover.
A **Tora** consulta seu próprio **Vazio** fornecendo o azimute para obter o **Vazio** destino.
O **Vazio** destino convida a **Tora** para ocupá-lo. Ao receber este convite, a **Tora** encaminha
o convite ao **Indio** para que ele agora se mova para o lugar onde a **Tora** estava.


Interação do Indio e Tora com os Vazios
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Existe uma movimentação em cadeia onde o **Indio** move a **Tora** e por sua vez
ele mesmo se move para onde estava a **Tora**.

.. mermaid ::

    sequenceDiagram
        participant Indio
        participant Tora
        participant Vazio[tora]
        participant Vazio[azimute]
        Indio->>Tora: empurrar(self, azimute) # pede para sair
        Note left of Tora: Tora empurrada <br/>neste azimute
        Tora->>Vazio[tora]: acessar(self,azimute)
        Note right of Tora: Tora consulta <br/>seu Vazio
        Vazio[tora]->>Vazio[azimute]: acessa(ocupante)
        Note right of Vazio[tora]: Vazio consulta <br/>neste azimute
        Vazio[azimute]->>Tora: ocupa(self)
        Note right of Tora: Vazio convida <br/>a ocupar
        Tora->>Indio: ocupa(self.vaga)
        Note right of Indio: Tora convida <br/>a ocupar

O Indio que Empurra
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O **Indio** empurra a **Tora** e por sua vez
a **Tora** libera o espaço eonde estava para o indio ocupar.

.. mermaid ::

    sequenceDiagram
        participant Indio
        participant Tora
        Indio->>Tora: empurrar(self, azimute) # pede para sair
        Note left of Tora: Tora empurrada <br/>neste azimute
        Tora->>Indio: ocupa(self.vaga)
        Note right of Indio: Tora convida <br/>a ocupar

.. code :: python


    class Indio():
        """ Cria o personagem principal na arena do Kwarwp na posição definida.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
        AZIMUTE = Rosa(Ponto(0, -1),Ponto(1, 0),Ponto(0, 1),Ponto(-1, 0),)
        """Constante com os pares ordenados que representam os vetores unitários dos pontos cardeais."""
        
        def __init__(self, imagem, x, y, cena, taba):

        def empurra(self):
            """Objeto tenta sair, tem que consultar a vaga onde está"""
            # self.vaga.sair() # esta parte vai ser feita mais tarde.
            ...
            # de resto o código é semelhante ao _anda


A Tora que é Empurrada
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A **Tora** deve consultar um **Vazio** adjacente para que ela se desloque para lá.
Ela adquire uma nova operação de **empurrar ()**, que consulta o espaço **Vazio**
na direção do azimute em que foi empurrada. O **Vazio** libera a movimentação da  
**Tora** que por sua vez convoca o **Indio** para ocupar o **Vazio** em que estava.

.. mermaid ::

    sequenceDiagram
        participant Tora
        participant Vazio[tora]
        participant Vazio[azimute]
        Tora->>Vazio[tora]: acessar(self,azimute)
        Note right of Tora: Tora consulta <br/>seu Vazio
        Vazio[tora]->>Vazio[azimute]: acessa(ocupante)
        Note right of Vazio[tora]: Vazio consulta <br/>neste azimute
        Vazio[azimute]->>Tora: ocupa(self)
        Note right of Tora: Vazio convida <br/>a ocupar


.. code :: python


    class Tora(Piche):
        """  A Tora é um pedaço de tronco cortado que o índio pode carregar ou empurrar.
        
            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Linha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
            
        def empurrar(self, empurrante, azimute):
            """ Registra o empurrante para uso no procolo e inicia dispathc com a vaga.

                :param requistante: O ator querendo pegar o objeto.
            """
            self.empurrante = empurrante
            # continue aqui com o início do double dispatch para ocupar a vaga na direção do azimute
            self.vaga # acrescente o resto do comndo
            
        def ocupa(self, vaga):
            """ Pedido por uma vaga para que ocupe a posição nela.
            
            :param vaga: A vaga que será ocupada pelo componente.

            No caso da tora, requisita que a vaga seja ocupada por ele.
            Também autoriza o empurrante a ocupar a vaga onde estava.
            """
            ... # ocódigo usual do ocupa
            self.empurrante # .xxx(zzz) if www else None -> continue o código
            self.empurrante = NULO
            self.vaga = vaga


Interação de Vazios no Empurra
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

O **Vazio** ganha uma operação de **empurrar ()** que determina um empurrante e um azimute.
Esta operação vai consultar o ocupante do **Vazio** da sua capacidade de ser empurrado.
O ocupante que é empurrável inicia um double dispatch com o **Vazio** que ocupa,
na expectativa de que seja convidado a ocupar o **Vazio** adjacente. Este protocolo é iniciado
por uma operação **acessar ()** que recebe o ocupante e o azimute.
No início deste protocolo, o **acessar ()** determina que é o **Vazio** adjacente na
direção do azimute. Depois prossege com um protocolo semelhante ao usado pelo índio
na operação de **_anda ()**.

.. mermaid ::

    sequenceDiagram
        participant Vazio[tora]
        participant Vazio[azimute]
        participant Tora
        Vazio[tora]->>Vazio[azimute]: acessa(ocupante)
        Note right of Vazio[tora]: Vazio consulta <br/>neste azimute
        Vazio[azimute]->>Tora: ocupa(self)
        Note right of Vazio[azimute]: Vazio convida <br/>a ocupar


.. code :: python

    class Vazio():
        """ Cria um espaço vazio na taba, para alojar os elementos do desafio.

            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Referência onde ele pode encontrar a taba.
            :param ocupante: Objeto que ocupa inicialmente a vaga.
        """
        VITOLLINO, LADO = None, None
        
        def __init__(self, imagem, x, y, cena, taba, ocupante=None):
            self.taba = taba
            """ Agora recebe um argumento taba, para que ache os vazios adjacentes"""
            ...

        
        def empurrar(self, requisitante, azimute):
            """ Consulta o ocupante atual se há permissão para empurrá-lo na direção do azimute.

                :param requistante: O ator querendo empurrar o objeto.
                :param azimute: A direção que se quer empurrar  o ocupante.
            """
            self.ocupante.empurrar(requisitante, azimute)        

        def acessar(self, ocupante, azimute):
            """ Obtém o Vazio adjacente na direção dada pelo azimute e envio ocupante para lá.
            """
            destino = (self.posicao[0]+azimute.x, self.posicao[1]+azimute.y)
            """A posição para onde o índio vai depende do vetor de azimute corrente"""
            ... # o resto é semelhante ao código do _anda no Índio

