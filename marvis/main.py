from marvis import *
import click


@click.command()
@click.option('--wav', type=click.Path(exists=True), default=None)
@click.option('--vmd', default='vmd')
@click.option('--port', default=None, type=int)
@click.option('--mock', default=False, is_flag=True)
@click.option('--safe_mode', default=False, is_flag=True)
def main(wav, vmd, port, mock, safe_mode):
    if mock:
        vmd = VMDMock()
    else:
        vmd = VMDStream(port, vmd)
    sel = ''
    print('==========================')
    print('==== MARVIS IS READY =====')
    print('==========================')
    if wav:
        qiter = transcribe_wav_file(wav)
    else:
        qiter = microphone_iter(safe_mode)
    for i, query in enumerate(qiter):
        print(f'({i}) Text: "{query}"')
        result = run_gpt_search(query)
        print(f'({i}) Type: {result["type"]}')
        print(f'({i}) Command: {result["data"]}')
        # have to cache selection because vmd sockets are weird
        if result['type'] == 'VMD Selection':
            sel = result['data']
        else:
            vmd.send(sel + ';' + result['data'])
    vmd.wait()


@click.command()
@click.option('--vmd', default='vmd')
@click.option('--port', default=None, type=int)
@click.option('--mock', default=False, is_flag=True)
@click.option('--safe_mode', default=False, is_flag=True)
@click.option('--transcript', default=None)
def text(vmd, port, mock, safe_mode, transcript):
    if mock:
        vmd = VMDMock()
    else:
        vmd = VMDStream(port, vmd)
    print('==========================')
    print('==== MARVIS IS READY =====')
    print('==========================')
    sel = ''
    trans = []
    for i, query in enumerate(text_iter()):
        result = run_gpt_search(query)
        # have to cache selection because vmd sockets are weird
        if result['type'] == 'VMD Selection':
            sel = result['data']
        else:
            vmd.send(sel + ';' + result['data'])
        print(f'\t({result["type"]})|{result["data"]}')
        trans.append(f'{query}')
        trans.append(f'\t({result["type"]})|{result["data"]}')
    if transcript is not None:
        with open(transcript, 'a') as f:
            f.writelines(trans)
    vmd.wait()
