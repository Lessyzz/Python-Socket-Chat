import socket
import threading

SERVER = "localhost"
PORT = 666
FORMAT = "utf-8"
clients, names = [], []
ADDRESS = (SERVER, PORT)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDRESS)

def startChat():
    print("Server is working on " + SERVER)
    server.listen(10)
    while True:
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(conn)
        print(f"{name} Joined!")
        broadcastMessage(f"{name} Joined!".encode(FORMAT))
        # Threads
        thread = threading.Thread(target=handle,args=(conn,addr))
        thread.start()
        print(f"Online: {threading.active_count()-1}")

def handle(conn,addr):
    global message
    print(f"New connection:  {addr}")
    name = names[clients.index(conn)]
    connected = True

    while connected:
        try:
            message = conn.recv(1024)
            broadcastMessage(message)
        except:
            clients.remove(conn)
            conn.close()
            broadcastMessage(f"{name} left the chat!".encode(FORMAT))
            print(f"{name} left the chat!")
            connected = False
            continue

def broadcastMessage(message):
    for client in clients:
        client.send(message)

startChat()
