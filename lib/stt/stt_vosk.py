import sys
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel


SetLogLevel(-1)
def transcribe_stt_vosk(file_path: str, model_path: str):
    """Transcribes an audio file

    Args:
        file_path (str): path to audio-file
        model_path (str): path to the model to use
    """
    model_path = "lib/stt/model/vosk-model-de-0.21"
    with wave.open(file_path, "rb") as audio_file:
        sample_rate = audio_file.getframerate()
        num_channels = audio_file.getnchannels()
        if num_channels != 1:
            print("Error: Audio file must be mono.")
            sys.exit(1)

        model = Model(model_path)
        recognizer = KaldiRecognizer(model, sample_rate)

        data = audio_file.readframes(4000)

        while len(data) > 0:
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                print(result["text"])
            data = audio_file.readframes(4000)
        result = json.loads(recognizer.FinalResult())
        print(result["text"])


