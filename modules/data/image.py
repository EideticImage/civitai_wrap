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

    @staticmethod
    def from_dict(data: dict) -> "Image":
        return Image(
            id=data.get("id"),
            url=data.get("url"),
            width=data.get("width"),
            height=data.get("height"),
            meta=data.get("meta", {}).get("meta", {}),
            base_model=data.get("baseModel", ""),
        )

    @staticmethod
    def fetch_from_api(image_id: int) -> "Image":
        import requests

        url = f"https://civitai.com/api/v1/images?imageId={image_id}"
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
