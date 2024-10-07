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

# Load restaurant names from JSON file
with open('restaurants_2000.json', 'r') as f:
    data = json.load(f)
    restaurants = data['restaurants']

# Set up Selenium WebDriver (Chrome)
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode
driver = webdriver.Chrome(options=options)

# Create a directory to store PDFs
if not os.path.exists('menus'):
    os.makedirs('menus')

# Function to check if URL is a PDF
def is_pdf(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        content_type = response.headers.get('content-type', '').lower()
        return 'application/pdf' in content_type
    except requests.RequestException:
        return False

# Function to download PDF
def download_pdf(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# Function to extract title and description from search result
def extract_result_info(result):
    title = result.find_element(By.CSS_SELECTOR, 'h3').text
    description = result.find_element(By.CSS_SELECTOR, 'div.VwiC3b').text
    return title, description

# Function to check for the Google Places "Menu" button
def check_for_menu_button(driver):
    try:
        menu_button = driver.find_element(By.CSS_SELECTOR, 'div[data-id="menu-viewer-entrypoint"]')
        return menu_button
    except NoSuchElementException:
        return None

# Function to extract menu items
def extract_menu_items(driver):
    menu_items = []
    
    # Wait for 8 seconds after clicking the menu button
    time.sleep(8)
    
    # Wait for the menu container to be present
    menu_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Menu"]'))
    )
    
    # Take a screenshot after waiting for menu_container
    driver.save_screenshot('screenshots/menu_container_screenshot.png')
    
    # Find all items with data-hashed-menu-item-id attribute
    # items = menu_container.find_elements(By.CSS_SELECTOR, 'div[data-hashed-menu-item-id]')
    items = menu_container.find_elements(By.CSS_SELECTOR, 'div[role="treeitem"]')
    
    for item in items:
        item_text = item.text.strip()
        if item_text:  # Only add non-empty items
            menu_items.append(item_text)
    
    return menu_items

# Iterate through restaurants and search for menus
for restaurant in restaurants[:3]:
    # search_query = f"{restaurant} menu filetype:pdf"
    search_query = f"{restaurant} sydney"
    
    # Perform Google search
    driver.get('https://www.google.com')
    search_box = driver.find_element(By.NAME, 'q')
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    
    # Wait for search results
    wait = WebDriverWait(driver, 10)
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g')))
    
    # Check if there are any results
    if results:
        # Get the first result
        first_result = results[0]
        link = first_result.find_element(By.CSS_SELECTOR, 'a')
        pdf_url = link.get_attribute('href')
        
        # Extract title and description
        title, description = extract_result_info(first_result)
        print(f"Restaurant: {restaurant}")
        print(f"Result Title: {title}")
        print(f"Result Description: {description}")
        print(f"URL: {pdf_url}")
        print("---")

        # Here you would send this information to OpenAI for confirmation
        # openai_confirmation = send_to_openai(restaurant, title, description, pdf_url)

        # Check if the URL is actually a PDF
        if is_pdf(pdf_url):
            # Download the PDF
            filename = f"menus/{restaurant.replace(' ', '_')}_menu.pdf"
            try:
                download_pdf(pdf_url, filename)
                print(f"Downloaded menu for {restaurant}")
            except Exception as e:
                print(f"Error downloading menu for {restaurant}: {str(e)}")
        else:
            print(f"The first result for {restaurant} is not a PDF")
            
            # Perform a new search for just the restaurant name
            # driver.get('https://www.google.com')
            # search_box = driver.find_element(By.NAME, 'q')
            # search_box.send_keys(restaurant)
            # search_box.send_keys(Keys.RETURN)
            
            # Wait for search results
            # wait.until(EC.presence_of_element_located((By.ID, 'search')))
            
            menu_button = check_for_menu_button(driver)

            # Check for the Menu button
            if menu_button:
                print(f"Menu button found for {restaurant}")
                # Here you can add code to interact with the Menu button if needed
                ActionChains(driver).move_to_element(menu_button).click().perform()
                
                try:
                    menu_items = extract_menu_items(driver)
                    print(f"Menu items extracted for {restaurant}:")
                    for item in menu_items:
                        print(item)
                    
                    # Here you can save the menu items to a file or database
                except Exception as e:
                    print(f"Error extracting menu items for {restaurant}: {str(e)}")
            else:
                print(f"No Menu button found for {restaurant}")
                
                # Create a directory to store screenshots if it doesn't exist
                if not os.path.exists('screenshots'):
                    os.makedirs('screenshots')
                
                # Take a screenshot and save it
                screenshot_path = f"screenshots/{restaurant.replace(' ', '_')}_no_menu.png"
                driver.save_screenshot(screenshot_path)
                print(f"Screenshot saved to {screenshot_path}")
    else:
        print(f"No PDF menu found for {restaurant}")
    
    # Add a small delay to avoid overwhelming the server
    time.sleep(2)

# Close the browser
driver.quit()

print("Menu scraping completed.")
