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
    incoming.init()
    myName = incoming.myName()
    myPort = incoming.myPort()

  def createScreen(self):
    self.TEST = Button(self,text="Connect",command=connect)
    self.TEST.pack()
    print myName
    self.myname = Label(self,text=incoming.myName(), relief=RAISED)
    self.myname.pack()
    self.cName = Entry(self)
    self.cName.pack()
    
    self.myPort = Label(self,text=incoming.myPort(),relief=RAISED)
    self.myPort.pack()
    self.cPort = Entry(self)
    self.cPort.pack()
    self.mes = Label(self,text=outgoing.getMessage())
    self.mes.pack()


def connect():
  print "name %s" % (a.cName.get())
  print "port %s" % (a.cPort.get())
  thread.start_new_thread(outgoing.makeConnection, (a.cName.get(),a.cPort.get()))
  
  #print 'Name: %s' % (a.cName.get())
  #print 'Port %s' % (a.cPort.get())



root = Tk()
a = app(master=root)
a.mainloop()
