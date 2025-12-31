from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_headers():
    return {
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }