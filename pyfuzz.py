import coverage
import sys
import runpy
import traceback

if __name__ == "__main__":

  if len(sys.argv) < 2:
     print("Invalid usage. Please provide the target python code!")
     sys.exit(1)
     
  data_file = ".coverage"
  cover_pylib = False # measure also Python code within the interpreter
  auto_data = True
  timid = False
  branch = True
  cov = coverage.Coverage(data_file, cover_pylib, auto_data, timid, branch)
  cov.start()

  print("Executing " + sys.argv[1])
  
  target = sys.argv[1]
  # provide the target with only the command line arguments that are meant for it 
  sys.argv[1:] = sys.argv[2:]
  
  # run the target and catch exceptions
  try:
    runpy.run_path(target, run_name="__main__") 
  except (KeyboardInterrupt, SystemExit):
    print ("[ignoring KeyboardIntterupt or SystemExit]")
  except:
    print ("Cought one!")
    traceback.print_exc()
  cov.stop()
  cov.save()

  cov.html_report()
