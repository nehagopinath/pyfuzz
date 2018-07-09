#
# Based on mem.java from kelinci
# "Class to record branching, analogous to the shared memory in AFL.
# 
# Because we measure inside a particular target method, we need
# a way to start/stop measuring. Therefore, the array can be cleared.
# 
# @author rodykers
# "

class Mem:
  SIZE = 65536
  mem = bytearray(SIZE)
  prev_location = 0
	
	#def __init__(self):
	#  self.clear()
	
	# Clears the current measurements.
  @staticmethod
  def clear():
    for i in range(0, Mem.SIZE):
      Mem.mem[i] = 0
	
  # Prints to stdout any cell that contains a non-zero value.
  @staticmethod
  def print():
    for i in range(0, Mem.SIZE):
      if Mem.mem[i] != 0:
        print (str(i) + ": " + str(Mem.mem[i]))
