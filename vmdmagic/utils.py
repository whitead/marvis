import rcsbsearch


def text2pdb(text):
    q1 = rcsbsearch.TextQuery(f'{text}')
    return next(iter(q1("assembly"))).split("-")[0]


def tcl_preamble():
    from importlib_resources import files
    import vmdmagic.tcl
    fp = files(vmdmagic.tcl).joinpath(
        'utils.tcl')
    with open(fp, 'r') as f:
        return f.read()
