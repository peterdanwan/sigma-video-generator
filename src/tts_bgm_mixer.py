# tts_bgm_mixer.py
import json
from pydub import AudioSegment
from utils import log_action

class TTSBGMMixer:
    def __init__(self, config):
        self.config = config

    def load_json(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: The file '{file_path}' was not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{file_path}' contains invalid JSON.")
        except Exception as e:
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def timestretch_audio(self, audio, target_length):
        # TODO: Implement this function to timestretch the audio to the target length
        # For now, we'll just return the original audio
        return audio

    def get_tts_duration(self, tts_data):
        characters = tts_data['alignment']['characters']
        end_times = tts_data['alignment']['character_end_times_seconds']

        # Start from the end and find the last alphanumeric character
        for i in range(len(characters) - 1, -1, -1):
            if characters[i].isalnum():
                return end_times[i]

        # Die if no alphanumeric characters are found
        log_action("Something's gone horribly wrong when trying to get_tts_duration. No characters found.")
        raise ValueError("NO ALPHANUMERIC CHARACTER FOUND when trying to get_tts_duration! SOMETHING WENT HORRIBLY WRONG!")

    def mix_tts_with_bgm(self, tts_audio_path, tts_json_path, output_path):
        """Mix a single TTS file with background music, aligning to the drop"""
        # Load BGM paths from config
        bgm_audio_path = self.config["bgm_audio_path"]
        bgm_json_path = self.config["bgm_json_path"]

        # Load JSON data
        tts_data = self.load_json(tts_json_path)
        bgm_data = self.load_json(bgm_json_path)

        # Load audio files with volume adjustments
        tts_audio = AudioSegment.from_mp3(tts_audio_path) + self.config.get("tts_volume_adjustment", 6)
        bgm_audio = AudioSegment.from_mp3(bgm_audio_path) + self.config.get("bgm_volume_adjustment", -6)

        # Get TTS duration and BGM drop timestamp
        tts_duration = self.get_tts_duration(tts_data)
        drop_timestamp = bgm_data['drop_timestamp_in_seconds'] - bgm_data['pre_drop_duration']

        # Check if TTS duration is longer than drop timestamp
        if tts_duration > drop_timestamp:
            if not self.config.get("allow_timestretch", False):
                raise ValueError(f"Music too short ({drop_timestamp}s), or text too long ({tts_duration}s).")
            tts_audio = self.timestretch_audio(tts_audio, drop_timestamp)
            tts_duration = drop_timestamp

        # Calculate the start time for BGM and mix
        bgm_start_time = drop_timestamp - tts_duration
        trimmed_bgm = bgm_audio[bgm_start_time * 1000:]
        mixed_audio = trimmed_bgm.overlay(tts_audio)

        # Export the final mix
        mixed_audio.export(output_path, format="mp3")
        log_action(f"Mixed audio saved to {output_path}")

        return output_path
