import Gui.windows.preparation as preparation
from customtkinter import CTkButton, CTkEntry, CTkFrame, CTkLabel, CTkCheckBox, CTkOptionMenu
from tkinter import LEFT


class Receptors(CTkFrame):

    MENU = "-Select Execute to prepare receptors\n-Select Back to return to the home page"

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

        label_pdb_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the pdb folder or leave it blank to use the default path:")
        label_pdb_folder.grid(column=0, row=4, sticky="nwe", padx=1, pady=1)
        entry_pdb_folder = CTkEntry(master=frame_right, width=120)
        entry_pdb_folder.grid(row=5, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        label_pdbqt_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the pdbqt folder or leave it blank to use the default path:")
        label_pdbqt_folder.grid(column=0, row=7, sticky="nwe", padx=1, pady=5)
        entry_pdbqt_folder = CTkEntry(master=frame_right, width=120)
        entry_pdbqt_folder.grid(row=8, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        label_gridbox_output_folder = CTkLabel(master=frame_right, height=1, text="Specify the path of the output gridbox or leave it blank to use the default path")
        label_gridbox_output_folder.grid(column=0, row=10, sticky="nwe", padx=15, pady=1)
        entry_gridbox_output_folder = CTkEntry(master=frame_right, width=120)
        entry_gridbox_output_folder.grid(row=11, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        label_margin = CTkLabel(master=frame_right, height=1, text="Specify the value of margin or leave it blank to use the default value(3):")
        label_margin.grid(column=0, row=13, sticky="nwe", padx=1, pady=1)
        entry_margin = CTkEntry(master=frame_right, width=120)
        entry_margin.grid(row=14, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        label_charges_to_add = CTkLabel(master=frame_right, height=1, text="Specify charges to add or leave it blank to use the default value(Kollman):")
        label_charges_to_add.grid(column=0, row=15, sticky="nwe", padx=1, pady=1)
        entry_charges_to_add = CTkEntry(master=frame_right, width=120)
        entry_charges_to_add.grid(row=16, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")

        check_box = CTkCheckBox(master=frame_right, text="Keep pdb files previously downloaded")
        check_box.grid(row=17, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_left ============

        frame_left.grid_rowconfigure(0, minsize=10)
        frame_left.grid_rowconfigure(5, weight=1)
        frame_left.grid_rowconfigure(8, minsize=20)
        frame_left.grid_rowconfigure(11, minsize=10)

        label_options = CTkLabel(master=frame_left, text="Options:", text_font=("Roboto Medium", -16))
        label_options.grid(row=1, column=0, pady=10, padx=10)

        button_execute = CTkButton(master=frame_left, text="Execute", command=lambda: controller.execute_receptors(
                True,
                entry_excel_folder.get(),
                entry_pdb_folder.get(),
                entry_pdbqt_folder.get(),
                entry_gridbox_output_folder.get(),
                entry_margin.get(),
                entry_charges_to_add.get(),
                check_box.get()
            )
        )
        button_execute.grid(row=2, column=0, pady=10, padx=20)

        button_back = CTkButton(master=frame_left, text="Back", command=lambda: controller.show_frame(preparation.Preparation))
        button_back.grid(row=3, column=0, pady=10, padx=20)

        label_mode = CTkLabel(master=frame_left, text="Appearance Mode:")
        label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        optionmenu = CTkOptionMenu(master=frame_left, values=["Light", "Dark", "System"], command=controller.change_appearance_mode)
        optionmenu.grid(row=10, column=0, pady=10, padx=20, sticky="w")