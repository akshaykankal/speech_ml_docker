import os

def inspect_file_content(file_path, lines_to_read=5):
    """
    Read and return the first few lines of a file.
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return ''.join(f.readline() for _ in range(lines_to_read))

def analyze_dataset(dataset_path):
    """
    Analyze the content of files in the dataset.
    """
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' does not exist.")
        return

    total_files = 0
    sample_contents = []

    for emotion in ['anger', 'happy', 'neutral', 'sadness']:
        emotion_dir = os.path.join(dataset_path, emotion)
        if not os.path.exists(emotion_dir):
            print(f"Warning: Emotion directory not found: {emotion_dir}")
            continue

        for file in os.listdir(emotion_dir):
            if file.endswith('.wav'):
                total_files += 1
                file_path = os.path.join(emotion_dir, file)
                content = inspect_file_content(file_path)
                if len(sample_contents) < 5:
                    sample_contents.append((file_path, content))

    print(f"\nDataset Analysis Report:")
    print(f"Total files found: {total_files}")
    print("\nSample file contents:")
    for file_path, content in sample_contents:
        print(f"\nFile: {file_path}")
        print(content)
        print("-" * 50)

if __name__ == "__main__":
    dataset_path = "Dataset"  # Adjust this if your dataset is in a different location
    analyze_dataset(dataset_path)