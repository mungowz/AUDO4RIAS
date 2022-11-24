import Gui.windows.preparation as preparation
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkCheckBox, CTkOptionMenu
from tkinter import LEFT


class Receptors(CTkFrame):

    MENU = "- Select Execute to prepare receptors\n\
- Select Back to return to the preparation page"

    def __init__(self, parent, controller):
        
        CTkFrame.__init__(self, parent)
          
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        frame_left = CTkFrame(self, parent, width=180, corner_radius=0)
        frame_left.grid(row=0, column=0, sticky="nswe")

        frame_right = CTkFrame(self, parent)
        frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_right ============

        frame_info = CTkFrame(master=frame_right)
        frame_info.grid(row=0, column=0, columnspan=1, rowspan=1, pady=1, padx=1, sticky="nsew")

        # ============ frame_info ============

        frame_info.rowconfigure(0, weight=1)
        frame_info.columnconfigure(0, weight=1)

        label_menu = CTkLabel(master=frame_info, text=Receptors.MENU, height=2, corner_radius=1, fg_color=("white", "gray38"), justify=LEFT)
        label_menu.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)
        
        label_excel_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the input excel folder or leave it blank to use the default path")
        label_excel_folder.grid(column=0, row=1, sticky="nwe", padx=15, pady=1)
        entry_excel_folder = CTkEntry(master=frame_right, width=120)
        entry_excel_folder.grid(row=2, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_excel_folder = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_directory(entry_excel_folder))
        button_browse_excel_folder.place(x=334, y=93)

        label_pdb_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the pdb folder or leave it blank to use the default path:")
        label_pdb_folder.grid(column=0, row=4, sticky="nwe", padx=1, pady=1)
        entry_pdb_folder = CTkEntry(master=frame_right, width=120)
        entry_pdb_folder.grid(row=5, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_pdb_folder = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_directory(entry_pdb_folder))
        button_browse_pdb_folder.place(x=334, y=144)

        label_pdbqt_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the pdbqt folder or leave it blank to use the default path:")
        label_pdbqt_folder.grid(column=0, row=7, sticky="nwe", padx=1, pady=5)
        entry_pdbqt_folder = CTkEntry(master=frame_right, width=120)
        entry_pdbqt_folder.grid(row=8, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_pdbqt_folder = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_directory(entry_pdbqt_folder))
        button_browse_pdbqt_folder.place(x=334, y=203)

        label_margin = CTkLabel(master=frame_right, height=1, text="Specify the value of margin or leave it blank to use the default value:")
        label_margin.grid(column=0, row=10, sticky="nwe", padx=1, pady=1)
        entry_margin = CTkEntry(master=frame_right, width=120)
        entry_margin.grid(row=11, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        check_box_pdb_files = CTkCheckBox(master=frame_right, text="Keep pdb files previously downloaded")
        check_box_pdb_files.grid(row=13, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_left ============

        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(5, weight=1)
        frame_left.grid_rowconfigure(8, minsize=20)
        frame_left.grid_rowconfigure(11, minsize=10)

        label_options = CTkLabel(master=frame_left, text="Options:", text_font=("Roboto Medium", -16))
        label_options.grid(row=1, column=0, pady=10, padx=10)

        button_execute = CTkButton(master=frame_left, text="Execute", command=lambda: controller.execute_receptors(
                entry_excel_folder.get(),
                entry_pdb_folder.get(),
                entry_pdbqt_folder.get(),
                entry_margin.get(),
                check_box_pdb_files.get()
            )
        )
        button_execute.grid(row=2, column=0, pady=10, padx=20)

        button_back = CTkButton(master=frame_left, text="Back", command=lambda: controller.show_frame(preparation.Preparation))
        button_back.grid(row=3, column=0, pady=10, padx=20)

        button_help = CTkButton(master=frame_left, text="Help", command=lambda: controller.help(Receptors))
        button_help.grid(row=4, column=0, pady=10, padx=20)

        label_mode = CTkLabel(master=frame_left, text="Appearance Mode:")
        label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        optionmenu = CTkOptionMenu(master=frame_left, values=["Light", "Dark", "System"], command=controller.change_appearance_mode)
        optionmenu.grid(row=10, column=0, pady=10, padx=20, sticky="w")