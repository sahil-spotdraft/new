from threading import Lock


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def __init__(self, value: str) -> None:
        self.value = value

    def display(self):
        print(self.value)


class ThreadSafeSingletonMeta(type):
    _instances = {}

    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class ThreadSafeSingleton(metaclass=ThreadSafeSingletonMeta):
    def __init__(self, value: str) -> None:
        self.value = value

    def display(self):
        print(self.value, id(self))