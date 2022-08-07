from gui.model import Model
from gui.view import View


class Controller:
    
    
    def __init__(self):
        self.model = Model()
        self.view = View(self)


    def main(self):
        self.view.main()

