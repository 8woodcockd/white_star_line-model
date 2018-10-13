import tkinter as tk
import white_star_model
from tkinter.filedialog import askopenfilename
from tkinter.font import Font
import os

class App:
    """ Create a GUI for the user to select files and options to run the model.
    """
    
    def __init__(self, master):
        """ Customise GUI features and appearance.
        """
        # Create font types.
        fontBold = Font(family="Arial", size=8, weight=tk.font.BOLD)
        fontReg =  Font(family="Arial", size=8)
        
        # Create a frame.
        frame1 = tk.Frame(master)
        frame1.grid(row=0, padx=6, pady=5)
        frame2 = tk.Frame(frame1)
        frame2.grid(row=0, columnspan=5, padx=5)
    
        # Create a line in the frame and the header in bold for the window.
        tk.Canvas(frame2, borderwidth=0, relief="flat", height=1, width=20,
               background="#cccccc").grid(row=0)
        tk.Label(frame2, text="Load Radar and Lidar Data", font=fontBold,
              width=22).grid(row=0, column=1)
        tk.Canvas(frame2, borderwidth=0, relief="flat", height=1, width=440,
               background="#cccccc").grid(row=0, column=2, sticky="WE")
        
        # Create a label, entry window and browse files button.
        tk.Label(frame1, text="Radar data file:", font=fontReg).grid(row=1,
                                                                  sticky="W") 
        Path1 = tk.Entry(frame1, width=30, font=fontReg)
        Path1.grid(row=1, column=1, sticky="W")
        Browse1 = tk.Button(frame1, text="Browse...", font=fontReg, 
                         command=lambda : self.get_dir(Path1))
        Browse1.grid(row=1, column=2, sticky="W")
        
        # Create a second label, entry window and browse files button.
        tk.Label(frame1, text="Lidar data file:", font=fontReg).grid(row=2,
                                                                  sticky="W")
        Path2 = tk.Entry(frame1, width=30, font=fontReg)
        Path2.grid(row=2, column=1, sticky="W")
        Browse2 = tk.Button(frame1, text="Browse...", font=fontReg, 
                         command=lambda : self.get_dir(Path2))
        Browse2.grid(row=2, column=2, sticky="W")
        
        # Create a checkbutton so the user can choose to plot the input data.
        show_input = tk.IntVar()
        xb_plot_inputs = tk.Checkbutton(frame1, text="Plot input data",
                                     font=fontReg, variable = show_input)
        xb_plot_inputs.grid(row=3, column=1, sticky="W")
        
        # Add labels that inform the user what file types are acceptable.
        tk.Label(frame1, text="Radar data file must be a comma separated txt "\
              "or csv file ", font=fontReg).grid(row = 1, column = 3, 
                                                 sticky="W")
        tk.Label(frame1, text="Lidar data file must be a comma separated txt "\
              "or csv file ", font=fontReg).grid(row = 2, column = 3,
                                                 sticky="W")
        # Create a line along the bottom of the GUI. 
        tk.Canvas(frame1, borderwidth=1, relief="groove", width=350, 
               height=0).grid(row=3, columnspan=5, pady=10)
    
        def run():
            """ Command the White Star Model.py script to run using the input 
            files selected by the user.
            """
            # Retrieve filename from user input.
            P1 = Path1.get()
            print('THIS IS P1', P1)
            P2 = Path2.get()
            filename1 = P1.rsplit("/",1)[1]
            filename2 = P2.rsplit("/",1)[1]
            
            # Create variable to communicate with 'White_Star_Model.py' whether
            # the user wishes to plot the input data.
            plot_inputs = show_input.get()
            
            # Call and run the white_star_model.py script if the user has
            # selected two files and pressed the run button.
            if (filename1 != '') & (filename2 != ''):
                white_star_model.running_model(P1, P2, filename1, filename2, 
                                               plot_inputs)
                                               
        # Create a button to run the program.
        btnRun = tk.Button(frame1, text="Run", width=10, font=fontReg, 
                        command=run)
        btnRun.grid(row=4, column=3, sticky="E")
        
        # Create a button to cancel the running of the program
        btnClose = tk.Button(frame1, text="Close", width=10, font=fontReg,
                           command=root.destroy)
        btnClose.grid(row=4, column=4, sticky="W")
    
    ## This is here to provide a docstring for the run function.
    def run():
        """ Command the White Star Model.py script to run using the input 
            #files selected by the user. 222
        """
    
    def get_dir(self, box):
        """Allow user to browse for csv and text files and show file path
        in the entry window once selected.
        """
        tmp = askopenfilename(
                initialdir='/home/', title="Browse to and select input files", 
                filetypes=[('text files', '.txt'), 
                           ('comma seperated value files', '.csv')])
        box.delete(0, tk.END) # Clear entry box when browse button is pushed.
        box.insert(0, tmp) # Insert text at beginning of entry box.
     
root = tk.Tk()
root.title('White Star Line Model')
root.resizable(0,0)
app = App(root)
root.mainloop()


     
