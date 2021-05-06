from vmdmagic import *
import click


@click.command()
@click.argument('wav', type=click.Path(exists=True))
@click.option('--vmd', default='vmd')
def main(wav, vmd):
    vmd = get_vmd(vmd)
    print('----------------------------------------------------------------')
    for query in transcribe_wav_file(wav):
        print(f'Text: "{query}"')
        result = run_gpt_search(query)
        print(f'Type: {result["type"]}')
        print(f'Command: {result["data"]}')
        print('----------------------------------------------------------------')
