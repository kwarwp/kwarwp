.. Jogo para ensino de programação Python.
    Changelog
    ---------
    .. versionadded::    20.08.b0
        Tora e outras partes.

.. _tora_partes:

A Tora e Outras Partes
======================

Esta página descreve como foi feito o módulo **kwarwp.kwarwpart**.
Para incluir a **Tora**, decidimos mover várias classes, tirando do
módulo **kwarwp.kwarapp** e trazendo para este novo módulo.
Procure construir este módulo com as dicas do tutorial.
Caso tenha muita dificuldade em fazer funcionar, consulte o código aqui:

- :py:class:`kwarwp.kwarwpart.Vazio`     Espaço vago na arena do desafio.
- :py:class:`kwarwp.kwarwpart.Oca`       Destino final da aventura.
- :py:class:`kwarwp.kwarwpart.Piche`     Uma armadilha para prender o índio.
- :py:class:`kwarwp.kwarwpart.Tora`      Uma tora que o índio pode pegar.
- :py:class:`kwarwp.kwarwpart.Nulo`      Objeto nulo passivo a todas as requisições.

Nesta parte do tutorial mostramos uma nova classe e seus comportamentos, a **Tora**.
Ela tem comportamento que se assemelham ao **Vazio** e mais especificamente
ao do seu descendente **Piche** e para isso usaremos a herança.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`melhora_indio`.
 O código da classe **Indio** adaptada para interagir com a **Tora**
 pode ser visto em :ref:`inclui_tora`.

.. _tora_tronco:

Tora - O Tronco Carregável
-----------------------------

O objeto Tora foi criado neste novo módulo herdando do objeto **Piche**.
A definição do **Piche** pode ser visto em :ref:`melhora_indio`.

Protocolos de Interação com a Tora
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A Tora tem que ser implementada incorporando um novo `duplo despacho`_ de saída.
Ela terá que interagir com o índio para poder ser carregada por ele.

O método **pega ()** é usado pelo índio para adquirir  e carregar a tora.
O método **pega ()** invoca sua contrapartida **pegar ()** na instância de **Tora**.
A tora responde à requisição invocando **ocupar ()** no **Indio**.

O método **larga ()** invoca **acessa ()** na instância de **Vaga** onde
a Tora deve ser colocada, mas passa como parâmetro o ocupante em vez
de si próprio. De resto é executado o double dispatch como no anda,
sendo que "andarilho" é a **Tora**.

.. mermaid ::

    sequenceDiagram
        participant Evento
        participant Indio
        participant Tora
        participant Origem
        Evento->>Indio: pega # pede para entrar
        Indio->>Tora: pegar # pede para sair
        Note left of Tora: Pede à Tora <br/>mover ao Indio
        Tora->>Origem: sai
        Tora->>Indio: ocupou
        Indio->>Indio: ocupa
        Note left of Indio: Incorpora a Tora <br/>como ocupante

.. note ::
 O principal mecanismo do recurso da herança é permitir que uma classe possa
 ser derivada de uma classe base, permitindo que um comportamento mais especifico
 seja implementado na subclasse. A herança, é também uma importante característica 
 para ao reuso de algoritmos e evitar códigos redundantes que possam tornar difícil 
 a manutenção da base de códigos. Ver externamente `O Uso da Herança`_

.. _`O Uso da Herança`: https://professormarcolan.com.br/como-utilizar-a-heranca-em-python/

.. code :: python

    class Tora(Piche):
        """  A Tora é um pedaço de tronco cortado que o índio pode carregar ou empurrar.
        
            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Linha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
            
        def pegar(self, requisitante):
            """ Consulta o ocupante atual se há permissão para pegar e entregar ao requistante.

                :param requistante: O ator querendo pegar o objeto.
            """
            vaga = requisitante
            self.vaga.sai()
            # self.posicao = vaga.posicao
            vaga.ocupou(self)
            self.vaga = vaga

        @property        
        def posicao(self):
            """ A propriedade posição faz parte do protocolo do double dispatch com o Indio .

            No caso da tora, retorna o a posição do atributo **self.vaga**.
            """
            return self.vaga.posicao

        @posicao.setter        
        def posicao(self, _):
            """ A propriedade posição faz parte do protocolo do double dispatch com o Indio .

            No caso da tora, é uma propriedade de somente leitura, não executa nada.
            """
            pass

        @property        
        def elt(self):
            """ A propriedade elt faz parte do protocolo do Vitollino para anexar um elemento no outro .

            No caso da tora, retorna o elt do elemento do atributo **self.vazio**.
            """
            return self.vazio.elt
            
        def _acessa(self, ocupante):
            """ Pedido de acesso a essa posição, delegada ao ocupante pela vaga.
            
            :param ocupante: O componente candidato a ocupar a vaga já ocupada pelo índio.

            No caso da tora, ela age como um obstáculo e não prossegue com o protocolo.
            """
            pass
            
Os Objetos Piche e Oca
----------------------

Este objetos foram copiados sem alteração do módulo original para cá.
A única alteração foi no **Piche** que teve que importar localmente
o **Kwarwp** que estava no mesmo móduo e agora ficou no **kwarwp.kwarapp**.

.. seealso::
 Este código é uma modificação do código descrito em :ref:`melhora_indio`.

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
            from kwarwp.kwarapp import Kwarwp
            """Importando localmente o Kwarwp para evitar referência circular."""
            ... # copie o resto do tutorial anterior


    class Oca(Piche):
        """  A Oca é o destino final do índio, não poderá sair se ele entrar nela.
        
            :param imagem: A figura representando o índio na posição indicada.
            :param x: Coluna em que o elemento será posicionado.
            :param y: Cinha em que o elemento será posicionado.
            :param cena: Cena em que o elemento será posicionado.
            :param taba: Representa a taba onde o índio faz o desafio.
        """
        
        def _pede_sair(self):
            """Objeto tenta sair mas não é autorizado"""
            ... # copie o resto do tutorial anterior     

O Objeto Nulo
-------------------

O Objeto Nulo foi extraído em uma classe própria.

.. code :: python


    class Nulo:
        """Objeto nulo que responde passivamente a todas as requisições."""
        def __init__(self):
            self.pegar = self.ocupa = self.nulo
            
        def nulo(self, *_, **__):
            """Método nulo, responde passivamente a todas as chamadas.
            
            :param _: aceita todos os argumentos posicionais.
            :param __: aceita todos os argumentos nomeados.
            :return: retorna o próprio objeto nulo.
            """
            return self 

    NULO = Nulo()


.. _`duplo despacho`: http://www.dpi.ufv.br/projetos/apri/?page_id=726
.. _`estado de objeto`: http://www.dpi.ufv.br/projetos/apri/?page_id=745
