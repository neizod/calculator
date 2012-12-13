#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tokenize import tokenize, untokenize, NUMBER, STRING, NAME, OP
from io import BytesIO
import callnum

__all__ = ['interact']

def numeric_type(tokval):
    return 'complex' if 'j' in tokval else 'float' if '.' in tokval else 'int'

def hook_callable_number(s):
    result = []
    g = tokenize(BytesIO(s.encode('utf-8')).readline)
    for toknum, tokval, _, _, _  in g:
        if toknum == NUMBER:
            result.extend([ (NAME, 'callnum'),
                            (OP, '.'),
                            (NAME, numeric_type(tokval.lower())),
                            (OP, '('),
                            (NUMBER, tokval),
                            (OP, ')'), ])
        else:
            result.append((toknum, tokval))
    return untokenize(result).decode('utf-8')

def input_with_callable_number(prompt=''):
    return hook_callable_number(input(prompt))

def interact( banner   = 'calculator the right way',
              readfunc = input_with_callable_number,
              local    = { '__name__': '__calculator__',
                           '__doc__':  None,
                           'callnum':  callnum, }, ):
    ''' Start interactive Python-base calculator. '''
    from code import interact
    import readline
    return interact(banner, readfunc, local)

if __name__ == '__main__':
    interact()

