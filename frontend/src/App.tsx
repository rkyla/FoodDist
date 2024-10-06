import React, { useState } from 'react'
import ChatMessage from './components/ChatMessage'
import VenueInput from './components/VenueInput'
import { ChatMessageType, Stage } from './types'
import { searchRestaurant, getMenu } from './services/api'

function App() {
  const [messages, setMessages] = useState<ChatMessageType[]>([
    { role: 'assistant', content: "Hi Ari! I'm your AI sales assistant. Enter a venue name, and I'll provide product suggestions based on their menu.", stage: 'initial' },
  ])

  const handleSendMessage = async (venue: string) => {
    if (venue.trim() === '') return

    const newUserMessage: ChatMessageType = { role: 'user', content: venue }
    setMessages((prevMessages) => [...prevMessages, newUserMessage])

    try {
      addAIMessage('Searching for restaurant...', 'searching')
      const searchResult = await searchRestaurant(venue)
      addAIMessage(`Found restaurant: ${searchResult.title}`, 'found')

      addAIMessage('Loading menu...', 'menu_loaded')
      const menuResult = await getMenu(venue)
      
      if (menuResult.menu_items && menuResult.menu_items.length > 0) {
        addAIMessage('Menu items:', 'ingredients')
        addAIMessage(menuResult.menu_items.map((item: { name: string; ingredients: string[] }) => `${item.name} (${item.ingredients.join(', ')})`).join(', '), 'ingredients')
      } else {
        addAIMessage('No menu items found.', 'ingredients')
      }

      const aiResponse = generateAIResponse(venue, menuResult.menu_items)
      addAIMessage(aiResponse, 'ingredients')
    } catch (error) {
      console.error('Error:', error)
      addAIMessage('Sorry, I encountered an error while processing your request.', 'error')
    }
  }

  const addAIMessage = (content: string, stage: Stage) => {
    setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content, stage }])
  }

  const generateAIResponse = (venue: string, menuItems: string[] = []) => {
    // You can implement more sophisticated logic here based on the menu items
    const responses = [
      `For ${venue}, I recommend our new line of plant-based proteins. They're perfect for vegan cafes and health-conscious customers.`,
      `${venue} might be interested in our seasonal fruit selection. We have a great variety of locally sourced produce.`,
      `Based on ${venue}'s menu, our artisanal cheese collection could be a great fit. It pairs well with their wine selection.`,
      `For ${venue}, our premium coffee beans would be an excellent addition. They're sourced from sustainable farms.`,
      `${venue} could benefit from our range of gluten-free products. They're becoming increasingly popular among health-conscious diners.`,
    ]
    return responses[Math.floor(Math.random() * responses.length)]
  }

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4">
        <h1 className="text-2xl font-bold">Ari's Sales Assistant</h1>
      </header>
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}
      </div>
      <VenueInput onSendMessage={handleSendMessage} />
    </div>
  )
}

export default App