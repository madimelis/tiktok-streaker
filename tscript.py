import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager

def send_tiktok_streak():
    options = webdriver.FirefoxOptions()
    # Specify the path to the Firefox profile
    profile_path = r"..."
    options.profile = profile_path
    
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    
    try:
        driver.get("https://www.tiktok.com/messages")
        
        print("Waiting for the chat list to load...")
        time.sleep(6)
        
        # Enter your friend's nickname here
        friend_name = "..." 
        
        print(f"Looking for chat with user: {friend_name}...")
        
        chats = driver.find_elements(By.XPATH, f"//*[contains(text(), '{friend_name}')]")
        
        chat_found = False
        for chat in chats:
            try:
                chat.click()
                chat_found = True
                print(f"Chat with {friend_name} opened successfully!")
                break
            except:
                continue
                
        if not chat_found:
            print(f"Failed to find chat with '{friend_name}' in the list. Make sure the name is correct.")
            return

        time.sleep(3)
        
        message_boxes = driver.find_elements(By.CSS_SELECTOR, "[contenteditable='true']")
        
        if message_boxes:
            chat_input = message_boxes[-1]
            chat_input.click()
            chat_input.send_keys("🔥")
            chat_input.send_keys(Keys.ENTER)
            print("Streak sent successfully!")
        else:
            print("Failed to find the message input field in the open chat.")
            
        time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_tiktok_streak()