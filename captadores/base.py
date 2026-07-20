from abc import ABC, abstractmethod


class CaptadorBase(ABC):


    def __init__(
        self,
        nome,
        url
    ):

        self.nome = nome

        self.url = url



    @abstractmethod
    def capturar(self):

        pass



    def informacao(self):

        return {

            "portal": self.nome,

            "url": self.url

        }