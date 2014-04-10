#!/usr/bin/env python

import zerorpc
import nltk

from types import ModuleType

def rpcize(module, join='_'):
  result = {}

  for name, value in module.__dict__.items():
    if name.startswith('_'): continue

    if callable(value):
      result[name] = value
    elif isinstance(value, ModuleType) and (value.__package__ or '').startswith(module.__package__ + '.'):
      result.update(dict(
        (name + join + subname, subvalue)
      for subname, subvalue in rpcize(value, join).items()))
    else:
      result[name] = lambda: value

  return result

s = zerorpc.Server(rpcize(nltk))
s.bind("tcp://127.0.0.1:4242")
s.run()
