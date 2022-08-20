from gui.model import Model
from gui.view import Start_page, tk


class Controller(tk.Tk):
    
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.model = Model(self)
        self.raise_page(Start_page)


    def raise_page(self, page):
        container = tk.Frame(self)
        container.pack(
            side = "top", 
            fill = "both", 
            expand = True
        )
        container.grid_rowconfigure(
            0, 
            weight = 1
        )
        container.grid_columnconfigure(
            0, 
            weight = 1
        )
        
        frame = page(
            container, 
            self
        )
        frame.grid(
            row = 0, 
            column = 0, 
            sticky ="nsew"
        )
        self.model.show_frame(page)