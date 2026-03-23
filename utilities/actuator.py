class TetrActuator:

    FIRST_HOLD_FLAG = 'HOLD'

    def __init__(self):

        # Mapeo de la convención del agente
        self.ACTIONS = {

            '<': self._left,
            
            '>': self._right,
            
            'r': self._rotate,
            
            'f': self._flip,
            
            '_': self._drop,
            
            'c': self._hold
        }

    def _left(self):
        print('<')

    def _right(self):
        print('>')

    def _rotate(self):
        print('^')

    def _flip(self):
        print('A')

    def _drop(self):
        print('SPACE')

    def _main_hold(self):           # Sin actualización de flag.
        print('C')

    def _hold(self):
        print('C')
        self._flag = self.FIRST_HOLD_FLAG

    def main_act(self, actions):    # Sin revisión de hold.
        for action in actions:
            self.ACTIONS.get(action)()

    def act(self, actions):
        self._flag = False
        for action in actions:
            self.ACTIONS.get(action)()
        return self._flag
    
    def ignore_hold(self):
        self.act = self.main_act
        self._hold = self._main_hold
