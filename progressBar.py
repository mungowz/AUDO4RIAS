from sys import flags
import tkinter
import tkinter.messagebox
from tkinter.messagebox import showinfo
from tkinter import ttk
import time


class   ProgressBar(tkinter.Tk):
    
    WIDTH = 250
    HEIGHT = 120

    def __init__(self, pb_tile, pb_lenght, flag_determinate):
        super().__init__()

        self.title(pb_tile)
        self.geometry(f"{ProgressBar.WIDTH}x{ProgressBar.HEIGHT}")
        self.pb_lenght = pb_lenght
        self.flag_determinate = flag_determinate

        self.frame_pb = tkinter.Frame(master=self)
        if self.flag_determinate:    
            self.progress_bar = ttk.Progressbar(
                                            self,
                                            orient="horizontal",
                                            mode="determinate",
                                            length=100
                                )
        else:
            self.progress_bar = ttk.Progressbar(
                                            self,
                                            orient="horizontal",
                                            mode="indeterminate",
                                            length=100
                                )
            self.flag_increase = True
        self.progress_bar.pack(padx=10, pady=20)

        self.value_label = ttk.Label(
                                self, 
                                text=self.update_progress_label()
        )
        self.value_label.pack(padx=10, pady=10)


    def update_progress_label(self):
        if self.flag_determinate: 
            if self.progress_bar['value'] >= 100:
                return f"Current Progress: 100.00%"    
            else:
                return f"Current Progress: {format(self.progress_bar['value'], '.2f')}%"
        else:
            return f"The process may take some\ntime, please wait"

    def progress(self):
        if self.flag_determinate:    
            step = 100 / self.pb_lenght
            if self.progress_bar['value'] <= self.pb_lenght:
                self.progress_bar['value'] += step
                self.value_label['text'] = self.update_progress_label()
        else:
            self.increase()

    def increase(self):
        if self.progress_bar['value'] < 100 and self.flag_increase:
            self.progress_bar['value'] += 20 
        else:
            self.flag_increase = False
            self.decrease()

    def decrease(self):
        if self.progress_bar['value'] > 0 and not self.flag_increase:
            self.progress_bar['value'] -= 20
        else:
            self.flag_increase = True
            self.increase()

    def close(self):
        showinfo(message='The progress completed!')
        self.destroy()

    def stop(self):
        self.progress_bar.stop()
        self.value_label['text'] = self.update_progress_label()