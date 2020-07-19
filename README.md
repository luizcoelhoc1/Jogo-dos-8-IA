# Jogo dos 8
Inteligência Artificial - DCC/UFLA - 2020

## Requisitos
Para executar este programa, é necessário ter o Python instalado (versão 3 ou acima), PIP e a biblioteca PyGame

Com o python instalado, execute:
```bash
pip install pygame
```

Para instalar a biblioteca [PyGame](https://www.pygame.org/ "PyGame")
## Executar
Para executar o programa:
```bash
python jogo_dos_8.py
```
ou
```bash
python3 jogo_dos_8.py
```
Caso você tenha mais de uma versão do python instaladas.

## Instruções
Na interface gráfica, o usuário pode clicar nos botões para escolher qual algoritmo a I.A. deverá executar para solucionar o problema. Antes de cada nova tentativa, é necessário reiniciar o problema com um dos 4 botões de "Novo Jogo" escolhendo quantas movimentações de embaralhamento devem ser feitas.

O botão "Reverter tudo" faz com que o jogo retorne ao estado inicial voltando na pilha de ações que são armazenadas.
Em "Resolver com heurística" o jogo será resolvido pelo método heurístico que geralmente é bem mais rápido mas não oferece a resposta otimizada.
Já com "Resolver usando BFS" a resolução será obtida com busca em largura, garantindo asua otimalidade porém pode levar mais tempo

### Desinstalar o PyGame
```bash
pip uninstall pygame
```
