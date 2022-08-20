class Model:
    

    def __init__(self, controller):
        self.controller = controller


    def show_frame(self, page):
        page.tkraise(self.controller)
    