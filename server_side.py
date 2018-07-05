import time
import socket
import sys
from threading import Thread

#
# BASED ON KELINCI
#

class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port

    def run(self):
        while True:
            data = conn.recv(2048)

            conn.send(resp)


# for t in threads:
#      t.join()




class ApplicationCall:
    def __init__(self, path):
        self.path = path

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
            self.fuzz_requests.add(fuzz_request)
            return True
        return False

class Mem:
    def __init__(self):
        pass
    def clear(self):
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

# accept TCP connections and put them in a queue
def run_server():
    tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpServer.bind((IP, port))
    threads = []
    if verbosity > 1:
        print("Server listening on port " + port)

    while True:
        tcpServer.listen(BUFFER_SIZE)
        (conn, (client_ip, client_port)) = tcpServer.accept()

        if verbosity > 1:
            print("Connection established.")

        requestQueue = RequestQueue()
        status = requestQueue.offer(FuzzRequest(conn))
        if status and verbosity > 1:
           print("Request added to queue: " + status)

        if not status:
            if verbosity > 1:
                print("Queue full.")
            conn.send(STATUS_QUEUE_FULL)
            conn.close()
            if verbosity > 1:
                print("Connection closed.")


def run_application(filename):
    # @todo: handle @@
    start_time = int(round(time.time() * 1000))
    # @todo: call wrapper python script
    end_time = int(round(time.time() * 1000))
    return end_time - start_time


# @todo: run_application with byte[]

# run one request from the queue at a time
def do_fuzzer_runs():
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
            
            

            if (result != STATUS_COMM_ERROR && appCall != None):
              # run app with input
              ExecutorService executor = Executors.newSingleThreadExecutor()
              Future < Long > future = executor.submit(appCall)

              try:
                if (verbosity > 1):
                  print("Started...")
                future.get(timeout, TimeUnit.MILLISECONDS)
                result = STATUS_SUCCESS
                if (verbosity > 1):
                  print("Finished!")
              catch (TimeoutException te):
                future.cancel(true)
                if (verbosity > 1):
                  print("Time-out!")
                  result = STATUS_TIMEOUT
              catch (Throwable e):
                future.cancel(true)
                if (e.getCause() instanceof RuntimeException):
                  if (verbosity > 1):
                    print("RuntimeException thrown!")
                else:
                  if (e.getCause() instanceof Error):
                    if (verbosity > 1):
                      print("Error thrown!")
                  else:
                    if (verbosity > 1):
                      print("Uncaught throwable!")
                  
                e.printStackTrace()
              }
              executor.shutdownNow()
          

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
          Thread.sleep(100)
        
   if __name__ == "__main__":

        if len(sys.argv) < 1:
          print("Invalid usage. Expected [-v N] [-p N] [-t N] python_script <args>")
          sys.exit(1)

        port = DEFAULT_PORT
        timeout = DEFAULT_TIMEOUT
        verbosity = DEFAULT_VERBOSITY

        curArg = 0
        while len(sys.argv) > curArg):
            if (sys.argv[curArg] == "-p") || (sys.argv[curArg] == "-port"):
              port = int(sys.argv[curArg + 1])
              curArg = curArg + 2
            else:
              if (sys.argv[curArg] == "-v") | | (sys.argv[curArg] == "-verbosity"):
                  verbosity = int(argv[curArg + 1])
              curArg = curArg + 2
              else:
                if (sys.argv[curArg] == "-t") | | (sys.argv[curArg] == "-timeout"):
                    timeout = Long.parseLong(args[curArg + 1])
                curArg += 2
                else:
                break

        target = argv[curArg]
        # provide the target with only the command line arguments that are meant for it
        targetArgs = argv[curArgv + 1:]

# @todo: maybe search for @@
# @todo: maybe redirect outout do /dev/null in case verbosity <= 0

# create tmp file to server as input for the target
# start server thread
# start fuzzer thread


