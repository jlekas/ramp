from Tkinter import *
import thread
import outgoing 
import incoming 
import ramp_db

connections = dict()

myName = ""
myPort = ""

messages = ["o", "su!", "my", "lmepoop tonight !", "big poopy cuisine", "poop"]

class app(Frame):
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createScreen()
    self.pack()
    server = None
    incoming.init(server)
    myName = incoming.myName()
    myPort = incoming.myPort()
    
  def fillerFunction(self):
      return

  def createScreen(self):
    menubar = Menu(self)
    fileShareMenu = Menu(menubar, tearoff=0)
    fileShareMenu.add_command(label="Search For File", command=self.fillerFunction)
    fileShareMenu.add_command(label="General Search", command=self.fillerFunction)
    fileShareMenu.add_command(label="Add Files to Public", command=self.fillerFunction)
    fileShareMenu.add_command(label="Add Files to Private", command=self.fillerFunction)
   # for message in messages:
   #   self.a = Message(self, text=message,anchor=SW, width = 100)
   #   self.a.pack()
    self.chatBox = Listbox(root)
    self.chatBox.pack()
    self.myname = Label(self,text="S:128.237.139.33\nJ:128.237.92.230", relief=RAISED)
    self.myname.pack()
    self.cName = Entry(self)
    self.cName.pack()
    
    self.myPort = Label(self,text="Connecting port",relief=RAISED)
    self.myPort.pack()
    self.cPort = Entry(self)
    self.cPort.pack()
    
    self.message = Entry(self)
    self.message.pack()
    self.Send = Button(self, text="Send Message",command= lambda: connect(self.message.get()))
    self.Send.pack()

def connect(message):
  thread.start_new_thread(outgoing.sendMessage,(a.cName.get(),a.cPort.get(),message))
  
  #print 'Name: %s' % (a.cName.get())
  #print 'Port %s' % (a.cPort.get())



root = Tk()
a = app(master=root)
a.mainloop()
