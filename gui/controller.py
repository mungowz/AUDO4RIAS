from gui.model import Model
from gui.view import Start_page, tk


class Controller(tk.Tk):
    
    
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.container = tk.Frame(self)
        self.container.pack(
            side = "top", 
            fill = "both", 
            expand = True
        )
        self.container.grid_rowconfigure(
            0, 
            weight = 1
        )
        self.container.grid_columnconfigure(
            0, 
            weight = 1
        )

        self.model = Model(self)
        self.raise_page(Start_page)


    def raise_page(self, page):
        frame = page(
            self.container, 
            self
        )
        frame.grid(
            row = 0, 
            column = 0, 
            sticky ="nsew"
        )
        page.tkraise(self)
        #self.model.show_frame(page)