"""
TetrisPlayer: Agente que juega TETR.IO automáticamente, llevando altura máxima.

Este agente mantiene internamente el estado del tablero y las figuras 
pendientes, calcula futuros posibles para la figura actual (y la opción 
de hold), evalúa su “costo” en función de la altura mínima alcanzada 
y las filas eliminadas, y devuelve la secuencia de acciones óptima para 
colocar la figura en la mejor posición posible. 

Incluye manejo de:
- Rotación y flips de las piezas.
- Colisiones y colocación de piezas en el tablero.
- Eliminación de filas completas y cálculo de alturas por columna.
- Estrategia de hold para almacenar una pieza temporalmente.
- Estrategia de minimización de altura añadida.
- Estrategia de llenado de filas bajas.
"""

from numpy import zeros, rot90, all, where, arange, sum, cumsum, int16
from numpy import any as np_any


class TetrisPlayer2:
    """
    Agente que juega Tetris (para la página TETR.IO).
    """

    SUPER_COST = 100

    LEFT = 0
    RIGHT = 1
    ROTATE = 2
    FLIP = 3
    DROP = 4
    HOLD = 5

    actions = ('<','>','r','f','_','c')


    def __init__(self, cost_strategy = 'min_height'):
        """
        Constructor del agente con los atributos que requiere para llevar el
        estado interno.
        """
        cost_strategies = {
            'min_height': self._cost_min_height,
            'fill_rows': self._cost_fill_rows
        }
        self._cost = cost_strategies[cost_strategy]         # Método de cálculo de costo
        
        self._current_shape = None                          # Por ejemplo: array([])
        self._next_shapes = []                              # Por ejemplo: [array([]) for _ in 5]
        self._held_shape = None                             # Por ejemplo: array([])
        self._state = zeros((22,10), dtype=int16)           # Tablero
        self._min_height = 0                                # Altura mínima en las columnas
        self._max_height = 1                                # Altura máxima en las columnas


    def _square(self, shape):
        """
        Devuelve True si la figura es el cuadrado.
        """
        return shape.shape[0] == shape.shape[1]
    

    def _line(self, shape):
        """
        Devuelve True si la figura es la línea.
        """
        return shape.shape[0] == 1 or shape.shape[1] == 1
    

    def _rotate(self, shape):
        """
        Rota la figura pasada como argumento (matriz)
        90 grados en sentido horario.
        """
        return rot90(shape, 1)


    def _collision(self, shape, row, col):
        """
        Devuelve:
        - True si la figura colisiona con el tablero o bloques existentes
        - False si se puede colocar, y además devuelve una copia del estado con la figura puesta
        """
        h, w = shape.shape
        new_state = self._state.copy()  # Copia para colocar la figura

        for r in range(h):
            for c in range(w):

                if shape[r, c] == 0:
                    continue

                state_r = row + r
                state_c = col + c

                # Fuera del tablero.
                if state_c < 0 or state_c >= self._state.shape[1] or state_r < 0 or state_r >= self._state.shape[0]:
                    return True, None

                # Colisión con bloque existente.
                if new_state[state_r, state_c] != 0:
                    return True, None

                # Obstáculos encima para hacer drop.
                if np_any(self._state[state_r + 1 :, state_c] != 0):
                    return True, None

                # Colocar bloque en copia del tablero.
                new_state[state_r, state_c] = shape[r, c]

        return False, new_state


    def _kill_rows(self, state, max_height):
        """
        Elimina filas completas hasta max_height y calcula la nueva altura mínima
        entre todas las columnas.
        """
        killed_rows = 0
        row = 0

        while row < max_height:
            # Fila completa.
            if all(state[row] != 0):
                killed_rows += 1

                # Bajar todo lo superior.
                state[row:-1] = state[row+1:]
                state[-1] = 0

                max_height -= 1

            else:
                row += 1

        # Índice de la celda ocupada más alta por columna.
        heights = where(
            state[:self._max_height] != 0,
            arange(self._max_height)[:, None],
            0
        ).max(axis=0)

        # Elegir la altura menor.
        new_min_height = heights.min()
        new_max = heights.max() + 2

        return state, new_min_height, new_max, killed_rows
    

    def _count_holes(self, state, max_height):
        """
        Calcula el número de huecos en el tablero hasta max_height.
        Un hueco es un 0 que tiene un bloque por encima en su columna.
        """
        state = state[:max_height]

        # Donde hay bloques.
        filled = state != 0

        # Indica si ya apareció algún bloque arriba.
        seen_block_above = cumsum(filled[::-1], axis=0)[::-1] > 0

        # Huecos como celdas vacías con bloque arriba.
        holes = (~filled) & seen_block_above

        return sum(holes)
        

    def _cost_min_height(self, state, max_height):
        """
        Calcula el costo del futuro dado, en función de la altura añadida
        correspondiente a la figura operada, descontando filas removidas.
        """
        state, new_min_height, new_max, killed_rows = self._kill_rows(state, max_height)
        return state, new_min_height, new_max, max_height - killed_rows * 4 + self._count_holes(state, max_height) * 3
    

    def _cost_fill_rows(self, state, max_height):
        """
        Calcula el costo del futuro dado, en función del tamaño de las
        filas que coinciden con la posición del agente.
        """
        cost = 0
        for row in range(max_height):
            cost -= sum(state[row]) * 2 ** (-row)

        state, new_min_height, new_max, killed_rows = self._kill_rows(state, max_height)
        cost -= killed_rows * 20
        cost += self._count_holes(state, max_height) * 15
        return state, new_min_height, new_max, cost


    def _calculate_actions(self, shape, column, rotation):
        """
        Cálcula la lista de acciones a realizar para llegar al estado objetivo.
        """
        actions = []
        dist2right = self._state.shape[1] - shape.shape[1] - column

        # Rotaciones.
        if rotation == 1 or rotation == 3:
            actions += [self.actions[self.ROTATE]]

        if rotation == 2 or rotation == 3:
            actions += [self.actions[self.FLIP]]
        
        # Desplazamientos.
        if rotation == 0 or rotation == 2:
            actions += (
                [self.actions[self.LEFT] for _ in (
                range(4 - column) if self._square(shape)
                else range(3 - column))] +
                [self.actions[self.RIGHT] for _ in (
                range(3 - dist2right) if self._line(shape)
                else range(4 - dist2right))]
            )

        elif rotation == 1:
            actions += (
                [self.actions[self.LEFT] for _ in (
                range(5 - column) if self._line(shape)
                else range(4 - column))] +
                [self.actions[self.RIGHT] for _ in (
                range(4 - dist2right))]
            )

        elif rotation == 3:
            actions += (
                [self.actions[self.LEFT] for _ in (
                range(4 - column) if self._line(shape) or self._square(shape)
                else range(3 - column))] +
                [self.actions[self.RIGHT] for _ in (
                range(4 - dist2right) if self._square(shape)
                else range(5 - dist2right))]
            )

        return actions + [self.actions[self.DROP]]

    def _calculate_best_future(self, shape):
        """
        Método que calcula el estado destino, la lista de acciones para llegar a ella 
        y algún tipo de costo asociado a ese futuro.
        """
        state = self._state
        min_height = self._min_height
        max_height = self._max_height
        actions = []
        cost = self.SUPER_COST

        # Recorrido por alturas si no hay candidatos.
        for height in range(self._min_height, self._max_height):
            column = 0

            # Prueba en todas las columnas.
            while column < self._state.shape[1]:
                shape = shape.copy()
                rotation = 0

                # Prueba con todas las rotaciones.
                while rotation < 4:
                    collision, new_state = self._collision(shape, height, column)

                    if not collision:
                        new_state, new_min_heigt, new_max, new_cost = (
                            self._cost(new_state, height + shape.shape[0])
                        )

                        # Se mantiene el futuro de menor costo.
                        if new_cost < cost:
                            state = new_state
                            min_height = new_min_heigt
                            max_height = new_max
                            actions = self._calculate_actions(shape, column, rotation)
                            cost = new_cost

                    shape = self._rotate(shape)
                    rotation += 1

                column += 1

        return state, min_height, max_height, actions, cost


    def _main_compute(self, perception):
        """
        Método principal que recibe una lista de figuras nuevas a considerar y devuelve 
        las acciones para llegar al siguiente estado ideal, llevando el estado interno,
        ignorando el caso inicial donde el espacio de hold está vacío.
        """
        if not perception or any(x is None for x in perception):
            return []
        
        self._next_shapes += perception
        self._current_shape = self._next_shapes.pop(0)

        # Cálculo de futuros para figura actual y la obtenida al hacer hold.
        new_state, new_height, new_max, new_actions, cost = self._calculate_best_future(self._current_shape)
        hold_state, hold_height, hold_max, hold_actions, hold_cost = self._calculate_best_future(self._held_shape)

        # Retorno de las mejores acciones, actualizando estado interno.
        if hold_cost >= cost:

            # Sin hold.
            self._state = new_state
            self._min_height = new_height
            self._max_height = new_max
            return new_actions
        
        # Con hold.
        self._state = hold_state
        self._min_height = hold_height
        self._max_height = hold_max
        self._held_shape = self._current_shape
        return [self.actions[self.HOLD]] + hold_actions


    def compute(self, perception):
        """
        Método principal que recibe una lista de figuras nuevas a considerar y devuelve 
        las acciones para llegar al siguiente estado ideal, llevando el estado interno.
        """
        if not perception or any(x is None for x in perception):
            return []
        
        self._next_shapes += perception     # El ambiente (sensor-actuador) pasaría inicialmente las 5 
                                            # primeras figuras, luego, solo la última de las 5 que vienen 
                                            # (la nueva), a excepción de tras el primer hold, donde pasa 
                                            # las últimas 2 de las 5 que vienen.
                                            # Las figuras percibidas se reciben invertidas.
        self._current_shape = self._next_shapes.pop(0)

        # Obtención de la siguiente figura si se hiciera hold.
        if self._held_shape:
            hold_shape = self._held_shape.copy()
        else:
            hold_shape = self._next_shapes[0].copy()

        # Cálculo de futuros para figura actual y la obtenida al hacer hold.
        new_state, new_height, new_max, new_actions, cost = self._calculate_best_future(self._current_shape)
        hold_state, hold_height, hold_max, hold_actions, hold_cost = self._calculate_best_future(hold_shape)

        # Retorno de las mejores acciones, actualizando estado interno.
        if hold_cost >= cost:

            # Sin hold.
            self._state = new_state
            self._min_height = new_height
            self._max_height = new_max
            return new_actions
        
        # Con hold.
        self._state = hold_state
        self._min_height = hold_height
        self._max_height = hold_max
        
        if not self._held_shape:
            self._next_shapes.pop(0)
            self.compute = self._main_compute
        
        self._held_shape = self._current_shape
        return [self.actions[self.HOLD]] + hold_actions
