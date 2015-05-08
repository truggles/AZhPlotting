#!/usr/bin/env python

import argparse
import os
#import sys
from subprocess import call
import time

p = argparse.ArgumentParser(description="Target image path file (sans .txt): HTC_A510, SPH-D710VMUB, RAZR, SAMSUNG-SGH, standard")
p.add_argument("file", nargs=1,
               help="target image path file")
args = p.parse_args()
filename = args.file[0]

name = filename 
print "Created a folder for images: '%s' and a text output file with data logged: '%s_log.out'" % (name, name) 
#sys.stdout = open('%s_log.out' % name, 'w')

#name = '2013_02_21'
#name = 'ffffffff-cd8a'
#name = 'standard'
ifile = open('%s.txt' % name, 'r')

name = filename + 'small'

if not os.path.exists(name):
    os.makedirs(name)

now = time.strftime("%c")
print "Start date & time: " + now

for line_ in ifile:
    info = line_.split('/')
    #print info[-1]
    
    line = line_.strip()
    #print line
    #command = "./plotBlobs.py %s --contours 20 --min-area=10 --distance=40 --output=tester" % line
    #print command
    #call([command])
    outCommand = "--output=%s/image_%s" % (name, info[-1][:-5] )
    call(["./plotBlobs.py", line, "--contours=25", "--min-area=4.5", "--distance=40", outCommand])

now = time.strftime("%c")
print "Finish date & time: " + now
