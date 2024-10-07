import React, { useState } from 'react'
import { User, Bot, ChevronDown, ChevronUp } from 'lucide-react'
import { ChatMessageType, MenuItem } from '../types'

interface ChatMessageProps {
  message: ChatMessageType
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [isExpanded, setIsExpanded] = useState(false)
  const isUser = message.role === 'user'

  const getStageColor = (stage?: string) => {
    switch (stage) {
      case 'searching':
        return 'bg-blue-100 text-blue-800'
      case 'found':
        return 'bg-green-100 text-green-800'
      case 'menu_loaded':
        return 'bg-yellow-100 text-yellow-800'
      case 'ingredients':
        return 'bg-purple-100 text-purple-800'
      case 'analysis_summary':
        return 'bg-green-800 text-green-100'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const renderContent = () => {
    if (message.stage === 'ingredients' && Array.isArray(message.content)) {
      const menuItems = message.content as MenuItem[]
      const displayedMenuItems = isExpanded ? menuItems : menuItems.slice(0, 3)

      return (
        <>
          <ul className="list-disc pl-5 mb-2">
            {displayedMenuItems.map((menuItem, index) => (
              <li key={index}>
                <strong>{menuItem.name}</strong>
                <ul className="list-circle pl-5">
                  {menuItem.ingredients?.map((ingredient, i) => (
                    <li key={i}>{ingredient}</li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
          {menuItems.length > 3 && (
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-blue-500 hover:text-blue-700 font-medium flex items-center"
            >
              {isExpanded ? (
                <>
                  <ChevronUp size={16} className="mr-1" /> Collapse
                </>
              ) : (
                <>
                  <ChevronDown size={16} className="mr-1" /> Expand
                </>
              )}
            </button>
          )}
        </>
      )
    }
    return <p className="text-sm">{message.content as string}</p>
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
          {renderContent()}
        </div>
      </div>
    </div>
  )
}

export default ChatMessage