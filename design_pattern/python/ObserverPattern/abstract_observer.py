import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ObserverPattern.abstract_observable import AbstractObservable


class AbstractObserver(abc.ABC):
    @abc.abstractmethod
    def update(self, obs: "AbstractObservable", *args, **kwargs):
        pass