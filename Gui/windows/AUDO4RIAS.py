from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkOptionMenu, CTkProgressBar
import Gui.windows.preparation as preparation
import Gui.windows.docking as docking
import Gui.windows.analysis as analysis
from tkinter import LEFT


class AUDO4RIAS(CTkFrame):

    MENU = " Welcome:\n\
       - Select Preparation to prepare ligands and receptors\n\
       - Select Docking to perform docking\n\
       - Selext Analyses to perform analyses on docking outputs\n\
       - Select help to get more information on default parameters and inputs"

    def __init__(self, parent, controller):
        
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
        frame_left.grid_rowconfigure(6, weight=1)  
        frame_left.grid_rowconfigure(8, minsize=20)   
        frame_left.grid_rowconfigure(11, minsize=10)  
        
        label_options = CTkLabel(master=frame_left, text="Options:", text_font=("Roboto Medium", -16))
        label_options.grid(row=1, column=0, pady=10, padx=10)
        
        button_preparation = CTkButton(master=frame_left, text="Preparation", command=lambda: controller.show_frame(preparation.Preparation))
        button_preparation.grid(row=2, column=0, pady=10, padx=20)
        
        button_docking = CTkButton(master=frame_left, text="Docking", command=lambda: controller.show_frame(docking.Docking))
        button_docking.grid(row=3, column=0, pady=10, padx=20)
        
        button_analyses = CTkButton(master=frame_left, text="Analysis", command=lambda: controller.show_frame(analysis.Analysis))
        button_analyses.grid(row=4, column=0, pady=10, padx=20)

        button_help = CTkButton(master=frame_left, text="Help", command=lambda: controller.help(AUDO4RIAS))
        button_help.grid(row=5, column=0, pady=10, padx=20)

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
        
        label_menu = CTkLabel(master=frame_info, text= AUDO4RIAS.MENU, height=400, corner_radius=6, fg_color=("white", "gray38"), justify=LEFT)
        label_menu.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        progressbar = CTkProgressBar(master=frame_info)
        progressbar.grid(row=1, column=0, sticky="ew", padx=15, pady=15)