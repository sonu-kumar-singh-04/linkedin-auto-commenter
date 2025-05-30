# 🤖 LinkedIn GenAI Auto-Commenter (For Educational Use Only)

This project demonstrates how to automate LinkedIn post engagement using Python, Selenium, and OpenAI. It scrapes posts related to a specific topic, generates meaningful comments using a large language model (LLM) via LangChain and OpenAI, and automatically posts the comments back to LinkedIn.

> ⚠️ **Disclaimer:** This project is created for **educational and learning purposes only**. Do not use it to spam or violate LinkedIn’s terms of service. Misuse may lead to account suspension.

---

## ✨ Features

- 🔍 Scrapes LinkedIn posts based on a specific keyword or topic
- 🧠 Uses OpenAI's GPT-based model to generate relevant and human-like comments
- 💬 Automatically posts the generated comment to the corresponding LinkedIn post
- 🔐 Securely manages credentials using `.env` file

---

## 🧰 Tech Stack

- `Python`
- `Selenium` – for browser automation
- `LangChain` – for prompt handling and OpenAI integration
- `OpenAI` – for natural language comment generation
- `webdriver-manager` – to auto-manage browser drivers
- `python-dotenv` – to load environment variables
- `pyperclip` – to handle clipboard operations (if needed)

---

## 📦 Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/linkedin-auto-commenter.git
cd linkedin-auto-commenter
``````
### 2. Create a virtual environment (recommended)
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Create a .env file in the root directory and add the following:
```
OPENAI_API_KEY=your_openai_api_key
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
TOPIC=your_desired_topic  # e.g., Artificial Intelligence
```
📝 Note: Never commit `.env` or real credentials to a public repository.

## 🚀 How It Works
- Logs into LinkedIn using Selenium.

- Searches for posts containing the topic you specify.

- Extracts post content from the LinkedIn feed.

- Sends the post content to OpenAI via LangChain to generate a suitable, human-like comment.

- Automatically submits the comment back on the same post using Selenium.

## ▶️ Running the Script
```
python main.py
```
## 🔒 Important Notes

- Avoid excessive usage — LinkedIn may detect bot-like behavior.
- Use a test account for experiments, not your personal or company profile.
- Do not use this tool for mass commenting or unsolicited promotions.
- Captchas or login challenges may interfere with automation.
- You may need to keep browser window visible to avoid detection.

## 📚 Learning Objectives
This project is a practical demonstration of how to:
- Automate web interactions with Selenium

- Integrate LangChain with OpenAI's LLMs for text generation

 - Apply dotenv for configuration and credential management

- Respect rate limits, UI structures, and ethical boundaries of web automation