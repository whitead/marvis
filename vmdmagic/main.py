from vmdmagic import *
import click


@click.command()
@click.option('--wav', type=click.Path(exists=True), default=None)
@click.option('--vmd', default='vmd')
@click.option('--port', default=None)
@click.option('--mock', default=False, is_flag=True)
@click.option('--safe_mode',default=False, is_flag=True)
def main(wav, vmd, port, mock, safe_mode):
    if mock:
        vmd = VMDMock()
    else:
        vmd = VMDStream(port, vmd)
    sel = ''
    print('----------------------------------------------------------------')
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
        print('----------------------------------------------------------------')
    vmd.wait()


@click.command()
@click.argument('text', nargs=-1)
@click.option('--transcript', default=None)
def text(text, transcript):
    query = ' '.join(text)
    print(f'Text: "{query}"')
    result = run_gpt_search(query)
    print(f'> ({result["type"]}) {result["data"]}')
    if transcript is not None:
        with open(transcript, 'a') as f:
            f.write(f'{query}\n')
            f.write(f'> ({result["type"]}) {result["data"]}\n')
