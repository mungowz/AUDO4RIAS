from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkProgressBar, CTkOptionMenu
from tkinter import LEFT


class Help(CTkFrame):
        
    MENU = "DEFAULT OPTIONS\n\n\
        - Ligands:\n\
        • Input file: Computational-Docking/data/files/ligands.txt\n\
        • Excel folder: Computational-Docking/output/excel_files/\n\
        • Sdf folder: Computational-Docking/data/ligands/sdf/\n\
        • Pdb folder: Computational-Docking/data/ligands/pdb/\n\
        • Pdbqt folder: Computational-Docking/data/ligands/pdbqt/\n\n\
        - Receptors:\n\
        • Excel folder: Computational-Docking/output/excel_files/\n\
        • Pdb folder: Computational-Docking/data/proteins/pdb/\n\
        • Pdbqt folder: Computational-Docking/data/proteins/pdbqt/\n\
        • Margin: 3\n\n\
        - Docking:\n\
        • Ligands folder: Computational-Docking/data/ligands/pdbqt/\n\
        • Proteins folder: Computational-Docking/data/proteins/pdbqt/\n\
        • Gridboxes folder: Computational-Docking/data/proteins/gridbox/\n\n\
INPUTS\n\n\
        • Ligands: ligands input consists of a .txt file where all the names of the ligands\n\
        are listed one below the other.\n\
        To add, edit, or remove inputs, modify the ligands_list.txt file."

    def __init__(self, parent, controller, window):

        CTkFrame.__init__(self, parent)

        # ============ create two frames ============

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_left = CTkFrame(self, parent, width=180, corner_radius=0)
        frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = CTkFrame(self, parent)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(5, weight=1)
        frame_left.grid_rowconfigure(8, minsize=20)
        frame_left.grid_rowconfigure(11, minsize=10)

        label_options = CTkLabel(master=frame_left, text="Options:", text_font=("Roboto Medium", -16))
        label_options.grid(row=1, column=0, pady=10, padx=10)

        button_back = CTkButton(frame_left, text="Back", command=lambda: controller.show_frame(window))
        button_back.grid(row=4, column=0, pady=10, padx=20)

        label_mode = CTkLabel(master=frame_left, text="Appearance Mode:")
        label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        optionmenu = CTkOptionMenu(master=frame_left, values=["Light", "Dark", "System"], command=controller.change_appearance_mode)
        optionmenu.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        frame_right.rowconfigure(7, weight=10)
        frame_right.columnconfigure((0, 1), weight=1)
        frame_right.columnconfigure(2, weight=0)

        frame_info = CTkFrame(master=frame_right)
        frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        frame_info.rowconfigure(0, weight=1)
        frame_info.columnconfigure(0, weight=1)

        label_menu = CTkLabel(master=frame_info, text=Help.MENU, height=400, corner_radius=6, fg_color=("white", "gray38"), justify=LEFT)
        label_menu.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        progressbar = CTkProgressBar(master=frame_info)
        progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)
        