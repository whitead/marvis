import os
import sys
import socket
import subprocess
import time
import tempfile
from .utils import tcl_preamble, find_free_port


# See https://github.com/hockyg/pyvmdstream
class VMDStream:
    def __init__(self, port, vmd_exe):
        if port is None:
            port = find_free_port()
        tp = tcl_preamble(port)
        fd, tmp_name = tempfile.mkstemp(text=True)
        with open(fd, 'w') as f:
            f.write(tp)
        self.p = subprocess.Popen([vmd_exe, '-e', tmp_name], shell=True)
        time.sleep(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        # time.sleep(2)
        self.s = s
        self.closed = False

    def close(self):
        ''' Close the connection to VMD '''
        if not self.closed:
            if self.p.poll() is None:
                self.send('exit')
                self.p.wait(5)
            self.s.close()
            self.closed = True

    def wait(self):
        self.p.wait()

    def __del__(self):
        self.close()

    def send(self, sendstring):
        ''' Send a command directly to VMD '''
        # can't be wrong to add this?
        sendstring += os.linesep
        self.s.send(sendstring.encode())
