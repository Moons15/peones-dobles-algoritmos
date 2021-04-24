from algorithm.hc_algorithm import HillClimbing
from algorithm.genetic_algorithm import GeneticAlgorithm
from model.state import State
from utils.reader import Reader

_author_: ['Richard Cancino', 'Elio Campos', 'Gonzalo Uria']
_university_: 'UPC'
_course_: 'I.A'

# TODO = El juego viene de la base de "Damas", donde te mostraremos la mejor
#  combinacion que tendrán los peones dobles, en el que cada uno no se podrá
#  comer a otro peon doble, es decir, solo habrá una H por columna,
#  fila y diagonal (se pintara de amarillo), y se pintará de rojo en caso de
#  que sí haya un peon doble en la misma columna, diagonal o fila

# TODO = Variable para comenzar el juego, se recomienda jugar con Genetica
#  ya que en HC, te muestra una solucion alterna
PLAT_WITH = 'HC'


# TODO = Si desea jugar con el algoritmo Hill Climbing, colocar HC en la
#  constante PLAT_WITH, si en caso desea jugar con Gentica, poner  GA

def play_with_ga(dimension):
    ga = GeneticAlgorithm(500, dimension, 3)
    # TODO = Parametros : Tamaño , Dimension del tablero , transversal
    ga.start()
    ga.report(0)


def play_with_hc(initialSate, dimension):
    hc = HillClimbing(initialSate, dimension, False)
    # TODO = Usando tablero Incial como Estado , Dimension del tablero ,
    #  Poner True si desea reiniciar al momento de encontrar la solucion
    hc.start()
    hc.report()


dimension = 10
# TODO = Se crea un tablero de 10 * 10
r = Reader('sample.txt')
# TODO = Archivo de ejemplo para la creacion del tablero
board = r.readFile()
initialSate = State(board)
# TODO = Setear el tablero en arrays para ser trabajado en el algoritmo

if PLAT_WITH == 'GA':
    play_with_hc(initialSate, dimension)
else:
    play_with_ga(dimension)

# TODO = Conclusion
#  Al parecer, aquí el algoritmo genético está que realiza mucho más rápido
#  La lógica de encontrar la mejor solucion, en caso de que haya un bucle,
#  reiniciar el juego
