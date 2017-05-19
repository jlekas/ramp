from Tkinter import *
import thread
import outgoing 
import incoming 
import ramp_db
from cache import *

connections = dict()

myName = ""
myPort = ""

messages = ["o", "s!", "my", "lmepo oit!", "bgpuse", "op"]
users  = []
activeUser = None


class app(Frame):

  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.search = ""
    self.fType = None
    self.createScreen()
    self.pack()
    server = None
    incoming.init(server)
    myName = incoming.myName()
    myPort = incoming.myPort()

  def fillerFunction(self):
    return
  
  def select(self, v):
    self.fType = str(v)
    print(self.fType)

  def searchPrivateFiles(self):
    #will make connections and search files of peer
    q = None
    if (self.fType == "General Search"):
      q = query(123, self.fileSearch.get(), "Private")
      print(q, q.findLocal)
    elif (self.fType == "Specific File"):
      q = fileQuery(123, self.fileSearch.get(), "Private")
      print(q, q.findLocal())
  
  def createScreen(self):
    


    self.message = Label(self, text= "Connect to IP:").grid(row=0, column=1)
    self.serverIP = Entry(self, text="IP Address:", exportselection=True)
    self.connectButton = Button(self, text="connect", command= lambda: connect(self.serverIP.get())).grid(row=0, column=3)
 

    self.centerFrame = Frame(self)
    self.centerFrame.grid(row=1, column=1)

    self.activeUserlabel = Label(self.centerFrame, text="Peer:")
    self.activeUserlabel.pack(side="top")
    # self.peerlabel = Label(self.centerFrame)
    # self.peerlabel.pack(side="top")
    

    self.friendsList = Listbox(self)
    self.friendsList.grid(row=1, column=2)

    for u in users:
        self.friendsList.insert(END, u)

    self.serverIP.grid(row=0, column=2)
    self.myInfo = Label(self, text = "MyIP: %s" % (incoming.myName())).grid(row=0, column=0)
    self.chatbox = Listbox(self)
    self.chatbox.grid(row=1, column=0)
    self.chatentry = Entry(self, exportselection=True).grid(row=2, column=0)

    self.sendFilebutton = Button(self, text="Send Message", command=callback).grid(row=2, column=1)
    # self.b = Button(self, text="b").grid(row=0, column=1)
    # self.c = Button(self, text="c").grid(row=1, column=0)
    # self.d = Button(self, text="d").grid(row=1, column=1)
    #self.chatBox = Listbox(root).grid(row=0, column=0)
    # self.a = Label(self,text="S:128.237.139.33\nJ:128.237.92.230")
    # self.a.pack(side=LEFT, padx=5, pady=5)    
    # self.b = Label(self,text="S:128.237.139.33\nJ:128.237.92.230")
    
    # self.b.pack(side=LEFT, padx=5, pady=5)    
    # self.b = Label(self,text="S:128.237.139.33\nJ:128.237.92.230").grid(row=0,column=1)
    # self.c = Label(self,text="S:128.237.139.33\nJ:128.237.92.230").grid(row=1,column=0)
    # self.d = Label(self,text="S:128.237.139.33\nJ:128.237.92.230").grid(row=1,column=1)
   
#     test = Entry(self)
#      test2= Entry(self)
#      test.grid(row=0, column = 3)
#      test2.grid(row=1, column=3) 
#     menubar = Menu(self)
#     fileShareMenu = Menu(menubar, tearoff=0)
#     fileShareMenu.add_command(label="Search For File", command=self.fillerFunction)
#     fileShareMenu.add_command(label="General Search", command=self.fillerFunction)
#     fileShareMenu.add_command(label="Add Files to Public", command=self.fillerFunction)
#     fileShareMenu.add_command(label="Add Files to Private", command=self.fillerFunction)
# # for message in messages:
# #   self.a = Message(self, text=message,anchor=SW, width = 100)
# #   self.a.pack()
#     self.chatBox = Listbox(root).grid(row=0, column=0)
#     #self.chatBox.pack()
#     self.myname = Label(self,text="S:128.237.139.33\nJ:128.237.92.230").grid(row=0,column=1)
#     #self.myname.pack()
#     self.cName = Entry(self, exportselection=True)
#     self.cName.pack()
#     #self.m = (self,orient=HORIZONTAL).grid(row=20, columnspan=10)
#       #self.m.pack(fill=BOTH, expand=1)
#     self.myPort = Label(self,text="Connecting port")
#     self.myPort.pack()
#     self.cPort = Entry(self, exportselection=True)
#     self.cPort.pack()

#     self.message = Entry(self,exportselection=True)
#     self.message.pack()
#     self.Send = Button(self, text="Send Message",command= lambda: connect(self.message.get()))
#     self.Send.pack()
    
#     self.var = StringVar()
#     self.var.set("File or Search:")
#     self.fileSearch = Entry(self, textvariable=self.var, exportselection=True)
#     self.fileSearch.pack()
#     self.type = ["Specific File","General Search"]
#     v = StringVar() 
#     x=Radiobutton(self, text=self.type[0],variable=v,value=self.type[0],command=lambda: self.select(self.type[0]))
#     x.pack()
#     y=Radiobutton(self, text=self.type[1],variable=v,value=self.type[1],command=lambda: self.select(self.type[1]))
#     y.pack()
#     searchTitle = Button(self, text="Search",command=self.searchPrivateFiles)
#     searchTitle.pack()

#     for a in users:
#       self.b=Radiobutton(self, text=a,variable=activeUser,value=a)
#       self.b.pack()
#       print "a user button exists"




def callback():
    name= askopenfilename() 
    print name

def connect(message):
  if a.serverIP.get() not in users:
    users.append(a.serverIP.get())
    a.friendsList.insert(END, a.serverIP.get())
    newPeer()
  elif a.serverIP.get() != activeUser:
    newPeer()
    


    # $$$$$ fn for send $$$$$$$$$ 
  #thread.start_new_thread(outgoing.sendMessage,(activeUser,1085,message))
  
  #print 'Name: %s' % (a.cName.get())
  #print 'Port %s' % (a.cPort.get())

def newPeer():
    try: a.peerlabel.destroy()
    except: pass
    activeUser = a.serverIP.get()
    a.peerlabel = Label(a.centerFrame, text="%s" % activeUser)
    a.peerlabel.pack(side="bottom")


root = Tk()
a = app(master=root)
a.mainloop()
