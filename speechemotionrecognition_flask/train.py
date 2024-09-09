import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, LSTM, Conv1D, MaxPooling1D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import librosa
import soundfile as sf
import warnings
from tensorflow.keras.regularizers import l2
import joblib

# Suppress warnings
warnings.filterwarnings("ignore")

# ... [Download and organize functions remain the same] ...

def extract_features(file_path, mfcc=True, chroma=True, mel=True):
    try:
        X, sample_rate = sf.read(file_path)
    except Exception as e:
        try:
            X, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
        except Exception as e:
            print(f"Error reading {file_path}: {str(e)}")
            return None

    if mfcc:
        mfccs = librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40)
        mfccs_processed = np.mean(mfccs.T, axis=0)
    if chroma:
        chroma = librosa.feature.chroma_stft(y=X, sr=sample_rate)
        chroma_processed = np.mean(chroma.T, axis=0)
    if mel:
        mel = librosa.feature.melspectrogram(y=X, sr=sample_rate)
        mel_processed = np.mean(mel.T, axis=0)
    
    features = np.concatenate((mfccs_processed, chroma_processed, mel_processed))
    
    return features

def load_data(dataset_path):
    X, y = [], []
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.wav'):
                file_path = os.path.join(root, file)
                emotion = os.path.basename(root)
                features = extract_features(file_path)
                if features is not None:
                    X.append(features)
                    y.append(emotion)
    return np.array(X), np.array(y)

def create_model(input_shape, num_classes):
    model = Sequential([
        Conv1D(64, kernel_size=3, activation='relu', input_shape=(input_shape, 1), kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Conv1D(128, kernel_size=3, activation='relu', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Conv1D(256, kernel_size=3, activation='relu', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        LSTM(128, return_sequences=True),
        Dropout(0.5),
        LSTM(64),
        Dropout(0.5),
        Dense(64, activation='relu', kernel_regularizer=l2(0.01)),
        BatchNormalization(),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    return model

def train_model():
    # Load data
    X, y = load_data("Dataset")

    # Print dataset statistics
    print(f"Total number of samples: {len(X)}")
    print(f"Number of features: {X.shape[1]}")
    print(f"Emotion distribution: {np.unique(y, return_counts=True)}")

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)

    # Normalize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Reshape input for CNN-LSTM
    X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], X_train_scaled.shape[1], 1))
    X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], X_test_scaled.shape[1], 1))

    # Convert to categorical
    num_classes = len(np.unique(y_encoded))
    y_train_cat = to_categorical(y_train, num_classes=num_classes)
    y_test_cat = to_categorical(y_test, num_classes=num_classes)

    # Create and compile the model
    model = create_model(X_train_reshaped.shape[1], num_classes)
    optimizer = Adam(learning_rate=0.001)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

    # Define callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6)
    model_checkpoint = ModelCheckpoint('best_model.keras', monitor='val_accuracy', save_best_only=True, mode='max')

    # Train the model
    history = model.fit(
        X_train_reshaped, y_train_cat,
        validation_data=(X_test_reshaped, y_test_cat),
        epochs=200,
        batch_size=32,
        callbacks=[early_stopping, lr_reducer, model_checkpoint]
    )

    # Load the best model
    model.load_weights('best_model.keras')

    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(X_test_reshaped, y_test_cat, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")

    # Save the model and preprocessing objects
    model.save("improved_emotion_recognition_model.keras")
    joblib.dump(scaler, 'feature_scaler.joblib')
    joblib.dump(label_encoder, 'label_encoder.joblib')

    print("Model and preprocessing objects saved.")

# Main execution
if __name__ == "__main__":
    train_model()