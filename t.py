import app
import app.data_cache as dc
from app.singleton import UNLOCK_ARG
class P: 
    p = 10
    def __init__(self, *args, name):
        self.args = args 
        print('calling __init__')
        self.name = name 
    def __new__(cls, *args, **kwargs):
        return app.quicksingleton( P, _init_lock = True ) 
    def __str__(self):
        return f'{self.args = }, {self.name = }'
    pass
print(P(1, 2, 3, name='k') is P(4, 5, 6, name='asdkla'))
P(5, 6, 7, name='kk12e', **{UNLOCK_ARG: True})
print( P.instance, P.__instance_calls )
print(dc.DataHandle() is dc.DataHandle())
class X: 
    def __init__(self):
        print('init calling ')
def dummy(ins):
    print('calling dummy')
    return 
