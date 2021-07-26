import threading, multiprocessing

class CThread(threading.Thread):
    def __init__(self, target, name: str) -> None:
        super().__init__(target=target, name=name)

def Thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
    return wrapper

MULTI_MANAGER = multiprocessing.Manager()
MULTI_DATA = MULTI_MANAGER.dict({})