from pydub import AudioSegment
import soundfile as sf

FILE_NAME = "obama3"


def convert_to_PCM_16(file_path):
    # Convert wav file to PCM 16 for the modify_wav.py to read
    f = sf.SoundFile(file_path)
    sig, samplerate = sf.read(file_path)
    sf.write(file_path, sig, samplerate)


convert_to_PCM_16(f"./{FILE_NAME}.wav")


def convert_audio(input_path, output_path):
    # Load the audio file
    audio = AudioSegment.from_file(input_path, format="wav")

    # Convert to mono and 22050 Hz sample rate
    mono_audio = audio.set_channels(1)
    converted_audio = mono_audio.set_frame_rate(22050)

    # Export the converted file
    converted_audio.export(output_path, format="wav")


convert_audio(f"./{FILE_NAME}.wav", f"./{FILE_NAME}_converted.wav")
