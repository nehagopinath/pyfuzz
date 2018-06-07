#!/usr/bin/env python

from sys import argv,exit,stdout
from os import listdir,system,path
import os
import sys


OPTIONS = {"commandline": False, "html": False,"findings": False}

def printBanner():
	print "welcome to pyfuzz-resRep"

printBanner()

# Parse options
for c in range(len(argv)):
    arg = argv[c]
    if arg == "-c" or arg == "--commandLine":
        OPTIONS["commandline"] = True
    elif arg == "-h" or arg == "--html":
        try:
            OPTIONS["html"] = argv[c+1]
        except:
            print "\n\nERROR: No output directory specified for --html option!"
            exit()
    
OPTIONS["findings"] = argv[-1]

# Logic checks
if OPTIONS["commandline"] == False and OPTIONS["html"] == False:
    print "\n\nERROR: Need to specify at least one output method (-c | -h )!"
    exit()

if OPTIONS["html"]:
    try:
        listdir(OPTIONS["html"])
    except:
        print "\n\nERROR: Cannot access HTML output folder!"
        exit()

try:
    listdir(OPTIONS["findings"])
except:
    
    print "\n\nERROR: Cannot access findings_directory!"
    exit()


if OPTIONS["html"]:
	cmd = './afl-plot' #afl-plot code taken from afl-fuzz master
	so = os.popen(cmd).read()
	print so

elif OPTIONS["commandline"]:
	output=sys.argv[2]
	out=open(output+"/fuzzer_stats","r").read()
	print out



