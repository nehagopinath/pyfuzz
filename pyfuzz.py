import time
import socket
import sys
from threading import Thread
from mem import Mem
from monitor import Monitor

#
# BASED ON KELINCI
#

class ApplicationCall:
  def __init__(self, path: str):
    self.path = path

  def __init__(self, bytes: bytearray):
    self.bytes = bytes

  def run(self):
    if (path != None):
      self.__run_application(self.path)
    else:
      self.__run_application(self.bytes)

  def __run_application(self, filename: str):
    # @todo: handle @@
    start_time = int(round(time.time() * 1000))
    # call wrapper python script
    crashed = not Monitor.run(filename, args)
    
    end_time = int(round(time.time() * 1000))
    self.exec_time = end_time - start_time

  def __run_application(self, bytes: bytearray):
	  # create tmp file
	  self.tmpfile = open("pyfuzz_input", wb)
	  self.tmpfile.write(bytes)
	  self.tmpfile.close()
		
	  self.__run_application("pyfuzz_input")

class FuzzRequest:
  def __init__(self, conn):
    self.conn = conn

class RequestQueue:
  def __init__(self):
    self.max_requests = 10
    self.fuzz_requests = []
    self.request_cnt = 0

  def offer(self, fuzz_request: FuzzRequest):
    if self.request_cnt < self.max_requests:
      self.fuzz_requests.append(fuzz_request)
      return True
    return False
        
  def poll(self):
    if self.request_cnt > 0:
      self.request_cnt = self.request_cnt - 1
      return self.fuzz_requets.pop()
    return None    

class Executor:
  def __init__(self, appCall: ApplicationCall):
    self.appCall = appCall
    self.thread = Thread(target=appCall.run, args=())
    
  def start(self):
    self.thread.start()
    
  def join(self, ms: int):
    self.thread.join(ms / 1000.0)
    if (self.thread.is_alive()):
      return False
    return True
    
  def shutdown(self):
    # @todo
    pass
    

STATUS_SUCCESS = 0
STATUS_TIMEOUT = 1
STATUS_CRASH = 2
STATUS_QUEUE_FULL = 3
STATUS_COMM_ERROR = 4
STATUS_DONE = 5
DEFAULT_TIMEOUT = 300000 # in milliseconds
timeout = DEFAULT_TIMEOUT

DEFAULT_VERBOSITY = 2
verbosity = DEFAULT_VERBOSITY

DEFAULT_PORT = 7007
port = DEFAULT_PORT
IP = '0.0.0.0'
BUFFER_SIZE = 1024

DEFAULT_MODE = 0
LOCAL_MODE = 1
mode = DEFAULT_MODE

requestQueue = RequestQueue()

args = []

class ServerThread(Thread):
  # accept TCP connections and put them in a queue
  def run(self):
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((IP, port))

    if verbosity > 1:
        print("Server listening on port " + str(port))

    while True:
        tcpServer.listen(BUFFER_SIZE)
        (conn, (client_ip, client_port)) = tcpServer.accept()

        if verbosity > 1:
            print("Connection established.")

        status = requestQueue.offer(FuzzRequest(conn))
        if status and verbosity > 1:
           print("Request added to queue: " + str(status))

        if not status:
            if verbosity > 1:
                print("Queue full.")
            conn.send(STATUS_QUEUE_FULL)
            conn.close()
            if verbosity > 1:
                print("Connection closed.")

class FuzzerThread(Thread):
  # run one request from the queue at a time
  def run(self):
      if verbosity > 1:
          print("Fuzzer runs handler thread started.")

      while (True):
          request = requestQueue.poll()
          if request != None:
              if verbosity > 1:
                  print("Handling request 1 of " + (requestQueue.size + 1))

              #InputStream is = request.clientSocket.getInputStream()
              #OutputStream os = request.clientSocket.getOutputStream()

              Mem.clear()

              result = STATUS_CRASH

              appCall = None

              # read the mode (local or default)
              mode = request.conn.read(1)

              # LOCAL MODE
              if mode == LOCAL_MODE:
                  if verbosity > 1:
                      print("Handling request in LOCAL MODE.")

                  # read the length of the path (integer)
                  #pathlen = is.read() | is.read() << 8 | is.read() << 16 | is.read() << 24
                  pathlen = int.from_bytes(int, request.conn.read(4), "LITTLE")
                  if verbosity > 2:
                      print("Path len = " + pathlen)

                  if pathlen < 0:
                      if verbosity > 1:
                          print("Failed to read path length")
                      result = STATUS_COMM_ERROR
                  else:
                      # read the path
                      input = []
                      read = 0
                      while read < pathlen:
                          if request.conn.available() > 0:
                              input[read] = request.conn.read(1)
                              read = read + 1
                          else:
                              if verbosity > 1:
                                  print("No input available from stream, strangely, breaking.")
                                  result = STATUS_COMM_ERROR
                                  break

                      path = string(input)
                      if verbosity > 1:
                          print("Received path: " + path)

                      appCall = ApplicationCall(path)


              # DEFAULT MODE
              else:
                  if (verbosity > 1):
                      print("Handling request in DEFAULT MODE.")

                  # read the size of the input file (integer)
                  #filesize = is.read() | is.read() << 8 | is.read() << 16 | is.read() << 24
                  filesize = int.from_bytes(int, request.conn.read(4), "LITTLE")
                  if (verbosity > 2):
                      print("File size = " + filesize)

                  if (filesize < 0):
                    if (verbosity > 1):
                      print("Failed to read file size")  
                    result = STATUS_COMM_ERROR
                  else:

                    # read the input file
                    input = bytestream(filesize)
                    read = 0
                    while read < filesize:
                      if request.conn.available() > 0:
                        input[read] = request.conn.read(1)
                        read = read + 1
                      else:
                        if (verbosity > 1):
                          print("No input available from stream, strangely")
                          print("Appending a 0")
                        
                        input[read] = 0
                        read = read + 1
                    
                    appCall = ApplicationCall(input)
              
              

              if (result != STATUS_COMM_ERROR and appCall != None):
                # run app with input
                #ExecutorService executor = Executors.newSingleThreadExecutor()
                #Future < Long > future = executor.submit(appCall)
                executor = Executor(appCall)
                try:
                  if (verbosity > 1):
                    print("Started...")
                  executor.start()
                  if (executor.join(timeout)): 
                    if (verbosity > 1):
                      print("Finished!")
                    if executor.crashed():
                      result = STATUS_CRASHED
                    else:
                      result = STATUS_SUCCESS
                  else:
                    result = STATUS_TIMEOUT
                    if (verbosity > 1):
                      print("Timeout!")
                except:
                  if (verbosity > 1):
                    print("Something didn't work!")
                  result = STATUS_CRASHED
                
                executor.shutdown()
            

              if (verbosity > 1):
                print("Result: " + result)

              if (verbosity > 2):
                Mem.print()
              # send back status
              os.write(result)
              # send back "shared memory" over TCP
              os.write(Mem.mem, 0, Mem.mem.length)
              # close connection
              os.flush()
              request.clientSocket.shutdownOutput()
              request.clientSocket.shutdownInput()
              request.clientSocket.setSoLinger(true, 100000)
              request.clientSocket.close()
              if (verbosity > 1):
                print("Connection closed.")
          else:
            # if no request, close your eyes for a bit
            time.sleep(0.10)
        
if __name__ == "__main__":

  if len(sys.argv) < 1:
    print("Invalid usage. Expected [-v N] [-p N] [-t N] python_script <args>")
    sys.exit(1)

  port = DEFAULT_PORT
  timeout = DEFAULT_TIMEOUT
  verbosity = DEFAULT_VERBOSITY

  curArg = 0
  while len(sys.argv) > curArg:
    if (sys.argv[curArg] == "-p") or (sys.argv[curArg] == "-port"):
      port = int(sys.argv[curArg + 1])
      curArg = curArg + 2
    else:
      if (sys.argv[curArg] == "-v") or (sys.argv[curArg] == "-verbosity"):
        verbosity = int(argv[curArg + 1])
        curArg = curArg + 2
      else:
        if (sys.argv[curArg] == "-t") or (sys.argv[curArg] == "-timeout"):
          timeout = Long.parseLong(args[curArg + 1])
          curArg += 2
        else:
          break

  target = sys.argv[curArg]
  # provide the target with only the command line arguments that are meant for it
  args = sys.argv[curArg + 1:]

  # @todo: maybe search for @@
  # @todo: maybe redirect outout do /dev/null in case verbosity <= 0

  # @todo: create tmp file to server as input for the target
        
  # start server thread
  server = ServerThread()
  server.start()    
        
  # start fuzzer thread
  fuzzer = FuzzerThread()
  fuzzer.start()

  while True:
    time.sleep(1)
