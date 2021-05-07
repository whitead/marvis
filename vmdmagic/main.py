from vmdmagic import *
import click


@click.command()
@click.argument('wav', type=click.Path(exists=True))
@click.option('--vmd', default='vmd')
@click.option('--port', default=None)
def main(wav, vmd, port):
    vmd = VMDStream(port, vmd)
    sel = ''
    print('----------------------------------------------------------------')
    for i, query in enumerate(transcribe_wav_file(wav)):
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
def text(text):
    print('----------------------------------------------------------------')
    query = ' '.join(text)
    print(f'Text: "{query}"')
    result = run_gpt_search(query)
    print(f'Type: {result["type"]}')
    print(f'Command: {result["data"]}')
    print('----------------------------------------------------------------')
