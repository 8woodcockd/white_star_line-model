from tkinter import *
import tkinter.font as tkFont
from tkinter.filedialog import askopenfilename
import csv
import white_star_model

class App:
    #global run_program
    #run_program = True
    def __init__(self, master):
            
        fontHead = tkFont.Font(family="Arial", size=10, weight=tkFont.BOLD)
        fontBold = tkFont.Font(family="Arial", size=8, weight=tkFont.BOLD)
        fontReg =  tkFont.Font(family="Arial", size=8)
    
        frameN = Frame(master)
        frameN.grid(row=0,padx=5,pady=5)
    
        frameXBH = Frame(frameN)
        frameXBH.grid(row=0,columnspan=5,padx=5)
    
        #creates the line of the frame and the header in bold for the window
        Canvas(frameXBH,borderwidth=0,relief="flat",height=1,width=20,background="#cccccc").grid(row=0)
        Label(frameXBH, text="Load Radar and Lidar Data",font=fontBold,width=22).grid(row=0,column=1)
        Canvas(frameXBH,borderwidth=0,relief="flat",height=1,width=440,background="#cccccc").grid(row=0,column=2,sticky="WE")
    
        #widget 1
        Label(frameN, text="Radar data file:",font=fontReg).grid(row=1,sticky="W") # sticky refers to positioning
        Path1 = Entry(frameN,width=30,font=fontReg)
        Path1.grid(row=1,column=1,sticky="W")
        Browse1 = Button(frameN,text="Browse...",font=fontReg, command=lambda : self.get_dir(Path1))
        Browse1.grid(row=1,column=2,sticky="W")
        
        #widget 2
        Label(frameN, text="Lidar data file:",font=fontReg).grid(row=2,sticky="W")
        Path2 = Entry(frameN,width=30,font=fontReg)
        Path2.grid(row=2,column=1,sticky="W")
        Browse2 = Button(frameN,text="Browse...",font=fontReg, command=lambda : self.get_dir(Path2))
        Browse2.grid(row=2,column=2,sticky="W")
        
        show_input = IntVar()
        xb_plot_inputs = Checkbutton(frameN,text="Plot input data",font=fontReg, variable = show_input)
        xb_plot_inputs.grid(row=3,column=1,sticky="W")
        
        Label(frameN, text="Radar data file must be a comma separated .txt or .csv file ",font=fontReg).grid(row = 1,column = 3,sticky="W")
        Label(frameN, text="Lidar data file must be a comma separated .txt or .csv file ",font=fontReg).grid(row = 2, column = 3,sticky="W")
        
        Canvas(frameN,borderwidth=1,relief="groove",width=350,height=0).grid(row=3,columnspan=5,pady=10)
    
        # RUN AND CANCEL
    
        def cancel():
            """Cancel processes by setting the global flag to False."""
            global run
            run = False
    
        def run():
            P1 = Path1.get()
            P2 = Path2.get()
            filename1 = P1.rsplit("/",1)[1]
            filename2 = P2.rsplit("/",1)[1]
            plot_inputs = show_input.get()
            
            if (filename1 != '') & (filename2 != ''):
                white_star_model.running_model(filename1,filename2,plot_inputs)
           
            if xb_plot_inputs == False:
                print('False xb_plot_inputs', show_input.get())
            else:
                print('True xb_plot_inputs', show_input.get())
            
        btnRun = Button(frameN,text="Run",width=10,font=fontReg,command=run)
        btnRun.grid(row=4,column=3,sticky="E")
        
        print('xb_plot_inputs', xb_plot_inputs)
        
    
        btnCancel = Button(frameN,text="Cancel",width=10,font=fontReg,command=cancel)
        btnCancel.grid(row=4,column=4,sticky="W")
    
    def get_dir(self,box):
        tmp = askopenfilename(initialdir='/home/',title="filetext" , 
                              filetypes=[('text files', '.txt'),
                                         ('comma seperated value files', 
                                          '.csv')])
        box.delete(0,END) #clear entry widget when a button is pushed
        box.insert(0,tmp) #insert text at beginning of text box
        print(tmp)
        return tmp

     
root = Tk()
root.title('White Star Line Model')
root.resizable(0,0)
app = App(root)
root.mainloop()


     
