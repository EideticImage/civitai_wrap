from dotenv import load_dotenv
import os


class NoCivitaiKeySet(Exception):
    pass


class Config:
    @classmethod
    def _load(cls):
        load_dotenv()
        cls.API_KEY = os.getenv("CIVITAI_API_KEY")

    @classmethod
    def get_api_key(cls):
        if cls.API_KEY is None:
            raise NoCivitaiKeySet()
        return cls.API_KEY

    @classmethod
    def get_headers(cls):
        if cls.API_KEY is None:
            raise NoCivitaiKeySet()

        return {
            "Authorization": f"Bearer {cls.API_KEY}",
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
        }

    @classmethod
    def set_api_key(cls, api_key):
        cls.API_KEY = api_key

Config._load()