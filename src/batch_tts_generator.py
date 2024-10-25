# batch_tts_generator.py
from utils import log_action
from tts_generator import TTSGenerator

def batch_generate_tts(lines):
    tts = TTSGenerator()

    generated_files = []  # This will store each file's info as a tuple

    for line in lines:
        audio_filename, metadata_filename = tts.generate_tts(line)
        generated_files.append((audio_filename, metadata_filename))  # Add to list

    return generated_files  # Return list of generated files for further use
