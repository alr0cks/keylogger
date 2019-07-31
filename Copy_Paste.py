#!/usr/bin/env python

import pyperclip
import time


paste_list = []

if pyperclip.paste() != 'None':
    paste_value = pyperclip.paste()

    if paste_value not in paste_list:
        paste_list.append(paste_value)

    print(paste_list)
    time.sleep(10)
