# text_preparation.py
import os
import random
from utils import log_action, load_config

config = load_config()
text_input_file = config["text_input_file"]

def write_to_input_file(text, input_file=text_input_file):
    os.makedirs(os.path.dirname(input_file), exist_ok=True)
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write(text)
    log_action(f"Text written to input file: {input_file}")

def read_and_format_input_text(input_file=text_input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        non_empty_lines = [line.strip() for line in lines if line.strip()]

        if len(non_empty_lines) == 0:
            log_action("Error: Input file is empty or contains only empty lines")
            raise ValueError("Input file is empty or contains only empty lines")

        log_action(f"Found {len(non_empty_lines)} non-empty lines to process")
        return non_empty_lines

    except FileNotFoundError:
        log_action(f"Error: Input file not found at {input_file}")
        raise
