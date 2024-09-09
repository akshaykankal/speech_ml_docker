import React from 'react';

const ProjectInfo = () => {
  return (
    <div className="bg-white w-full flex flex-col justify-center items-center p-10 space-y-6">
      <h1 className="text-4xl font-bold text-center text-gray-800">
        VaaniVibes: Indian Multi-Lingual Speech Emotion Recognition System
      </h1>
      
      <section className="w-full max-w-3xl">
        <h2 className="text-2xl font-semibold mb-4">Introduction</h2>
        <p className="text-gray-700 mb-4">
          The Speech Emotion Recognition System is designed to analyse speech input and determine the emotional content of the speech. This system is intended for researchers, developers, and organizations interested in analysing emotions in spoken language.
        </p>
        <p className="text-gray-700">
          Speech Emotion Recognition system can assist healthcare professionals in diagnosing and monitoring mental health conditions by analyzing patient's emotional states during conversations in their native languages. It can aid in early detection, personalized treatment, and remote monitoring.
        </p>
      </section>
      
      <section className="w-full max-w-3xl">
        <h2 className="text-2xl font-semibold mb-4">Research Paper</h2>
        <p className="text-gray-700 font-semibold">
          Optimal trained ensemble of classification model for speech emotion recognition: Considering cross‐lingual and multi‐lingual scenarios
        </p>
        <p className="text-gray-600 mt-2">
          Authors: Rupali Ramdas Kawade · Sonal K. Jagtap
        </p>
      </section>
      
      <section className="w-full max-w-3xl">
        <h2 className="text-2xl font-semibold mb-4">Contact Us</h2>
        <div className="space-y-2">
          <p className="text-gray-700"><strong>Rupali Kawade</strong></p>
          <p className="text-gray-600">Department of E&TC Engineering, G H Raisoni College of Engineering and Management, Wagholi, Pune 412207</p>
          <p className="text-gray-600">Email: rupali2118@gmail.com</p>
        </div>
        <div className="mt-4 space-y-2">
          <p className="text-gray-700"><strong>Dr. Sonal Jagtap</strong></p>
          <p className="text-gray-600">Department of E&TC Engineering, Smt. Kashibai Navale College of Engineering, Vadgaon(Bk), Pune 411041, India</p>
        </div>
      </section>
    </div>
  );
};

export default ProjectInfo;