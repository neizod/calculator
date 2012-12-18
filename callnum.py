import builtins

__all__ = ['int', 'float', 'complex', 'builtins_name']

builtins_name = ['real', 'imag', 'conjugate', 'phi']

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
    if isinstance(cmpr, builtins.int):
        return True
    # since python can manipulate string w/ num, like 5*'-'
    # False must be returns to prevent conflict.
    return False

def magic_setattr( cls, name, reflex=False, container=False,
                   specific=False, notint=False ):
    f = getattr(cls, name)
    def magic_method(self, *args, **kwargs):
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
    setattr(cls, name, magic_method)

def magic_happens(cls):
    unary_oprt  = { '__abs__', '__hash__', '__neg__', '__pos__', '__sizeof__', }
    binary_oprt = { '__add__', '__floordiv__', '__mod__', '__mul__',
                    '__pow__', '__sub__', }
    reflex_oprt = { '__radd__', '__rmul__', '__rfloordiv__', '__rmod__',
                    '__rpow__', '__rsub__', }
    binary_cont = { '__divmod__', '__getnewargs__', }
    reflex_cont = { '__rdivmod__', }
    binary_nint = { '__truediv__', }
    reflex_nint = { '__rtruediv__', }
    specific    = { '__int__', '__float__', }

    if set(cls.__bases__) <= { builtins.int }:
        unary_oprt  |= { '__ceil__', '__floor__', '__index__', '__invert__', }
        binary_oprt |= { '__and__', '__or__', '__xor__', 
                         '__lshift__', '__rshift__', }
        reflex_oprt |= { '__rand__', '__ror__', '__rxor__', 
                         '__rlshift__', '__rrshift__', }
    if set(cls.__bases__) <= { builtins.int, builtins.float }:
        unary_oprt  |= { '__round__', '__trunc__', }

    magic_types = [ (unary_oprt,  {}),
                    (binary_oprt, {'reflex': False}),
                    (reflex_oprt, {'reflex': True}),
                    (binary_cont, {'reflex': False, 'container': True}),
                    (reflex_cont, {'reflex': True,  'container': True}),
                    (binary_nint, {'reflex': False, 'notint': True}),
                    (reflex_nint, {'reflex': True,  'notint': True}),
                    (specific,    {'specific': True}), ]

    for names, flag in magic_types: 
        for name in names:
            magic_setattr(cls, name, **flag)

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


def real(x):
    return type(x)(x.real)

def imag(x):
    return type(x)(x.imag)

def conjugate(x):
    return float(x.conjugate())


def duality(value):
    def hook_call(func):
        class Duality(type(value)):
            def __call__(self, other):
                return func(self, other)
        return Duality(value)
    return hook_call

@duality((1 + 5**0.5) / 2)
def phi(self, n):
    n = abs(n)
    if 0 <= n <= 1:
        return 1
    p = 2
    r = 1
    while n != 1:
        if p ** 2 > n:
            r *= n - 1
            break
        k = 0
        while not n % p:
            k += 1
            n //= p
        if k:
            r *= p - 1
            r *= p ** (k - 1)
        p += 1 # actuly the next prime
    return int(r)

