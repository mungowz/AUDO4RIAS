import tkinter
import tkinter.messagebox
import customtkinter

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class HomePage(customtkinter.CTk):
	WIDTH = 780
	HEIGHT = 520
	
	def __init__(self):
		super().__init__()
		
		self.title("Home Page")
		self.geometry(f"{HomePage.WIDTH}x{HomePage.HEIGHT}")
		self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)
		
		self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
		self.frame_left.grid(row=0, column=0, sticky="nswe")
		
		self.frame_right = customtkinter.CTkFrame(master=self)
		self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
		self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
		self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
		self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
		self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing
		
		self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Options:",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
		self.label_1.grid(row=1, column=0, pady=10, padx=10)
		self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Preparation",
                                                command=self.button_event)
		self.button_1.grid(row=2, column=0, pady=10, padx=20)
		
		self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Docking",
                                                command=self.button_event)
		self.button_2.grid(row=3, column=0, pady=10, padx=20)
		
		self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
		self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")
		
		self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
		self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
		self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
		self.frame_right.rowconfigure(7, weight=10)
		self.frame_right.columnconfigure((0, 1), weight=1)
		self.frame_right.columnconfigure(2, weight=0)

		self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
		self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
		self.frame_info.rowconfigure(0, weight=1)
		self.frame_info.columnconfigure(0, weight=1)

		self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Welcome\n-Select preparation to prepare ligands and receptors\n" \
													"-Select docking to perform docking" ,
                                                   height=400,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
		self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

		self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
		self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

	def button_event(self):
		self.destroy()
		Preparation()

	def change_appearance_mode(self, new_appearance_mode):
		customtkinter.set_appearance_mode(new_appearance_mode)
	
	def on_closing(self, event=0):
		self.destroy()

class Preparation(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Preparation")
        self.geometry(f"{HomePage.WIDTH}x{HomePage.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Options:",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_1 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Ligands",
                                                command=self.button_event)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Receptors",
                                                command=self.button_event)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)
        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Receptors",
                                                command=self.button_event)
        self.button_3.grid(row=3, column=0, pady=10, padx=20)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(
													master=self.frame_info,
                                                   	text="-Select Ligands to prepare ligands\n" \ 
														"-Select receptors to prepare\n" \
														"-Select back to return to the home page",
                                                   	height=400,
                                                   	corner_radius=6,  # <- custom corner radius
                                                   	fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   	justify=tkinter.LEFT
    											)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

    def button_event(self):
        print("Button pressed")

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

'''
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
'''
