
class DataHandle:
    instance : 'DataHandle' = None
    def __init__(self, *args, **kw):
        self.args = args
        self.kw = kw 
    def __str__(self):
        return f'{self.args = }, {self.kw = }'
    def __new__(cls, *a, **kw):
        if cls.instance is None:
            cls.instance = super().__new__( cls )
        return cls.instance


p = DataHandle(1, 2, p=2)
p2 = DataHandle(15, 2, p=10)

print(str(p), str(p2))
