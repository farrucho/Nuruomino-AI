# Lê uma instância de NURUOMINO a partir do standard input no formato descrito na secção 4.1.
# O programa deve resolver o problema utilizando uma técnica à escolha e imprimir a solução para o standard output no formato descrito na secção 4.2.


# import sys

# with open(sys.argv[1],'r') as in_file


# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 52:
# 100286 André Gonçalo Dias Feliciano
# 106345 Francisco Dinis Feteira Laranjo

from search import Problem
from search import Node

import numpy as np

from sys import stdin

class NuruominoState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        # WTF OQUE É ISTO DO ID?
        # self.id = Nuroumino.state_id
        # Nuroumino.state_id += 1

    # def __lt__(self, other):
    #     """ Este método é utilizado em caso de empate na gestão da lista
    #     de abertos nas procuras informadas. """
    #     return self.id < other.id

    def getBoard(self):
        return self.board
    


class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""
    def __init__(self, board : list):
        self.board = np.array(board)
        self.xlength = np.size(self.board,axis=0)
        self.ylength = np.size(self.board,axis=1)

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""

        adjacent_list = []
        regionChar = str(region)
        
        for row in range(0,self.xlength):
            for col in range(0,self.ylength):
                if self.board[row][col] == regionChar:
                    adjacent_cells = []

                    if row > 0:
                        adjacent_cells.append(self.board[row - 1][col])     # Up
                    if row < self.xlength - 1:
                        adjacent_cells.append(self.board[row + 1][col])     # Down
                    if col > 0:
                        adjacent_cells.append(self.board[row][col - 1])     # Left
                    if col < self.ylength - 1:
                        adjacent_cells.append(self.board[row][col + 1])     # Right

                    for elem in adjacent_cells:
                        if elem not in adjacent_list and elem not in regionChar: 
                            adjacent_list.append(elem) 
        
        return adjacent_list
    
    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        
        adjacent_positions_list = []
        regionChar = str(self.board[row-1][col-1]) # argument region
        
        for row in range(0,self.xlength):
            for col in range(0,self.ylength):
                if self.board[row][col] == regionChar:
                    adjacent_cells = []

                    if row > 0:
                        adjacent_cells.append(f"l{row-1 + 1}c{col + 1}")     # Top
                        if col > 0:
                            adjacent_cells.append(f"l{row-1 + 1}c{col-1 + 1}") # Left-Top
                        if col < self.ylength - 1:
                            adjacent_cells.append(f"l{row-1 + 1}c{col+1 + 1}") # Right-Top
                    if row < self.xlength - 1:
                        adjacent_cells.append(f"l{row+1 + 1}c{col + 1}")     # Bot
                        if col > 0:
                            adjacent_cells.append(f"l{row+1 + 1}c{col-1 + 1}") # Left-Bot
                        if col < self.ylength - 1:
                            adjacent_cells.append(f"l{row+1 + 1}c{col+1 + 1}") # Right-Bot
                    if col > 0:
                        adjacent_cells.append(f"l{row + 1}c{col-1 + 1}")     # Left
                    if col < board.ylength - 1:
                        adjacent_cells.append(f"l{row + 1}c{col+1 + 1}")     # Right

      


                    for elem in adjacent_cells:
                        if elem not in adjacent_positions_list and self.board[int(elem[1])-1][int(elem[3])-1] not in regionChar: 
                            adjacent_positions_list.append(elem) 
        
        return adjacent_positions_list

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        
        adjacent_values_list = []
        regionChar = str(self.board[row-1][col-1]) # argument region
        
        for row in range(0,self.xlength):
            for col in range(0,self.ylength):
                if self.board[row][col] == regionChar:
                    adjacent_cells = []

                    if row > 0:
                        adjacent_cells.append(self.board[row-1][col])     # Top
                        if col > 0:
                            adjacent_cells.append(self.board[row-1][col-1]) # Left-Top
                        if col < self.ylength - 1:
                            adjacent_cells.append(self.board[row-1][col+1]) # Right-Top
                    if row < self.xlength - 1:
                        adjacent_cells.append(self.board[row+1][col])     # Bot
                        if col > 0:
                            adjacent_cells.append(self.board[row+1][col-1]) # Left-Bot
                        if col < self.ylength - 1:
                            adjacent_cells.append(self.board[row+1][col+1]) # Right-Bot
                    if col > 0:
                        adjacent_cells.append(self.board[row][col-1])     # Left
                    if col < board.ylength - 1:
                        adjacent_cells.append(self.board[row][col+1])     # Right


                    for elem in adjacent_cells:
                        if elem not in adjacent_values_list and elem not in regionChar: 
                            adjacent_values_list.append(elem) 
        
        return adjacent_values_list
    
    def get_value(self, row:int, col:int) -> chr:
        """Devole o valor do tabuleiro com base na posição dada"""
        return self.board[row-1][col-1]

    def print_instance(self):
        """Imprime o tabuleiro com o formato descrito na secção 4.2."""
        
        for y in range(0,self.ylength):
            for x in range(0,self.xlength-1):
                print(self.board[y][x],end="\t")
            print(self.board[y][-1],end="\n")

    def available_regions(self) -> list:
        """Devolve todas as regiões do tabuleiro."""
        regions = []
        for y in range(0,self.ylength):
            for x in range(0,self.xlength):
                current_elem = self.board[y][x]
                if current_elem not in regions:
                    regions.append(current_elem)
        return regions
    
    def getAllActions(self) -> list:
        "Devolve lista com espaço completo das ações"
        # todas as combinacoes possiveis de peças+orientações
        all_placements = []

        # pecas dadas
        pieces = [
                ['L', [[1,0],[1,0],[1,1]]], # L
                ['I', [[1],[1],[1],[1]]], # I
                ['T', [[[1,0],[1,1],[1,0]]]], # T
                ['S', [[1,0],[1,1],[0,1]]] # S
                ]
        
        orientations = [] # manter histórico de orientações repetidas
        for piece in pieces:
            for i in range(1,4):
                normal = [piece[0],np.rot90(piece[1],i).tolist()]
                vertical = [piece[0],np.rot90(np.flipud(piece[1]),i).tolist()]
                horizontal = [piece[0],np.rot90(np.fliplr(piece[1]),i).tolist()]
                
                if normal[1] not in orientations:
                    all_placements.append(normal)
                    orientations.append(normal[1])
                if vertical[1] not in orientations:
                    all_placements.append(vertical)
                    orientations.append(vertical[1])
                if horizontal[1] not in orientations:
                    all_placements.append(horizontal)
                    orientations.append(horizontal[1])
        return all_placements
        

    # def get_region(self, region:int):
    #     """Devolve a forma da região."""
        # for y in range(0,self.ylength):
        #     for x in range(0,self.xlength):
        #         current_elem = self.board[y][x]
        #         if current_elem not in regions:
        #             regions.append(current_elem)
        # return regions

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
        
        newBoard = []
        text = stdin.readlines()
        for line in text:
            newBoard += [line.split()]

        return Board(newBoard)


class Nuruomino(Problem):
    # estamos com um problema que é como é que o computador sabe distinguir a área mesmo em si que esta preenhcida, tem que haver uma array que de tracking das regioes preenchidas e com que peça!!!! isto pode ser um problema a posteriori
    
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initialBoard = board

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        stateBoard = state.getBoard()
        arrayBoard = stateBoard.board

        # action -> (REGION, TETROMINO_CHAR, ORIENTATION)
        available_regions = stateBoard.available_regions()

        all_actions = stateBoard.getAllActions()

        possible_actions = []
        for y in range(0,stateBoard.ylength):
            for x in range(0,stateBoard.xlength):
                if arrayBoard[y][x].isdigit():
                    # se a célula já está preenchida não vale a pena procurar mais
                    for piece_char, orientation in all_actions:
                        piece = np.array(orientation)
                        if piece.ndim == 3:
                            # fix para nao ficar com np.array de 3 dimensões, nos casos por exemplo [1,0],[1,0],[1,1] ou [1] [1] [1] [1]
                            piece = piece.squeeze()

                        if y + piece.shape[0] <= arrayBoard.shape[0] and x + piece.shape[1] <= arrayBoard.shape[1]:
                            # se a peça encaixa no tabuleiro
                            sub_board = arrayBoard[y : y + piece.shape[0], x : x + piece.shape[1]]

                            mask = (piece == 1)
                                        
                            # print("debugging")
                            # print(y,x)
                            # print(mask)
                            # print(sub_board)
                            # print(piece)
            
                            if np.all(sub_board[mask] == arrayBoard[y][x]) and [arrayBoard[y][x], piece_char, orientation] not in possible_actions:
                                possible_actions.append([arrayBoard[y][x], piece_char, orientation])
        return possible_actions

                
        

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a, 'action' sobre
       , 'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        #TODO
        pass 
        

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #TODO
        pass 

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


if __name__ == "__main__":
    # Exemplo 1
    # Ler grelha do figura 1a:
    # board = Board.parse_instance()
    # print(board.board)
    # print(board.adjacent_regions(1))
    # print(board.adjacent_regions(3))
    # Output:
    # [2, 3]
    # [1, 2, 4, 5]

    # python nuruomino.py < ../projbase-02-05/sample-nuruominoboards/test-01.txt
    # para conseguir fazer -i 
    board = Board([['1', '1', '2', '2', '3', '3'],
                    ['1', '2', '2', '2', '3', '3'],
                    ['1', '3', '3', '2', '3', '5'],
                    ['3', '3', '3', '3', '3', '5'],
                    ['4', '4', '4', '3', '3', '5'],
                    ['4', '3', '3', '3', '3', '5']])
    a = board.board
    print(board.adjacent_regions(3))
    print(board.adjacent_positions(1,1))
    print(board.adjacent_values(1,1))
    
    board.print_instance()
    print(board.get_value(3,1))
    print(board.available_regions())

    problem = Nuruomino(board)
    initial_state = NuruominoState(board)
    for e in sorted(problem.actions(initial_state),key=lambda x:x[0]):
        print(e)