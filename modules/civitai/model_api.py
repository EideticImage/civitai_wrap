import subprocess
import os
import requests
from dataclasses import asdict

from modules.utils import API_KEY, get_headers, save_json, download_image
from modules.data import Model

class ModelApi:
    @staticmethod
    def download_weights(modelVersionId: int, folder) -> None:
        url = f"https://civitai.com/api/download/models/{modelVersionId}?token={API_KEY}"
        filename = os.path.join(folder, f'{modelVersionId}.safetensors')
        command = ["wget", url] if os.name == 'posix' else ['curl', '-L', '-o', filename,  url, ' --content-disposition']
        subprocess.call(command)

    @staticmethod
    def fetch_by_id(modelId: int) -> "Model":
        url = f"https://civitai.com/api/v1/models/{modelId}"

        params = {}

        try:
            resp = requests.get(url, headers=get_headers(), params=params, timeout=2)
            resp.raise_for_status()
            data = resp.json()

            return Model.from_dict(data)
        except Exception as e:
            print(e)
            return None

    def download(modelId: int, folder='', name=''):
        model = ModelApi.fetch_by_id(modelId)
        if model is None:
            print(f'Could not fetch the model')
            return

        name = name or model.name
        folder = folder or os.path.join('models')

        import os
        if not os.path.exists(folder):
            os.makedirs(folder) 

        save_json(asdict(model), folder, name)
        
        version1 = model.get_latest_version()
        miniature = version1.images[0]

        download_image(miniature['url'], folder, filename='miniature')
        ModelApi.download_weights(version1.id, folder)
