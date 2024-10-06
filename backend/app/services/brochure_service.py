import json
import pickle
from openai import OpenAI
from typing import List, Dict, Tuple

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

class BrochureService:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.brochure_data = self._load_brochure_data()
        self.full_embeddings = None
        self.subcategory_item_embeddings = None
        self.load_embeddings()

    def _load_brochure_data(self) -> Dict:
        with open('/Users/rohithkyla/FoodDist/backend/app/services/cleanedBrochure.json', 'r') as file:
            return json.load(file)

    def load_embeddings(self):
        try:
            with open('/Users/rohithkyla/FoodDist/backend/app/services/full_embeddings.pkl', 'rb') as f:
                self.full_embeddings = pickle.load(f)
            print("Full embeddings loaded successfully.")
        except FileNotFoundError:
            print("Full embeddings file not found. Please run process_brochure() first.")

        # try:
        #     with open('/Users/rohithkyla/FoodDist/backend/app/services/subcategory_item_embeddings.pkl', 'rb') as f:
        #         self.subcategory_item_embeddings = pickle.load(f)
        #     print("Subcategory item embeddings loaded successfully.")
        # except FileNotFoundError:
        #     print("Subcategory item embeddings file not found. Please run process_brochure() first.")

    def get_embedding(self, text: str, model: str = "text-embedding-3-large") -> List[float]:
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def get_embeddings(self, texts: List[str], model: str = "text-embedding-3-large") -> List[List[float]]:
        texts = [text.replace("\n", " ") for text in texts]
        response = self.client.embeddings.create(input=texts, model=model)
        return [data.embedding for data in response.data]

    def generate_embeddings(self) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
        full_embeddings = {}
        subcategory_item_embeddings = {}
        batch_size = 100
        texts_to_embed = []
        keys = []
        
        for category, subcategories in self.brochure_data.items():
            for subcategory, items in subcategories.items():
                for item in items:
                    combined_text = f"{subcategory} - {item}"
                    texts_to_embed.append(combined_text)
                    keys.append((combined_text, f"{subcategory} - {item.split(' ', 1)[0]}"))
                    
                    if len(texts_to_embed) == batch_size:
                        print(f"Processing batch of {batch_size} items...")
                        embeddings = self.get_embeddings(texts_to_embed)
                        for (full_key, subcategory_item_key), embedding in zip(keys, embeddings):
                            full_embeddings[full_key] = embedding
                            subcategory_item_embeddings[subcategory_item_key] = embedding
                        texts_to_embed = []
                        keys = []
        
        # Process any remaining items
        if texts_to_embed:
            print(f"Processing remaining {len(texts_to_embed)} items...")
            embeddings = self.get_embeddings(texts_to_embed)
            for (full_key, subcategory_item_key), embedding in zip(keys, embeddings):
                full_embeddings[full_key] = embedding
                subcategory_item_embeddings[subcategory_item_key] = embedding
        
        return full_embeddings, subcategory_item_embeddings

    def generate_ingredient_embeddings(self, ingredients: List[str]) -> Dict[str, List[float]]:
        ingredient_embeddings = {}
        batch_size = 100
        
        for i in range(0, len(ingredients), batch_size):
            batch = ingredients[i:i+batch_size]
            print(f"Processing batch of {len(batch)} ingredients...")
            embeddings = self.get_embeddings(batch)
            
            for ingredient, embedding in zip(batch, embeddings):
                ingredient_embeddings[ingredient] = embedding
        
        print(f"Generated embeddings for {len(ingredient_embeddings)} ingredients.")
        return ingredient_embeddings

    def process_brochure(self):
        full_embeddings, subcategory_item_embeddings = self.generate_embeddings()

        import pickle

        # Store full embeddings in a pickle file
        with open('/Users/rohithkyla/FoodDist/backend/app/services/full_embeddings.pkl', 'wb') as f:
            pickle.dump(full_embeddings, f)

        # Store subcategory item embeddings in a separate pickle file
        with open('/Users/rohithkyla/FoodDist/backend/app/services/subcategory_item_embeddings.pkl', 'wb') as f:
            pickle.dump(subcategory_item_embeddings, f)

        print("Embeddings have been stored in pickle files.")
        # You can further process or store the embeddings as needed
        return full_embeddings, subcategory_item_embeddings

# brochure_service = BrochureService()
# brochure_service.process_brochure()