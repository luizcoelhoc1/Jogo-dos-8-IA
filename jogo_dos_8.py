# Jogo dos 8
# Por: Gustavo Rodrigues Sousa
#      Luiz Carlos Coelho Conde

import pygame, sys, random
from threading import Thread
from pygame.locals import *

#configurações do jogo
BOARDWIDTH = 3
BOARDHEIGHT = 3
ANIMATIONSPEED = 33
FPS = 30 #"vsync"
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

#cores
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
BRIGHTBLUE =    ( 38,  91, 189)
DARKTURQUOISE = (  3,  44,  59)
GREEN =         ( 61, 219, 161) 

#temas
BGCOLOR = BLACK
TILECOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

#tamanhos
TILESIZE = 100
BASICFONTSIZE = 20
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)-120
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

#dados
BLANK = None
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF_1, SOLVE_SURF_2, SOLVE_SURF_3, SOLVE_RECT, SOLVE_H, SOLVE_BFS, RESULTOFTHREAD, SOLUTION_TIME

    #init config
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Jogo dos 8')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    RESULTOFTHREAD = []
    RESET_RECT = []
    RESET_SURF = []
    for i in range(0,4):
        RESET_RECT.append(None)
        RESET_SURF.append(None)

    # Opções de ação
    RESET_SURF[0], RESET_RECT[0] = makeText('Novo jogo com 3 mov',   TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 395)
    RESET_SURF[1], RESET_RECT[1] = makeText('Novo jogo com 6 mov',   TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 365)
    RESET_SURF[2], RESET_RECT[2] = makeText('Novo jogo com 9 mov',   TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 335)
    RESET_SURF[3], RESET_RECT[3] = makeText('Novo jogo com 12 mov',  TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 305)
    SOLVE_SURF_1, SOLVE_RECT = makeText('Reverter tudo',    TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 165)
    SOLVE_SURF_2, SOLVE_H = makeText('Resolver usando heurística', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 135)
    SOLVE_SURF_3, SOLVE_BFS = makeText('Resolver usando bfs',      TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 270, WINDOWHEIGHT - 105)

    #init game
    mainBoard, solutionSeq = generateNewPuzzle(6)
    solvedBoard = getStartingBoard()
    allMoves = [] 

    # main loop
    while True: 
        # inicia variaveis necessárias para todos os loops
        slideTo = None
        msg = 'Clique no bloco ou pressione as setas para mover' # contains the message to show in the upper left corner.
        if mainBoard == solvedBoard:
            msg = 'Solucionado em ' + str(SOLUTION_TIME) + 'ms'

        # em todo loop desenha e checa se deve sair do jogo ou não
        drawBoard(mainBoard, msg)
        checkForQuit()

        #tratador de eventos
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    # novo jogo com 3 movimentos requisitado
                    if RESET_RECT[0].collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(3) 
                        allMoves += solutionSeq
                        
                    # novo jogo com 6 movimentos requisitado
                    if RESET_RECT[1].collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(6) 
                        allMoves += solutionSeq
                        
                    # novo jogo com 9 movimentos requisitado
                    if RESET_RECT[2].collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(9) 
                        allMoves += solutionSeq
                        
                    # novo jogo com 12 movimentos requisitado
                    if RESET_RECT[3].collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(12) # clicked on New Game button
                        allMoves += solutionSeq
                        
                    # requisitado evento de retroceder todos os passos do tabuleiro
                    elif SOLVE_RECT.collidepoint(event.pos):
                        solution = solvedByReverse(mainBoard, allMoves)
                        makeAllMoves(mainBoard, solution, True)
                        allMoves = []

                    # requisitado evento de resolução por metodo heuristico
                    elif SOLVE_H.collidepoint(event.pos):
                        callResolution(solveByHeuristic, mainBoard, "Heuristica")
                        allMoves += RESULTOFTHREAD

                    # requisitado evento de resolução por metodo de busca em largura
                    elif SOLVE_BFS.collidepoint(event.pos):
                        callResolution(solveByBFS, mainBoard, "BFS")
                        allMoves += RESULTOFTHREAD  

                #verifica se o usuário moveu peças com click do mouse                  
                else:
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            #verifica se o usuário moveu peças com click do teclado       
            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        
        #efetua a ação de movimentação da peça caso o usuário tenha requisitado, seja por teclado ou mouse
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Clique no bloco ou pressione as setas para mover', int(TILESIZE / 2)) # show slide on screen
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)

        #fim mainloop update
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#função para terminar o programa
def terminate():
    pygame.quit()
    sys.exit()

#ferificação de evento de termino do programa
def checkForQuit():
    for event in pygame.event.get(QUIT): 
        terminate() 
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

#retorna as coordenadas de uma peça dado um click
def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

#retorna o ponto inicial no canto superior esquerdo de uma peça
def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

#desenha uma peça
def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

#cria uma opção de texto(surf) retornando, também, seu evento
def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

#desenha o tabuleiro inteiro, com todas as peças, opções e mensagem acima da tela para informar o usuário
def drawBoard(board, message):
    #fundo
    DISPLAYSURF.fill(BGCOLOR)

    #msg
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    #tabuleiro
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    #borda
    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)

    #opções em texto
    DISPLAYSURF.blit(RESET_SURF[0], RESET_RECT[0])
    DISPLAYSURF.blit(RESET_SURF[1], RESET_RECT[1])
    DISPLAYSURF.blit(RESET_SURF[2], RESET_RECT[2])
    DISPLAYSURF.blit(RESET_SURF[3], RESET_RECT[3])
    DISPLAYSURF.blit(SOLVE_SURF_1, SOLVE_RECT)
    DISPLAYSURF.blit(SOLVE_SURF_2, SOLVE_H)
    DISPLAYSURF.blit(SOLVE_SURF_3, SOLVE_BFS)

#realiza a animação do movimento da peça
def slideAnimation(board, direction, message, animationSpeed=ANIMATIONSPEED):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepara o tabuleiro 
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()

    # desenha um espaço em branco sobre a peça na basesurf
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    #animação
    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#chama uma resolução por meio de uma thread para não travar o programa
def callResolution(method, board, nameMethod):
    #init
    global RESULTOFTHREAD           
    RESULTOFTHREAD = []
    thread = Thread(target=method, args=[board])
    thread.start()
    
    # Espera o resultado 
    i = 0
    while not RESULTOFTHREAD:
        drawBoard(board, "Esperando Resultado do algoritmo \"" + nameMethod +"\" " +  "." * ((i%5) + 1))
        i += 1
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    #informa no terminal e atualiza a GUI
    print(RESULTOFTHREAD)
    makeAllMoves(board, RESULTOFTHREAD, True)


#define e retorna uma posição inicial de um tabuleiro
def getStartingBoard():
    board = [[1, 2, 3], [8, BLANK, 4], [7, 6, 5]]
    return board
    
#retorna os indices da posição em branco
def getBlankPosition(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)

#faz uma cópia de um tabuleiro
def copyBoard(board):
    newBoard = []
    for i, x in enumerate(board):
        newBoard.append([])
        for j, y in enumerate(board):
            newBoard[i].append(board[i][j])
    return newBoard

#faz um movimento dado um tabuleiro
def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

# Faz uma sequencia de movimentos em um determinado tabuleiro
def makeAllMoves(board, allMoves, makeOnGUIToo=False):
    if makeOnGUIToo:
        for move in allMoves:
            slideAnimation(board, move, 'Resolvendo...')
            makeMove(board, move)
    else: 
        for move in allMoves:
            makeMove(board, move)

#verifica se dado um movimento é valido ou não dado um tabuleiro
def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)

#retorna todos os movimentos validos de um tabuleiro em uma lista
def getAllValidMoves(board):
    moves = [UP, DOWN, LEFT, RIGHT]
    validMoves = []
    for move in moves:
        if isValidMove(board, move):
            validMoves.append(move)
    return validMoves

#retorna um movimento válido aleatorio dado um tabuleiro
def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    return random.choice(validMoves)

#retorna movimento contrário
def undoMove(move):
    if move == UP:
        oppositeMove = DOWN
    elif move == DOWN:
        oppositeMove = UP
    elif move == RIGHT:
        oppositeMove = LEFT
    elif move == LEFT:
        oppositeMove = RIGHT
    return oppositeMove

#gera um novo jogo a partir de uma quantidade de movimentos aleatorios
def generateNewPuzzle(numSlides):
    #prepara o tabuleiro e espera meio segundo para dar efeito de mudança
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    lastMove = None
    pygame.time.wait(500)

    #movimenta aleatoriamente numSlides vezes atualizando a GUI também para dar efeito de animação
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Gerando novo jogo' + ('.' * (i%5 + 1)))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return (board, sequence)


#função que determina a distancia entre duas peças no tabuleiro (Distancia manhattan)            
def getDistanceBoard(board, solvedBoard):
    sumOfDistances = 0
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            for k in range(BOARDWIDTH):
                for l in range(BOARDHEIGHT):
                    if (board[i][j] != None and board[i][j] == solvedBoard[k][l]):
                        sumOfDistances += abs(i - k) + abs(j - l)
    return sumOfDistances
    
# Retorna uma lista de tabuleiros com todos os movimentos possiveis realizados de um determinado tabuleiro excluindo aqueles tabuleiros setados pelo parametro history 
def makeCopyOfAllPossibleMovesWithoutHistory(board, history = []):
    boardsCopý = []
    for move in getAllValidMoves(board):
        copiedBoard =  copyBoard(board)
        makeMove(copiedBoard, move)
        if copiedBoard not in history:
            boardsCopý.append((copiedBoard, move))
    return boardsCopý

# Resolve por heuristica e retorna uma lista de movimentos possíveis para a resolução de um tabuleiro
def solveByHeuristic(board):
    #init boarders de solução e de teste junto com a lista de movimentos
    start_time = pygame.time.get_ticks()
    global RESULTOFTHREAD
    solvedBoard = getStartingBoard()
    boardChosen = copyBoard(board)
    history = [boardChosen]
    moves = []

    #verifica se a solução já está pronta
    if solvedBoard == boardChosen:
        moves = [getAllValidMoves(boardChosen)[0]]
        moves.append(undoMove(moves[0]))
        RESULTOFTHREAD = moves
        return moves

    #realiza a heuristica
    while boardChosen != solvedBoard:
        print("calculando " + str(boardChosen))
        #copia dos possíveis movimentos dos tabuleiros sem repetir os tabuleiros que ja foram testados anteriormente
        boardsTests = makeCopyOfAllPossibleMovesWithoutHistory(boardChosen, history)

        #caso tenha entrado em loop infinito faz movimento aleatorio
        if not boardsTests:
            move = getRandomMove(boardChosen)
            makeMove(boardChosen, move)
            moves.append(move)
            history.append(boardChosen)
            continue

        #acha o minimo da mannhattan distance
        minD = getDistanceBoard(boardsTests[0][0], solvedBoard)
        for bt, pm in boardsTests:
            if minD > getDistanceBoard(bt, solvedBoard):
                minD = getDistanceBoard(bt, solvedBoard)

        #Pega todos os possíveis movimentos com distancia minima (repetidos)
        allMinsBoards = []
        allMinsMoves = []
        for bt, mp in boardsTests:
            if minD == getDistanceBoard(bt, solvedBoard):
                allMinsBoards.append(bt)
                allMinsMoves.append(mp)

        #escolhe um dos possíveis movimentos com distancia minimia aleatoriamente
        randomInt = random.randint(0, len(allMinsBoards)-1)
        moves.append(allMinsMoves[randomInt])
        boardChosen = allMinsBoards[randomInt]

        #adiciona no histórico
        history.append(boardChosen)

    #retorna os resultados
    RESULTOFTHREAD = moves
    computeTime(start_time)
    return moves

# Resolve por busca em largura e retorna uma lista de movimentos possíveis para a resolução de um tabuleiro
def solveByBFS(board):
    start_time = pygame.time.get_ticks()
    solvedBoard = getStartingBoard()

    #Solução inicial
    queue = []
    for move in getAllValidMoves(board):
        queue.append([move])
    
    while True:
        #checa se a fila está vazia
        if not queue:
            raise Exception("Houve uma falha na busca em largura ;(")
        
        #pop
        solution = queue.pop(0)

        #checa se a solução do topo da fila é a correta, se for retorna 
        newBoard = copyBoard(board)
        makeAllMoves(newBoard, solution)
        print("calculando "+ str(solution))
        if newBoard == solvedBoard:
            global RESULTOFTHREAD
            RESULTOFTHREAD = solution
            computeTime(start_time)
            return solution
            
        #adiciona na fila novas soluções encontradas
        for newNode in getAllValidMoves(newBoard):
            queue.append(solution + [newNode])
    return []

# Retorna uma sequencia de movimentos possíveis para retornar ao estado de inicio
def solvedByReverse(board, allMoves):
    #reverte a lista de movimentos
    revAllMoves = allMoves[:]
    revAllMoves.reverse()
    
    #desfaz todas os movimentos revertidos
    solution = []
    for move in revAllMoves:
        solution.append(undoMove(move))
    return solution


def computeTime(start_time):
    finish_time = pygame.time.get_ticks()
    global SOLUTION_TIME
    SOLUTION_TIME = finish_time - start_time

if __name__ == '__main__':
    main()