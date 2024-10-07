export type Stage = 'initial' | 'searching' | 'found' | 'menu_loaded' | 'ingredients' | 'computing' | 'computed' | 'similarities' | 'analyzing' | 'analysis_summary' | 'error'

export interface ChatMessageType {
  role: 'user' | 'assistant'
  content: string | MenuItem[] | SimilarityItem[]
  stage?: Stage
}

export interface MenuItem {
  name: string
  ingredients: string[] | undefined
}

export interface SimilarityItem {
  menuItem: string
  ingredient: string
  match: string
}