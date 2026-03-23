from .keys_controller import KeysController
from time import sleep

class TetrActuator:

    FIRST_HOLD_FLAG = 'HOLD'

    LEFT = 0x25
    RIGHT = 0x27
    UP = 0x26
    A = 0x41
    SPACE = 0x20
    C = 0x43

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

        self._controller = KeysController()

    def _left(self):
        self._controller.tap(self.LEFT)

    def _right(self):
        self._controller.tap(self.RIGHT)

    def _rotate(self):
        self._controller.tap(self.UP)

    def _flip(self):
        self._controller.tap(self.A)

    def _drop(self):
        self._controller.tap(self.SPACE)

    def _main_hold(self):           # Sin actualización de flag.
        self._controller.tap(self.C)

    def _hold(self):
        self._controller.tap(self.C)
        self._flag = self.FIRST_HOLD_FLAG

    def main_act(self, actions):    # Sin revisión de hold.
        for action in actions:
            self.ACTIONS.get(action)()
            sleep(0.2)          ##### DEBUG #####

    def act(self, actions):
        self._flag = False
        for action in actions:
            self.ACTIONS.get(action)()
            sleep(0.2)          ##### DEBUG #####
        return self._flag
    
    def ignore_hold(self):          # Llamada desde el env
        self.act = self.main_act
        self._hold = self._main_hold
