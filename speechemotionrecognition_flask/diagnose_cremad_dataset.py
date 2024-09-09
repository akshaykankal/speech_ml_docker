import os
import wave

def check_wav_file(file_path):
    """
    Attempt to read a WAV file and return file information.
    """
    file_size = os.path.getsize(file_path)
    info = f"File size: {file_size} bytes\n"

    try:
        with wave.open(file_path, 'rb') as wf:
            info += f"Channels: {wf.getnchannels()}\n"
            info += f"Sample width: {wf.getsampwidth()} bytes\n"
            info += f"Frame rate: {wf.getframerate()} Hz\n"
            info += f"Number of frames: {wf.getnframes()}\n"
            info += f"Compression type: {wf.getcomptype()}\n"
            info += f"Compression name: {wf.getcompname()}\n"
        return info, True
    except Exception as e:
        return f"Error: {str(e)}", False

def diagnose_dataset(dataset_path):
    """
    Check the structure of the dataset and attempt to read each audio file.
    """
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' does not exist.")
        return

    total_files = 0
    readable_files = 0
    problematic_files = []

    for emotion in ['anger', 'happy', 'neutral', 'sadness']:
        emotion_dir = os.path.join(dataset_path, emotion)
        if not os.path.exists(emotion_dir):
            print(f"Warning: Emotion directory not found: {emotion_dir}")
            continue

        for file in os.listdir(emotion_dir):
            if file.endswith('.wav'):
                total_files += 1
                file_path = os.path.join(emotion_dir, file)
                file_info, is_readable = check_wav_file(file_path)
                
                if is_readable:
                    readable_files += 1
                else:
                    problematic_files.append((file_path, file_info))

    print(f"\nDataset Diagnosis Report:")
    print(f"Total audio files found: {total_files}")
    print(f"Successfully readable files: {readable_files}")
    print(f"Problematic files: {len(problematic_files)}")

    if problematic_files:
        print("\nDetailed information for problematic files:")
        for file_path, info in problematic_files:
            print(f"\n{file_path}:")
            print(info)

    if readable_files == 0:
        print("\nWarning: No audio files could be read successfully. Please check your audio file formats and ensure they are not corrupted.")
    else:
        print("\nSample information for a readable file:")
        sample_file = next((file for file in os.listdir(os.path.join(dataset_path, 'anger')) if file.endswith('.wav')), None)
        if sample_file:
            sample_path = os.path.join(dataset_path, 'anger', sample_file)
            sample_info, _ = check_wav_file(sample_path)
            print(f"\n{sample_path}:")
            print(sample_info)

if __name__ == "__main__":
    dataset_path = "Dataset"  # Adjust this if your dataset is in a different location
    diagnose_dataset(dataset_path)