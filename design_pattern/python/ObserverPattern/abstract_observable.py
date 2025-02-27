import abc
from typing import List

from ObserverPattern.abstract_observer import AbstractObserver


class AbstractObservable(abc.ABC):
    def __init__(self):
        self.observers: List[AbstractObserver] = []

    @abc.abstractmethod
    def addObservers(self, observers: List[AbstractObserver]):
        pass

    @abc.abstractmethod
    def removeObservers(self, observers: List[AbstractObserver]):
        pass

    @abc.abstractmethod
    def notifyObservers(self):
        pass