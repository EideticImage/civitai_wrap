from dataclasses import dataclass
from civitai_wrap import Config, download_image
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
    
    def get_civitai_ressources(self):
        metadata = self.meta
        if metadata is None:
            return []
        return metadata.get('civitaiResources', [])

    def get_prompt(self):
        metadata = self.meta
        if metadata is None:
            return ''
        return metadata.get('prompt', '')

    @staticmethod
    def from_dict(data: dict) -> "Image":
        meta = (
            data.get("meta", {}).get("meta", {})
            if data.get("meta", {}) is not None
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

        url = f"https://civitai.com/api/v1/images?imageId={image_id}"
        resp = requests.get(url, Config.get_headers())
        resp.raise_for_status()

        for img in resp.json().get("items", []):
            return Image.from_dict(img)
        return None

    def download(self, folder: str = "default") -> None:
        import os
        download_image(self.url, os.path.join('output', folder), self.id)
