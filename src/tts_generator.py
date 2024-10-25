# tts_generator.py
import os
import json
import base64
import requests
from dotenv import load_dotenv
from utils import log_action, load_config, generate_filename, generate_base_filename

class TTSGenerator:
    def __init__(self):
        load_dotenv()
        self.config = load_config()
        self.voice_id = "nPczCjzI2devNBz1zQrb"  # Brian
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}/with-timestamps"
        self.headers = {
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    def add_word_timings(self, alignment):
        """
        Add word-level timing information to an alignment dictionary that contains character-level timings.

        Args:
        alignment (dict): Dictionary containing 'characters', 'character_start_times_seconds',
        and 'character_end_times_seconds'

        Returns:
        dict: Updated alignment dictionary with added word-level timing information
        """
        chars = alignment['characters']
        char_starts = alignment['character_start_times_seconds']
        char_ends = alignment['character_end_times_seconds']

        words = []
        word_starts = []
        word_ends = []

        current_word = []
        word_start = 0.0  # First word always starts at 0.0

        for i, char in enumerate(chars):
            if char == " ":
                if current_word:  # Finish current word
                    words.append("".join(current_word))
                    word_starts.append(word_start)
                    word_ends.append(char_starts[i])
                    # Next word will start at the end of the space
                    word_start = char_ends[i]
                    current_word = []
            else:
                current_word.append(char)

        # Handle the last word if it exists
        if current_word:
            words.append("".join(current_word))
            word_starts.append(word_start)
            word_ends.append(char_ends[-1])

        # Add the new information to the alignment dictionary
        alignment['words'] = words
        alignment['word_start_times_seconds'] = word_starts
        alignment['word_end_times_seconds'] = word_ends

        return alignment

    def generate_tts(self, text):
        try:
            log_action(f"Generating TTS for text: {text[:50]}...")

            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.2,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(self.url, json=data, headers=self.headers)

            if response.status_code != 200:
                error_message = f"Error from ElevenLabs API: {response.status_code} - {response.text}"
                log_action(error_message)
                raise Exception(error_message)

            response_dict = json.loads(response.content.decode("utf-8"))
            audio_bytes = base64.b64decode(response_dict["audio_base64"])

            # Generate filenames and paths
            tts_dir = self.config['directories']['generated_tts_dir']
            os.makedirs(tts_dir, exist_ok=True)

            base_name = generate_base_filename(text)
            audio_filename = generate_filename(base_name, "mp3")
            metadata_filename = generate_filename(base_name, "json")

            output_audio_path = os.path.join(tts_dir, audio_filename)
            output_metadata_path = os.path.join(tts_dir, metadata_filename)

            # Write audio file
            with open(output_audio_path, 'wb') as f:
                f.write(audio_bytes)
            log_action(f"Audio file saved: {audio_filename}")

            # Write metadata file
            metadata = {
                "audio_filename": audio_filename,
                "full_text": text,
                "alignment": self.add_word_timings(response_dict['alignment'])
            }
            with open(output_metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            log_action(f"Metadata file saved: {metadata_filename}")

            return audio_filename, metadata_filename

        except Exception as e:
            log_action(f"Error in TTS generation: {str(e)}")
            raise
