# PySTT.py
# from lib.util.config import config
import sys
import os
import glob
import importlib
import concurrent.futures

def main(audio_file_path):
    """Run Transcription

    Args:
        audio_file_path (str): Path to the audio file 
    """
    api_files = glob.glob('lib/stt/*.py')
    api_names = [os.path.splitext(os.path.basename(f))[0] for f in api_files]

    transcription_functions = []
    for api_name in api_names:
        module = importlib.import_module(f'lib.stt.{api_name}')
        transcription_functions.append(getattr(module, f'transcribe_{api_name}'))

    with concurrent.futures.ProcessPoolExecutor(max_workers=len(api_names)) as executor:
        futures = [executor.submit(transcription_function, audio_file_path, api_name)
                for transcription_function, api_name in zip(transcription_functions, api_names)]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                print(f'Transcription with {api_name} completed successfully!')
            except Exception as exc:
                print(f'Error transcribing with {api_name}: {exc}')
    print("diobe")
                
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Using example file (examples/german/test1.wav)')
        audio_file_path = "examples/german/test1.wav"
    else:
        audio_file_path = sys.argv[1]
    main(audio_file_path)
