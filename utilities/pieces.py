from numpy import array, int16

class Pieces:
    def __init__(self):
        
        # La simulación se hace espejada horizontalmente
        self.PIECES = {

            'turquoise': array([[1,1,1,1]], dtype=int16),       # I

            'yellow': array([[1,1],[1,1]], dtype=int16),        # O

            'rose': array([[1,1,1],[0,1,0]], dtype=int16),      # T

            'green': array([[1,1,0],[0,1,1]], dtype=int16),     # S

            'red': array([[0,1,1],[1,1,0]], dtype=int16),       # Z

            'orange': array([[1,1,1],[0,0,1]], dtype=int16),    # L

            'blue': array([[1,1,1],[1,0,0]], dtype=int16)       # J
        }

    def get(self, color):
        return self.PIECES.get(color)
