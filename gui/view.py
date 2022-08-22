import tkinter as tk
from tkinter import ttk


LARGEFONT =("Verdana", 35)


class Button(tk.Frame):


	def __init__(self, root, controller, button_caption, page_to_raise, button_row):
		tk.Frame.__init__(self, root)
		self.root = root
		self.controller = controller
		self.button_caption = button_caption
		self.page_to_raise = page_to_raise
		self.button_row = button_row
		self.main()


	def main(self):
		button = ttk.Button(
			self.root,
			text=self.button_caption,
			command=lambda : self.controller.raise_page(self.page_to_raise) 
		)	
		button.grid(
			row = self.button_row, 
			column = 1, 
			padx = 10, 
			pady = 10
		)
		button.pack()


class Label(tk.Frame):


	def __init__(self, root, controller, label_caption, label_font, label_row):
		tk.Frame.__init__(self, root)
		self.root = root
		self.controller = controller
		self.label_caption = label_caption
		self.label_font = label_font
		self.label_row = label_row
		self.main()


	def main(self):
		label = ttk.Label(
			self.root,
			text=self.label_caption,
			font=self.label_font
		)
		label.grid(
			row=self.label_row, 
			column=4, 
			padx=10, 
			pady=10
		)
		label.pack()


class Start_page(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.label_row = 1
		self.button_row = 1
		self.controller = controller
		self.main()
		

	def main(self):
		Label(
			self, 
			self.controller,
			'Select one button', 
			LARGEFONT,
			self.label_row
		)
		self.label_row += 1

		Button(
			self,
			self.controller,
			'Preparation', 
			Preparation,
			self.button_row
		)
		self.button_row +=1

		Button(
			self, 
			self.controller,
			'Docking',
			Docking,
			self.button_row
		)
		self.button_row +=1
		

class Preparation(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.label_row = 1
		self.button_row = 1
		self.controller = controller
		self.main()
		

	def main(self):
		Label(
			self, 
			self.controller,
			'Select one button', 
			LARGEFONT,
			self.label_row
		)
		self.label_row +=1

		Button(
			self,
			self.controller, 
			'Ligands', 
			Ligands,
			self.button_row
		)
		self.button_row +=1
		
		Button(
			self,
			self.controller, 
			'Receptors', 
			Receptors,
			self.button_row
		)
		self.button_row +=1
		

class Ligands(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.label_row = 1
		self.button_row = 1
		self.controller = controller


	def main(self):
		pass


class Receptors(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.label_row = 1
		self.button_row = 1
		self.controller = controller
		

	def main(self):
		pass


class Docking(tk.Frame):
	
	
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)

		self.label_row = 1
		self.button_row = 1
		self.controller = controller
		

	def main(self):
		pass		