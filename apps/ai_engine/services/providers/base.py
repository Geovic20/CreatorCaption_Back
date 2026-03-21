from abc import ABC, abstractmethod


class BaseAIProvider(ABC):

    @abstractmethod
    def generate_captions(self, topic: str, platform: str, tone: str) -> list:
        pass