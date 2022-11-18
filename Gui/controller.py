from customtkinter import CTk, CTkFrame, set_appearance_mode, set_default_color_theme, CTkTextbox, CTkScrollbar
import Gui.windows.computationalDocking as computationalDocking
import Gui.windows.preparation as preparation
import Gui.windows.ligands as ligands
import Gui.windows.receptors as receptors
import Gui.windows.docking as docking
from Gui.scripts.prepare_ligands2 import prepare_ligands
from Gui.scripts.prepare_receptors2 import prepare_receptors
from Gui.scripts.performDocking import performDocking
from os.path import join
from config import Config
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import Tk, Frame, Button, Scrollbar, Text, END
from threading import Thread
import sys

LARGEFONT =("Verdana", 35)


set_appearance_mode("System")  
set_default_color_theme("blue")


class Controller(CTk):

    def __init__(self, *args, **kwargs):

        CTk.__init__(self, *args, **kwargs)
        
        FRAMES = (computationalDocking.ComputationalDocking, preparation.Preparation, ligands.Ligands, receptors.Receptors, docking.Docking)
        TITLES = ("Computational Docking", "Preparation", "Ligands", "Receptors", "Docking")
        DIMENSIONS = ("720x520", "720x520", "720x520", "720x520", "720x520")

        self.container = CTkFrame(self)
        self.container.pack(side = "top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F, title, dimension in zip(FRAMES, TITLES, DIMENSIONS):

            frame = F(self.container, self)

            self.frames[F] = (frame, title, dimension)

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(computationalDocking.ComputationalDocking)

    def show_frame(self, cont):
        
        frame, title, dimension = self.frames[cont]
        self.update_idletasks()
        self.title(title)
        self.geometry(dimension)
        frame.tkraise()

    def change_appearance_mode(self, new_appearance_mode):
        
        set_appearance_mode(new_appearance_mode)

    def browse_directory(self, entry):
        entry.delete(0, END)

        filename = askdirectory(
            initialdir = "/",
            title = "Select a File",
        )

        entry.insert(0, filename)


    def browse_files(self, entry):
        
        entry.delete(0, END)

        filename = askopenfilename(
            initialdir = "/",
            title = "Select a File",
            filetypes = [("All files", "*.*")]
        )

        entry.insert(0, filename)

    def execute_ligands(self, verbose, input_file, excel_folder, sdf_folder, pdb_folder, pdbqt_folder, keep_ligands):

        if input_file == "":
            input_file = join(Config.INPUT_FOLDER, "ligands_list.txt")

        if excel_folder == "":
            excel_folder = Config.EXCEL_FOLDER

        if sdf_folder == "":
            sdf_folder = Config.LIGANDS_SDF_FOLDER

        if pdb_folder == "":
            pdb_folder = Config.LIGANDS_PDB_FOLDER

        if pdbqt_folder == "":
            pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER

        with open(input_file) as f:
            contents = f.readlines()

        root = Tk()

        root.title("Ligands preparation")

        frame = CTkFrame(root)
        frame.pack(expand=True, fill='both')

        text = Text(frame)
        text.pack(side='left', fill='both', expand=True)

        scrollbar = CTkScrollbar(frame)
        scrollbar.pack(side='right', fill='y')

        text['yscrollcommand'] = scrollbar.set
        scrollbar['command'] = text.yview

        old_stdout = sys.stdout    
        sys.stdout = Redirect(text)

        # - after close window -

        Thread(target=prepare_ligands, args=(verbose, input_file, excel_folder, sdf_folder, pdb_folder, pdbqt_folder, keep_ligands, contents)).start()

        root.mainloop()

        sys.stdout = old_stdout
        

    def execute_receptors(self, verbose, excel_folder, pdb_folder, pdbqt_folder, margin, keep_pdb_files, gridbox_output_folder, charges_to_add):

        if excel_folder == "":
            excel_folder = Config.EXCEL_FOLDER

        if pdb_folder == "":
            pdb_folder = Config.RECEPTORS_PDB_FOLDER

        if pdbqt_folder == "":
            pdbqt_folder = Config.RECEPTORS_PDBQT_FOLDER

        if margin == "":
            margin = 3

        if gridbox_output_folder == "":
            gridbox_output_folder = Config.GRIDBOX_FOLDER

        if charges_to_add == "":
            charges_to_add = "Kollman"       
            
        prepare_receptors(verbose, excel_folder, pdb_folder, pdbqt_folder, margin, keep_pdb_files, gridbox_output_folder, charges_to_add)

    def execute_docking(self, gridboxes_folder, proteins_folder, ligands_folder, outputs_folder):

        print("qui")

        if gridboxes_folder == "":
            gridboxes_folder = Config.GRIDBOX_FOLDER

        if proteins_folder == "":
            proteins_folder = Config.RECEPTORS_PDBQT_FOLDER

        if ligands_folder == "":
            ligands_folder = Config.LIGANDS_PDBQT_FOLDER

        if outputs_folder == "":
            outputs_folder = Config.VINA_DOCKING_FOLDER

        performDocking(gridboxes_folder, proteins_folder, ligands_folder, outputs_folder)
        

class Redirect():

    def __init__(self, widget, autoscroll=True):
        self.widget = widget
        self.autoscroll = autoscroll

    def write(self, text):
        self.widget.insert('end', text)
        if self.autoscroll:
            self.widget.see("end")  # autoscroll
        

