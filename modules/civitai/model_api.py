import subprocess
import os

from modules.utils import API_KEY


class ModelApi:
    @staticmethod
    def download_model(modelVersionId=None):
        url = f"https://civitai.com/api/download/models/{modelVersionId}?token={API_KEY}"
        command = ["wget", url] if os.name == 'posix' else ['curl', '-L', '-o', f'{modelVersionId}.safetensors',  url, ' --content-disposition']
        subprocess.call(command)
