from Tkinter import *
import thread
import outgoing 

connections = dict()


class app(Frame):
  
  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.createScreen()
    self.pack()

  def createScreen(self):
    self.TEST = Button(self,text="Connect",command=connect)
    self.TEST.pack({"side": "left"})
    self.cName = Entry(self,text="Name")
    self.cName.pack({"side":"right"})
    self.cPort = Entry(self,text="Port")
    self.cPort.pack({"side":"right"})


def connect():
  port = int(a.cPort.get())
  thread.start_new_thread(outgoing.makeConnection, (a.cName.get(),a.cPort.get()))
  
  #print 'Name: %s' % (a.cName.get())
  #print 'Port %s' % (a.cPort.get())



root = Tk()
a = app(master=root)
a.mainloop()
