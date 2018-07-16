from mem import Mem
import crc16


class Translator:
  #mem = None
  def __init__(self):
    #mem = Mem()
    self.file_switching_list = []
    self.switching_file = None
    self.last_switch_cnt = -1
    pass
    
  def __computeLocationId(self, filename, line):
    # returns a pseudounique id between 0 and Mem.SIZE
    # for now Mem.SIZE is 65536
    return int(crc16.crc16xmodem(str.encode(filename + str(line))))
    
  # call at start of functions, labels (also else) and after jumps  
  def __instrumentLocation(self, filename, line):
    # Mem.mem[id^Mem.prev_location]++;
    # Mem.prev_location = id >> 1;
    
    
    id = self.__computeLocationId(filename, line)
    
    #print("instrumenting " + filename + ": " + str(line) + " -> " + str(id))    
    
    Mem.mem[id^Mem.prev_location] = Mem.mem[id^Mem.prev_location] + 1
    Mem.prev_location = id >> 1;

  def __parse_file_switching_log(self):
    # filename\n | entry line | switch cnt
    # var        | 4B         | 4B
    
    # split the content of this file into a list of dicts of form {filename, [switching_indexes]} 
    while True:
      file_from_b = self.switching_file.readline()
      if file_from_b == b'':
        break
      file_from = file_from_b.decode()
      file_from = file_from.strip()
      
      entry_line = int.from_bytes(self.switching_file.read(4), "little")
      switch_cnt = int.from_bytes(self.switching_file.read(4), "little")
      #print(file_from)
      #print(str(entry_line))
      #print(str(switch_cnt))
      found = False
      #print ("comparing " + file_from)
      for (filename, entry_lines) in self.file_switching_list:
        ##print("comparing against " + filename)
        if filename == file_from:
          entry_lines.append((entry_line, switch_cnt))
          found = True
          break
      if found is False:
        self.file_switching_list.append((file_from, [(entry_line, switch_cnt)]))
    #for (file_from, line_indexes, _) in self.file_switching_list:
    #print ("------ " + file_from + ": " + str(line_indexes))
  
  
  def __next_execution_index(self, filename):
    #print("here: " + filename)
    for (file_from, switch_points) in self.file_switching_list:
      if filename == file_from:
        last_cheched_switch_cnt = -1
        for (line_indexes, switch_cnt) in switch_points:
          if switch_cnt > self.last_switch_cnt:
            self.last_switch_cnt = switch_cnt
            return switch_cnt
          last_cheched_switch_cnt = switch_cnt  
         
        #print ("index not found " + str(self.last_switch_cnt) + " for file " + filename + " with " + str (switch_points))
        return last_cheched_switch_cnt
    #print ("filename not found " + filename)      
    return -1 # filename not found

  def onExecution(self, path_arcs):    
    self.switching_file = open("/tmp/file_switching.log", "rb")
    
    self.__parse_file_switching_log()
    
    self.switching_file.close()
    
    assert(len(self.file_switching_list) > 0), "missing the execution path"
    
    total_path = [None] * len(self.file_switching_list)
    execution_index = -1
    
    
    # the lines must be instrumented in their execution order
    # python coverage provides an ordered list of arcs per file, not per process
    
    # take list of arcs per file, split them per execs, and reorder them chronologically
    is_in_file = False
    for (filename, file_arcs) in path_arcs:
      current_path = []
      for (src, dst) in file_arcs:
        if src >= 0:
          current_path.append((filename, src))
          # normal arc or exit point
          if dst < 0:
            # exit point
            is_in_file = False
            if execution_index >= 0:
              total_path.insert(execution_index, current_path)
            current_path = []
          else:
            # normal arc
            pass        
        else:
          # entry point
          current_path.append((filename, -1 * src))
        
          if is_in_file is False:
            is_in_file = True
            # read execution_index
            execution_index = self.__next_execution_index(filename)
            #assert(execution_index >= 0), "negative execution index"
    
    # compress total_path
    # total_path is at this point a list of lists containing arcs, ordered
    #print(str(total_path))
    for path in total_path:
      if path is None:
        continue # this file was ignored
      for (filename, line_nr) in path:
        self.__instrumentLocation(filename, line_nr)
    
  
