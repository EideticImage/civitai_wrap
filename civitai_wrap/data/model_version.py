from dataclasses import dataclass

@dataclass
class ModelVersion:
    id: int
    name: str
    base_model: str
    download_url: str
    images: list

    @staticmethod
    def from_dict(data: dict) -> "ModelVersion":
        return ModelVersion(
            id = data.get('id'),
            name = data.get('name'),
            base_model = data.get('baseModel'),
            images = data.get('images'),
            download_url = data.get('downloadUrl'),
        )
