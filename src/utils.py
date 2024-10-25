# utils.py
import datetime
import os
import yaml
import random
import string

def load_config():
    with open('config/settings.yaml', 'r') as file:
        return yaml.safe_load(file)

def log_action(description):
    # Define the log directory and file
    log_directory = 'logs'
    log_file_path = os.path.join(log_directory, 'logs.txt')

    # Create the logs directory if it doesn't exist
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    # Create the logs.txt file if it doesn't exist
    if not os.path.exists(log_file_path):
        open(log_file_path, 'a').close()

    # Prepare the log entry
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    script_name = os.path.basename(__file__)
    log_entry = f"{timestamp} - {script_name}: {description}\n"

    # Write the log entry to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry)

def generate_base_filename(text):
    # Split into words and take first 5
    words = text.split()[:5]

    # Clean each word individually, keeping only alphanumeric chars
    cleaned_words = []
    for word in words:
        # Keep only alphanumeric chars in each word
        cleaned_word = ''.join(c for c in word if c.isalnum())
        if cleaned_word:  # Only add non-empty words
            cleaned_words.append(cleaned_word.lower())

    # Join words with underscores
    base = '_'.join(cleaned_words)

    # Generate 8 random alphanumeric characters
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    # Combine everything, ensuring total length doesn't exceed 50 chars
    return f"{base[:40]}_{random_suffix}"

def generate_filename(base_name, extension):
    return f"{base_name}.{extension}"
