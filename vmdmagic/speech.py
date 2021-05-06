from google.cloud import speech
import io
import time


def transcribe_wav_file(speech_file):
    '''Transcribe the given audio file.'''

    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US',
        audio_channel_count=2,
        enable_separate_recognition_per_channel=False,
        max_alternatives=1,
        enable_word_time_offsets=True
    )

    response = client.recognize(config=config, audio=audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    last_word = None
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        # wait length between results
        first_word = result.alternatives[0].words[0].start_time
        if last_word is not None:
            td = first_word - last_word
            time.sleep(td.seconds)
        last_word = result.alternatives[0].words[-1].end_time
        yield result.alternatives[0].transcript
