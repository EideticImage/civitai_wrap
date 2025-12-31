from enum import Enum

import requests

from modules.data import Image
from modules.utils import get_headers

class ImagePeriodEnum(Enum):
    AllTime = 1
    Year    = 2
    Month   = 3
    Week    = 4
    Day     = 5

class ImageSortEnum(Enum):
    MostReactions   = 1
    MostComments    = 2
    Newest          = 3

class ImageApi:
    @staticmethod
    def fetch_images(
        count: int = -1,
        postId: int = None,
        modelId: int = None,
        modelVersionId: int = None,
        username: str = None,
        sort: ImageSortEnum = None,
        period: ImagePeriodEnum = None,
    ) -> list[Image]:
        url = f"https://civitai.com/api/v1/images?"

        params = {}
        if postId is not None:
            params["postId"] = postId
        if modelId is not None:
            params["modelId"] = modelId
        if modelVersionId is not None:
            params["modelVersionId"] = modelVersionId
        if username is not None:
            params["username"] = username
        if sort is not None:
            params["sort"] = sort.name
        if period is not None:
            params["period"] = period.name

        images = []
        while len(images) < count or count == -1:
            params["limit"] = 200 if count == -1 else min(count-len(images), 200)

            resp = requests.get(url, headers=get_headers(), params=params)
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items", [])
            if not len(items): break

            results = [Image.from_dict(img) for img in items]
            images.extend(results)
            params['cursor'] = data.get("metadata", {}).get("nextCursor", None)

            if params['cursor'] is None:
                break

        return images