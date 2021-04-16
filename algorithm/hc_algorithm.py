from time import time
from random import randint as rand, shuffle
from termcolor import colored
from model.state import State


# TODO = HC es un algoritmo iterativo que comienza con una solución arbitraria a
#  un problema, luego intenta encontrar una mejor solución variando
#  incrementalmente un único elemento de la solución.

class HillClimbing:
    def __init__(self, initialState, dimension, restart):
        self.is_found = False
        self.rand_solution = None
        self.is_restart = restart
        self.d = dimension
        self.running_time = 0
        self.expanded_nodes = 0
        self.board = list()
        self.steps = 0
        self.initial_state = initialState
        self.d = len(initialState.board)
        self.initial_board = initialState.board
        self.solutions = list()

        # Seteamos las variables de inicio

    def start(self):
        if self.initial_state.cost == 0:
            self.solutions.append(self.initial_state.board)
            self.steps = 0
            self.running_time = 0
            self.expanded_nodes = 0
            self.board = self.initial_state.board
            return
        # Seteamos las variables en 0 para comenzar a realizar el algoritmo

        start = time()
        # Creamos tiempo de inicio para saber la duracion de tiempo en segundo
        if not self.is_restart:
            # Si no hay reinicio, hacer esto
            BestCost = self.d * self.d
            # Calculamos el area de la dimension (recordemos que es un cuadrado)
            for i in range(0, self.d):
                for j in range(0, self.d - 1):
                    # Realizamos un recorrido dimensional y realizamos algoritmo
                    BestCost = self.make_temp_board_solution(i, j, BestCost)
            if len(self.solutions) > 0:
                index = rand(0, len(self.solutions) - 1)
                self.rand_solution = self.solutions[index]
        else:
            while not self.is_found:
                BestCost = self.d * self.d
                for i in range(0, self.d):
                    for j in range(0, self.d - 1):
                        # Realizamos un recorrido dimensional
                        BestCost = self.make_temp_board_solution(i, j, BestCost)
                        if BestCost == 0:
                            self.is_found = True
                if len(self.solutions) > 0:
                    index = rand(0, len(self.solutions) - 1)
                    self.rand_solution = self.solutions[index]
                print(self.initial_board, ">>", self.rand_solution, ">>",
                      BestCost)
                self.restart()
            index = rand(0, len(self.solutions))
            self.rand_solution = self.solutions[index]
        end = time()
        # Creamo fin del tiempo para realizar el conteo de la demora en segundos
        self.running_time = end - start
        self.expanded_nodes = (self.d) * (self.d - 1)
        # Calculamos el conteo de nodos en base al area del tablero
        tempBoard = self.initial_board
        self.steps = ((self.rand_solution[1]) * (self.d - 1)) + (
            abs(self.rand_solution[0] - tempBoard[self.rand_solution[1]]))
        tempBoard[self.rand_solution[1]] = self.rand_solution[0]
        self.board = tempBoard

    def make_temp_board_solution(self, i, j, BestCost):
        tempBoard = self.copyBoard()
        # creamos una variable temporal de borde
        tempBoard[i] = (tempBoard[i] + j + 1) % self.d
        tempState = State(tempBoard)
        if tempState.cost < BestCost:
            BestCost = tempState.cost
            self.solutions.clear()
            self.solutions.append([tempBoard[i], i, BestCost])
        elif tempState.cost == BestCost:
            self.solutions.append([tempBoard[i], i, BestCost])
        return BestCost

    def report(self):
        print("* * * * * * * * * * + * + * * * * * * * * * + *")
        print("Algoritmo usado: ***** HILL CLIMBING *******")
        print("Tiempo de ejecución : ", self.running_time, "s")
        print("Numero de pasos : ", self.steps)
        print("Número de nodo expandidos : ", self.expanded_nodes)
        print("La mejor solucion >> ", self.board)
        print("El cuadro final \n")
        print(self.board)
        self.constructBoard([6, 2, 5, 3, 7, 4, 1, 0])
        print("* * * * * * * * * * + * + * * * * * * * * * + *")

    def constructBoard(self, board):
        # Algoritmos para construir el tablero en base a la solucion dado
        finalBoard = list()
        for i in range(0, len(board)):
            temp = ['#'] * self.d
            finalBoard.append(temp)
        for i in range(0, len(board)):
            finalBoard[board[i]][i] = 'H'
        for i in range(0, len(board)):
            for j in range(len(finalBoard[i])):
                if finalBoard[i][j] == 'H':
                    print(colored(finalBoard[i][j], self.getColor(j, board)),
                          end=" ")
                else:
                    print(finalBoard[i][j], end=" ")
            print()

    def copyBoard(self):
        # Algoritmos para copiar el tablero
        temp = list()
        for i in self.initial_board:
            temp.append(i)
        return temp

    def restart(self):
        # Algoritmos para reiniciar el algoritmo
        self.solutions = list()
        self.rand_solution = None
        self.initial_board = list(range(self.d))
        shuffle(self.initial_board)

    def getColor(self, j, board):
        # Funcion para ver el tema de los colores
        for col in range(len(board)):
            if col != j:
                if self.isThreaten(board[j], j, board[col], col):
                    return "red"
        return "green"

    def isThreaten(self, i, param, j, param1):
        # Si coincide las H en el tablero, debe pintarse de rojo
        if i == j:
            return True
        if param == param1:
            return True
        if abs(i - j) == abs(param1 - param):
            return True
        return False
