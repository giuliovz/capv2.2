from abc import ABC, abstractmethod



class ExtratorBase(ABC):


    @abstractmethod
    def extrair(self, texto, link):

        pass