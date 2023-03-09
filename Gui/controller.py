from customtkinter import CTk, CTkFrame, set_appearance_mode, set_default_color_theme
import Gui.windows.AUDO4RIAS as AUDO4RIAS
import Gui.windows.preparation as preparation
import Gui.windows.ligands as ligands
import Gui.windows.receptors as receptors
import Gui.windows.docking as docking
import Gui.windows.help as help
import Gui.windows.analysis as analysis
from os.path import exists, join
from os import access, R_OK
from Utilities.utils import checkFilesInFolder, isWritable
from config import Config
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror, showinfo
from tkinter import END
from subprocess import Popen
from shlex import split
from threading import Thread
import time


LARGEFONT =("Verdana", 35)


set_appearance_mode("System")  
set_default_color_theme("blue")


class Controller(CTk):

    def __init__(self, *args, **kwargs):

        CTk.__init__(self, *args, **kwargs)
        
        self.resizable(False, False)

        FRAMES = (AUDO4RIAS.AUDO4RIAS, preparation.Preparation, ligands.Ligands, receptors.Receptors, docking.Docking, analysis.Analysis)
        TITLES = ("AUDO4RIAS", "Preparation", "Ligands", "Receptors", "Docking", "Analysis")
        DIMENSIONS = ("720x520", "720x520", "720x520", "720x520", "720x520", "720x520")

        self.container = CTkFrame(self)
        self.container.pack(side = "top", fill = "both", expand = True)

        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        for F, title, dimension in zip(FRAMES, TITLES, DIMENSIONS):

            frame = F(self.container, self)

            self.frames[F] = (frame, title, dimension)

            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.show_frame(AUDO4RIAS.AUDO4RIAS)

    def show_frame(self, cont):
        
        frame, title, dimension = self.frames[cont]
        self.update_idletasks()
        self.title(title)
        self.geometry(dimension)
        frame.tkraise()

    def help(self, window):

        frame = help.Help(self.container, self, window)
        frame.grid(row = 0, column = 0, sticky ="nsew")
        self.update_idletasks()
        self.title("Help")
        self.geometry("800x600")
        frame.tkraise()

    def change_appearance_mode(self, new_appearance_mode):
        
        set_appearance_mode(new_appearance_mode)

    def browse_directory(self, entry):
        entry.delete(0, END)

        filename = askdirectory(
            initialdir = "/",
            title = "Select a folder",
        )

        entry.insert(0, filename)

    def browse_files(self, entry):
        
        entry.delete(0, END)

        filename = askopenfilename(
            initialdir = "/",
            title = "Select a file",
            filetypes = [("All files", "*.*")]
        )

        entry.insert(0, filename)

    def execute_ligands(self, input_file, excel_folder, sdf_folder, pdb_folder, pdbqt_folder, keep_ligands):

        command = "xterm -xrm 'XTerm.vt100.allowTitleOps: false' -T Ligands -fg black -bg white -e python3 prepare_ligands.py -v"

        if input_file != "":
            if not exists(input_file):
                showerror("Error", "Specify a valid input file!")
                return
            if not access(input_file, R_OK):
                showerror("Error", "Modify file permission!")
                return
            command += " -i " + input_file
        else:
            input_file = join(Config.INPUT_FOLDER, "ligands_list.txt")

        if excel_folder != "":
            if not exists(excel_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for excel folder!")
                return
            command += " -e " + excel_folder
        else:
            excel_folder = Config.EXCEL_FOLDER

        if sdf_folder != "":
            if not exists(sdf_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for sdf folder!")
                return
            command += " -s " + sdf_folder
        else:
            sdf_folder = Config.LIGANDS_SDF_FOLDER

        if pdb_folder != "":
            if not exists(pdb_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for pdb folder!")
                return
            command += " -p " + pdb_folder
        else:
            pdb_folder = Config.LIGANDS_PDB_FOLDER

        if pdbqt_folder != "":
            if not exists(pdbqt_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for pdbqt folder!")
                return
            command += " -P " + pdbqt_folder
        else:
            pdbqt_folder = Config.LIGANDS_PDBQT_FOLDER

        if keep_ligands:
            command += " -k"

        args = split(command)
        thread = Thread(target=self.run_ligands, args=[args])
        thread.start()

    def run_ligands(self, args):
        Popen(args)

    def execute_receptors(self, excel_folder, pdb_folder, pdbqt_folder, margin, keep_pdb_files):

        command = "xterm -fg black -bg white -xrm 'XTerm.vt100.allowTitleOps: false' -T Receptors -e python3 prepare_receptors.py -v"

        if excel_folder != "":
            if not exists(excel_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for excel folder!")
                return
            command += " -E " + excel_folder
        else:
            excel_folder = Config.EXCEL_FOLDER

        if pdb_folder != "":
            if not exists(pdb_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for pdb folder!")
                return
            command += " -p " + pdb_folder
        else:
            pdb_folder = Config.RECEPTORS_PDB_FOLDER

        if pdbqt_folder != "":
            if not exists(pdbqt_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for pdbqt folder!")
                return
            command += " -P " + pdbqt_folder
        else:
            pdbqt_folder = Config.RECEPTORS_PDBQT_FOLDER 

        if margin != "":
            command += " -m " + margin
      
        if keep_pdb_files:
            command += " -k" 

        args = split(command)
        thread = Thread(target=self.run_receptors, args=[args])
        thread.start()

    def run_receptors(self, args):
        Popen(args)

    def execute_docking(self, gridboxes_folder, proteins_folder, ligands_folder, outputs_folder, software):

        command = "xterm -fg black -bg white -xrm 'XTerm.vt100.allowTitleOps: false' -T Docking -e python3 performDocking.py"

        if gridboxes_folder != "":
            if not exists(gridboxes_folder) or not isWritable(gridboxes_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for gridbox folder!")
                return
            command += " -g " + gridboxes_folder
        else:
            gridboxes_folder = Config.GRIDBOX_FOLDER

        if proteins_folder != "":
            if not exists(proteins_folder) or not isWritable(proteins_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for proteins folder!")
                return
            command += " -p " + proteins_folder
        else:
            proteins_folder = Config.RECEPTORS_PDBQT_FOLDER

        if ligands_folder != "":
            if not exists(ligands_folder)or not isWritable(ligands_folder):
                showerror("Error", "Specify a valid directory or modify dir permission for ligands folder!")
                return
            command += " -l " + ligands_folder
        else:
            ligands_folder = Config.LIGANDS_PDBQT_FOLDER

        if software == "AutoDockVina":
            if outputs_folder != "":
                if not exists(outputs_folder) or not isWritable(outputs_folder):
                    showerror("Error", "Specify a valid directory or modify dir permission for outputs folder!")
                    return
                command += " -o " + outputs_folder
            else:
                outputs_folder = Config.VINA_DOCKING_FOLDER
            command += " -s vina"
        else:
            if outputs_folder != "":
                if not exists(outputs_folder) or not isWritable(outputs_folder):
                    showerror("Error", "Specify a valid directory or modify dir permission for outputs folder!")
                    return
                command += " -o " + outputs_folder
            else:
                outputs_folder = Config.GNINA_DOCKING_FOLDER
            command += " -s gnina"

        if not checkFilesInFolder(folder=gridboxes_folder, docted_extension=".txt"):
            showerror("Error", "There's no txt file into gridbox folder")
            return

        if not checkFilesInFolder(folder=ligands_folder, docted_extension=".pdbqt"):
            showerror("Error", "There's no pdbqt file into ligands folder")
            return

        if not checkFilesInFolder(folder=proteins_folder, docted_extension=".pdbqt"):
            showerror("Error", "There's no pdbqt file into proteins folder")
            return

        args = split(command)
        thread = Thread(target=self.run_docking, args=[args])
        thread.start()

    def run_docking(self, args):
        Popen(args)

    def execute_analysis(self, software):

        command = "xterm -fg black -bg white -xrm 'XTerm.vt100.allowTitleOps: false' -T Analysis -e " + Config.PYTHONSH_PATH + " detect_interactions.py -s "

        if software == "AutoDockVina":
            command += "vina"
            docking_folder = Config.VINA_DOCKING_FOLDER
        else:
            command += "gnina"
            docking_folder = Config.GNINA_DOCKING_FOLDER         
        
        if not checkFilesInFolder(folder=Config.LIGANDS_PDBQT_FOLDER, docted_extension=".pdbqt"):
            showerror("Error", "There's no .pdbqt file into ligands folder")
            return

        if not checkFilesInFolder(folder=docking_folder, docted_extension=""):
            showerror("Error", "There's no output in docking outputs folder")
            return
            
        args = split(command)
        thread = Thread(target=self.run_analysis, args=[args])
        thread.start()

    def run_analysis(self, args):

        Popen(args)
    