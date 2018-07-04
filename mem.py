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
  def clear(self):
    for i in range(0, self.SIZE):
      self.mem[i] = 0
	
  # Prints to stdout any cell that contains a non-zero value.
  def print(self):
    for i in range(0, self.SIZE):
      if self.mem[i] != 0:
        print (str(i) + ": " + str(self.mem[i]))
