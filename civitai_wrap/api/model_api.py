import subprocess
import os
import requests
from dataclasses import asdict

from civitai_wrap import save_json, download_image, Config, Model
class ModelApi:
    @staticmethod
    def download_weights(modelVersionId: int, folder) -> None:
        url = f"https://civitai.com/api/download/models/{modelVersionId}?token={Config.get_api_key()}"
        filename = os.path.join(folder, 'model.safetensors')
        command = ["wget", url] if os.name == 'posix' else ['curl', '-L', '-o', filename,  url, ' --content-disposition']
        subprocess.call(command)

    @staticmethod
    def fetch_by_id(modelId: int) -> "Model":
        url = f"https://civitai.com/api/v1/models/{modelId}"

        params = {}

        try:
            resp = requests.get(url, headers=Config.get_headers(), params=params, timeout=2)
            resp.raise_for_status()
            data = resp.json()

            return Model.from_dict(data)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def download(modelId: int, folder='', name=''):
        model = ModelApi.fetch_by_id(modelId)
        if model is None:
            print(f'Could not fetch the model')
            return

        name = name or model.name
        folder = folder or os.path.join('models')

        if not os.path.exists(folder):
            os.makedirs(folder) 

        model_folder = os.path.join(folder, str(modelId))
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)

        save_json(asdict(model), model_folder, name)
        
        version1 = model.get_latest_version()
        miniature = version1.images[0]

        download_image(miniature['url'], model_folder, filename='miniature')
        ModelApi.download_weights(version1.id, model_folder)
