# imports
#==========================
from tkinter import * 
import pyttsx3
import PyPDF4
import webbrowser
from tkinter import filedialog as fd 
import os
import audioplayer


#==============================================================================================================

class app:
    #constructor for initialization of main window
    def __init__(self,window):
        self.window=window
        self.window.title("GyanaDhvani")              
        
        self.window.geometry("705x546")
        self.window.resizable(False,False)
        
        self.img = PhotoImage(file = "vibrations.png")
               
        t1 = "Welcome to GyanaDhvani!"
        t2= "One stop Guide for ultimate reading experience."
        
        self.canvas=Canvas(self.window,width = 754, height = 566)
        self.canvas.pack(fill = "both", expand = True)
        
        self.canvas.create_image( 327, 283, image = self.img)
        
        self.canvas.create_text( 370, 180, fill="white",font="Times 20 italic bold",text = t1)
        self.canvas.create_text( 350, 220, fill="white",font="Times 20 italic bold",text = t2)
        
        self.pdf = Button(self.window,text="Open PDF",command=self.pdfSelect)
        self.button1_canvas = self.canvas.create_window( 20, 500, anchor = "nw", window = self.pdf)
        
        self.hlp = Button(self.window,text="Introduction",command=self.Help)
        self.button2_canvas = self.canvas.create_window( 580, 500, anchor = "nw", window = self.hlp)
        

#=================================================================================================================
    
    #function for selecting pdf to be opened
    def pdfSelect(self):
        self.name= fd.askopenfilename(filetypes=(("pdf","*.pdf"),("all","*.*")))
        
        self.book =open(self.name,'rb') #self.name has complete address of the book
        
        webbrowser.open_new(self.name)
        self.read_window()



#==============================================================================================================



    #function for instruction screen
    def Help(self):
        
    #creating new window and setting background
        #==================================================
        self.help = Toplevel(self.window)
        self.help.resizable(False,False)
        self.help.title("Introduction")              
        self.help.geometry("600x350")
        
        
        intro= open("intro.txt",'r')
        lines=intro.read()
        

        self.txt=Text(self.help,font="Helvetica 12",background='lightblue')
        self.txt.tag_configure("center", justify='center')
        self.txt.insert("1.0",lines)
        self.txt.tag_add("center","1.0","end")
        

        self.txt.pack()
                  


#==============================================================================================================
    

    #reader window creation function
    def read_window(self):
        self.top=Toplevel(self.window)
        self.top.geometry("510x340")
        self.top.resizable(False,False)
        

        self.img3 = PhotoImage(file = "vibrations.png")
        self.canvas3=Canvas(self.top,width = 590, height = 393)
        self.canvas3.pack(fill = "both", expand = True)
        

        self.canvas3.create_image( 260, 182, image = self.img3)
        

        self.startButton= Button(self.top,text="Start Reading",command=self.Read_directly)
        S_Button = self.canvas3.create_window( 20, 200, anchor = "nw", window = self.startButton)
        

        self.convertButton = Button(self.top,text="Convert to mp3 and play",command =self.convert_and_play)
        C_Button = self.canvas3.create_window( 300, 200, anchor = "nw", window = self.convertButton)
        



#=================================================================================================================
   

    #if reading directly
    def Read_directly(self):  
        #self.top.destroy()
        
        #creating new window setting background
        #==================================================
        self.cur_read = Toplevel(self.window)
        self.cur_read.geometry("580x400")
        self.cur_read.resizable(False,False)
        self.cur_read.title("Read Directly")
        self.bg = PhotoImage(file = "vibrations.png")
        self.label =Label(self.cur_read,image = self.bg)
        self.label.place(x=0,y=-40,relwidth=1,relheight=1.2)
        
       
        # taking user input for page numbers and speed etc
        #======================================================
        start =StringVar()
        end =StringVar()
        volume=StringVar()
        speed =StringVar()
        
        #============================================
        
        self.st_label=Label(self.cur_read,text="Enter start page number:")
        self.st_label.grid(row=0,column=0,pady=20,padx=60)
        self.st_pg =Entry(self.cur_read,textvariable=start,justify=LEFT)
        self.st_pg.grid(row=0,column=1,pady=20,padx=0)
        
        #print(start)
        #===============================================
        
        self.en_label=Label(self.cur_read,text="Enter end page number:")
        self.en_label.grid(row=1,column=0,pady=0,padx=60)
        self.en_pg = Entry(self.cur_read,textvariable=end)
        self.en_pg.grid(row=1,column=1,pady=0,padx=0)
        #print(end)
        
        #================================================
        
        self.vol_label=Label(self.cur_read,text="Enter Volume (0 to 10):")
        self.vol_label.grid(row=2,column=0,pady=50,padx=60)
        self.vol = Entry(self.cur_read,textvariable=volume)
        self.vol.grid(row=2,column=1,pady=50,padx=30)
        #print(volume)
        
        #=================================================
        
        self.sp_label=Label(self.cur_read,text="Enter speed (100 to 250):")
        self.sp_label.grid(row=3,column=0,pady=0,padx=60)
        self.sp = Entry(self.cur_read,textvariable=speed)
        self.sp.grid(row=3,column=1,pady=0,padx=0)
        #print(speed)
       
        #buttons
        #===============================================
        
        setButton= Button(self.cur_read,text="Set Entries",command=self.setEntries)
        setButton.grid(row=5,column=0,padx=10,pady=50)

        startButton= Button(self.cur_read,text="Start Reading",command=self.Read)
        startButton.grid(row=5,column=1,padx=10,pady=50)



#==================================================================================================================


    #function to set the entries for direct reading
    def setEntries(self):
        self.reader = pyttsx3.init('sapi5')
        self.rate = int(self.sp.get())
        self.reader.setProperty('rate',self.rate)
        self.volm = int(str(self.vol.get()))
        self.reader.setProperty('volume',self.volm/10)
        voices = self.reader.getProperty('voices')
        self.reader.setProperty('voice',voices[11].id)
        
        
#=================================================================================================================


    #function for reading contents
    def Read(self):    
        self.pdfReader = PyPDF4.PdfFileReader(self.book)
        
        start =int(self.st_pg.get())-1
        end=int(self.en_pg.get())-1
        
        for i in range(start,end):
            self.page = self.pdfReader.getPage(i)
            text = self.page.extractText()
            #print(text)
            self.reader.say(text)
            self.reader.runAndWait()
        
        self.reader.stop()


#=================================================================================================================


    #take page number as input through a new window
    def convert_and_play(self):
        #self.top.destroy()
    
    #creating new window setting background
        #==================================================
        self.mp3_read = Toplevel(self.window)
        self.mp3_read.geometry("580x300")
        self.mp3_read.resizable(False,False)
        self.mp3_read.title("Convert to mp3")
        self.bg = PhotoImage(file = "vibrations.png")
        self.label =Label(self.mp3_read,image = self.bg)
        self.label.place(x=0,y=-60,relwidth=1,relheight=1.2)
        
       
        start =StringVar()
        end =StringVar()
        
        #=========================================================================
        
        self.st_label_cnv=Label(self.mp3_read,text="Enter start page number:")
        self.st_label_cnv.grid(row=0,column=0,pady=20,padx=60)
        self.st_pg_cnv =Entry(self.mp3_read,textvariable=start,justify=LEFT)
        self.st_pg_cnv.grid(row=0,column=1,pady=20,padx=20)
        
        #========================================================================
        
        self.en_label_cnv=Label(self.mp3_read,text="Enter end page number:")
        self.en_label_cnv.grid(row=1,column=0,pady=0,padx=60)
        self.en_pg_cnv= Entry(self.mp3_read,textvariable=end)
        self.en_pg_cnv.grid(row=1,column=1,pady=20,padx=20)
        
        #======================================================================
        
        Convert = Button(self.mp3_read,text ="CONVERT",command=self.txt_2_mp3)
        Convert.grid(row=3,column =0,padx=10,pady=10)
        
        
        playButton = Button(self.mp3_read,text ="PLAY",command=self.play_mp3)
        playButton.grid(row=3,column=1,padx=10,pady=10)
        
        
        pauseButton = Button(self.mp3_read,text="PAUSE",command=self.pause)
        pauseButton.grid(row=4,column=0,padx=10,pady=10)
        
        
        unpauseButton = Button(self.mp3_read,text="UNPAUSE",command=self.unpause)
        unpauseButton.grid(row=4,column=1,padx=10,pady=10)


#================================================================================================================


    #conversion to mp3
    def txt_2_mp3(self):
        self.reader_conv = pyttsx3.init('espeak')
        self.reader_conv.setProperty('rate',110)
        self.pdfReader_conv = PyPDF4.PdfFileReader(self.book)
        
        
        start =int(self.st_pg_cnv.get())-1
        end=int(self.en_pg_cnv.get())-1
        
        
        self.mp3_name = self.name+'Pg'+str(start)+'to'+str(end)+'.mp3'
        

        for i in range(start,end):
            self.page = self.pdfReader_conv.getPage(i)
            text = self.page.extractText()
            self.reader_conv.save_to_file(text,self.mp3_name)
            self.reader_conv.runAndWait()
        
        self.reader_conv.stop()
            


#=================================================================================================================

    #play mp3
    def play_mp3(self):
        audioFile = self.mp3_name
        self.player = audioplayer.AudioPlayer(audioFile)
        self.player.play()
        

#================================================================================================================    


    def pause(self):
        self.player.pause()
        
#=================================================================================================================


    def unpause(self):
        self.player.resume()
            
#=================================================================================================================

def main():
    window = Tk()
    app(window)
    window.mainloop()

