import os
import wave

def verify_wav_file(file_path):
    try:
        with wave.open(file_path, 'rb') as wav_file:
            # If we can open it as a WAV file, it's valid
            return True
    except:
        return False

def verify_dataset(dataset_path):
    total_files = 0
    valid_wav_files = 0

    for emotion in ['anger', 'happy', 'neutral', 'sadness']:
        emotion_dir = os.path.join(dataset_path, emotion)
        if not os.path.exists(emotion_dir):
            print(f"Warning: Emotion directory not found: {emotion_dir}")
            continue

        for file in os.listdir(emotion_dir):
            if file.endswith('.wav'):
                total_files += 1
                file_path = os.path.join(emotion_dir, file)
                if verify_wav_file(file_path):
                    valid_wav_files += 1

    print(f"Total files: {total_files}")
    print(f"Valid WAV files: {valid_wav_files}")

    if valid_wav_files == total_files:
        print("All files are valid WAV files. You can proceed with your training script.")
    else:
        print(f"Warning: {total_files - valid_wav_files} files are not valid WAV files.")
        print("You may need to re-run 'git lfs pull' or check your Git LFS setup.")

if __name__ == "__main__":
    dataset_path = "Dataset"  # Adjust this if your dataset is in a different location
    verify_dataset(dataset_path)