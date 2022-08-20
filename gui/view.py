import tkinter as tk
from tkinter import ttk
from tkinter import font


LARGEFONT =("Verdana", 35)


class Button(tk.Frame):


	def __init__(self, root, controller, button_caption, page_to_raise):
		tk.Frame.__init__(self, root)
		self.root = root
		self.controller = controller
		self.button_caption = button_caption
		self.page_to_raise = page_to_raise
		self.main()


	def main(self):
		button = ttk.Button(
			self.root,
			text=self.button_caption,
			command=lambda : self.controller.raise_page(self.page_to_raise) 
		)
		button.pack()



class Label(tk.Frame):


	def __init__(self, root, controller, label_caption, label_font):
		tk.Frame.__init__(self, root)
		self.root = root
		self.controller = controller
		self.label_caption = label_caption
		self.label_font = label_font
		self.main()


	def main(self):
		label = ttk.Label(
			self.root,
			text=self.label_caption,
			font=self.label_font
		)
		label.grid(
			row=0, 
			column=4, 
			padx=10, 
			pady=10
		)
		label.pack()


class Start_page(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.main()
		

	def main(self):
		Label(
			self, 
			self.controller,
			'Select one button', 
			LARGEFONT
		)

		Button(
			self,
			self.controller,
			'Preparation', 
			Preparation
		)

		Button(
			self, 
			self.controller,
			'Docking',
			Docking
		)
		

class Preparation(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		self.main()
		

	def main(self):
		Label(
			self, 
			self.controller,
			'Select one button', 
			LARGEFONT
		)

		Button(
			self,
			self.controller, 
			'Ligands', 
			Ligands
		)
		
		Button(
			self,
			self.controller, 
			'Receptors', 
			Receptors
		)
		

class Ligands(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller


	def main(self):
		pass


class Receptors(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		

	def main(self):
		pass


class Docking(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		self.controller = controller
		

	def main(self):
		pass		