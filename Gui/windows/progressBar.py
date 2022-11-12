from tkinter import Tk, Frame
from tkinter.ttk import Progressbar, Label
from tkinter.messagebox import showinfo


class determinateProgressBar(Tk):

    def __init__(self, size, title):
        
        super().__init__()

        self.geometry("250x120")
        self.title(title)
        self.size = size
        
        frame = Frame(master=self)
        frame.pack(side = "top", fill = "both", expand = True)

        self.progress_bar = Progressbar(frame, orient="horizontal", mode="determinate", length=size)
        self.progress_bar.pack(padx=10, pady=20)

        self.value_label = Label(frame, text=self.update_progress_label())
        self.value_label.pack(padx=10, pady=10)

    def update_progress_label(self): 
        
        if self.progress_bar['value'] >= 100:
            return f"Current Progress: 100.00%"    
        else:
            return f"Current Progress: {format(self.progress_bar['value'], '.2f')}%"

    def progress(self):    
        
        step = 100 / self.size
        if self.progress_bar['value'] <= self.size:
            self.progress_bar['value'] += step
            self.value_label['text'] = self.update_progress_label()

    def close(self):
        showinfo(message='The progress completed!')
        self.destroy()


class indeterminateProgressBar(Tk):
    
    def __init__(self, size, title):
        
        super().__init__()

        self.geometry("250x120")
        self.title(title)
        self.size = size

        frame = Frame(master=self)
        frame.pack(side = "top", fill = "both", expand = True)

        self.progress_bar = Progressbar(frame, orient="horizontal", mode="indeterminate", length=size)
        self.progress_bar.pack(padx=10, pady=20)

        value_label = Label(self, text=self.update_progress_label())
        value_label.pack(padx=10, pady=10)

        self.flag_increase = True

    def update_progress_label(self):

        return f"The process may take some\ntime, please wait"

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