#import moviepy.editor as mp
#my_clip = mp.VideoFileClip(r"testvideo.mov")
#my_clip.audio.write_audiofile(r"result.wav")

import subprocess
import sys
import os


def main():
    if len(sys.argv) == 1:  # if parameter wasn't specified
        print('Set filename as a parameter. For example:')
        print('>>> python script_vosk.py filename.wav')
        sys.exit()
    elif len(sys.argv) == 2:
        video_filename = sys.argv[1]

    if not os.path.exists(video_filename):
        print(f"File '{video_filename}' doesn't exist")
        sys.exit()
    audio_filename = video_filename.split('.')[0]
    print('ffmpeg -i {} -ac 1 -acodec pcm_s16le {}.wav'.format(video_filename, audio_filename))
    command = 'ffmpeg -i {} -ac 1 -acodec pcm_s16le {}.wav'.format(video_filename, audio_filename)
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()