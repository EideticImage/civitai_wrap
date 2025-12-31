from dataclasses import dataclass
from ..utils.headers import get_headers

# TODO: Add the remaining fields


@dataclass
class Image:
    id: int
    url: str
    width: int
    height: int
    meta: dict
    base_model: str

    def get_ressources(self):
        metadata = self.meta
        if metadata is None:
            return []
        return metadata.get('resources', [])

    def get_prompt(self):
        metadata = self.meta
        if metadata is None:
            return ''
        return metadata.get('prompt', '')

    @staticmethod
    def from_dict(data: dict) -> "Image":
        meta = (
            data.get("meta", {}).get("meta", {})
            if data.get("meta", {}).get("meta", {})
            else data.get("meta", {})
        )
        return Image(
            id=data.get("id"),
            url=data.get("url"),
            width=data.get("width"),
            height=data.get("height"),
            meta=meta,
            base_model=data.get("baseModel", ""),
        )

    @staticmethod
    def fetch_from_api(image_id: int) -> "Image":
        import requests

        resp = requests.get(url, get_headers())
        resp.raise_for_status()

        for img in resp.json().get("items", []):
            return Image.from_dict(img)
        return None

    def download(self, folder: str = "default") -> None:
        import os
        import requests

        folder = f"output/{folder}"
        filename = f"{folder}/{self.id}.jpg"

        if not os.path.exists(folder):
            os.makedirs(folder)

        resp = requests.get(self.url)
        resp.raise_for_status()

        with open(filename, "wb") as f:
            f.write(resp.content)
