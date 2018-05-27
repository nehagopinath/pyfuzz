#!/usr/bin/env python3

import sys

def f(x):
  if x == 3:
    print ("==3")
  else:
    if x > 12:
      print (">12")
    else:
      raise ValueError(">3 && <= 12")

if __name__ == "__main__":
  f(int(sys.argv[1]))

