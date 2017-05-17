from Tkinter import *
import thread
import outgoing 
import incoming 

connections = dict()

myName = ""
myPort = ""

class app(Frame):
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createScreen()
    self.pack()
    server = None
    incoming.init(server)
    myName = incoming.myName()
    myPort = incoming.myPort()

  def createScreen(self):
    self.TEST = Button(self,text="Connect",command=connect)
    self.TEST.pack()
    print myName
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
  print "name %s" % (a.cName.get())
  print "port %s" % (a.cPort.get())
  thread.start_new_thread(outgoing.sendMessage,(a.cName.get(),a.cPort.get(),message))
  
  #print 'Name: %s' % (a.cName.get())
  #print 'Port %s' % (a.cPort.get())



root = Tk()
a = app(master=root)
a.mainloop()
