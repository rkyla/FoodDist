import React, { useState } from 'react'
import { User, Bot } from 'lucide-react'
import { ChatMessageType } from '../types'
import { render } from 'react-dom'

interface ChatMessageProps {
  message: ChatMessageType
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user'
  const [isExpanded, setIsExpanded] = useState(false)

  const toggleExpand = () => {
    setIsExpanded(!isExpanded)
  }

  const getStageColor = (stage?: string) => {
    switch (stage) {
      case 'searching':
        return 'bg-blue-100 text-blue-800'
      case 'found':
        return 'bg-orange-100 text-orange-800'
      case 'menu_loaded':
        return 'bg-green-100 text-green-800'
      case 'ingredients':
        return 'bg-purple-100 text-purple-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex items-start space-x-2 ${isUser ? 'flex-row-reverse' : ''}`}>
        <div className={`p-2 rounded-full ${isUser ? 'bg-blue-500' : 'bg-gray-300'}`}>
          {isUser ? <User size={24} className="text-white" /> : <Bot size={24} className="text-gray-700" />}
        </div>
        <div className={`max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl p-3 rounded-lg ${isUser ? 'bg-blue-100' : 'bg-white'}`}>
          {!isUser && message.stage && (
            <div className={`inline-block px-2 py-1 rounded-full text-xs font-medium mb-2 ${getStageColor(message.stage)}`}>
              {message.stage.charAt(0).toUpperCase() + message.stage.slice(1)}
            </div>
          )}
          <p className="text-sm">{message.content}</p>
        </div>
      </div>
    </div>
  )
}

export default ChatMessage