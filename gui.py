from tkinter import Frame, Label, OptionMenu, Entry, Button, Tk, StringVar
from Main import Main
from threading import Thread

class Interface(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title("SIVA")
        self.init_elements()

    def init_elements(self):
        self.label_1 = Label(
            self.master,
            text="API Token"
        )
        self.label_1.place(x=315, y=10)

        self.token_box = Entry(
            self.master,
            width=50
        )
        self.token_box.place(x=10, y=10)

        self.token_button = Button(
            self.master,
            width=20, height=1,
            text="How Do I Find This?", 
            command=lambda: self.token_button_command()
        )
        self.token_button.place(x=375, y=9)

        self.start_button = Button(
            self.master,
            width=72, height=5,
            text="Start!", 
            command=lambda: self.start_service()
        )
        self.start_button.place(x=10, y=70)

        self.option_menu_default = StringVar()
        self.option_menu_default.set("Playstation")
        self.option_menu = OptionMenu(
            self.master,
            self.option_menu_default,
            "BattleNet", 
            "Playstation", 
            "Xbox"
        )
        self.option_menu.place(x=8, y=35)

        self.label_2 = Label(
            self.master,
            text="Select Platform"
        )
        self.label_2.place(x=110, y=40)

        self.username_box = Entry(
            self.master,
            width=40
        )
        self.username_box.place(x=220, y=40)

        self.label_3 = Label(
            self.master,
            text="Username"
        )
        self.label_3.place(x=460, y=40)

        

    def start_service(self):
        packaged_data = {
            "api_token": self.token_box.get(),
            "platform": self.option_menu_default.get(),
            "username":self.username_box.get()
        }
        self.thread = threading.Thread(target=Main, args=(packaged_data,))
        self.thread.daemon = True
        self.thread.start()

def start():
    root = Tk()
    root.geometry("540x170")
    interface = Interface(root)
    root.resizable(False, False)
    root.mainloop()