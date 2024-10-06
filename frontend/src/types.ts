export type Stage = 'initial' | 'searching' | 'found' | 'menu_loaded' | 'ingredients' | 'error'

export interface ChatMessageType {
  role: 'user' | 'assistant'
  content: string | MenuItem[]
  stage?: Stage
}

export type MenuItem = {
  name: string;
  ingredients: string[] | undefined;
};