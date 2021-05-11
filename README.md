# marvis
**VMD Audio/Text control with natural language**

This repository is a proof of principle for performing Molecular Dynamics analysis, in this case with the program VMD, via natural language commands.

It contains code to generate VMD commands from natural language queries given as text commands. 
It also contains code to control VMD via audio commands contained in a .wav recording, and via a live speak-to-text interface.

Converting text queries into VMD commands requires an OpenAI API key that allows access to the GPT-3 model.
Live speak-to-text requies [a google cloud speech-to-text authentication](https://googleapis.dev/python/speech/latest/index.html#quick-start)

## Example
Here is an example in text mode


https://user-images.githubusercontent.com/908389/117870697-71c5d480-b26a-11eb-81a3-60e4f7ed06d3.mp4



## Installation
- Installation can be performed with the command `pip install -e .` inside the main directory. We recommend doing this inside of a virtual environment.
- Transcription of live audio requires the additional installation of the pyaudio package (in conda, this can be achieved by `conda install pyaudio`).

Use of the two APIs above requires setting environment variables. In `BASH`, one would do

        export GOOGLE_APPLICATION_CREDENTIALS=path_to_google_api_license_file.json
        export OPENAI_API_KEY=sh-....

## Usage
After installation, the commands `marvis`, `marvis-text` will be added to your path. 

To convert text commands to VMD commands, use the `marvis-text`, for example:

    $ marvis-text --mock "rotate the protein around the z axis by 45 degrees"
    Text: "rotate the protein around the z axis by 45 degrees"
    > (VMD Command) rotate z by 45 1

To interface with VMD in live mode, use `marvis` or `marvis-text`. The `--vmd` flag can be used to specify the path to VMD, which by default is `vmd`. 

In the simplest case, simply type 

    $ marvis 

To run `marvis` on a Mac in "safe mode", one might do:

    $ marvis --vmd "/Applications/VMD\ 1.9.4a51-x86_64-Rev9.app/Contents/vmd/vmd_MACOSXX86_64" --safe_mode
