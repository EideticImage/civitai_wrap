from enum import Enum

import requests

from civitai_wrap.data import Image
from civitai_wrap import Config


class ImagePeriodEnum(Enum):
    AllTime = 1
    Year = 2
    Month = 3
    Week = 4
    Day = 5


class ImageSortEnum(Enum):
    MostReactions = 1
    MostComments = 2
    Newest = 3


class ImageApi:
    @staticmethod
    def fetch_images(
        postId: int = None,
        modelId: int = None,
        modelVersionId: int = None,
        username: str = None,
        sort: ImageSortEnum = None,
        period: ImagePeriodEnum = None,
        limit: int = None,
        cursor=None,
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
        if limit is not None:
            params["limit"] = limit
        if cursor is not None:
            params["cursor"] = cursor

        resp = requests.get(url, headers=Config.get_headers(), params=params, timeout=2)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("items", [])
        if not len(items):
            return [], {}

        results = [Image.from_dict(img) for img in items]
        return results, data.get("metadata", {})
