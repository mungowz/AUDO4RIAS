import tkinter as tk
import os
import prepare_ligands
from tkinter import ttk, IntVar, Checkbutton


class tkinterApp(tk.Tk):


	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		
		container = tk.Frame(self)
		container.pack(
			side='top', 
			fill='both', 
			expand=True
		)

		container.grid_rowconfigure(
			0, 
			weight=1
		)
		container.grid_columnconfigure(
			0, 
			weight=1
		)

		self.frames = {}

		for F in (StartPage, Preparation, Docking, Ligands):

			frame = F(
				container, 
				self
			)
			self.frames[F] = frame

			frame.grid(
				row=0, 
				column=0, 
				sticky="nsew"
			)

		self.show_frame(StartPage)


	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()


class StartPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		menuLabel = ttk.Label(
			self, 
			text='-Select preparation to prepare ligands\n-Select receptors to perform docking or select docking to execute docking', 
			font=('Verdana', 10)
		)
		menuLabel.pack( 
			padx=10, 
			pady=10
		)

		preparationButton = ttk.Button(
			self, 
			text='Preparation',
			command=lambda : controller.show_frame(Preparation)
		)
		preparationButton.pack( 
			padx=10, 
			pady=10
		)

		dockingButton = ttk.Button(
			self, 
			text='Docking',
			command=lambda : controller.show_frame(Docking)
		)
		dockingButton.pack(
			padx=10, 
			pady=10
		)


class Preparation(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)
		menuLabel = ttk.Label(
			self, 
			text ='-Select ligands to prepare ligands\n-Select receptors to prepare receptors\n-Select back to return to start page', 
			font=('Verdana', 10)
		)
		menuLabel.pack( 
			padx=10, 
			pady=10
		)

		ligandsButton = ttk.Button(
			self, 
			text='Ligands',
			command=lambda : controller.show_frame(Ligands)
		)
		ligandsButton.pack(
			padx=10, 
			pady=10
		)
		
		dockingButton = ttk.Button(
			self, 
			text='Docking',
			command=lambda : controller.show_frame(Docking)
		)
		dockingButton.pack( 
			padx=10, 
			pady=10
		)

		backButton = ttk.Button(
			self, 
			text='Back',
			command=lambda : controller.show_frame(StartPage)
		)
		backButton.pack(
			padx=10, 
			pady=10
		)


class Docking(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		label = ttk.Label(self, text ="Page 2", font = ('Verdana', 10))
		label.grid(row = 0, column = 4, padx = 10, pady = 10)

		# button to show frame 2 with text
		# layout2
		button1 = ttk.Button(self, text ="Page 1",
							command = lambda : controller.show_frame(Preparation))
	
		# putting the button in its place by
		# using grid
		button1.grid(row = 1, column = 1, padx = 10, pady = 10)

		button2 = ttk.Button(self, text ="Startpage",
							command = lambda : controller.show_frame(StartPage))
	
		# putting the button in its place by
		# using grid
		button2.grid(row = 2, column = 1, padx = 10, pady = 10)



class Ligands(tk.Frame):
	
	def __init__(self, parent, controller):
		
		tk.Frame.__init__(self, parent)

		command = 'python prepare_ligands.py'
		menu = '-Select keep ligands to keep ligands that have been previously installed\n-Select execute to prepare ligands \
			   \n-Select back to go back to preparation page \
			   \n-Select keep ligands to to keep previously saved ligands'

		menuLabel = ttk.Label(
			self, 
			text=menu, 
			font=('Verdana', 10)
		)
		menuLabel.pack(
			padx=10, 
			pady=10
		)

		
		
		verboseCheckButton = IntVar() 
		verboseButton = Checkbutton(
			self, 
			text='Verbose', 
            variable=verboseCheckButton,
            onvalue=1,
            offvalue=0,
            height=2,
            width=10
		)
		verboseButton.pack(
			padx=10, 
			pady=10
		)

		
		
		keepLigandsCheckButton = IntVar() 
		keepLigandsButton = Checkbutton(
			self, 
			text='keep ligands', 
            variable=keepLigandsCheckButton,
            onvalue=1,
            offvalue=0,
            height=2,
            width=10
		)
		keepLigandsButton.pack(
			padx=10, 
			pady=5
		)

		
		
		excelFolderInput = tk.StringVar()
		excelFileInputLabel = ttk.Label(
			self, 
			text='Define an excel file as input file to select needed ligands otherwise the default folder will be used:', 
			font=('Verdana', 10)
		)
		excelFileInputLabel.pack(
			padx=10, 
			pady=10
		)
		
		excelFileInputEntry = ttk.Entry(
			self, 
			textvariable=excelFolderInput
		)
		excelFileInputEntry.pack(
			padx=10, 
			pady=10
		)

		
		
		excelFolderOutput = tk.StringVar()
		excelFileOutputLabel = ttk.Label(
			self, 
			text='Define a folder where excel files has to be stored or are stored:', 
			font=('Verdana', 10)
		)
		excelFileOutputLabel.pack(
			padx=10, 
			pady=10
		)
		
		excelFileOutputEntry = ttk.Entry(
			self, 
			textvariable=excelFolderOutput
		)
		excelFileOutputEntry.pack(
			padx=10, 
			pady=10
		)

		
		sdfFolder = tk.StringVar()
		sdfFolderLabel = ttk.Label(
			self, 
			text='Define a folder where sdf files has to be stored or are stored:', 
			font=('Verdana', 10)
		)
		sdfFolderLabel.pack(
			padx=10, 
			pady=10
		)
		
		sdfFolderEntry = ttk.Entry(
			self, 
			textvariable=sdfFolder
		)
		sdfFolderEntry.pack(
			padx=10, 
			pady=10
		)


		executeButton = ttk.Button(
			self, 
			text='Execute',
			command=lambda : self.onCheckButton(
				verboseCheckButton.get(), 
				keepLigandsCheckButton.get(),
				excelFileInputEntry.get(),
				excelFileOutputEntry.get(),
				sdfFolderEntry.get(),
				command
			)
		)
		executeButton.pack(
			padx=10, 
			pady=10
		)


	def onCheckButton(self, verboseCheckButton, keepLigandsCheckButton, excelFolderInput, excelFolderOutput, sdfFolder, command):
		if verboseCheckButton:
			command += ' -v'
		if keepLigandsCheckButton:
			command += ' -k'
		if excelFolderInput:
			command += ' -e ' + excelFolderInput
		if excelFolderOutput:
			command += ' -E ' + excelFolderOutput
		if sdfFolder:
			command += ' -s ' + sdfFolder
		
		os.system(command=command)
			


# Driver Code
app = tkinterApp()
app.mainloop()

