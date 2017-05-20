from Tkinter import *
import thread
import outgoing 
import incoming 
import ramp_db
from cache import *



messages = dict() #ADDED
users  = []
# activeUser;

class app(Frame):

  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.activeUser = None
    self.search = ""
    self.fType = None
    self.createScreen()
    self.pack()
    server = None
    incoming.init(server, self,messages)
    myName = incoming.myName()
    myPort = incoming.myPort()

  def fillerFunction(self):
    return
  
  def select(self, v):
    self.fType = str(v)
    print(self.fType)

  
  def createScreen(self):
    self.message = Label(self, text= "Connect to IP:").grid(row=0, column=1)
    self.serverIP = Entry(self, text="IP Address:", exportselection=True)
    self.connectButton = Button(self, text="connect", command= lambda: connect(self.serverIP.get())).grid(row=1, column=3)
 

    self.centerFrame = Frame(self)
    self.centerFrame.grid(row=1, column=1)

    self.activeUserlabel = Label(self.centerFrame, text="Peer:")
    self.activeUserlabel.pack(side="top")

    self.friendsList = Listbox(self)
    self.friendsList.bind('<<ListboxSelect>>', clearConnectEntry)
    self.friendsList.grid(row=1, column=2)

    for u in users:
        self.friendsList.insert(END, u)


    self.chatBoxFrame = Frame(self)
    self.chatBoxFrame.grid(row=1, column=0)

    self.scroll = Scrollbar(self.chatBoxFrame)
    self.chatBox = Text(self.chatBoxFrame, width=50, height=15, state=DISABLED)
    self.scroll.pack(side=RIGHT, fill=Y)
    self.chatBox.pack(side=LEFT)

    self.serverIP.grid(row=0, column=2)
    self.myInfo = Label(self, text = "MyIP: %s" % (incoming.myName())).grid(row=0, column=0)

    self.chatFrame = Frame(self)
    self.chatFrame.grid(row=2, column=0)
    self.sendChatButton = Button(self.chatFrame, text="Send Chat", command= lambda: chatOut(1),width=8)
    self.sendChatButton.pack(side=RIGHT)

    self.chatentry = Entry(self.chatFrame, exportselection=True,width=37)
    self.chatentry.bind('<Return>', chatOut)
    self.chatentry.pack(side=LEFT)

    self.vidChatButton = Button(self, text="Start Video Chat", command=vidOut).grid(row=2, column=2)
    self.fileLabel = Label(self, text="Search for Friends' Files").grid(row=3, column=1)
    self.var = StringVar()
    self.var.set("File or Search:")
    self.fileSearch = Entry(self, exportselection=True)
    self.fileSearch.grid(row=4, column=1)
    self.type = ["Specific File","General Search"]
    v = StringVar() 
    x=Radiobutton(self, text=self.type[0],variable=v,value=self.type[0],command=lambda: self.select(self.type[0])).grid(row=4, column=0)
    y=Radiobutton(self, text=self.type[1],variable=v,value=self.type[1],command=lambda: self.select(self.type[1])).grid(row=5, column=0)
    searchTitle = Button(self, text="Search Files",command=self.searchPrivateFiles).grid(row=4, column=2)

  def searchPrivateFiles(self):
    #will make connections and search files of peer
    q = None
    if (self.fType == "General Search"):
      q = query(123, self.fileSearch.get(), "Private")
      outgoing.sendFileRequest(a.activeUser, "1085", q)
    elif (self.fType == "Specific File"):
      q = fileQuery(123, self.fileSearch.get(), "Private")
      outgoing.sendFileRequest(a.activeUser, "1085", q)




def callback():
    name= askopenfilename() 
    print name

def connect(message):
  if a.serverIP.get() == "":
    newPeer(users[a.friendsList.curselection()[0]])
  elif a.serverIP.get() not in users:
    try: 
        outgoing.sendPing(a.serverIP.get())
    except:
        a.chatBox.config(state=NORMAL)
        a.chatBox.delete(1.0, END)
        a.chatBox.insert(END, "Could not connect to: %s\n" % a.serverIP.get())
        a.chatBox.config(state=DISABLED)
        return

    users.append(a.serverIP.get())
    a.friendsList.insert(END, a.serverIP.get())

    if a.serverIP.get() not in messages:
        messages[a.serverIP.get()] = [] #ADDED 
    
    # print messages  
    newPeer(a.serverIP.get())
  elif a.serverIP.get() != a.activeUser:
    newPeer(a.serverIP.get())
  

  a.chatBox.config(state=NORMAL)
  a.chatBox.delete(1.0, END) #ADDED
  a.chatBox.config(state=DISABLED)

  for m in  messages[a.activeUser]: #ADDED
    a.chatBox.config(state=NORMAL)
    a.chatBox.insert(END, m) #ADDED
    a.chatBox.config(state=DISABLED)



def clearConnectEntry(abc):
    a.serverIP.delete(0,'end')

def newPeer(string):
    try: a.peerlabel.destroy()
    except: pass
    a.activeUser = string
    a.peerlabel = Label(a.centerFrame, text="%s" % a.activeUser)
    a.peerlabel.pack(side="bottom")

def chatOut(event):
    if a.activeUser == None:
        a.chatBox.config(state=NORMAL)
        a.chatBox.insert(END, "You are not connected to anyone\n Connect to someone first ----------------->\n")
        a.chatBox.config(state=DISABLED)
        a.chatentry.delete(0,'end')
        return
    if a.chatentry.get() != "":
        a.chatBox.config(state=NORMAL)
        a.chatBox.insert(END, "Me: %s\n" % a.chatentry.get())
        a.chatBox.config(state=DISABLED)

        messages[a.activeUser].append("Me: %s\n" % a.chatentry.get()) #ADDED


        port = 1085
        print '%s %s' % (a.activeUser, port)
        thread.start_new_thread(outgoing.sendMessage,(a.activeUser,port,a.chatentry.get()))
        a.chatentry.delete(0,'end')


def vidOut():
  port = 1085
  print(a.activeUser)
  thread.start_new_thread(outgoing.sendVideo,(a.activeUser,port))

root = Tk()
a = app(master=root)
a.mainloop()
