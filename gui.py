import os
from pickle import TRUE
from pydoc import text
from config import Config
import tkinter
import tkinter.messagebox
import customtkinter
from prepare_ligands2 import prepare_ligands

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
                                                command=self.button_event_preparation)
		self.button_1.grid(row=2, column=0, pady=10, padx=20)
		
		self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Docking",
                                                command=self.button_event_docking)
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
                                                   text="Welcome\n-Select Preparation to prepare ligands and receptors\n-Select Docking to perform docking" ,
                                                   height=400,
                                                   corner_radius=6,  # <- custom corner radius
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
		self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

		self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
		self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

    def button_event_preparation(self):
        Preparation()
        self.destroy()
	
	def button_event_docking(self):
		print("button pressed")


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
        self.geometry(f"{Preparation.WIDTH}x{Preparation.HEIGHT}")
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
                                                command=self.button_event_ligands)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Receptors",
                                                command=self.button_event_receptors)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Back",
                                                command=self.button_event_back)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

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
                                                   	text="-Select Ligands to prepare ligands\n-Select receptors to prepare\n-Select back to return to the home page",
                                                   	height=400,
                                                   	corner_radius=6,  # <- custom corner radius
                                                   	fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   	justify=tkinter.LEFT
    											)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

    def button_event_ligands(self):
        self.destroy()
        Ligands()

    def button_event_receptors(self):
        self.destroy()

    def button_event_back(self):
        self.destroy()
        HomePage()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


class Ligands(customtkinter.CTk):
    excel_folder = Config.EXCEL_FOLDER
    excel_folder_flag = False
    excel_file = None
    default_file = os.path.join(Config.INPUT_FOLDER, "pest_group_MOA.xlsx")
    input_file = default_file
    sdf_folder = Config.LIGANDS_SDF_FOLDER
    sdf_folder_flag = False
    pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER
    pdbqt_folder_flag = False
    pdb_folder = Config.LIGANDS_PDB_FOLDER
    pdb_folder_flag = False
    keep_ligands = False
    verbose = True

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Ligands")
        self.geometry(f"{Ligands.WIDTH}x{Ligands.HEIGHT}")
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
                                                text="Execute",
                                                command=self.button_event_execute)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = customtkinter.CTkButton(master=self.frame_left,
                                                text="Back",
                                                command=self.button_event_back)
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

        self.label_info_1 = customtkinter.CTkLabel(
													master=self.frame_info,
                                                   	text="-Select Execute to prepare ligands\n-Select back to return to the home page",
                                                   	height=400,
                                                   	corner_radius=6,  # <- custom corner radius
                                                   	fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   	justify=tkinter.LEFT
    											)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            text="Specify the path of the input excel file or leave it blank to use the default path"
        )
        self.entry.grid(row=4, column=0, columnspan=2, pady=20, padx=20, sticky="we")
        print(self.entry.get())

        self.progressbar = customtkinter.CTkProgressBar(master=self.frame_info)
        self.progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)

    def button_event_execute(self):
        self.destroy()
        prepare_ligands(
            self.verbose, 
            self.excel_file, 
            self.input_file, 
            self.excel_folder_flag, 
            self.excel_folder, 
            self.sdf_folder_flag, 
            self.sdf_folder, 
            self.pdb_folder_flag, 
            self.pdb_folder, 
            self.pdbqt_folder_flag,
            self.pdbqt_folder,
            self.keep_ligands
        )

    def button_event_back(self):
        self.destroy()
        HomePage()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
