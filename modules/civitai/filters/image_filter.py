from modules.data import Image
from .filter import Filter

class ImageLoraNameFilter(Filter):
    def __init__(self, lora_name):
        self.lora_name = lora_name

    def __call__(self, image: Image):
        return any(r['name'] == self.lora_name for r in image.get_ressources())

class ImageLoraExactCountFilter(Filter):
    def __init__(self, count):
        self.count = count

    def __call__(self, image: Image):
        return len(image.get_ressources()) == self.count

class ImagePromptFilter(Filter):
    def __init__(self, text):
        self.text = text.lower()
    
    def __call__(self, image: Image):
        return self.text in image.get_prompt().lower()
    
class ImageCivitaiRessourcesFilter(Filter):
    def __init__(self, modelVersionId):
        self.modelVersionId = modelVersionId

    def __call__(self, image: Image):
        return any(r['modelVersionId'] == self.modelVersionId for r in image.get_civitai_ressources())