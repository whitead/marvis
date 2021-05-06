from vmdmagic import *
import click


@click.command()
@click.argument('wav', type=click.Path(exists=True))
@click.option('--vmd', default='vmd')
@click.option('--port', default=None)
def main(wav, vmd, port):
    vmd = VMDStream(port, vmd)
    print('----------------------------------------------------------------')
    for i, query in enumerate(transcribe_wav_file(wav)):
        print(f'Text {i}: "{query}"')
        result = run_gpt_search(query)
        print(f'Type {i}: {result["type"]}')
        print(f'Command {i}: {result["data"]}')
        vmd.send(result['data'])
        print('----------------------------------------------------------------')
