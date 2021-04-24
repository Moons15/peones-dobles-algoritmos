from copy import deepcopy
from random import shuffle
from random import randint as rand
from time import time
from termcolor import colored
from model.state import State


# TODO = Los algoritmos genéticos (AG) funcionan entre el conjunto de
#  soluciones de un problema llamado fenotipo, y el conjunto de individuos
#  de una población natural, codificando la información de cada solución
#  en una cadena, generalmente binaria, llamada cromosoma. Los símbolos que
#  forman la cadena son llamados genes. Cuando la representación de los
#  cromosomas se hace con cadenas de dígitos binarios se le conoce como
#  genotipo. Los cromosomas evolucionan a través de iteraciones,
#  llamadas generaciones. En cada generación, los cromosomas son evaluados
#  usando alguna medida de aptitud. Las siguientes generaciones (nuevos
#  cromosomas), son generadas aplicando los operadores genéticos repetidamente,
#  siendo estos los operadores de selección, cruzamiento, mutación y reemplazo.

class GeneticAlgorithm:
    def __init__(self, population, dimension, crossover):
        self.generationNumber = 1
        self.pSize = population
        self.d = dimension
        self.co = crossover
        self.environment = list()
        self.solved = False
        self.solution = None
        self.un = list()
        self.minCosts = list()
        self.runningTime = 0
        self.expandedNodes = population

        # Seteamos las variables para iniciar en el constructor

    def start(self):
        start = time()
        # Iniciamos el tiempo
        self.initializeEnvironmnt()
        self.checkGoal()
        aux = 0
        while not self.solved:
            # Hacemos un bucle hasta que se encuentre la solucion del juego
            self.generationNumber += 1
            # Creamos un incrementador para ver el numero de generaciones
            chroms = self.crossOver()
            # Se ejecuta la funciona para setear los "cromosomas" en cada entorno
            self.updateEnvironment()
            # Actualizamod el entorno
            self.checkGoal()
            try:
                if not self.solved:
                    aux += 1
                    if aux > 20:
                        break
            except:
                pass
            # Revisamos si se encontró la solución o no
        end = time()
        # Finalizamos el tiempo
        self.runningTime = end - start
        # Calculamos la diferencia de tiempo en segundos
        if len(self.un) != 0:
            self.expandedNodes = len(self.un)
            # Calculamos los nodos expandidos

    def initializeEnvironmnt(self):
        for i in range(self.pSize):
            chrom = list(range(self.d))
            shuffle(chrom)
            while chrom in self.environment:
                shuffle(chrom)
            self.environment.append(chrom)

    def checkGoal(self):
        for chrom in self.environment:
            state = State(chrom)
            if (state.cost == 0):
                self.solved = True
                self.solution = chrom

    def crossOver(self):
        for i in range(0, len(self.environment) - 1, 2):
            chrom1 = self.environment[i][:]
            chrom2 = self.environment[i + 1][:]
            chromo1 = chrom1[0:self.co] + chrom2[self.co:]
            chromo2 = chrom2[0:self.co] + chrom1[self.co:]
            self.mutant(chromo1)
            self.mutant(chromo2)

    def mutant(self, param):
        choice = rand(0, 3)
        if choice == 0:
            self.mutantZero(param)
        elif choice == 1:
            self.mutantOne(param)
        elif choice == 2:
            self.mutantTwo(param)

    def updateEnvironment(self):
        # Aqui vamos a actualizar el entorno
        for chrom in self.environment:
            # Por cada cromo en el entorno, si no esta en el listado,
            # aumentarlo mediante un append
            if chrom not in self.un:
                self.un.append(chrom)
        self.minCosts = list()
        costs = list()
        newEnvironment = list()
        # Creamos un nuevo entorno
        for chrom in self.environment:
            state = State(chrom)
            costs.append(state.cost)
        if min(costs) == 0:
            self.solution = costs.index(min(costs))
            self.goal = self.environment[self.solution]
            return self.environment
        while len(newEnvironment) < self.d:
            minCost = min(costs)
            minIndex = costs.index(minCost)
            self.minCosts.append(costs[minIndex])
            newEnvironment.append(self.environment[minIndex])
            costs.remove(minCost)
            self.environment.remove(self.environment[minIndex])
        self.environment = newEnvironment
        # Seteamos la nueva variable en el entorno ya mencionado
        # para seguir trabajando con esto
        print(self.minCosts, ">>", len(self.un))

    def report(self, number):
        print("* * * * * * * * * * + * + * * * * * * * * * + *")
        print("Algoritmo usado: ***** GENETICA *******")
        print("Tiempo de ejecución : ", self.runningTime, "s")
        print("Numero de generaciones : ", self.generationNumber)
        print("Numero de nodos expandidos : ", self.expandedNodes)
        print("La mejor solucion>> ", self.solution)
        print("Numero de iteraciones: ", number)
        print("Cuadro final\n")
        self.constructBoard()

    def constructBoard(self):
        aux = 5
        # Construcion del tablero en base a la solución
        try:
            if self.solution is not None:
                print('SE ENCONTRÓ LA SOLUCIÓN')
            else:
                print("NO ENCONTRO SOLUCION......... VOLVIENDO A EJECUTAR")
                aux += 1
                new = GeneticAlgorithm(500, 10, 3)
                new.start()
                new.report(aux)
        except:
            pass
        try:
            for i in range(0, len(self.solution)):
                temp = ['#'] * self.d
                index = self.solution.index(i)
                temp[index] = 'H'
                for j in range(len(temp)):
                    if temp[j] == 'H':
                        print(colored(temp[j], self.getColor(j, self.solution)),
                              end=" ")
                    else:
                        print(temp[j], end=" ")
                print()
        except:
            pass

    def mutantZero(self, param):
        bound = self.d // 2
        leftIndex = rand(0, bound)
        RightIndex = rand(bound + 1, self.d - 1)
        newGen = []
        for dna in param:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.d):
            if i not in newGen:
                newGen.append(i)
        gen = newGen
        gen[leftIndex] = gen[RightIndex]
        gen[RightIndex] = gen[leftIndex]
        self.environment.append(gen)

    def mutantOne(self, param):
        newGen = []
        for dna in param:
            if dna not in newGen:
                newGen.append(dna)
        for i in range(self.d):
            if i not in newGen:
                newGen.append(i)
        gen = newGen
        for i in range(0, len(gen), 2):
            temp = deepcopy(gen[i])
            gen[i] = gen[i + 1]
            gen[i + 1] = temp
        self.environment.append(gen)

    def mutantTwo(self, param):
        bound = self.d // 2
        leftIndex = rand(0, bound)
        RightIndex = rand(bound + 1, self.d - 1)
        newGen = []
        for dna in param:
            newGen.append(dna)
        gen = newGen
        gen[leftIndex] = gen[RightIndex]
        gen[RightIndex] = gen[leftIndex]
        self.environment.append(gen)

    def mutantThree(self, param):
        newGen = []
        for dna in param:
            newGen.append(dna)
        gen = newGen
        while gen not in self.environment:
            print(gen, len(self.environment))
            shuffle(gen)
        self.environment.append(gen)

    def getColor(self, j, board):
        for col in range(len(board)):
            if col != j:
                if self.isThreaten(board[j], j, board[col], col):
                    return "red"

        return "green"

    def isThreaten(self, i, param, j, param1):
        if i == j:
            return True
        if param == param1:
            return True
        if abs(i - j) == abs(param1 - param):
            return True
        return False
