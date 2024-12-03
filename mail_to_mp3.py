from pydub import AudioSegment
import pyttsx3
import json
import os
from datetime import datetime
import time


def mail_to_mp3(mail):
    # Initialize Engine
    engine = pyttsx3.init()

    # Set properties (optional)
    engine.setProperty('rate', 150)  # Speed
    engine.setProperty('volume', 0.9)  # Volume

    # Get HeHeMail bodies
    # with open("hehemail.json", "r") as f:
        # mail = json.load(f)
    print()
    print(mail)

    today = datetime.today().strftime('%Y_%m_%d')
    new_fold = f"./output_hehemails/{today}"
    if not os.path.exists(new_fold):
        os.makedirs(new_fold)

    # Text you want to convert to audio
    for i, m in enumerate(mail):
        # print(m)
        key = f"Email {i}"
        mail_str = f"New Mail: {m[key]}"

        # Save the speech to a .wav file
        new_file = f'{new_fold}/hehemail_email_{i}.wav'

        # Run the speech engine to process the file
        engine.runAndWait()
        engine.save_to_file(mail_str, new_file)

        while True:
            try:
                add_background_music("./background.mp3", new_file)
                break
            except FileNotFoundError:
                continue

            

# Step 2: Add Background Music
def add_background_music(tts_file, music_file, delay=10, music_volume=-10):
    # Load the TTS audio and background music
    tts_audio = AudioSegment.from_file(tts_file)
    music = AudioSegment.from_file(music_file)

    # Adjust background music volume
    music = music - abs(music_volume)  # Reduce music volume (default -10 dB)

    # Add delay (silence) to the TTS audio
    silence = AudioSegment.silent(duration=delay * 1000)  # delay in milliseconds
    tts_audio = silence + tts_audio

    # Loop the music if it's shorter than the TTS audio
    if len(music) < len(tts_audio):
        music = music * (len(tts_audio) // len(music) + 1)

    # Trim the music to the same length as the TTS audio
    music = music[:len(tts_audio)]

    # Combine TTS audio and background music
    combined = tts_audio.overlay(music)

    # Save the combined audio to a file
    combined.export(tts_file, format="mp3")
    print(f"Combined audio saved to: {tts_file}")

if __name__ == "__main__":
    mail_to_mp3()
