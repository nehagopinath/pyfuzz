#!/usr/bin/env python3

from test_proj.a import A
from test_proj.b import B

import sys

def f(x):
  if len(x) == 10:
    a = A()
    a.f1()
    
  else:
    if len(x) < 8:
      print("bla")
      b = B()
      b.f1(len(x))
    else:
      raise ValueError("sdsad")
      
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("invalid nr or arguments")
    sys.exit(0)
  file = open(sys.argv[1], "r")
  
  x = file.readline()
  
  f(x)
