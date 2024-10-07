import React, { useState } from 'react'
import ChatMessage from './components/ChatMessage'
import VenueInput from './components/VenueInput'
import { ChatMessageType, Stage, MenuItem, SimilarityItem } from './types'
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

        if (similaritiesResult.menu_items) {
          const topSimilarities: SimilarityItem[] = similaritiesResult.menu_items.flatMap((item: any) => 
            Object.entries(item.similarities).map(([ingredient, similarity]) => ({
              menuItem: item.name,
              ingredient,
              match: (similarity as { most_similar_item: string }).most_similar_item
            }))
          )
          addAIMessage(topSimilarities, 'similarities')
        }

        // Analyze matches
        addAIMessage('Analyzing matches...', 'analyzing')
        const analysisResult = await analyzeMatches()
        console.log('Analysis result:', analysisResult)

        addAIMessage(`Analysis summary: ${analysisResult.summary}`, 'analysis_summary')
      } else {
        addAIMessage('No menu items found.', 'ingredients')
      }

    } catch (error) {
      console.error('Error:', error)
      addAIMessage('Sorry, I encountered an error while processing your request.', 'error')
    }
  }

  const addAIMessage = (content: string | MenuItem[] | SimilarityItem[], stage: Stage) => {
    setMessages((prevMessages) => [...prevMessages, { role: 'assistant', content, stage }])
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