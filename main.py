
import os
import csv
import json
import time
import pickle
import logging
import hashlib
import pyperclip
import traceback
from datetime import datetime
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.prompts import PromptTemplate
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Constants
COOKIES_FILE = "linkedin_cookies.pkl"
CSV_FILE = "commented_posts.csv"
LOG_FILE = "linkedin_posts.log"

# Logger setup
class CustomFormatter(logging.Formatter):
    def format(self, record):
        level_name = record.levelname
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] {level_name}: {record.getMessage()}"

class LinkedInAutomation:
    def __init__(self):
        self.logger = self.setup_logger()
        self.driver = self.setup_driver()
        self.email = os.getenv("LINKEDIN_EMAIL")
        self.password = os.getenv("LINKEDIN_PASSWORD")
        self.commented_hashes = self.load_commented_posts()
        self.chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.6)

    def setup_logger(self):
        logger = logging.getLogger("LinkedInAutomation")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(CustomFormatter())
        logger.addHandler(handler)
        return logger

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        return driver

    def load_commented_posts(self):
        if not os.path.exists(CSV_FILE):
            return set()
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            return set(row[0] for row in csv.reader(file))

    def save_commented_post(self, post_hash):
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([post_hash])

    def login_with_cookies_or_credentials(self):
        self.driver.get("https://www.linkedin.com/")
        if os.path.exists(COOKIES_FILE):
            self.logger.info("Loading cookies from file...")
            with open(COOKIES_FILE, "rb") as file:
                cookies = pickle.load(file)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
            self.driver.refresh()
        else:
            self.logger.info("Logging in using credentials...")
            email_field = self.driver.find_element(By.ID, "session_key")
            password_field = self.driver.find_element(By.ID, "session_password")
            email_field.send_keys(self.email)
            password_field.send_keys(self.password)
            password_field.send_keys(Keys.RETURN)
            time.sleep(5)
            with open(COOKIES_FILE, "wb") as file:
                pickle.dump(self.driver.get_cookies(), file)

    def generate_comment(self, post_text):
        try:
            template = PromptTemplate.from_template("Write a short and professional comment to this LinkedIn post:{post_text}"
            )
            prompt = template.format(post_text=post_text.strip())
            messages = [
                SystemMessage(content="You're a professional LinkedIn content commenter."),
                HumanMessage(content=prompt)
            ]
            result = self.chat(messages)
            return result.content
        except Exception as e:
            self.logger.error(f"Error in generate_comment: {e}\n{traceback.format_exc()}")
            return None

    def automate_ai_commenting(self):
        self.login_with_cookies_or_credentials()
        self.logger.info("Starting LinkedIn AI commenting automation...")
        # Extend this with your scraping and interaction logic
        # For demo, simulate a comment:
        dummy_post = "How AI is changing the hiring process in 2025."
        post_hash = hashlib.sha256(dummy_post.encode()).hexdigest()

        if post_hash in self.commented_hashes:
            self.logger.info("Post already commented.")
        else:
            comment = self.generate_comment(dummy_post)
            if comment:
                self.logger.info(f"Generated comment: {comment}")
                pyperclip.copy(comment)
                self.logger.info("Comment copied to clipboard.")
                self.save_commented_post(post_hash)
                self.logger.info("Post hash saved to avoid future duplicates.")

    def cleanup_log_file(self):
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as file:
                file.truncate()
            self.logger.info("Log file cleared.")

    def close(self):
        self.driver.quit()
        self.logger.info("Browser closed.")

def main():
    bot = LinkedInAutomation()
    try:
        bot.cleanup_log_file()
        bot.automate_ai_commenting()
    except Exception as e:
        bot.logger.error(f"Unhandled exception: {e}\n{traceback.format_exc()}")
    finally:
        bot.close()

if __name__ == "__main__":
    main()
