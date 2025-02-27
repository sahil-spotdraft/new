
from threading import Thread

from SingletonPattern.singleton import Singleton, ThreadSafeSingleton


def test_thread_safe_singleton(val) -> None:
    obj = ThreadSafeSingleton(val)
    obj.display()

def test_thread_unsafe_singleton(val) -> None:
    obj = Singleton(val)
    obj.display()


class SingletonExample:
    @staticmethod
    def run():
        print("\n=====Execution of SingletonExample example=====")
        obj1 = Singleton("foo")
        obj2 = Singleton("foo")
        print(id(obj2) == id(obj1))
        # process1 = Thread(target=test_thread_unsafe_singleton, args=("foo",))
        # process2 = Thread(target=test_thread_unsafe_singleton, args=("bar",))
        # process1.start()
        # process2.start()


        process1 = Thread(target=test_thread_safe_singleton, args=("foo",))
        process2 = Thread(target=test_thread_safe_singleton, args=("bar",))
        process1.start()
        process2.start()