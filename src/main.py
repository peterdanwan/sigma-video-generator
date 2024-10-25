# main.py
from utils import load_config, log_action
from text_preparation import read_and_format_input_text, write_to_input_file
from batch_tts_generator import batch_generate_tts
from tts_bgm_mixer import TTSBGMMixer
import sys
import os

def test_tts_bgm_mixer():
    log_action(" ")
    log_action("Start new run of main.py (testing tts bgm mixer)")
    try:
        # Load config
        config = load_config()

        # Generate tts audio and metadata for each line in the input
        generated_tts_filenames = []  # This will store each file's info as a tuple

        def return_already_generated_tts_file():
            return "the_wiser_you_are_the_b6nyrwfl.mp3", "the_wiser_you_are_the_b6nyrwfl.json"

        audio_filename, metadata_filename = return_already_generated_tts_file()
        generated_tts_filenames.append((audio_filename, metadata_filename))  # Add to list
        log_action("return_already_generated_tts_file() completed successfully")

        # Now generated_tts_filenames contains all filenames for later use

        # Initialize the mixer
        mixer = TTSBGMMixer(config)

        # Mix each TTS file with the background music
        mixed_outputs = []
        for i, (audio_file, metadata_file) in enumerate(generated_tts_filenames):
            audio_file_path = os.path.join(config["directories"]["generated_tts_dir"], audio_file)
            metadata_file_path = os.path.join(config["directories"]["generated_tts_dir"], metadata_file)
            mixed_audio_path = os.path.join(config["directories"]["mixed_audio_dir"])

            # Ensure the directory exists
            os.makedirs(os.path.dirname(mixed_audio_path), exist_ok=True)

            try:
                mixed_file = mixer.mix_tts_with_bgm(audio_file_path, metadata_file_path, mixed_audio_path)
                mixed_outputs.append(mixed_file)
                log_action(f"Successfully mixed TTS with BGM for file {i+1}")
            except Exception as e:
                log_action(f"Error mixing file {i+1}: {str(e)}")
                continue

        log_action(f"Successfully mixed {len(mixed_outputs)} files with background music")

    except Exception as e:
        log_action(f"Error in main execution: {str(e)}")
        sys.exit(1)

def main():
    log_action(" ")
    log_action("Start new run of main.py")
    try:
        # Load config
        config = load_config()

        # Process the text input file
        text_input_file = config["text_input_file"]
        lines = read_and_format_input_text(text_input_file)
        log_action("Read input from input/input.txt")

        # Generate tts audio and metadata for each line in the input
        generated_tts_filenames = batch_generate_tts(lines)
        log_action("Batch TTS generation completed successfully")

        # Now generated_tts_filenames contains all filenames for later use

        # Initialize the mixer
        mixer = TTSBGMMixer(config)

        # Mix each TTS file with the background music
        mixed_outputs = []
        for i, (audio_file, metadata_file) in enumerate(generated_tts_filenames):
            audio_file_path = os.path.join(config["directories"]["generated_tts_dir"], audio_file)
            metadata_file_path = os.path.join(config["directories"]["generated_tts_dir"], metadata_file)
            mixed_audio_path = os.path.join(config["directories"]["mixed_audio_dir"])

            # Ensure the directory exists
            os.makedirs(os.path.dirname(mixed_audio_path), exist_ok=True)

            try:
                mixed_file = mixer.mix_tts_with_bgm(audio_file_path, metadata_file_path, mixed_audio_path)
                mixed_outputs.append(mixed_file)
                log_action(f"Successfully mixed TTS with BGM for file {i+1}")
            except Exception as e:
                log_action(f"Error mixing file {i+1}: {str(e)}")
                continue

        log_action(f"Successfully mixed {len(mixed_outputs)} files with background music")

    except Exception as e:
        log_action(f"Error in main execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
