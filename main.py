from Tkinter import *
import thread
import outgoing 
import incoming 
import ramp_db
from cache import *


messages = dict() #stores keys of other users and a list of messages since start


class app(Frame):


  def __init__(self, master=None):
    Frame.__init__(self, master)
    self.activeUser = None #always one connected to when displayed on UI
    self.search = ""
    self.fType = None
    self.createScreen()
    self.pack()
    server = None
    incoming.init(server, self,messages) #initializes server socket
    myName = incoming.myName()
    myPort = incoming.myPort()

  
  def select(self, v): #command for radio buttons
    self.fType = str(v)
    print(self.fType)

  
  def createScreen(self):
    #top row
    self.message = Label(self, text= "Connect to IP:").grid(row=0, column=1)
    self.serverIP = Entry(self, text="IP Address:", exportselection=True)
    self.serverIP.grid(row=0, column=2)
    self.connectButton = Button(self, text="Connect", command= lambda: connect(self.serverIP.get())).grid(row=1, column=3)
    self.myInfo = Label(self, text = "MyIP: %s" % (incoming.myName())).grid(row=0, column=0)

    #peer label and active user (center) also hold peer label in newPeer
    self.centerFrame = Frame(self)
    self.centerFrame.grid(row=1, column=1) 
    self.activeUserlabel = Label(self.centerFrame, text="Peer:")
    self.activeUserlabel.pack(side="top")

    #friends list and connect (right)
    self.friendsList = Listbox(self)
    self.friendsList.bind('<<ListboxSelect>>', clearConnectEntry)
    self.friendsList.grid(row=1, column=2)

    #chat logs, scroll bar, text entry and button (left)
    self.chatBoxFrame = Frame(self)
    self.chatBoxFrame.grid(row=1, column=0)
    self.scroll = Scrollbar(self.chatBoxFrame)
    self.chatBox = Text(self.chatBoxFrame, width=50, height=15, state=DISABLED)
    self.scroll.pack(side=RIGHT, fill=Y)
    self.chatBox.pack(side=LEFT)
    self.chatFrame = Frame(self)
    self.chatFrame.grid(row=2, column=0)
    self.sendChatButton = Button(self.chatFrame, text="Send Chat", command= lambda: chatOut(1),width=8)
    self.sendChatButton.pack(side=RIGHT)
    self.chatentry = Entry(self.chatFrame, exportselection=True,width=37)
    self.chatentry.bind('<Return>', chatOut)
    self.chatentry.pack(side=LEFT)

    #file search/download, options, and video chat button
    self.vidChatButton = Button(self, text="Start Video Chat", command=vidOut).grid(row=2, column=2)
    self.fileLabel = Label(self, text="File Name").grid(row=3, column=1)
    self.var = StringVar()
    self.var.set("File or Search:")
    self.fileSearch = Entry(self, exportselection=True)
    self.fileSearch.grid(row=4, column=1)
    self.type = ["Specific File","General Search"]
    v = StringVar() 
    x=Radiobutton(self, text="Exact File",variable=v,value=self.type[0],command=lambda: self.select(self.type[0])).grid(row=4, column=0)
    y=Radiobutton(self, text="Similar Files",variable=v,value=self.type[1],command=lambda: self.select(self.type[1])).grid(row=5, column=0)
    searchTitle = Button(self, text="Download Files",command=self.searchPrivateFiles).grid(row=4, column=2)


  def searchPrivateFiles(self):
    #outer function for calling get file request with user options selected
    q = None
    if (self.fType == "General Search"):
      q = query(123, self.fileSearch.get(), "Private")
      outgoing.sendFileRequest(a.activeUser, "1085", q)
    elif (self.fType == "Specific File"):
      q = fileQuery(123, self.fileSearch.get(), "Private")
      outgoing.sendFileRequest(a.activeUser, "1085", q)


def connect(message):
  #called whenever the connect button is clicked
  if a.serverIP.get() == "":
    #case where user selects from friends list and clicks connect
    newPeer(messages[a.friendsList.curselection()[0]])
  elif a.serverIP.get() not in messages:
    #case where connecting to a new ip
    try: 
        #check if connection works with ping
        outgoing.sendPing(a.serverIP.get())
    except:
        a.chatBox.config(state=NORMAL)
        a.chatBox.delete(1.0, END)
        a.chatBox.insert(END, "Could not connect to: %s\n" % a.serverIP.get())
        a.chatBox.config(state=DISABLED)
        return
    #add friend and retrieve messages if they exist
    a.friendsList.insert(END, a.serverIP.get())
    if a.serverIP.get() not in messages:
        messages[a.serverIP.get()] = [] 
    
    newPeer(a.serverIP.get())
    #set to active user
  elif a.serverIP.get() != a.activeUser:
    newPeer(a.serverIP.get())
  
  a.chatBox.config(state=NORMAL)
  a.chatBox.delete(1.0, END) #ADDED
  a.chatBox.config(state=DISABLED)
  #load messages
  for m in  messages[a.activeUser]: #ADDED
    a.chatBox.config(state=NORMAL)
    a.chatBox.insert(END, m) #ADDED
    a.chatBox.config(state=DISABLED)



def clearConnectEntry(abc): 
    #removes entry from connect to ip when friends list is clicked to avoid confusion
    a.serverIP.delete(0,'end')

def newPeer(string): #corrects and displays active user
    try: a.peerlabel.destroy()
    except: pass
    a.activeUser = string
    a.peerlabel = Label(a.centerFrame, text="%s" % a.activeUser)
    a.peerlabel.pack(side="bottom")

def chatOut(event):
    #outer function for sending message
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
        #sends message on new thread, handled in outgoing
        thread.start_new_thread(outgoing.sendMessage,(a.activeUser,port,a.chatentry.get()))
        a.chatentry.delete(0,'end')


def vidOut():
  #outer function for video chat
  port = 1085
  print(a.activeUser)
  thread.start_new_thread(outgoing.sendVideo,(a.activeUser,port))


#tkinter startup
root = Tk()
a = app(master=root)
a.mainloop()
