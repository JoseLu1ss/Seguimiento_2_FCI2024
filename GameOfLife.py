#GOL  
import numpy as np
import random
import os




#from # `IPython.display` is a module that provides a set of functions for displaying interactive
# widgets and output in Jupyter notebooks or IPython environments. In this specific code snippet,
# `IPython.display` is being used to clear the output and display the game board in a visually
# appealing way by updating it dynamically during each iteration of the Game of Life simulation.
#from IPython.display import clear_output
import time


def new_board(x, y, NA, NB):
    """Inicializa un tablero para el Juego de la Vida con dos eespecies"""
    board = []
    for i in range(y):
        Fila = []
        for j in range(x):
            # Escoge aleatoriamente entre las dos eespecies o células muertas
            Tipo_Celula=random.choice([2]*NB + [1]*NA + [0]*(x*y-NA -NB))
            Fila.append(Tipo_Celula)
        board.append(Fila)
    return board

def get(board, x, y):
    """Devuelve el valor en la posición (x, y) en un tablero, haciendo un bucle si está fuera de los límites"""
    return board[y % len(board)][x % len(board[0])]

def assign(board, x, y, value):
    """Asigna un valor en la posición (x, y) en un tablero, haciendo un bucle si está fuera de los límites"""
    board[y % len(board)][x % len(board[0])] = value


def count_neighbors(board, x, y, especies):
    """Cuenta el número de vecinos vivos de una célula en la posición (x, y) de una especie en el tablero"""
    C = 0
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            neighbor_especies = get(board, x + dx, y + dy)
            if neighbor_especies == especies:
                C += 1
    return C

def process_life(board):
    """Crea la siguiente iteración a partir de un estado dado del Juego de la Vida"""
    next_board = [[0] * len(board[0]) for _ in range(len(board))]
    for y in range(len(board)):
        for x in range(len(board[y])): 
            """#Aplicacion de las condiciones de juego. Se modificaron las reglas segun: 
            Condición adicional de competencia: Se incluye una condición adicional en la que una célula se alimente de otra
            con el fin de incluir una dinámica de cazador-presa. Si una célula A está rodeada por un numero mayor que células B
            esta cambia a ser célula tipo B. Las células B fagocitaron la célula A y se produjeron una nueva célula B en su lugar."""
            
            
            especie_actual = get(board, x, y)
            neighbors_especies_1 = count_neighbors(board, x, y, 1)
            neighbors_especies_2 = count_neighbors(board, x, y, 2)

            # Reglas para la especie 1
            if especie_actual == 1:
                if neighbors_especies_2 > neighbors_especies_1:  # La especie 1 se convirerte en una especie 2
                    assign(next_board, x, y, 2)  
                elif neighbors_especies_1 == 2 or neighbors_especies_1 == 3:
                    assign(next_board, x, y, 1)  # La especie 1 sobrevive
                else:
                    assign(next_board, x, y, 0)  # La especie 1 muere por falta de vecinos

            # Reglas para la especie 2
            elif especie_actual == 2:
                if neighbors_especies_1 > neighbors_especies_2:
                    assign(next_board, x, y, 1) 
                elif neighbors_especies_2 == 2 or neighbors_especies_2 == 3:
                    assign(next_board, x, y, 2)  
                else:
                    assign(next_board, x, y, 0)  

            # Reglas para el nacimiento de células muertas
            else:
                if neighbors_especies_1 == 3:
                    assign(next_board, x, y, 1)  # Nace una célula de la especie 1
                elif neighbors_especies_2 == 3:
                    assign(next_board, x, y, 2)  # Nace una célula de la especie 2

    return next_board

#Graficacion
"""
board = new_board(36,36,600,606)
for Fila in board:
    print(Fila)

print("\n")

for _ in range(1):
    board = process_life(board)
    for Fila in board:
        print(Fila)
    print("\n") """
    
def draw_board(board):
    res = ''
    for row in board:
        for col in row:
            if col == 1:
                res +=' 1 '
            if col == 2:
                res +=' 2 '
            else:
                res +='  '
        res += '\n'
    return res


def Seleccion(arreglo, n):
    contador = 0
    for i in arreglo:
        if i == n:
            contador += 1
    return contador



board = new_board(100,100,1000,1006)
h_a=[]
h_b=[]
NUM_ITERATIONS = 1000

for i in range(0, NUM_ITERATIONS):

    print('Iteration ' + str(i + 1))

    board = process_life(board)
    res = draw_board(board)
    Ha=[Seleccion(board[j],1)for j in range(0,len(board[0]))]
    Hb=[Seleccion(board[j],2)for j in range(0,len(board[0]))]
    h_a.append(sum(Ha))
    h_b.append(sum(Hb))
    #print(res)
    time.sleep(0.01)
    #clear_output(wait=True)
    #os.system('cls' if os.name == 'nt' else 'clear')
    #clear_screen()

import matplotlib.pyplot as plt
import numpy as np


plt.hist2d(h_b, h_a, bins=30, density=True)

# Añadir etiquetas y título
plt.xlabel('Celulas Tipo B')
plt.ylabel('Celulas Tipo A')
plt.title('Histograma 2D')

# Mostrar el histograma
plt.colorbar(label='Frecuencia')
plt.show()