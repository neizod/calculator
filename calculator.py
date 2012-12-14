#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tokenize import tokenize, untokenize, TokenError, NUMBER, NAME, OP, NL
from io import BytesIO

import builtins
import callnum

__all__ = ['interact']

def hook_builtins(func):
    setattr(builtins, func.__name__, func)

@hook_builtins
def real(x):
    return type(x)(x.real)

@hook_builtins
def imag(x):
    return type(x)(x.imag)

@hook_builtins
def conjugate(x):
    return type(x)(x.conjugate())

def numeric_type(tokval):
    tokval = tokval.lower()
    return 'complex' if 'j' in tokval else 'float' if '.' in tokval else 'int'

def hook_callable_number(string):
    # since Untokenize.compat() ignore INDENT, unless there exists NL.
    # initialize result with NL is a must. (then remove it at returns).
    result = [(NL, '\n')]
    token_sequence = tokenize(BytesIO(string.encode('utf-8')).readline)
    try:
        for toknum, tokval, _, _, _  in token_sequence:
            if toknum == NUMBER:
                result.extend([ (NAME, 'callnum'),
                                (OP, '.'),
                                (NAME, numeric_type(tokval)),
                                (OP, '('),
                                (NUMBER, tokval),
                                (OP, ')'), ])
            else:
                result.append((toknum, tokval))
    except TokenError:
        pass
    return untokenize(result).decode('utf-8').replace('\n', '', 1)

def input_with_callable_number(prompt=''):
    return hook_callable_number(input(prompt))

def interact( banner   = 'Calculator the Right Way',
              readfunc = input_with_callable_number,
              local    = { '__name__':      '__calculator__',
                           '__doc__':       None,
                            '__builtins__': builtins,
                           'callnum':       callnum, }, ):
    ''' Start interactive Python-base calculator. '''
    from code import interact
    import readline
    return interact(banner, readfunc, local)

if __name__ == '__main__':
    interact()

