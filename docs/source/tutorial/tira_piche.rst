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
