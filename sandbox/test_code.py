#!/usr/bin/env python3

import sys

def f(x):
  if x == 3:
    print ("==3")
    print ("bla")
  else:
    if x > 12:
      print (">12")
    else:
      raise ValueError(">3 && <= 12")

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("invalid nr or arguments")
    sys.exit(0)
  file = open(sys.argv[1], "r")
  x = int(file.read())
  f(x)

