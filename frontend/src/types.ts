export type Stage = 'initial' | 'searching' | 'found' | 'menu_loaded' | 'ingredients' | 'error' | 'computing' | 'computed' | 'similarities' | 'analyzing' | 'analysis_summary'

export interface ChatMessageType {
  role: 'user' | 'assistant'
  content: string | MenuItem[]
  stage?: Stage
}

export type MenuItem = {
  name: string;
  ingredients: string[] | undefined;
};