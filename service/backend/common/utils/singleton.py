class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs): #__call__ in cls!!
        if cls not in cls._instances:
            cls._instances[cls] = super()._call__(*args, **kwargs)
        return cls._instances[cls]