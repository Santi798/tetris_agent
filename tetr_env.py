from time import sleep
from utilities import SetupWindow, TetrBrowser, AreaSearcher, PieceDetector

class Env():
    def __init__(self):
        self.create_page()
        self.wait_for_setup()
        self.find_search_area()
        self.index = 0

    def create_page(self):
        self.browser = TetrBrowser()
        self.driver = self.browser.driver

    def wait_for_setup(self):
        SetupWindow()

    def find_search_area(self):
        self.searcher = AreaSearcher()
        self.detector = PieceDetector()
        self.next_box_corner = self.searcher.get_corner()
        self.searcher.get_box_dim()

    def get_perception(self):
        image = self.searcher.grab_from_corner()

        dims = self.searcher.get_box_dim()

        self.searcher.save(image=image, path=f"next_box{self.index}.png")
        self.index += 1
        return self.detector.detect(image, dims)


if __name__ == "__main__":
    env = Env()
    while True:
        print(env.get_perception())
        sleep(5)
