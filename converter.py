#import moviepy.editor as mp
#my_clip = mp.VideoFileClip(r"testvideo.mov")
#my_clip.audio.write_audiofile(r"result.wav")

import subprocess
import sys
import os


def main(video_filename):
    if not os.path.exists(video_filename):
        print(f"File '{video_filename}' doesn't exist")
        sys.exit()
    audio_filename = video_filename.split('.')[0].split('/')[1]
    command = 'ffmpeg -i {} -ac 1 -acodec pcm_s16le audio/{}.wav'.format(video_filename, audio_filename)
    subprocess.call(command, shell=True)

#if __name__ == "__main__":
#    main()