from abc import ABC, abstractmethod

class BaseAIProvider(ABC):

    @abstractmethod
    def generate_captions(self, topic: str, platform: str, tone: str, length: str = "medium", cta: str = "") -> list:
        pass