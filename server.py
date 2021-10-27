import socket
from sqlite3.dbapi2 import Cursor
import threading
import sqlite3

host = 'localhost'
port = 9099

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

clients =[]
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def user_register(username, password):
    db = sqlite3.connect('user_login.sqlite')
    # db.execute("CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT)")
    db.execute("INSERT INTO login(username, password) VALUES (? , ?)", (username, password))
    cursor = db.cursor()
    cursor.connection.commit()
    db.close()
def user_login(user, password1):
    db = sqlite3.connect('user_login.sqlite')
    cursor = db.cursor()
    cursor.execute("SELECT * FROM login where username = ? AND password = ?",(user, password1))
    row = cursor.fetchone()
    if row:
        return True
    else:
        return False



def handle(client):
    while True:
        try:
            index = clients.index(client)
            data = client.recv(1024).decode()
            tokens = data.split("#")
            instruction = tokens[0]
            msg = message = tokens[1]
            if(instruction == 'send'):
                print(f"{nicknames[index]} says the message {message}")
                broadcast(message.encode())
            elif(instruction == 'kick'):
                kick_user(msg)
                print(f'{msg} was kicked!')
            elif(instruction == 'ban'):
                kick_user(msg)
                with open ('bans.txt', 'a') as f:
                    f.write(f'{msg}\n')
                print(f'{msg} was banned!')
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break

def receive():
    global admin_password
    admin_password = 'admin'

    #create table
    db = sqlite3.connect('user_login.sqlite')
    db.execute("CREATE TABLE IF NOT EXISTS login(username TEXT, password TEXT)")
    
    while True:
        client, address = server.accept()
        print(f"[NEW CONNECTION]: connected with {str(address)}!")
        main_running = False
        with open('bans.txt', 'r') as f:
            bans = f.readlines()
        while(main_running == False):
            
            reg_type = client.recv(1024).decode()
            if(reg_type == "1"):
                data = client.recv(1024).decode()
                tokens = data.split("#")
                username = tokens[0]
                password = tokens[1]
                user_register(username, password)
            if(reg_type == "2"):
                data1 = client.recv(1024).decode()
                tokens = data1.split("#")
                user = tokens[0]
                password1 = tokens[1]

                if user+'\n' in bans:
                    client.send('BAN'.encode())
                    continue


                if user == 'admin':
                   if password1 == admin_password:
                       client.send('admin'.encode())
                       main_running = True
                   else:
                       client.send('not_admin'.encode())
                else:
                    isinformation = user_login(user, password1)
                    if(isinformation):
                        information = "1"
                    else:
                        information = "0"
                    client.send(information.encode())
                    if isinformation:
                        main_running = True


        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        client.send("[CONNECTED] you are connected to the server.".encode())
        nicknames.append(nickname)
        clients.append(client)
        # print(nicknames)
        # print(clients)
        
        print(f"Name of the client is {nickname}")
        broadcast(f"{nickname}, connected to the server!\n".encode())
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        client_to_kick.send('You are kicked by an admin'.encode())
        client_to_kick.close()
        nicknames.remove(name)
        broadcast(f'{name} is kicked by an admin\n'.encode())


print("[SERVER ON]: server is running ......")
receive()
