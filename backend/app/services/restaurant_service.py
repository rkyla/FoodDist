import json
import os
import time
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
from typing import List

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
        structured_menu_items = self.openai_service.extract_structured_information(
            user_input="\n".join(raw_menu_items),
            output_class=MenuItems,
            system_prompt=system_prompt
        )
        
        return structured_menu_items.items
