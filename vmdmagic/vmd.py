from .utils import *
import pexpect


class VMD:
    def __init__(self, vmd_exec):
        from pexpect.popen_spawn import PopenSpawn
        self.msg_end = 'MESSAGE_END'
        tp = tcl_preamble()
        self._vmd = PopenSpawn(
            [vmd_exec, '-nt'], shell=True)
        self._vmd.expect(self.msg_end)
        self._vmd.sendline('puts "MESSAGE_END"')
        print('VMD Loaded')
