import coverage
import sys
import runpy
import traceback
import os

from translator import Translator
from mem import Mem


class Monitor:
  @staticmethod
  def run(target: str, filename: str, args):
      # data_file=None, data_suffix=None, cover_pylib=None, auto_data=False, timid=None, branch=None, config_file=True, source=None, omit=None, include=None, debug=None, concurrency=None
      # @todo: move this in constructor
      # @todo: get source from params or cfg file
      data_file = ".coverage"
      data_suffix = None
      cover_pylib = False # measure also Python code within the interpreter
      auto_data = False
      timid = False
      branch = True
      config_file = False
      source = None #["pdfrw", os.path.dirname(target)]
      omit = None
      include = "*"
      debug = None
      concurrency = None
      
      cov = coverage.Coverage(data_file, data_suffix, cover_pylib, auto_data, timid, branch, config_file, source, omit)
      
      crashed = False
      
      _test = False
      if _test:
        sys.argv[1:] = args
        with open(filename, "rb") as f_r:
          with open("1.txt", "wb") as f_w:
            f_w.write(f_r.read())
      else:
        #target = sys.argv[1]
        # provide the target with only the command line arguments that are meant for it 
        sys.argv[1] = filename
        sys.argv[2:] = args
        
      #print("target: " + target)
      #print("old args: " + str(args))
      #print("new args: " + str(sys.argv))
      
      for i in range(0, 1): # @todo: maybe optimize here
        print ("Executing " + target)
        cov.erase()
        
        # run the target and catch exceptions
        try:
          #sys.argv[1] = str(i + 12) # test manu
          cov.start()
          ret_val = runpy.run_path(target, run_name="__main__") # @todo: maybe optimize here by reseting global variables (state)
          cov.stop() 
        except (KeyboardInterrupt, SystemExit) as e:
          cov.stop()
          print ("[ignoring KeyboardIntterupt or SystemExit]")
          if str(e) != "0":
            print ("Caught one!")
            crashed = True
        except:
          cov.stop()
          print ("Caught one!")
          traceback.print_exc()
          crashed = True
        covData = cov.get_data()
        print (covData.measured_files())
        
        """  
        covData = cov.get_data()
        translator = Translator()
        total_arcs = []
        for filename in covData.measured_files():
          #print (filename)
          arcs = covData.arcs(os.path.abspath(filename)) # @todo
          if len(arcs) < 1:
            continue
          if arcs is None:
            print ("arcs of " + filename + " missing!")
            return True
          else:
            total_arcs.append((filename, arcs))
            #print ("arcs: " + str(arcs))
        
        #print ("total arcs: " + str(total_arcs))      
        translator.onExecution(total_arcs)
        cov.save()
        """
        translator = Translator()
        translator.onExecution([])
        #_, executable_statements, excluded_statements, not_run_statements, missing = #cov.analysis2('/home/manu/TUM/sem2/graybox_fuzzing/pyfuzz/sandbox/test_code.py')

        #print ("executable_statements: ")
        #print (executable_statements)
        #print ("excluded_statements: ")
        #print (excluded_statements)
        #print ("not_run_statements: ")
        #print (not_run_statements)
        #print ("missing: ")
        #print (missing)
        
        
        #cov.html_report()
        #Mem.print()
        
        return not crashed
