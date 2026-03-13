from numpy import array

class Pieces:
    def __init__(self):

        self.PIECES = {

            'turquoise': [          # I
                array([[1,1,1,1]]),         # 0 — base: horizontal
                array([[1],[1],[1],[1]])     # 1 — vertical
            ],

            'yellow': [             # O
                array([[1,1],[1,1]])         # 0 — única orientación
            ],

            'rose': [               # T
                array([[0,1,0],[1,1,1]]),    # 0 — base: punta arriba
                array([[1,0],[1,1],[1,0]]),  # 1 — giro der: punta derecha
                array([[1,1,1],[0,1,0]]),    # 2 — giro 180: punta abajo
                array([[0,1],[1,1],[0,1]])   # 3 — giro izq: punta izquierda
            ],

            'green': [              # S
                array([[0,1,1],[1,1,0]]),    # 0 — base: diagonal
                array([[1,0],[1,1],[0,1]])   # 1 — vertical
            ],

            'red': [                # Z
                array([[1,1,0],[0,1,1]]),    # 0 — base: diagonal
                array([[0,1],[1,1],[1,0]])   # 1 — vertical
            ],

            'orange': [             # L
                array([[0,0,1],[1,1,1]]),    # 0 — base: pico arriba-derecha
                array([[1,0],[1,0],[1,1]]),  # 1 — giro der: pie abajo-derecha
                array([[1,1,1],[1,0,0]]),    # 2 — giro 180: pico abajo-izquierda
                array([[1,1],[0,1],[0,1]])   # 3 — giro izq: pie arriba-izquierda
            ],

            'blue': [               # J
                array([[1,0,0],[1,1,1]]),    # 0 — base: pico arriba-izquierda
                array([[1,1],[1,0],[1,0]]),  # 1 — giro der: pie arriba-izquierda
                array([[1,1,1],[0,0,1]]),    # 2 — giro 180: pico abajo-derecha
                array([[0,1],[0,1],[1,1]])   # 3 — giro izq: pie abajo-derecha
            ],
        }

    def get(self, color, rotation=0):
        orientations = self.PIECES[color]
        return orientations[rotation % len(orientations)]
