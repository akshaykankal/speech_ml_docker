import os
import struct

def identify_file_format(file_path):
    """
    Attempt to identify the file format by reading the first few bytes.
    """
    with open(file_path, 'rb') as f:
        header = f.read(12)  # Read the first 12 bytes
    
    if header.startswith(b'RIFF') and header[8:12] == b'WAVE':
        return "WAV (RIFF)"
    elif header.startswith(b'FORM') and header[8:12] == b'AIFF':
        return "AIFF"
    elif header.startswith(b'fLaC'):
        return "FLAC"
    elif header.startswith(b'ID3') or header.startswith(b'\xFF\xFB'):
        return "MP3"
    elif header.startswith(b'OggS'):
        return "Ogg"
    else:
        # If we can't identify the format, return the hex representation of the header
        return f"Unknown: {header.hex()}"

def analyze_dataset(dataset_path):
    """
    Analyze the audio files in the dataset and report on their formats.
    """
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' does not exist.")
        return

    total_files = 0
    format_counts = {}

    for emotion in ['anger', 'happy', 'neutral', 'sadness']:
        emotion_dir = os.path.join(dataset_path, emotion)
        if not os.path.exists(emotion_dir):
            print(f"Warning: Emotion directory not found: {emotion_dir}")
            continue

        for file in os.listdir(emotion_dir):
            if file.endswith('.wav'):
                total_files += 1
                file_path = os.path.join(emotion_dir, file)
                file_format = identify_file_format(file_path)
                format_counts[file_format] = format_counts.get(file_format, 0) + 1

    print(f"\nDataset Analysis Report:")
    print(f"Total audio files found: {total_files}")
    print("\nFile format distribution:")
    for format, count in format_counts.items():
        print(f"{format}: {count} files")

    if 'Unknown' in format_counts:
        print("\nSample of files with unknown format:")
        unknown_count = 0
        for emotion in ['anger', 'happy', 'neutral', 'sadness']:
            emotion_dir = os.path.join(dataset_path, emotion)
            for file in os.listdir(emotion_dir):
                if file.endswith('.wav'):
                    file_path = os.path.join(emotion_dir, file)
                    file_format = identify_file_format(file_path)
                    if file_format.startswith("Unknown"):
                        print(f"{file_path}: {file_format}")
                        unknown_count += 1
                        if unknown_count >= 5:
                            break
            if unknown_count >= 5:
                break

if __name__ == "__main__":
    dataset_path = "Dataset"  # Adjust this if your dataset is in a different location
    analyze_dataset(dataset_path)