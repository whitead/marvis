import socket
from contextlib import closing
import rcsbsearch
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory


def text2pdb(text):
    q1 = rcsbsearch.TextQuery(f'{text}')
    return next(iter(q1("assembly"))).split("-")[0]


def tcl_preamble(port):
    from importlib_resources import files
    import marvis.tcl
    fp = files(marvis.tcl).joinpath(
        'utils.tcl')
    with open(fp, 'r') as f:
        s = f.read()
    return s.replace('%(PORT)', str(port))


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def text_iter():
    #history = InMemoryHistory()
    # session = PromptSession(
    #    history=history,
    # auto_suggest=AutoSuggestFromHistory(),
    # enable_history_search=True,
    # complete_while_typing=True
    # )
    while True:
        # this always freezes on windows. Looks cool though!
        #q = session.prompt('marvis-text> ')
        q = input('marvis-text> ')
        if q.strip() == '':
            continue
        yield q
