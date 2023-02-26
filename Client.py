import socket
import threading
from tkinter import *

SERVER = ""
PORT = 0
SERVER = str(SERVER)
PORT = int(PORT)
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
proccess = 0

def save():
    global SERVER
    global PORT
    global ADDRESS
    SERVER = ipAdressEntry.get()
    PORT = portEntry.get()
    PORT = int(PORT)
    ADDRESS = (SERVER, PORT)
    ipPort.destroy()

ipPort = Tk()
ipPort.title("LessyChat")
ipPort.geometry("250x170+780+420")
ipPort.attributes('-topmost',True)
ipPort.configure(background="black")
ipPort.resizable(False, False)
# IpAdressLabel
ipAdressLabel = Label(ipPort,text="Ip adress:",font="Times  10",bg="black",fg="red")
ipAdressLabel.place(x=40, y=30)
# IpAdressEntry
ipAdressEntry = Entry(ipPort,font="Times 10",width=13,bg="black",fg="red")
ipAdressEntry.pack(side = RIGHT)
ipAdressEntry.place(x=110, y=30)
ipAdressEntry.focus()
# PortLabel
portLabel = Label(ipPort,text="Port:",font="Times  10",bg="black",fg="red")
portLabel.place(x=40,y=60)
# PasswordEntry
portEntry = Entry(ipPort,font="Times 10",width=13,bg="black",fg="red")
portEntry.pack()
portEntry.place(x=110, y=60)
# LoginButton
loginButton = Button(ipPort,bg="black",fg="red",width=7,text="Log In",command=save,font="Times 10")
loginButton.pack()
loginButton.place(x=97, y=110)
ipPort.mainloop()

class GUI:
    def __init__(self):
        self.Window = Tk()
        self.Window.withdraw()
        self.login = Toplevel()
        self.login.title("LessyChat")
        self.login.attributes('-topmost',True)
        self.login.configure(background="black")
        self.login.resizable(width=False,height=False)
        self.login.geometry("250x170+780+420")

        self.pls = Label(self.login,text="LessyChat",font="Times 12",bg="black",fg="red")
        self.pls.place(x=90)

        # NicknameLabel
        self.nicknameLabel = Label(self.login,text="Nickname:",font="Times  10",bg="black",fg="red")
        self.nicknameLabel.place(x=40,y=40)
        # Nicknamentry
        self.nicknameEntry = Entry(self.login,font="Times 10",width=13,bg="black",fg="red")
        self.nicknameEntry.place(x=110,y=40)
        self.nicknameEntry.focus()
        # PasswdLabel
        self.passwdLabel = Label(self.login,text="Password:",font="Times  10",bg="black",fg="red")
        self.passwdLabel.place(x=40,y=70)
        # PasswdEntry
        self.passwdEntry = Entry(self.login,font="Times 10",width=13,bg="black",fg="red")
        self.passwdEntry.place(x=110,y=70)
        # Button
        self.go = Button(self.login,text="Log in",font="Times 10",command=lambda: self.goAhead(self.nicknameEntry.get()),width=7,bg="black",fg="red")
        self.go.place(x=97, y=120)
        self.Window.mainloop()
    def goAhead(self, name):
        global proccess
        if self.passwdEntry.get() == "onurc123":
            proccess = 1
        else:
            byLabel = Label(self.login, bg="black", fg="magenta", text="Wrong password!", font="Times 8")
            byLabel.pack()
            byLabel.place(x=85, y=150)
        if proccess == 1:
            self.login.destroy()
            self.layout(name)
            rcv = threading.Thread(target=self.receive)
            rcv.start()

    
    def layout(self, name):
 
        self.name = name
        # To show chat window
        self.Window.deiconify()
        self.Window.bind("<Return>", lambda x: self.sendButton(self.entryMsg.get()))
        self.Window.title("LessyChat")
        self.Window.resizable(width=False,height=False)
        self.Window.configure(width=470,height=550,bg="black")

        self.labelHead = Label(self.Window,bg="black",fg="red",text="LessyChat",font="Times 12",pady=5)
        self.labelHead.place(relwidth=1,y=7)
        self.labelBottom = Label(self.Window,bg="black",height=80)
        self.labelBottom.place(relwidth=1,rely=0.825)

        self.line = Label(self.Window,width=450,bg="black")
        self.line.place(relwidth=1,rely=0.07,relheight=0.012)

        self.textCons = Text(self.Window,width=20,height=2,bg="black",fg="red",font="Helvetica 14",padx=5,pady=5)
        self.textCons.place(relheight=0.745,relwidth=1,rely=0.08)

        self.entryMsg = Entry(self.labelBottom,bg="black",fg="magenta",font="Times 13")
        self.entryMsg.place(relwidth=0.74,relheight=0.06,rely=0.008,relx=0.011)
        self.entryMsg.focus()

        # Create a Send Button
        self.buttonMsg = Button(self.labelBottom,text="Send",font="Times 10 bold",width=20,bg="black",fg="red",command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77,rely=0.008, relheight=0.06,relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons,background="yellow")
        scrollbar.place(relheight=1,relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)
 
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # Insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,message+"\n\n")
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                print("An error occurred!")
                client.close()
                break
 

    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)
g = GUI()
