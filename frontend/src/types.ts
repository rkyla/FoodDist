export type Stage = 'initial' | 'searching' | 'found' | 'menu_loaded' | 'ingredients'

export interface ChatMessageType {
  role: 'user' | 'assistant'
  content: string
  stage?: Stage
}