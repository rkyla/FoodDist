import React from 'react'
import { Stage } from '../types'

interface StageDisplayProps {
  currentStage: Stage
}

const StageDisplay: React.FC<StageDisplayProps> = ({ currentStage }) => {
  const stages: { [key in Stage]: { text: string; color: string } } = {
    initial: { text: 'AI', color: 'bg-blue-200 text-blue-800' },
    searching: { text: 'Found Restaurant', color: 'bg-blue-200 text-blue-800' },
    found: { text: 'Restaurant XYZ in Sydney', color: 'bg-orange-200 text-orange-800' },
    menu_loaded: { text: 'Menu Loaded', color: 'bg-green-200 text-green-800' },
    ingredients: { text: 'Ingredients', color: 'bg-purple-200 text-purple-800' },
  }

  return (
    <div className="flex flex-wrap gap-2">
      {Object.entries(stages).map(([stage, { text, color }]) => (
        <div
          key={stage}
          className={`px-3 py-1 rounded-full text-sm font-medium ${color} ${
            currentStage === stage ? 'opacity-100' : 'opacity-50'
          }`}
        >
          {text}
        </div>
      ))}
    </div>
  )
}

export default StageDisplay