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

Já com "Resolver usando BFS" a resolução será obtida com busca em largura, garantindo asua otimalidade porém pode levar mais tempo.

## Resultados
Testando 3 jogos de 12 movimentos em cada algoritmo, obteve-se os seguintes resultados:

A heurística levou 30ms, 4ms e 80ms com média de 38ms.

A BFS levou 21055ms, 30375ms e 78387ms com média de 43272ms.

Porém em alguns casos a heurística pode ficar por tempo indeterminado executando até que ache um resultado, o que torna impraticável a espera.

Heurística  | BFS
------------- | -------------
30ms | 21055ms
4ms | 30375ms 
38ms | 78387ms

Testes feitos em um processador Intel Core i7-3770k.

## Problemas encontrados
- No Windows o jogo pode aparecer como "Não respondendo" em algum momento, mas ele continua executando mesmo assim, pra isso é só esperar um pouco.
- Tentamos adicionar threads para evitar que a heurística fosse executada por tempo indeterminado, mas não adiantou muito.

### Desinstalar o PyGame
```bash
pip uninstall pygame
```
