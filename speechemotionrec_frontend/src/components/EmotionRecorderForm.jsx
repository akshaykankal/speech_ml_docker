import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { Mic, Upload, Play, RotateCcw, Send, RefreshCw } from 'lucide-react';

const CustomAlert = ({ message }) => (
  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
    <strong className="font-bold">Error: </strong>
    <span className="block sm:inline">{message}</span>
  </div>
);

const EmotionRecorderForm = () => {
  const [selectedEmotion, setSelectedEmotion] = useState('happy');
  const [audioBlob, setAudioBlob] = useState(null);
  const [recording, setRecording] = useState(false);
  const [remainingTime, setRemainingTime] = useState(0);
  const [emotion, setEmotion] = useState({ predicted_emotion: '', real_emotion: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);

  const emotions = ['happy', 'anger', 'sadness', 'neutral'];
  

  const handleEmotionChange = (emotion) => {
    setSelectedEmotion(emotion);
  };

  const handleAudioRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      const audioChunks = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        setAudioBlob(audioBlob);
        setRecording(false);
      };

      setRecording(true);
      setRemainingTime(5);
      mediaRecorder.start();

      const timer = setInterval(() => {
        setRemainingTime((prevTime) => {
          if (prevTime <= 1) {
            clearInterval(timer);
            mediaRecorder.stop();
            stream.getTracks().forEach(track => track.stop());
            return 0;
          }
          return prevTime - 1;
        });
      }, 1000);
    } catch (err) {
      console.error('Error accessing microphone:', err);
      setError(`Error accessing microphone: ${err.message}`);
    }
  };

  const handleReplay = () => {
    const audioURL = URL.createObjectURL(audioBlob);
    const audio = new Audio(audioURL);
    audio.play();
  };

  const handleRestartRecording = () => {
    setAudioBlob(null);
  };

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'audio/wav') {
      setUploadedFile(file);
    } else {
      setError('Please upload a .wav file.');
      setUploadedFile(null);
    }
  };

  const handleReset = () => {
    setSelectedEmotion('happy');
    setAudioBlob(null);
    setRecording(false);
    setRemainingTime(0);
    setEmotion({ predicted_emotion: '', real_emotion: '' });
    setLoading(false);
    setError('');
    setUploadedFile(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError('');
    try {
      const formData = new FormData();
      formData.append('emotion', selectedEmotion);
      if (audioBlob) {
        formData.append('file', audioBlob);
      } else if (uploadedFile) {
        formData.append('file', uploadedFile);
      } else {
        throw new Error('No audio file selected');
      }

      
      const response = await axios.post('http://localhost:10000/predict', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      if (response.data.success) {
        setEmotion({
          predicted_emotion: response.data.predicted_emotion,
          real_emotion: response.data.real_emotion
        });
      } else {
        throw new Error(response.data.error);
      }
    } catch (error) {
      setError(error.message || 'An error occurred during submission.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col md:flex-row w-full  bg-gradient-to-br from-yellow-100 to-red-100 p-4 space-y-4 md:space-y-0 md:space-x-4">
      <div className="flex flex-col w-full md:w-1/3 bg-white rounded-lg shadow-lg p-6 space-y-6">
        <h2 className="text-2xl font-bold text-center text-gray-800">VaaniVibes</h2>
        <p className="text-sm text-center text-gray-600">Indian Multi-Lingual Speech Emotion Recognition System</p>

        <div className="flex flex-wrap justify-center gap-2">
          {emotions.map((emotion) => (
            <motion.button
              key={emotion}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className={`px-4 py-2 rounded-full ${
                selectedEmotion === emotion
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
              onClick={() => handleEmotionChange(emotion)}
            >
              {emotion.charAt(0).toUpperCase() + emotion.slice(1)}
            </motion.button>
          ))}
        </div>

        {!audioBlob && !uploadedFile && (
          <div className="flex flex-col items-center space-y-4">
            <input
              type="file"
              accept=".wav"
              onChange={handleFileChange}
              className="hidden"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="flex items-center justify-center w-full px-4 py-2 bg-green-500 text-white rounded-lg cursor-pointer hover:bg-green-600 transition-colors"
            >
              <Upload size={20} className="mr-2" />
              Upload Audio
            </label>
            <p className="text-xs text-gray-500">or</p>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="flex items-center justify-center w-full px-4 py-2 bg-blue-500 text-white rounded-lg"
              onClick={handleAudioRecording}
              disabled={recording}
            >
              <Mic size={20} className="mr-2" />
              {recording ? `Recording... ${remainingTime}s` : 'Record Audio'}
            </motion.button>
          </div>
        )}

        {(audioBlob || uploadedFile) && (
          <div className="flex flex-col items-center space-y-4">
            <audio controls className="w-full">
              <source
                src={audioBlob ? URL.createObjectURL(audioBlob) : URL.createObjectURL(uploadedFile)}
                type="audio/wav"
              />
              Your browser does not support the audio element.
            </audio>
            <div className="flex justify-center space-x-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-4 py-2 bg-gray-500 text-white rounded-lg"
                onClick={handleReplay}
              >
                <Play size={20} />
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-4 py-2 bg-yellow-500 text-white rounded-lg"
                onClick={handleRestartRecording}
              >
                <RotateCcw size={20} />
              </motion.button>
            </div>
          </div>
        )}

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-full px-4 py-2 bg-indigo-500 text-white rounded-lg"
          onClick={handleSubmit}
          disabled={!audioBlob && !uploadedFile}
        >
          <Send size={20} className="inline mr-2" />
          Analyze Emotion
        </motion.button>

        {error && <CustomAlert message={error} />}
      </div>

      <div className="flex flex-col w-full md:w-2/3 bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">Emotion Analysis Result</h2>
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <RefreshCw size={40} className="animate-spin text-blue-500" />
          </div>
        ) : (
          <div className="flex flex-col md:flex-row justify-around items-center h-64">
            <EmotionDisplay title="Real Emotion" emotion={emotion.real_emotion} />
            <EmotionDisplay title="Predicted Emotion" emotion={emotion.predicted_emotion} />
          </div>
        )}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="mt-6 px-4 py-2 bg-red-500 text-white rounded-lg self-center"
          onClick={handleReset}
        >
          Reset
        </motion.button>
      </div>
    </div>
  );
};

const emotionIcons = {
  happy: '😃',
  anger: '😡',
  sadness: '😔',
  neutral: '😐',
};
const EmotionDisplay = ({ title, emotion }) => (
  <div className="flex flex-col items-center">
    <h3 className="text-xl font-semibold mb-2">{title}</h3>
    <div className="text-6xl mb-2">{emotion ? emotionIcons[emotion] : '❓'}</div>
    <p className="text-lg capitalize">{emotion || 'Unknown'}</p>
  </div>
);

export default EmotionRecorderForm;