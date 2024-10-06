import json
import os
import time
from .brochure_service import BrochureService
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from .openai_service import OpenAIService
from pydantic import BaseModel
from typing import List, Dict
import numpy as np

class MenuItem(BaseModel):
    name: str
    ingredients: List[str]

class MenuItems(BaseModel):
    items: List[MenuItem]

class RestaurantService:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=self.options)
        self.openai_service = OpenAIService()
        self.brochure_service = BrochureService()
        self.structured_items = None

    async def search_restaurant(self, restaurant_name: str):
        search_query = f"{restaurant_name} sydney"
        self.driver.get('https://www.google.com')
        search_box = self.driver.find_element(By.NAME, 'q')
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)

        wait = WebDriverWait(self.driver, 10)
        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))

        if results:
            first_result = results[0]
            link = first_result.find_element(By.CSS_SELECTOR, 'a')
            url = link.get_attribute('href')
            title, description = self.extract_result_info(first_result)
            return {"restaurant": restaurant_name, "title": title, "description": description, "url": url}
        else:
            return {"error": f"No results found for {restaurant_name}"}

    async def get_menu(self, restaurant_name: str):
        search_result = await self.search_restaurant(restaurant_name)
        
        if "error" in search_result:
            return search_result

        menu_button = self.check_for_menu_button()
        if menu_button:
            ActionChains(self.driver).move_to_element(menu_button).click().perform()
            try:
                menu_items = self.extract_menu_items()
                return {"restaurant": restaurant_name, "menu_items": [item.dict() for item in menu_items]}
            except Exception as e:
                return {"error": f"Error extracting menu items for {restaurant_name}: {str(e)}"}
        else:
            return {"error": f"No Menu button found for {restaurant_name}"}

    def extract_result_info(self, result):
        title = result.find_element(By.CSS_SELECTOR, 'h3').text
        description = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
        return title, description

    def check_for_menu_button(self):
        try:
            return self.driver.find_element(By.CSS_SELECTOR, 'div[data-id="menu-viewer-entrypoint"]')
        except NoSuchElementException:
            return None

    def extract_menu_items(self):
        time.sleep(8)
        menu_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Menu"]'))
        )
        items = menu_container.find_elements(By.CSS_SELECTOR, 'div[role="treeitem"]')
        raw_menu_items = [item.text.strip() for item in items if item.text.strip()]
        
        # Use OpenAI to extract structured information
        system_prompt = """
        You are an AI assistant that extracts menu item information. 
        For each menu item, provide the name and a list of likely ingredients.
        If ingredients are not explicitly mentioned, use your knowledge to suggest common ingredients for the dish.
        """
        self.structured_items = self.openai_service.extract_structured_information(
            user_input="\n".join(raw_menu_items),
            output_class=MenuItems,
            system_prompt=system_prompt
        )
        
        return self.structured_items.items

    def compute_similarities(self):
        if not self.structured_items:
            return {"error": "No menu items found. Please fetch a menu first."}

        if not self.brochure_service.full_embeddings:
            return {"error": "Embeddings not loaded. Please ensure the embedding files exist and are loaded correctly."}

        all_ingredients = set()
        for item in self.structured_items.items:
            all_ingredients.update(f"{item.name} - {ingredient}" for ingredient in item.ingredients)

        ingredient_embeddings = self.brochure_service.generate_ingredient_embeddings(list(all_ingredients))
        
        result = []
        for item in self.structured_items.items:
            item_similarities = {}
            for ingredient in item.ingredients:
                combined_key = f"{item.name} - {ingredient}"
                embedding = ingredient_embeddings[combined_key]
                max_similarity = -1
                max_similar_item = ""
                for brochure_item, brochure_embedding in self.brochure_service.full_embeddings.items():
                    similarity = self.cosine_similarity(embedding, brochure_embedding)
                    if similarity > max_similarity:
                        max_similarity = similarity
                        max_similar_item = brochure_item
                item_similarities[ingredient] = {
                    "similarity": max_similarity,
                    "most_similar_item": max_similar_item
                }
            result.append({
                "name": item.name,
                "similarities": item_similarities
            })

        return {"menu_items": result}

    @staticmethod
    def cosine_similarity(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
