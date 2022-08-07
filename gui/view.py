import imp
from re import S
from struct import pack
import tkinter as tk
from tkinter import ttk


class View(tk.Tk):


    PAD = 10

    button_captions = [
        'Preparation',
        'Docking'
    ]


    def __init__(self, controller):
        super().__init__()
        
        self.controller = controller


    def main(self):
        self._home_page()

        self.mainloop()

    
    def _home_page(self):
        self.title('Home Page')

        self.value_var = tk.StringVar()
        
        self._make_main_frame()
        #self._make_entry()
        self._make_button()


    def _make_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=self.PAD, pady=self.PAD)


    def _make_entry(self):
        entry = ttk.Entry(self.main_frame, textvariable=self.value_var) 
        entry.pack()


    def _make_button(self):
        frame = ttk.Frame(self.main_frame)
        frame.pack()   

        for caption in self.button_captions:
            button = ttk.Button(frame, text=caption)
            button.pack()