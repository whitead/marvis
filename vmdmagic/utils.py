import socket
from contextlib import closing
import rcsbsearch


def text2pdb(text):
    q1 = rcsbsearch.TextQuery(f'{text}')
    return next(iter(q1("assembly"))).split("-")[0]


def tcl_preamble(port):
    from importlib_resources import files
    import vmdmagic.tcl
    fp = files(vmdmagic.tcl).joinpath(
        'utils.tcl')
    with open(fp, 'r') as f:
        s = f.read()
    return s.replace('%(PORT)', str(port))


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]
