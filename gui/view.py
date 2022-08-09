import tkinter as tk
from tkinter import BOTH, ttk
from tkinter import font


class View(tk.Tk):


    large_font =("Verdana", 35)


    def __init__(self, controller):
        super().__init__()
        self.controller = controller


    def _make_frame(self, frame_title, frame_width, frame_height):
        dimension = frame_width + 'x' + frame_height 
        self.geometry(dimension)
        self.title(frame_title)
    
        return tk.Frame(self)


    def _make_label(self, caption, label_width):
        return ttk.Label(
            self,
            text=caption,
            width=label_width
        )


    def _make_button(self, caption, button_width):
        return ttk.Button(
            self,
            text=caption,
            width=button_width,
            command=(
                lambda button=caption: self.controller.on_button_click(button)
            )
        )


class Start_page(View):


    def __init__(self, controller):
        super().__init__(controller)
        self.frame = View._make_frame(
            self, 
            'Start page', 
            '300', 
            '100'
        )
        self.frame.pack()

        menu_label = View._make_label(
            self, 
            'Select one button:', 
            30
        )
        menu_label.pack()
        
        preparation_button = View._make_button(
            self, 
            'Preparation', 
            30
        )
        preparation_button.pack()

        docking_button = View._make_button(
            self, 
            'Docking', 
            30
        )
        docking_button.pack()


    def main(self):
        self.frame.tkraise()
        self.mainloop()


class Preparation(View):


    def __init__(self, controller):
        super().__init__(controller)
        self.frame = View._make_frame(
            self, 
            'Preparation', 
            '300', 
            '55'
        )


    def main(self):
        self.frame.tkraise()


class Docking(View):


    def __init__(self, controller):
        super().__init__(controller)
        self.frame = View._make_frame(
            self, 
            'Docking', 
            '300', 
            '55'
        )


    def main(self):
        self.frame.tkraise()
