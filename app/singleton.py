UNLOCK_ARG = '__unlock'

def __initlock_build(__initfun):
    cache = __initfun
    def __lock(ins, *args, **kwargs):
        if kwargs.get( UNLOCK_ARG, False):
            kwargs.pop(UNLOCK_ARG)
            return cache(ins, *args, **kwargs)
    return __lock
def quicksingleton( cls: object, prop_name = 'instance', 
                    _init_lock = False,
                    ): #NO SUPP 4 CHDR CLASSES
    
    issetprop = getattr(cls, prop_name, None)
    if (issetprop is None):
        setattr(cls, prop_name, object.__new__( cls ))
        setattr(cls, '__instance_calls', 1)        
    else:
        if _init_lock and getattr(cls, '__instance_calls', 0) == 1:
            cls.__init__ = __initlock_build( cls.__init__ )
            setattr(cls, '__instance_calls', 2)
            
    return getattr( cls, prop_name )


