.. Kwarwp documentation master file, created by
   sphinx-quickstart on Mon Jul 27 10:30:56 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Adicionando Indio
=================

Nesta tela vamos montar um simulacro do primeiro desafio kwarwp.
Precisamos ter uma classe.

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
