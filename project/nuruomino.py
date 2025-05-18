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
        self.id = Nuroumino.state_id
        Nuroumino.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id

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
        return self.board[row-1][col-1]

    def print_instance(self):
        """Imprime o tabuleiro com o formato descrito na secção 4.2."""
        
        for y in range(0,self.ylength):
            for x in range(0,self.xlength-1):
                print(self.board[y][x],end="\t")
            print(self.board[y][-1],end="\n")


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
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initialBoard = board

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        #TODO
        pass 

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