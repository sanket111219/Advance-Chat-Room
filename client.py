
import socket
import threading 
import tkinter as tk
import tkinter.scrolledtext
from tkinter import messagebox
from typing import TYPE_CHECKING
from tkinter import *


HOST = 'localhost'
PORT = 9099


class Client:
    
    def __init__(this, host, port):
        this.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.sock.connect((host, port))
        # this.nickname = ""
        # this.passw = ""
        
        
        this.gui_done = False
        # flag to run main chat window
        this.main_running = False

        #flag to run registation and login window
        this.ask_running = True

        this.ask()

        gui_thread = threading.Thread(target = this.gui_loop)
        receive_thread = threading.Thread(target = this.receive)

        gui_thread.start()
        receive_thread.start()
    
    def ask(this):
        while this.ask_running:
            this.ask_win = tkinter.Tk()
            this.ask_win.title('Welcome to Chat')
            this.ask_win.iconbitmap('1.ico')
            this.ask_win.configure(bg = '#1100a0')
            this.ask_win.geometry('400x300')

            this.ask_win['padx'] = 40

            this.registration_btn = tkinter.Button(this.ask_win, text='REGISTER', font = ('Times New Roman',12), width = 10, height = 1, bg = '#ff2e38', command=this.register)
            this.registration_btn.place(x=100, y=100)
            this.login_btn = tkinter.Button(this.ask_win, text='LOGIN',font = ('Times New Roman',12), width = 10, height = 1,bg = '#ff2e38', command=this.login)
            this.login_btn.place(x=100, y=150)

            this.ask_win.protocol("WM_DELETE_WINDOW", this.ask_stop)
            this.ask_win.mainloop()
            if(this.ask_running == False):
                break
    

    def ask_stop(this):
        this.ask_running = False
        this.ask_win.destroy()
        this.sock.close()
        
    # reistration code
    def register(this):
        this.main_reg = tkinter.Tk()
        this.main_reg.title('Entry')
        this.main_reg.configure(bg = '#1100a0')
        this.main_reg.iconbitmap('1.ico')

        this.main_reg.geometry('400x300')
        this.main_reg['padx'] = 20

        this.user_info = tkinter.Label(this.main_reg,  text='Username' , width = 10, height = 1, bg = '#A8FFAF',  font = ('Times New Roman',12))
        this.user_info.place(x=50,y = 80)
        this.userinput = tkinter.Entry(this.main_reg, bd = 3, font = ('Times New Roman',12))
        this.userinput.place(x = 150, y = 80)
        this.pass_info = tkinter.Label(this.main_reg, text='Password', width = 10, height = 1, bg = '#A8FFAF', font = ('Times New Roman',12))
        this.pass_info.place(x=50, y = 120)
        this.passinput = tkinter.Entry(this.main_reg, show="*", bd = 3, font = ('Times New Roman',12))
        this.passinput.place(x = 150, y = 120)

        this.reg_btn = tkinter.Button(this.main_reg, text='SUBMIT',font = ('Times New Roman',12), width = 10, height = 1,bg = '#ff2e38', command=this.onSubmit)
        this.reg_btn.place(x = 150,y=180)

     # submit for registration    
    def onSubmit(this):
        if this.userinput.get() == '' or this.passinput.get() == '':
            messagebox.showwarning('registration', 'Enter username/password')
        else:
            this.sock.send("1".encode())
            this.nickname = this.userinput.get()
            this.passw = this.passinput.get()
            this.data = this.nickname+"#"+this.passw
            this.sock.send(this.data.encode())
            this.main_reg.destroy()
            messagebox.showinfo('registration', 'registration successful')
    # login code    
    def login(this):
        this.main_log = tkinter.Tk()
        this.main_log.title('Entry')
        this.main_log.iconbitmap('1.ico')
        this.main_log.configure(bg = '#1100a0')
        this.main_log.geometry('400x300')

        this.main_log['padx'] = 20

        this.user_info1 = tkinter.Label(this.main_log,  text='Username' , width = 10, height = 1, bg = '#A8FFAF',  font = ('Times New Roman',12))
        this.user_info1.place(x=50,y = 80)
        this.userinput1 = tkinter.Entry(this.main_log, bd = 3, font = ('Times New Roman',12))
        this.userinput1.place(x = 150, y = 80)
        this.pass_info1 = tkinter.Label(this.main_log, text='Password', width = 10, height = 1, bg = '#A8FFAF', font = ('Times New Roman',12))
        this.pass_info1.place(x=50, y = 120)
        this.passinput1 = tkinter.Entry(this.main_log, show="*", bd = 3, font = ('Times New Roman',12))
        this.passinput1.place(x = 150, y = 120)

        this.log_btn = tkinter.Button(this.main_log, text='SUBMIT',font = ('Times New Roman',12), width = 10, height = 1,bg = '#ff2e38', command=this.onClick)
        this.log_btn.place(x = 150,y=180)

        this.main_log.mainloop()

    # submit for login
    def onClick(this):
        this.login_user = this.userinput1.get()
        this.login_password = this.passinput1.get()
        if this.login_user == '' or this.login_password == '':
            messagebox.showwarning('login', 'Enter username/password')
        else:
            this.sock.send("2".encode())
            this.data1 = this.login_user+ "#"+ this.login_password
            this.sock.send(this.data1.encode())
            isinformation = this.sock.recv(1024).decode()
            if isinformation == 'admin':
                this.main_log.destroy()
                messagebox.showinfo('login', 'Welcome admin')
                this.ask_running = False
                this.main_running = True
                this.ask_win.destroy()
            elif isinformation == 'not_admin':
                this.main_log.destroy()
                messagebox.showerror("login", "enter valid admin_password")
            elif(isinformation == "1"):
                this.main_log.destroy()
                messagebox.showinfo("login", "login Successful") 
                this.ask_running = False
                this.main_running = True
                this.ask_win.destroy()
            elif isinformation == 'BAN':
                this.main_log.destroy()
                messagebox.showerror('login', 'Sorry! You are banned!')
            else:
                this.main_log.destroy()
                messagebox.showerror("login", "login failed")
        

   
    
    def gui_loop(this):

        #UI for admin interface

        if this.login_user == 'admin':
            # window configaration 
            this.window = tkinter.Tk()
            this.window.title('Chat')
            this.window.iconbitmap('1.ico')
            file = PhotoImage(file ="F:\college\Code\socketProject/bg3.png")
            this.label = Label(this.window, image = file)
            this.label.place(x = 0, y = 0, relwidth= 1, relheight=1)
            this.window.geometry('500x760')
            
            


            #chat configaration
            this.chat_label = tkinter.Label(this.window, text ="Chat", bg="#5cb849")
            this.chat_label.config(font = ("Arial", 12))
            this.chat_label.pack(padx = 20, pady = 5)

            #text configaration
            this.text_area = tkinter.scrolledtext.ScrolledText(this.window, font = ('Montserrat',15))
            this.text_area.pack(padx =20, pady=5)
            this.text_area.config(state = 'disable')

            #message configaration
            this.msg_label = tkinter.Label(this.window, text ="Message", bg="#5cb849")
            this.msg_label.config(font = ("Arial", 12))
            this.msg_label.pack(padx = 20, pady = 5)

            this.input_area = tkinter.Text(this.window, height = 3,font = ('Montserrat',15))
            this.input_area.pack(padx = 20, pady = 5)

            frame = Frame(this.window, bg = "#5cb849")
            frame.pack(pady=5)

            this.send_button = tkinter.Button(frame, text = "Send", command=this.write,bg="#5cb849")
            this.send_button.config(font=("Arial", 12))
            this.send_button.grid(row = 0, column = 0, padx =2)

            this.kick_button = tkinter.Button(frame, text = "Kick", command=this.kick,bg="#5cb849")
            this.kick_button.config(font=("Arial", 12))
            this.kick_button.grid(row = 0, column = 1, padx =2)

            this.ban_button = tkinter.Button(frame, text = "Ban", command=this.ban,bg="#5cb849")
            this.ban_button.config(font=("Arial", 12))
            this.ban_button.grid(row = 0, column = 2, padx =2)

            this.gui_done = True

            this.window.protocol("WM_DELETE_WINDOW", this.stop)

            this.window.mainloop()

        #UI for admin interface
        else:
            # window configaration 
            this.window = tkinter.Tk()
            this.window.title('Chat')
            this.window.iconbitmap('1.ico')
            file = PhotoImage(file ="F:\college\Code\socketProject/bg3.png")
            this.label = Label(this.window, image = file)
            this.label.place(x = 0, y = 0, relwidth= 1, relheight=1) 
            this.window.geometry('500x760')

            #chat configaration
            this.chat_label = tkinter.Label(this.window, text ="Chat", bg="#5cb849")
            this.chat_label.config(font = ("Arial", 12))
            this.chat_label.pack(padx = 20, pady = 5)

            #text configaration
            this.text_area = tkinter.scrolledtext.ScrolledText(this.window,font = ('Montserrat',15))
            this.text_area.pack(padx =20, pady=5)
            this.text_area.config(state = 'disable')

            #message configaration
            this.msg_label = tkinter.Label(this.window, text ="Message", bg="#5cb849")
            this.msg_label.config(font = ("Arial", 12))
            this.msg_label.pack(padx = 20, pady = 5)

            this.input_area = tkinter.Text(this.window, height = 3,font = ('Montserrat',15))
            this.input_area.pack(padx = 20, pady = 5)

            this.send_button = tkinter.Button(this.window, text = "Send", command=this.write,bg="#5cb849")
            this.send_button.config(font=("Arial", 12))
            this.send_button.pack(padx=20, pady=5)

            this.gui_done = True

            this.window.protocol("WM_DELETE_WINDOW", this.stop)

            this.window.mainloop()


    def stop(this):
        this.main_running = False
        this.window.destroy()
        this.sock.close()

    def write(this):
        message = "send#"+f"{this.login_user} : {this.input_area.get('1.0', 'end')}"
        this.sock.send(message.encode())
        this.input_area.delete('1.0', 'end')
    
    def kick(this):
        message = "kick#"+f"{this.input_area.get('1.0', 'end-1c')}"
        this.sock.send(message.encode())
        this.input_area.delete('1.0', 'end')

    def ban(this):
        message = "ban#"+f"{this.input_area.get('1.0', 'end-1c')}"
        this.sock.send(message.encode())
        this.input_area.delete('1.0', 'end')

    def receive(this):
        # to run main chat window
        while this.main_running:
            try:
                message = this.sock.recv(1024).decode()
                if message == "NICK":
                    this.sock.send(this.login_user.encode())
                elif message == 'You are kicked by an admin':
                        this.main_running = False
                        if this.gui_done : 
                            this.text_area.config(state = 'normal')
                            this.text_area.insert('end', message)
                            this.text_area.yview('end')
                            this.text_area.config(state = 'disable')
                            return
                else:
                    if this.gui_done : 
                        this.text_area.config(state = 'normal')
                        this.text_area.insert('end', message)
                        this.text_area.yview('end')
                        this.text_area.config(state = 'disable')
            except ConnectionAbortedError:
                break
            except:
                print("Error")
                this.sock.close()
                break



client = Client(HOST,PORT)
