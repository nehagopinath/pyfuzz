import coverage
import sys
import runpy
import traceback

from translator import Translator
from mem import Mem

if __name__ == "__main__":

  if len(sys.argv) < 2:
     print ("Invalid usage. Please provide the target python code!")
     sys.exit(1)
     
  # data_file=None, data_suffix=None, cover_pylib=None, auto_data=False, timid=None, branch=None, config_file=True, source=None, omit=None, include=None, debug=None, concurrency=None
  data_file = ".coverage"
  data_suffix = None
  cover_pylib = False # measure also Python code within the interpreter
  auto_data = True
  timid = False
  branch = True
  cov = coverage.Coverage(data_file, data_suffix, cover_pylib, auto_data, timid, branch)
  
  
  target = sys.argv[1]
  # provide the target with only the command line arguments that are meant for it 
  sys.argv[1:] = sys.argv[2:]
    
  
  for i in range(0, 1): # test manu
    print ("Executing " + sys.argv[1])
    cov.erase()
    
    # run the target and catch exceptions
    try:
      #sys.argv[1] = str(i + 12) # test manu
      cov.start()
      runpy.run_path(target, run_name="__main__")
      cov.stop() 
    except (KeyboardInterrupt, SystemExit):
      cov.stop()
      print ("[ignoring KeyboardIntterupt or SystemExit]")
      
    except:
      cov.stop()
      print ("Caught one!")
      traceback.print_exc()
      
    covData = cov.get_data()
    arcs = covData.arcs('/home/manu/TUM/sem2/graybox_fuzzing/pyfuzz/sandbox/test_code.py')
    print (arcs)
    #cov.save()
    
    _, executable_statements, excluded_statements, not_run_statements, missing = cov.analysis2('/home/manu/TUM/sem2/graybox_fuzzing/pyfuzz/sandbox/test_code.py')

    print ("executable_statements: ")
    print (executable_statements)
    #print ("excluded_statements: ")
    #print (excluded_statements)
    #print ("not_run_statements: ")
    #print (not_run_statements)
    #print ("missing: ")
    #print (missing)
    
    translator = Translator()
    translator.onExecutedPath(target, arcs)
    
    #cov.html_report()
    mem = Mem()
    mem.print()
