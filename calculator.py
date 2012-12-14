#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP, NEWLINE
from io import BytesIO

import builtins
import callnum

__all__ = ['interact']

# hook into builtins
builtins.real = lambda x: type(x)(x.real)
builtins.imag = lambda x: type(x)(x.imag)
builtins.conjugate = lambda x: type(x)(x.conjugate()) # XXX
# conjugate int, float -> self // complex -> complex

def numeric_type(tokval):
    tokval = tokval.lower()
    return 'complex' if 'j' in tokval else 'float' if '.' in tokval else 'int'

def hook_callable_number(string):
    # since Untokenize.compat() ignore INDENT, unless there exists NEWLINE.
    # initialize result with NEWLINE is a must. (then remove it at returns).
    result = [(NEWLINE, '\n')]
    g = tokenize(BytesIO(string.encode('utf-8')).readline)
    for toknum, tokval, _, _, _  in g:
        if toknum == NUMBER:
            result.extend([ (NAME, 'callnum'),
                            (OP, '.'),
                            (NAME, numeric_type(tokval)),
                            (OP, '('),
                            (NUMBER, tokval),
                            (OP, ')'), ])
        else:
            result.append((toknum, tokval))
    return untokenize(result).decode('utf-8').replace('\n', '', 1)

def input_with_callable_number(prompt=''):
    return hook_callable_number(input(prompt))

def interact( banner   = 'calculator the right way',
              readfunc = input_with_callable_number,
              local    = { '__name__': '__calculator__',
                           '__doc__':  None,
                            '__builtins__': builtins,
                           'callnum':  callnum, }, ):
    ''' Start interactive Python-base calculator. '''
    from code import interact
    import readline
    return interact(banner, readfunc, local)

if __name__ == '__main__':
    interact()

