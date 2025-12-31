from modules.data import Image
from abc import ABC, abstractmethod

class ImageFilter(ABC):
    @abstractmethod
    def __call__(self, image: Image):
        pass

class ImageLoraFilter(ImageFilter):
    def __init__(self, lora_name):
        self.lora_name = lora_name

    def __call__(self, image: Image):
        metadata = image.meta
        if metadata is None:
            return False
        ressources = metadata.get('resources', [])
        for ressource in ressources:
            if ressource['name'] == self.lora_name:
                return True
        return False

class ImagePromptFilter(ImageFilter):
    def __init__(self, text):
        self.text = text.lower()
    
    def __call__(self, image: Image):
        metadata = image.meta
        if metadata is None:
            return False
        prompt = metadata.get('resources', '')

        return self.text in prompt.lower()
    
