from time import sleep
from matplotlib.pyplot import imshow, axis, show
from utilities import SetupWindow, TetrBrowser, AreaSearcher, PieceDetector, TetrActuator


class Env():

    PERCEPT_WAIT = 0.05

    def __init__(self, n_images):
        self.images = [None for _ in range(n_images)]
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
        self.images.append(image)
        self.images.pop(0)

        dims = self.searcher.get_box_dim()
        # self.searcher.save(image=image, path=f"next_box{self.index}.png")
        # self.index += 1
        return self.detector.detect(image, dims)
    
    def _execute(self, actions):
        return self.actuator.act(actions)       # None normalmente
    
    def _main_act_and_sense(self, actions):     # Siempre devuelve el último.
        self._execute(actions)
        sleep(self.PERCEPT_WAIT)
        return self._get_perception()[-1:]

    def act_and_sense(self, actions, last_n=1):
        flag = self._execute(actions)
        sleep(self.PERCEPT_WAIT)
        if not flag:
            return self._get_perception()[-last_n:]
        if flag == self.actuator.FIRST_HOLD_FLAG:
            self.act_and_sense = self._main_act_and_sense
            self.actuator.ignore_hold()
            return self._get_perception()[-last_n-1:]
    
    def show_score(self, n_images):
        axis('off')
        for image in range(n_images):
            imshow(self.images[image])
            show()
