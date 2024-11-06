from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import logging
import os
import schedule

logging.basicConfig(
    filename='spam_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def spam_login(npm, password, num_attempts=1000):
    driver = None
    attempt = 0
    try:
        logging.info(f"Starting spam login process for {num_attempts} attempts")
        
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        
        logging.info("Setting up Chrome driver")
        try:
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )
            logging.info("Chrome driver initialized successfully")
        except Exception as e:
            logging.error(f"Error installing/starting Chrome driver: {e}")
            return

        driver.set_page_load_timeout(10)
        
        while attempt < num_attempts:
            try:
                attempt += 1
                logging.info(f"Attempt {attempt} of {num_attempts}")
                
                driver.get("https://akademik.unbin.ac.id/absensi/")
                
                npm_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "userid"))
                )
                npm_field.clear()
                npm_field.send_keys(npm)
                
                password_field = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.ID, "pin"))
                )
                password_field.clear()
                password_field.send_keys(password)
                
                submit_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][name='login'][value='Login']"))
                )
                driver.execute_script("arguments[0].click();", submit_button)
                
                time.sleep(0.5)
                
                print(f"Login attempt {attempt} completed")
                logging.info(f"Login attempt {attempt} completed")
                
            except Exception as e:
                error_msg = f"Error on attempt {attempt}: {type(e).__name__}: {str(e)}"
                print(error_msg)
                logging.error(error_msg)
                continue
                
    except Exception as e:
        error_msg = f"Critical error: {type(e).__name__}: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        
    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Browser session closed")
            except Exception as e:
                logging.error(f"Error closing driver: {e}")

if __name__ == "__main__":
    npm = "12522023"
    password = "12522023"
    
    print("Starting spam login process...")
    spam_login(npm, password)
    
    print("Spam login completed.")
    logging.info("Spam login process finished")
