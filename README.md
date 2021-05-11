# marvis
**VMD Audio/Text control with natural language**

This repository is a proof of principle for performing Molecular Dynamics analysis, in this case with the program VMD, via natural language commands.

It contains code to generate VMD commands from natural language queries given as text commands. 
It also contains code to control VMD via audio commands contained in a .wav recording, and via a live speak-to-text interface.

Converting text queries into VMD commands requires an active OpenAI license that allows access to the GPT-3 model.
Live speak-to-text requies a google cloud speak-to-text license file.

## Installation
- Installation can be performed with the command `pip install -e .` inside the main directory. We recommend doing this inside of a virtual environment.
- Transcription of live audio requires the additional installation of the pyaudio package (in conda, this can be achieved by `conda install pyaudio`).

## Usage
After installation, the commands `marvis`, `marvis-text`, and `vmt` will be added to your path. 

To convert text commands to VMD commands, use the `vmt`, for example:

    $ vmt "rotate the protein around the z axis by 45 degrees"
    Text: "rotate the protein around the z axis by 45 degrees"
    > (VMD Command) rotate z by 45 1

To interface with VMD in live mode, use `marvis` or `marvis-text`. The `--vmd` flag can be used to specify the path to VMD, which by default is `vmd`. 

In the simplest case, simply type 

    $ marvis 

To run `marvis` on a Mac in "safe mode", one might do:

    $ marvis --vmd "/Applications/VMD\ 1.9.4a51-x86_64-Rev9.app/Contents/vmd/vmd_MACOSXX86_64" --safe_mode
