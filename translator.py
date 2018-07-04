from mem import Mem
import crc16

class Translator:
  #mem = None
  def __init__(self):
    #mem = Mem()
    pass
    
  def __computeLocationId(self, filename, line):
    # returns a pseudounique id between 0 and Mem.SIZE
    # for now Mem.SIZE is 65536
    return int(crc16.crc16xmodem(str.encode(filename + str(line))))
    
  # call at start of functions, labels (also else) and after jumps  
  def instrumentLocation(self, filename, line):
    # Mem.mem[id^Mem.prev_location]++;
    # Mem.prev_location = id >> 1;
    
    
    id = self.__computeLocationId(filename, line)
    
    print("instrumenting " + filename + ": " + str(line) + " -> " + str(id))    
    
    Mem.mem[id^Mem.prev_location] = Mem.mem[id^Mem.prev_location] + 1
    Mem.prev_location = id >> 1;

  def onExecutedPath(self, filename, path_arcs):
    path = []
    
    for (src, dst) in path_arcs:
      # @todo: handle negative indexes (external locations) if needed (if they are not handled in their respective file
      if src >= 0:
        path.append(src)
      
    
    for line in path:
      self.instrumentLocation(filename, line)
    
  
