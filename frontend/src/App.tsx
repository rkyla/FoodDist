import React, { useState } from 'react'
import ChatMessage from './components/ChatMessage'
import VenueInput from './components/VenueInput'
import { ChatMessageType, Stage, MenuItem } from './types'
import { searchRestaurant, getMenu, computeSimilarities, analyzeMatches } from './services/api'

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
        console.log(menuResult.menu_items)
        addAIMessage(menuResult.menu_items, 'ingredients')

        // Compute similarities after loading menu items
        addAIMessage('Computing similarities...', 'computing')
        const similaritiesResult = await computeSimilarities()
        console.log('Similarities result:', similaritiesResult)
        addAIMessage('Similarities computed', 'computed')

        // Analyze matches
        addAIMessage('Analyzing matches...', 'analyzing')
        const analysisResult = await analyzeMatches()
        console.log('Analysis result:', analysisResult)
        addAIMessage(`Analysis summary: ${analysisResult.summary}`, 'analysis_summary')

        // You can process the similarities result here if needed
        // For example, you could add a new message with the most similar items
        if (similaritiesResult.menu_items) {
          const topSimilarities = similaritiesResult.menu_items.map((item: any) => {
            const topIngredient = Object.entries(item.similarities).reduce((a, b) => a[1].similarity > b[1].similarity ? a : b)
            return `${item.name}: ${topIngredient[0]} - ${topIngredient[1].most_similar_item} (${topIngredient[1].similarity.toFixed(2)})`
          }).join('\n')
          addAIMessage(`Top similarities:\n${topSimilarities}`, 'similarities')
        }
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

  const addAIMessage = (content: string | MenuItem[], stage: Stage) => {
    setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content, stage }])
  }

  const generateAIResponse = (venue: string | string[], menuItems: string[] = []) => {
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