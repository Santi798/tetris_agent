"""
        
"""

import numpy as np



class TetrisPlayer:
    """
        
    """
    # Agente que juega Tetris (TETR.IO)

    actions = ('<','>','r','f','_','c') # move left, move right, rotate (right), flip, space (all down), hold
    LEFT = 0
    RIGHT = 1
    ROTATE = 2
    FLIP = 3
    DROP = 4
    HOLD = 5
    

    def __init__(self):
        """
        
        """
        self._current_shape = None  # np.array([])
        self._next_shapes = []      # [np.array([]) for _ in 5]
        self._held_shape = None     # np.array([])
        self._state = np.zeros((20,10), dtype=np.int16)
        self._height = 0    # Altura mínima en las columnas


    def _rotate(self, shape):
        """
        Rota la figura pasada como argumento (matriz)
        90 grados en sentido horario.
        """
        return np.rot90(shape, -1)


    def _collision(self, shape, row, col):
        """
        Devuelve True si la pieza colisiona con el tablero o bloques existentes.
        """
        h, w = shape.shape

        for r in range(h):
            for c in range(w):

                if shape[r, c] == 0:
                    continue

                board_r = row + r
                board_c = col + c

                # Fuera del tablero
                if board_c < 0 or board_c >= 10 or board_r < 0:
                    return (True, None)

                # Colisión con bloque existente
                if self.state[board_r, board_c] != 0:
                    return (True, None)

        return (False,) #, state (ficha puesta en el lugar)

    
    def _cost(self, state, height)

    def _calculate_best_future(self, shape):
        """
        
        """
        # Método que calcula el estado destino, la lista de acciones para llegar a ella 
        # y algún tipo de costo 
        # La idea inicial es que lo haga llevando la figura a la altura mínima y probando
        # para todas sus rotaciones y desplazamientos (cada columna) donde encaja. Se elige
        # la opción de menor costo de las canidatas y, si no hay, se prueba con la siguiente altura...
        cost = 
        found = False
        height = self._height
        while height < 22 and not found:
            column = 0
            while column < 10 and not found:
                shape = shape.copy()
                rotation = 0
                while rotation < 4:
                    collision, state = self._collision(shape, height, column)
                    if not collision:
                        new_cost = _cost(hei)

                
        

        # Return new_state, new_height, new_actions, cost
        pass


    def main_compute(self, perception):
        """
        
        """
        # Método que recibe una lista de figuras nuevas a considerar y devuelve las acciones para llegar
        # al siguiente estado ideal, llevando el estado interno, ignorando el caso inicial self._held_shape = None
        self._next_shapes += perception
        self._current_shape = self._next_shapes.pop(0)

        # Cálculo de futuros para figura actual y la obtenida al hacer hold.
        new_state, new_height, new_actions, cost = self._calculate_best_future(self._current_shape)
        hold_state, hold_height, hold_actions, hold_cost = self._calculate_best_future(self._held_shape)

        # Retorno de las mejores acciones, actualizando estado interno.
        if hold_cost >= cost:

            # Sin hold.
            self._state = new_state
            self._height = new_height
            return new_actions
        
        # Con hold.
        self._state = hold_state
        self._height = hold_height
        self._held_shape = self._current_shape
        return [self.actions[self.HOLD]] + hold_actions


    def compute(self, perception):
        """
        
        """
        # Método que recibe una lista de figuras nuevas a considerar y devuelve las acciones para llegar
        # al siguiente estado ideal, llevando el estado interno
        self._next_shapes += perception     # El ambiente (sensor-actuador) pasaría inicialmente las 5 
                                            # primeras figuras, luego, solo la última de las 5 que vienen 
                                            # (la nueva), a excepción de tras el primer hold, donde pasa 
                                            # las últimas 2 de las 5 que vienen.
        self._current_shape = self._next_shapes.pop(0)

        # Obtención de la siguiente figura si se hiciera hold.
        if self._held_shape:
            hold_shape = self._held_shape.copy()
        else:
            hold_shape = self._next_shapes[0].copy()

        # Cálculo de futuros para figura actual y la obtenida al hacer hold.
        new_state, new_height, new_actions, cost = self._calculate_best_future(self._current_shape)
        hold_state, hold_height, hold_actions, hold_cost = self._calculate_best_future(hold_shape)

        # Retorno de las mejores acciones, actualizando estado interno.
        if hold_cost >= cost:

            # Sin hold.
            self._state = new_state
            self._height = new_height
            return new_actions
        
        # Con hold.
        self._state = hold_state
        self._height = hold_height
        
        if not self._held_shape:
            self._next_shapes.pop(0)
            self.compute = self.main_compute
        
        self._held_shape = self._current_shape
        return [self.actions[self.HOLD]] + hold_actions


