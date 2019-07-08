from tkinter import Frame, Label, OptionMenu, Entry, Button, Tk, StringVar, END, messagebox
from Main import Main
from threading import Thread
from requests import get
from os import path, mkdir
from webbrowser import open_new_tab
import json



class Interface(Frame):
    def __init__(self, master=None, data={}):
        Frame.__init__(self, master)
        self.version = "0.1.4"
        self.master.title(data["window_name"])
        self.data = data        
        self.init_elements()
        self.check_for_config()
        self.dark_mode()

    def check_for_config(self):
        if path.isfile("./{0}/config.json".format(self.data["directory_name"])):
            with open("./{0}/config.json".format(self.data["directory_name"]), "r") as out:
                self.config = json.load(out)
            
            self.token_box.delete(0,END)
            self.token_box.insert(0,self.config["api_token"])

            self.option_menu_default.set(self.config["platform"])

            self.username_box.delete(0,END)
            self.username_box.insert(0,self.config["username"])

    def init_elements(self):
        self.label_1 = Label(self.master, text="API Token")
        self.label_1.place(x=315, y=10)

        self.token_box = Entry(self.master, width=50)
        self.token_box.place(x=10, y=10)

        self.token_button = Button(self.master, width=20, height=1, text="How Do I Find This?", command=lambda: open_new_tab("https://www.bungie.net/en/Application"))
        self.token_button.place(x=375, y=9)

        self.start_button = Button(self.master, width=72, height=5, text="Start!", command=lambda: self.start_service())
        self.start_button.place(x=10, y=70)

        self.option_menu_default = StringVar()
        self.option_menu_default.set("Playstation")
        self.option_menu = OptionMenu(self.master, self.option_menu_default, "BattleNet", "Playstation", "Xbox")
        self.option_menu.configure(highlightthickness=0)
        self.option_menu.place(x=8, y=35)

        self.label_2 = Label(self.master, text="Select Platform")
        self.label_2.place(x=110, y=40)

        self.username_box = Entry(self.master, width=40)
        self.username_box.place(x=220, y=40)

        self.label_3 = Label(self.master, text="Username")
        self.label_3.place(x=460, y=40)

        self.elements = {
            "labels": [self.label_1, self.label_2, self.label_3],
            "entrys": [self.username_box, self.token_box],
            "optionmenus": [self.option_menu],
            "buttons": [self.start_button, self.token_button]
        }

    def light_mode(self):
        text_colour = "black"
        box_colour = "white"
        background_colour = "#f0f0f0"
        self.master.configure(background=background_colour)
        for element in self.elements["labels"]:
            element.configure(background=background_colour, foreground=text_colour)
        for element in self.elements["buttons"]:
            element.configure(background=background_colour, foreground=text_colour)
        for element in self.elements["entrys"]:
            element.configure(background=box_colour, foreground=text_colour)
        for element in self.elements["optionmenus"]:
            element.configure(highlightthickness=0, background=background_colour, foreground=text_colour, activebackground=background_colour, activeforeground=text_colour) 

    def dark_mode(self):
        text_colour = "white"
        box_colour = "#484b52"
        background_colour = "#36393f"
        self.master.configure(background=background_colour)
        for element in self.elements["labels"]:
            element.configure(background=background_colour, foreground=text_colour)
        for element in self.elements["buttons"]:
            element.configure(background=background_colour, foreground=text_colour)
        for element in self.elements["entrys"]:
            element.configure(background=box_colour, foreground=text_colour)
        for element in self.elements["optionmenus"]:
            element.configure(highlightthickness=0, background=background_colour, foreground=text_colour, activebackground=background_colour, activeforeground=text_colour) 


    def start_service(self):
        packaged_data = {
            "api_token": self.token_box.get(),
            "platform": self.option_menu_default.get(),
            "username":self.username_box.get()
        }
        self._main = Main()
        self.thread = Thread(target=self._main.start_siva, args=(packaged_data,self))
        self.thread.daemon = True
        self.thread.start()

        self.start_button.config(text="Stop!", command=lambda: self.stop_service())

    def stop_service(self):
        self._main.run = False
        self.start_button.config(text="Start!", command=lambda: self.start_service())

    def get_conversion_table(self, table):
        _index = get("https://raw.githubusercontent.com/TheTimebike/SIVA/master/conversion_tables/index.json")
        _data_url = _index.json()[table]
        _data = get(_data_url)
        return _data.json()      

    def error(self, error_enum):
        self._main.run = False
        self.start_button.config(text="Start!", command=lambda: self.start_service())
        error_conversion_table = self.get_conversion_table("error")
        messagebox.showinfo(error_conversion_table["error_window_name"], error_conversion_table["errors"][error_enum])

def start():
    data = get("https://raw.githubusercontent.com/TheTimebike/SIVA/master/siva.json").json()
    root = Tk()
    root.geometry("540x170")
    interface = Interface(root, data)
    root.resizable(False, False)

    if not path.exists("./{0}/".format(data["directory_name"])):
        mkdir("./{0}".format(data["directory_name"]))

    if not path.isfile("./{0}/icon.ico".format(data["directory_name"])):
        _data = get(data["icon_url"])
        if _data.status_code == 200:
            with open("./{0}/icon.ico".format(data["directory_name"]), 'wb') as f:
                f.write(_data.content)
    root.iconbitmap("./{0}/icon.ico".format(data["directory_name"]))
    root.mainloop()