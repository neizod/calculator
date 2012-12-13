import builtins

__all__ = ['int', 'float', 'complex']

def class_comparison(base, cmpr):
    ''' returns base >= cmpr under condition complex > float > int '''
    if isinstance(base, builtins.complex):
        return True
    if isinstance(cmpr, builtins.complex):
        return False
    if isinstance(base, builtins.float):
        return True
    if isinstance(cmpr, builtins.float):
        return False
    return True

def magic_setattr( cls, name, reflex=False, container=False,
                   specific=False, notint=False ):
    f = getattr(cls, name)
    def magic_function(self, *args, **kwargs):
        if specific:
            if name == '__int__':
                return int(f(self))
            if name == '__float__':
                return float(f(self))
        if not args and not kwargs:
            # unary op
            return cls(f(self))
        other, *others = args
        if not others:
            # binary op
            if class_comparison(self, other):
                if container:
                    return tuple(cls(x) for x in f(self, other))
                if notint and isinstance(self, builtins.int):
                    return float(f(self, other))
                return cls(f(self, other))
            sub_args = ('__r', '__', 1) if reflex else ('__', '__r', 1)
            g = getattr(other, f.__name__.replace(*sub_args))
            return g(self)
        # many args
        return cls(f(self, *args, **kwargs))
    setattr(cls, name, magic_function)

def magic_happens(cls):
    specific    = { '__int__', '__float__', }
    unary_oprt  = { '__abs__', '__hash__', '__neg__', '__pos__', '__sizeof__', }
    binary_oprt = { '__add__', '__floordiv__', '__mod__', '__mul__',
                    '__pow__', '__sub__', }
    reflex_oprt = { '__radd__', '__rmul__', '__rfloordiv__', '__rmod__',
                    '__rpow__', '__rsub__', }
    binary_cont = { '__divmod__', '__getnewargs__', }
    reflex_cont = { '__rdivmod__', }
    binary_nint = { '__truediv__', }
    reflex_nint = { '__rtruediv__', }

    if set(cls.__bases__) <= { builtins.int }:
        unary_oprt  |= { '__ceil__', '__floor__', '__index__', '__invert__', }
        binary_oprt |= { '__and__', '__or__', '__xor__', 
                         '__lshift__', '__rshift__', }
        reflex_oprt |= { '__rand__', '__ror__', '__rxor__', 
                         '__rlshift__', '__rrshift__', }
    if set(cls.__bases__) <= { builtins.int, builtins.float }:
        unary_oprt  |= { '__round__', '__trunc__', }

    for name in specific:
        magic_setattr(cls, name, specific=True)
    for name in unary_oprt:
        magic_setattr(cls, name)
    for name in binary_oprt:
        magic_setattr(cls, name, reflex=False)
    for name in reflex_oprt:
        magic_setattr(cls, name, reflex=True)
    for name in binary_cont:
        magic_setattr(cls, name, reflex=False, container=True)
    for name in reflex_cont:
        magic_setattr(cls, name, reflex=True, container=True)
    for name in binary_nint:
        magic_setattr(cls, name, reflex=False, notint=True)
    for name in reflex_nint:
        magic_setattr(cls, name, reflex=True, notint=True)

    return cls


@magic_happens
class int(builtins.int):
    def __call__(self, other):
        return self * other

@magic_happens
class float(builtins.float):
    def __call__(self, other):
        return self * other

@magic_happens
class complex(builtins.complex):
    def __call__(self, other):
        return self * other

