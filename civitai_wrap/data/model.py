from dataclasses import dataclass
from .model_version import ModelVersion

@dataclass
class Model:
    id: int
    name: str
    description: str
    versions: list[ModelVersion]

    def get_latest_version(self):
        return self.versions[0]

    @staticmethod
    def from_dict(data: dict) -> "Model":
        return Model(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            versions=[ModelVersion.from_dict(v) for v in data.get('modelVersions', [])]
        )