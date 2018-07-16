#!/usr/bin/env python3

import sys

def f(x):
  if len(x) == 10:
    raise ValueError(">3 && <= 12")
  else:
    if len(x) < 8:
      print("bla")
    else:
      raise ValueError("sdsad")
      
if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("invalid nr or arguments")
    sys.exit(0)
  file = open(sys.argv[1], "r")
  
  x = file.readline()
  
  f(x)

