from tkinter import Frame, Label, OptionMenu, Entry, Button, Tk, StringVar, END, messagebox, Menu, BooleanVar, Toplevel, Listbox, SINGLE
from modules.Main import Main
from modules.update import update
from threading import Thread
from requests import get
from os import path, mkdir
from sys import exit
from webbrowser import open_new_tab
import json
from infi.systray import SysTrayIcon

class Interface(Frame):
    def __init__(self, master=None, data={}):
        Frame.__init__(self, master)
        self.version = "1.2.0"
        self.master.title(data["window_name"])
        self.data = data    
        self._main = Main(self.data["directory_name"])
        self.default = StringVar()
        self.default.set(self._main.language)
        self.load_config()
        self.init_elements()    
        self.fill_from_config()

        menu_options = (("Open Window", None, self.back),("Start", None, self.start_service),("Stop", None, self.stop_service))
        self.systray = SysTrayIcon("./{0}/icon.ico".format(self.data["directory_name"]), "SIVA", menu_options, on_quit=self.quit_service)
        self.systray.start()
        self.master.protocol("WM_DELETE_WINDOW", self.vanish)

    def quit_service(self, e=None):
        exit(0)

    def vanish(self):
        self.master.withdraw()
        
    def back(self, e=None):
        self.master.update()
        self.master.deiconify()

    def load_config(self):
        if path.isfile("./{0}/config.json".format(self.data["directory_name"])):
            with open("./{0}/config.json".format(self.data["directory_name"]), "r") as out:
                self.config = json.load(out)
        else:
            with open("./{0}/config.json".format(self.data["directory_name"]), "w+") as out:
                self.config = {
                    "api_token": "",
                    "platform": "Playstation",
                    "username": "",
                    "language": "en",
                    "autostart": False,
                    "id_search": False
                }
                json.dump(self.config, out, indent=4)

    def fill_from_config(self):
        self.token_box.delete(0,END)
        self.token_box.insert(0,self.config["api_token"])

        self.option_menu_default.set(self.config["platform"])

        self.username_box.delete(0,END)
        self.username_box.insert(0,self.config["username"])

        if self.config.get("autostart", None) == None:
            self.config["autostart"] = False
        if self.config.get("autostart", None) == True:
            self.start_service()
        if self.config.get("id_search", None) == None:
            self.config["id_search"] = False
        self.search_with_id.set(self.config["id_search"])

    def init_elements(self):
        self.menubar = Menu(self.master)
        self.master.config(menu=self.menubar)

        self.menu_dropdown_siva = Menu(self.menubar)
        self.menu_dropdown_themes = Menu(self.menubar)
        self.menu_dropdown_links = Menu(self.menubar)
        self.menu_dropdown_help = Menu(self.menubar)
        self.menu_dropdown_language = Menu(self.menubar)

        self.menu_dropdown_siva.add_command(label="Start", command=lambda: self.start_service())
        self.menu_dropdown_siva.add_command(label="Stop", command=lambda: self.stop_service())

        self.auto_start = BooleanVar()
        self.auto_start.set(self.config.get("autostart", False))
        self.menu_dropdown_siva.add_checkbutton(label="Autostart", onvalue=True, offvalue=False, variable=self.auto_start, command=lambda: self.start_service())

        self.search_with_id = BooleanVar()
        self.search_with_id.set(self.config.get("id_search", False))
        self.menu_dropdown_siva.add_checkbutton(label="Login With ID", onvalue=True, offvalue=False, variable=self.search_with_id)

        self.menu_dropdown_themes.add_command(label="Light Theme", command=lambda: self.light_mode())
        self.menu_dropdown_themes.add_command(label="Dark Theme", command=lambda: self.dark_mode())

        self.menu_dropdown_links.add_command(label="Get A Token", command=lambda: open_new_tab("https://www.bungie.net/en/Application"))
        self.menu_dropdown_links.add_command(label="Message Me On Reddit", command=lambda: open_new_tab("https://www.reddit.com/message/compose?to=TheTimebike&subject=SIVA"))
        self.menu_dropdown_links.add_command(label="Github", command=lambda: open_new_tab("https://github.com/TheTimebike/SIVA"))
        self.menu_dropdown_links.add_command(label="Report An Issue", command=lambda: open_new_tab("https://github.com/TheTimebike/SIVA/issues"))

        self.menu_dropdown_help.add_command(label="About", command=lambda: messagebox.showinfo("SIVA", "SIVA:\nVersion: {0}\nCreator: u/TheTimebike".format(self.version)))

        language_conversion_table = self.get_conversion_table("language")

        for lang, key in language_conversion_table.items():
            self.add_language(lang, key)

        self.menubar.add_cascade(label="SIVA", menu=self.menu_dropdown_siva)
        self.menubar.add_cascade(label="Themes", menu=self.menu_dropdown_themes)
        self.menubar.add_cascade(label="Links", menu=self.menu_dropdown_links)
        self.menubar.add_cascade(label="Help", menu=self.menu_dropdown_help)
        self.menubar.add_cascade(label="Languages", menu=self.menu_dropdown_language)

        if self.data["version"] != self.version:
            self.menubar.add_command(label="Update", command=lambda:update(self))

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
        self.option_menu = OptionMenu(self.master, self.option_menu_default, "Playstation", "Xbox", "Steam", "Stadia")
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

    def add_language(self, lang, key):
        self.menu_dropdown_language.add_radiobutton(label=lang, value=key, variable=self.default, command=lambda: self.change_language(key))

    def change_language(self, key):
        self._main.language = key
        self._main.configurator.save({
            "api_token": self.token_box.get(),
            "platform": self.option_menu_default.get(),
            "username": self.username_box.get(),
            "language": self._main.language,
            "autostart": self.auto_start.get()
        })

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


    def start_service(self, e=None):
        self._main.configurator.save({
            "api_token": self.token_box.get(),
            "platform": self.option_menu_default.get(),
            "username": self.username_box.get(),
            "language": self._main.language,
            "autostart": self.auto_start.get(),
            "id_search": self.search_with_id.get()
        })
        self.thread = Thread(target=self._main.start_siva, args=(self,))
        self.thread.daemon = True
        self.thread.start()

        self.start_button.config(text="Stop!", command=lambda: self.stop_service())

    def stop_service(self, e=None):
        self._main.run = False
        self.start_button.config(text="Start!", command=lambda: self.start_service())

    def get_conversion_table(self, table):
        _index = get("https://raw.githubusercontent.com/TheTimebike/SIVA/master/conversion_tables/index.json")
        _data_url = _index.json()[table]
        _data = get(_data_url)
        return _data.json()      

    def error(self, error_enum):
        self.stop_service()
        error_conversion_table = self.get_conversion_table("error")
        messagebox.showinfo(error_conversion_table["error_window_name"], error_conversion_table["errors"][error_enum])
        return None

    def create_pick_account_interface(self, acc_list):
        self.select_acc_window = SubWindow(self.master, acc_list, self._main)
        self.select_acc_window.master.iconbitmap("./{0}/icon.ico".format(self.data["directory_name"]))

class SubWindow():
    def __init__(self, main_window, acc_list, main):
        self.master = Toplevel(main_window)
        self.master.resizable(False, False)
        self.master.title("Select Your Account")
        self.main = main

        self.len_max = 50
        for m in acc_list:
            if len(m[0]) > self.len_max:
                self.len_max = len(m[0])
            
        self.listbox = Listbox(self.master, width=self.len_max, selectmode=SINGLE)
        self.listbox.grid(row=0, column=1)
        self.listbox.bind('<Double-Button>', self.selected_event)
        self.listbox_list = []
        for item in acc_list:
            self.listbox.insert(END, item[0])
            self.listbox_list.append(item[1])
        
    def selected_event(self, e=None):
        self.main.set_membershipID(self.listbox_list[self.listbox.curselection()[0]])
        self.master.destroy()

def start():
    data = get("https://raw.githubusercontent.com/TheTimebike/SIVA/master/siva.json").json()
    root = Tk()
    root.geometry("540x170")

    if not path.exists("./{0}/".format(data["directory_name"])):
        mkdir("./{0}".format(data["directory_name"]))

    interface = Interface(root, data)
    root.resizable(False, False)

    if not path.isfile("./{0}/icon.ico".format(data["directory_name"])):
        _data = get(data["icon_url"])
        if _data.status_code == 200:
            with open("./{0}/icon.ico".format(data["directory_name"]), 'wb') as f:
                f.write(_data.content)
    root.iconbitmap("./{0}/icon.ico".format(data["directory_name"]))
    root.mainloop()

start()
