"use client"; // This is a client component 👈🏽
import React from 'react'
import EmotionRecorderForm from './EmotionRecorderForm'

function MainForm() {
    return (
        <div className="w-full bg-white rounded-lg shadow-lg p-6 mb-8">
      <EmotionRecorderForm />
    </div>
    )
}

export default MainForm
