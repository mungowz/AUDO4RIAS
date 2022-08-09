from gui.model import Model
from gui.view import Start_page, Preparation, Docking


class Controller:
    
    
    def __init__(self):
        self.model = Model()
        self.view = Start_page(self)


    def main(self):
        self.view.main()


    def on_button_click(self, caption):
        if caption == 'Preparation':
            page = Preparation(self)
            self.model.show_frame(page)
        if caption == 'Docking':
            page = Docking(self)
            self.model.show_frame(page)