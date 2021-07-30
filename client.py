
import socket
import threading 
import tkinter
import tkinter.scrolledtext
from tkinter import messagebox
from typing import TYPE_CHECKING


HOST = 'localhost'
PORT = 9099


class Client:
    
    def __init__(this, host, port):
        this.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        this.sock.connect((host, port))
        this.nickname = ""
        this.passw = ""
        
        this.gui_done = False

        this.main_running = False
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
            this.ask_win.geometry('400x300')

            this.ask_win['padx'] = 40

            this.registration_btn = tkinter.Button(this.ask_win, text='register', command=this.register)
            this.registration_btn.grid(row=20, column=5, padx= 40,pady=5)
            this.login_btn = tkinter.Button(this.ask_win, text='login', command=this.login)
            this.login_btn.grid(row=20, column=8, pady=5, padx= 40)

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
        this.main_reg.geometry('400x300')
        padd = 20
        this.main_reg['padx'] = padd

        this.user_info = tkinter.Label(this.main_reg,  text='Username')
        this.user_info.grid(row=1,column=0)
        this.userinput = tkinter.Entry(this.main_reg)
        this.userinput.grid(row=1, column=1)
        this.pass_info = tkinter.Label(this.main_reg, text='Password')
        this.pass_info.grid(row=2, column=0, pady = 20)
        this.passinput = tkinter.Entry(this.main_reg, show="*")
        this.passinput.grid(row=2, column=1)

        this.reg_btn = tkinter.Button(this.main_reg, text='SUBMIT', command=this.onSubmit)
        this.reg_btn.grid(row = 3,column=1)

     # submit for registration    
    def onSubmit(this):
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
        this.main_log.geometry('400x300')
        padd = 20
        this.main_log['padx'] = padd

        this.user_info1 = tkinter.Label(this.main_log,  text='Username')
        this.user_info1.grid(row=1,column=0)
        this.userinput1 = tkinter.Entry(this.main_log)
        this.userinput1.grid(row=1, column=1)
        this.pass_info1 = tkinter.Label(this.main_log, text='Password')
        this.pass_info1.grid(row=2, column=0, pady = 20)
        this.passinput1 = tkinter.Entry(this.main_log, show="*")
        this.passinput1.grid(row=2, column=1)

        this.log_btn = tkinter.Button(this.main_log, text='SUBMIT', command=this.onClick)
        this.log_btn.grid(row = 3,column=1)

        this.main_log.mainloop()

    # submit for login
    def onClick(this):
        this.sock.send("2".encode())
        this.login_user = this.userinput1.get()
        this.login_password = this.passinput1.get()
        this.data1 = this.login_user+ "#"+ this.login_password
        this.sock.send(this.data1.encode())
        isinformation = this.sock.recv(1024).decode()
        if(isinformation == "1"):
            this.main_log.destroy()
            messagebox.showinfo("login", "login Successful") 
            this.ask_running = False
            this.main_running = True
            this.ask_win.destroy()
        else:
            this.main_log.destroy()
            messagebox.showerror("login", "login failed")
        

   
    
    def gui_loop(this):

        # window configaration 
        this.window = tkinter.Tk()
        this.window.configure(bg = "lightgray")

        #chat configaration
        this.chat_label = tkinter.Label(this.window, text ="Chat:", bg="lightgray")
        this.chat_label.config(font = ("Arial", 12))
        this.chat_label.pack(padx = 20, pady = 5)

        #text configaration
        this.text_area = tkinter.scrolledtext.ScrolledText(this.window)
        this.text_area.pack(padx =20, pady=5)
        this.text_area.config(state = 'disable')

        #message configaration
        this.msg_label = tkinter.Label(this.window, text ="Message:", bg="lightgray")
        this.msg_label.config(font = ("Arial", 12))
        this.msg_label.pack(padx = 20, pady = 5)

        this.input_area = tkinter.Text(this.window, height = 3)
        this.input_area.pack(padx = 20, pady = 5)

        this.send_button = tkinter.Button(this.window, text = "Send: ", command=this.write)
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
        message = f"{this.login_user} : {this.input_area.get('1.0', 'end')}"
        this.sock.send(message.encode())
        this.input_area.delete('1.0', 'end')

    def receive(this):
        while this.main_running:
            try:
                message = this.sock.recv(1024).decode()
                if message == "NICK":
                    this.sock.send(this.login_user.encode())
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
