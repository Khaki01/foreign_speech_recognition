import converter
import script_vosk
import sys

def main():
    if len(sys.argv) == 1:  # if parameter wasn't specified
        print('Set filename as a parameter. For example:')
        print('>>> python script_vosk.py filename.wav')
        sys.exit()
    elif len(sys.argv) == 2:
        video_filename = sys.argv[1]

    # extract audio file in wav mono format from input video and save in audio/ folder
    converter.main(video_filename)

    # 
    audio_filename = video_filename.split('.')[0].split('/')[1]
    script_vosk.main(audio_filename)


if __name__ == "__main__":
    main()


    