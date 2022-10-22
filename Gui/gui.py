import os
from tkinter import ttk
from config import Config
import tkinter
import tkinter.messagebox
from tkinter.messagebox import showinfo
import customtkinter
from Gui.prepare_ligands2 import *


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class HomePage(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        
        self.title("Home Page")
        self.geometry(f"{780}x{520}")
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

class ProgressBar(tkinter.Tk):
    
    WIDTH = 300
    HEIGHT = 120

    def __init__(self, pb_tile, pb_lenght):
        super().__init__()

        self.title(pb_tile)
        self.geometry(f"{ProgressBar.WIDTH}x{ProgressBar.HEIGHT}")
        self.pb_lenght = pb_lenght

        self.frame_pb = tkinter.Frame(master=self)
        self.progress_bar = ttk.Progressbar(
                                            self,
                                            orient="horizontal",
                                            mode="determinate",
                                            length=100,
        )
        self.progress_bar.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

        self.value_label = ttk.Label(
                                self, 
                                text=self.update_progress_label()
        )
        self.value_label.grid(column=0, row=1, columnspan=2)


    def update_progress_label(self):
        return f"Current Progress: {self.progress_bar['value']}%"


    def progress(self):
        if self.progress_bar['value'] < self.pb_lenght:
            self.progress_bar['value'] += 1 / 289
            self.value_label['text'] = self.update_progress_label()
        else:
            showinfo(message='The progress completed!')
            self.quit()


    def stop(self):
        self.progress_bar.stop()
        self.value_label['text'] = self.update_progress_label()
        

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
    default_file = os.path.join(Config.INPUT_FOLDER, "pest_group_MOA.xlsx")
    input_file = default_file
    excel_file = default_file
    sdf_folder = Config.LIGANDS_SDF_FOLDER
    pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER
    pdb_folder = Config.LIGANDS_PDB_FOLDER
    keep_ligands = False
    verbose = True

    WIDTH = 780
    HEIGHT = 500

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

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=1, rowspan=1, pady=1, padx=1, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info = customtkinter.CTkLabel(
                                                    master=self.frame_info,
                                                       text="-Select Execute to prepare ligands\n-Select back to return to the home page",
                                                       height=2,
                                                       corner_radius=1,  # <- custom corner radius
                                                       fg_color=("white", "gray38"),  # <- custom tuple-color
                                                       justify=tkinter.LEFT
                                                )
        self.label_info.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        self.label_excel_file = customtkinter.CTkLabel(
                                                    master=self.frame_right,
                                                    height=1,
                                                    text="Specify the path of the input excel file or leave it blank to use the default path:",
        )
        self.label_excel_file.grid(column=0, row=1, sticky="nwe", padx=1, pady=1)
        self.entry_excel_file = customtkinter.CTkEntry(
                                                        master=self.frame_right,
                                                        width=120,
        )
        self.entry_excel_file.grid(row=2, column=0, columnspan=1, pady=1, padx=1, sticky="nwe")

        self.label_excel_folder = customtkinter.CTkLabel(
                                                    master=self.frame_right,
                                                    height=1,
                                                    text="Specify the path of the input excel folder or leave it blank to use the default path:"
        )
        self.label_excel_folder.grid(column=0, row=4, sticky="nwe", padx=15, pady=1)
        self.entry_excel_folder = customtkinter.CTkEntry(
                                                        master=self.frame_right,
                                                        width=120,
        )
        self.entry_excel_folder.grid(row=5, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        self.label_sdf_folder = customtkinter.CTkLabel(
                                                    master=self.frame_right,
                                                    height=1,
                                                    text="Specify the path of the sdf folder or leave it blank to use the default path:"
        )
        self.label_sdf_folder.grid(column=0, row=7, sticky="nwe", padx=1, pady=1)
        self.entry_sdf_folder = customtkinter.CTkEntry(
                                                        master=self.frame_right,
                                                        width=120,
        )
        self.entry_sdf_folder.grid(row=8, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        self.label_pdb_folder = customtkinter.CTkLabel(
                                                    master=self.frame_right,
                                                    height=1,
                                                    text="Specify the path of the pdb folder or leave it blank to use the default path:"
        )
        self.label_pdb_folder.grid(column=0, row=10, sticky="nwe", padx=1, pady=1)
        self.entry_pdb_folder = customtkinter.CTkEntry(
                                                        master=self.frame_right,
                                                        width=120,
        )
        self.entry_pdb_folder.grid(row=11, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        self.label_pdbqt_folder = customtkinter.CTkLabel(
                                                    master=self.frame_right,
                                                    height=1,
                                                    text="Specify the path of the pdbqt folder or leave it blank to use the default path:"
        )
        self.label_pdbqt_folder.grid(column=0, row=13, sticky="nwe", padx=1, pady=5)
        self.entry_pdbqt_folder = customtkinter.CTkEntry(
                                                        master=self.frame_right,
                                                        width=120,
        )
        self.entry_pdbqt_folder.grid(row=14, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")


        self.check_box = customtkinter.CTkCheckBox(master=self.frame_right,
                                                     text="Keep Ligands previously downloaded")
        self.check_box.grid(row=15, column=0, pady=10, padx=20, sticky="w")
        

    def button_event_execute(self):

        if self.entry_excel_file.get() != "":
            self.entry_excel_file = self.entry_excel_file.get()
        
        if self.entry_excel_folder.get() != "":
            self.excel_folder = self.entry_excel_folder.get()
        
        if self.entry_sdf_folder.get() != "":
            self.sdf_folder = self.entry_sdf_folder.get() 
        
        if self.entry_pdb_folder.get() != "":
            self.pdb_folder = self.entry_pdb_folder.get()
        
        if self.entry_pdbqt_folder.get() != "":
            self.pdbqt_folder = self.entry_pdbqt_folder.get()
        
        if self.check_box.get() == 1:
            self.keep_ligands = True

        prepare_ligands(
            self.verbose, 
            self.excel_file, 
            self.input_file,  
            self.excel_folder,  
            self.sdf_folder, 
            self.pdb_folder, 
            self.pdbqt_folder,
            self.keep_ligands
        )

    def button_event_back(self):
        self.destroy()
        Preparation()

    def change_appearance_mode(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self, event=0):
        self.destroy()


if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
