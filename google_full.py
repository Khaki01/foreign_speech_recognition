import sys

import moviepy.editor as mp
#import speech_recognition as sr
#from google.cloud import speech
import os
import time
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
#from punctuator import Punctuator
#import nemo
from nemo.collections.nlp.models import PunctuationCapitalizationModel

# install with `pip install vosk`

SetLogLevel(0)

def converter(video_filename):
    clip = mp.VideoFileClip(video_filename)
    audio_filename = video_filename.split('.')[0].split('/')[1]
    audio_filename = 'audio/' + audio_filename + '.wav'
    clip.audio.write_audiofile(audio_filename, codec='pcm_s16le', ffmpeg_params=["-ac", "1"])
    return audio_filename

def recongize_vosk(audio_filename, text_filename, model_path='model') -> None:
    '''
    Recognize audio from 'audio_filename' with vosk model and 
    write text on the screen and into 'text_filename' file.

    Parameters:
        audio_filename (str): name of the audio file to recognize
        text_filename (str): name of the text file to write recognized text
        model_path (str): Path to vosk model. Default is 'model'.

    Returns:
        None
    '''

    print(f"Reading your file '{audio_filename}'...")
    wf = wave.open(audio_filename, "rb")
    print(f"'{audio_filename}' file was successfully read")

    # check if audio if mono wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit()

    print(f"Reading your vosk model '{model_path}'...")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    print(f"'{model_path}' model was successfully read")

    print('Start converting to text. It may take some time...')
    start_time = time.time()

    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # forming a final string from the words
    text = ''
    for r in results:
        text += r['text'] + ' '

    time_elapsed = time.strftime(
        '%H:%M:%S', time.gmtime(time.time() - start_time))
    print(f'Done! Elapsed time = {time_elapsed}\n')

    print("\tVosk thinks you said:\n")
    print(text)

    print(f"\nSaving text to '{text_filename}'...")
    with open(text_filename, "w") as text_file:
        text_file.write(text)
    print(f"Text successfully saved")

    #p = Punctuator('model.pcl')
    #print(p.punctuate(text))

    #PunctuationCapitalizationModel.list_available_models()
    model = PunctuationCapitalizationModel.from_pretrained("punctuation_en_bert")
    output = model.add_punctuation_capitalization([text])

    print(output)

#def punctuate(text_filename):

    

def main():
    if len(sys.argv) == 1:  # if parameter wasn't specified
        print('Set filename as a parameter. For example:')
        print('>>> python script_vosk.py filename.wav')
        sys.exit()
    elif len(sys.argv) == 2:
        video_filename = sys.argv[1]

    # extract audio file in wav mono format from input video and save in audio/ folder
    audio_filename = converter(video_filename)
    text_filename = audio_filename[:-3] + 'txt'
    # 
    recongize_vosk(audio_filename, text_filename)

    #punctuate(text_filename)



if __name__ == "__main__":
    main()