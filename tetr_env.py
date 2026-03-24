from utilities import SetupWindow, TetrBrowser, AreaSearcher, PieceDetector, TetrActuator
from time import sleep

class Env():
    def __init__(self):
        # self._create_page()
        self._wait_for_setup()
        self._find_search_area()
        self.actuator = TetrActuator()
        # self.index = 0

    def _create_page(self):
        self.browser = TetrBrowser()
        self.driver = self.browser.driver

    def _wait_for_setup(self):
        SetupWindow()

    def _find_search_area(self):
        self.searcher = AreaSearcher()
        self.detector = PieceDetector()
        self.next_box_corner = self.searcher.get_corner()
        self.searcher.get_box_dim()

    def _get_perception(self):
        image = self.searcher.grab_from_corner()

        dims = self.searcher.get_box_dim()

        # self.searcher.save(image=image, path=f"next_box{self.index}.png")
        # self.index += 1
        return self.detector.detect(image, dims)
    
    def _execute(self, actions):
        return self.actuator.act(actions)       # None normalmente
    
    def _main_act_and_sense(self, actions):     # Siempre devuelve el último.
        self._execute(actions)
        sleep(0.05)
        return self._get_perception()[-1:]

    def act_and_sense(self, actions, last_n=1):
        flag = self._execute(actions)
        sleep(0.05)
        if not flag:
            return self._get_perception()[-last_n:]
        if flag == self.actuator.FIRST_HOLD_FLAG:
            self.act_and_sense = self._main_act_and_sense
            self.actuator.ignore_hold()
            return self._get_perception()[-last_n-1:]
