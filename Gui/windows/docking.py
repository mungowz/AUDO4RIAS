import Gui.windows.computationalDocking as computationalDocking
from customtkinter import CTkFrame, CTkLabel, CTkEntry, CTkButton, CTkOptionMenu
from tkinter import LEFT


class Docking(CTkFrame):

    MENU = "- Select Execute to perform docking\n\
- Select Back to return to the home page"

    def __init__(self, parent, controller):

        CTkFrame.__init__(self, parent)

        # ============ create two frames ============

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

        label_menu = CTkLabel(master=frame_info, text=Docking.MENU, height=2, corner_radius=1, fg_color=("white", "gray38"), justify=LEFT)
        label_menu.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        label_gridbox = CTkLabel(master=frame_right, height=1, text="Specify the path of gridboxes folder or leave it blank to use the default path")
        label_gridbox.grid(column=0, row=1, sticky="nwe", padx=15, pady=1)
        entry_gridbox = CTkEntry(master=frame_right, width=120,)
        entry_gridbox.grid(row=2, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_gridbox = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_folder(entry_gridbox))
        button_browse_gridbox.place(x=308, y=93)

        label_proteins = CTkLabel(master=frame_right, height=1, text="Specify the path of proteins folder or leave it blank to use the default path")
        label_proteins.grid(column=0, row=4, sticky="nwe", padx=15, pady=1)
        entry_proteins = CTkEntry(master=frame_right, width=120)
        entry_proteins.grid(row=5, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_proteins = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_folder(entry_proteins))
        button_browse_proteins.place(x=308, y=144)

        label_ligands = CTkLabel(master=frame_right, height=1, text="Specify the path of ligands folder or leave it blank to use the default path:")
        label_ligands.grid(column=0, row=7, sticky="nwe", padx=1, pady=1)
        entry_ligands = CTkEntry(master=frame_right, width=120,)
        entry_ligands.grid(row=8, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_ligands = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_folder(entry_ligands))
        button_browse_ligands.place(x=308, y=195)

        label_outputs = CTkLabel(master=frame_right, height=1, text="Specify the path of outputs folder or leave it blank to use the default path:")
        label_outputs.grid(column=0, row=10, sticky="nwe", padx=1, pady=1)
        entry_outputs = CTkEntry(master=frame_right, width=120)
        entry_outputs.grid(row=11, column=0, columnspan=1, pady=1, padx=7, sticky="nwe")
        button_browse_outputs = CTkButton(master = frame_right, height=1, text="Browse folders", command=lambda: controller.browse_folder(entry_outputs))
        button_browse_outputs.place(x=308, y=246)

        # ============ frame_left ============

        frame_left.grid_rowconfigure(0, minsize=10)   
        frame_left.grid_rowconfigure(5, weight=1)  
        frame_left.grid_rowconfigure(8, minsize=20)    
        frame_left.grid_rowconfigure(11, minsize=10)

        label_options = CTkLabel(master=frame_left, text="Options:", text_font=("Roboto Medium", -16))
        label_options.grid(row=1, column=0, pady=10, padx=10)

        button_execute = CTkButton(master=frame_left, text="Execute", command=lambda: controller.execute_docking(
                entry_gridbox.get(),
                entry_proteins.get(),
                entry_ligands.get(),
                entry_outputs.get()
            )
        )
        button_execute.grid(row=2, column=0, pady=10, padx=20)

        button_back = CTkButton(master=frame_left, text="Back", command=lambda: controller.show_frame(computationalDocking.ComputationalDocking))
        button_back.grid(row=3, column=0, pady=10, padx=20)

        button_help = CTkButton(master=frame_left, text="Help", command=lambda: controller.help(Docking))
        button_help.grid(row=4, column=0, pady=10, padx=20)

        label_mode = CTkLabel(master=frame_left, text="Appearance Mode:")
        label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        optionmenu = CTkOptionMenu(master=frame_left, values=["Light", "Dark", "System"], command=controller.change_appearance_mode)
        optionmenu.grid(row=10, column=0, pady=10, padx=20, sticky="w")