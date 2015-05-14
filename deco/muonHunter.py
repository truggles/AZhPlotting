#!/usr/bin/env python

import argparse
import os
from subprocess import call
import time

p = argparse.ArgumentParser(description="Target image path file (sans .txt): HTC_A510, SPH-D710VMUB, RAZR, SAMSUNG-SGH, standard")
p.add_argument("file", nargs=1,
               help="target image path file")
args = p.parse_args()
filename = args.file[0]

name = filename 
print "Created a folder for images: '%s'" % name 

ifile = open('%s.txt' % name, 'r')

if not os.path.exists(name):
    os.makedirs(name)

now = time.strftime("%c")
print "Start date & time: " + now

for line_ in ifile:
    info = line_.split('/')
    line = line_.strip()
    outCommand = "--output=%s/image_%s" % (name, info[-1][:-5] )
    call(["./plotBlobs.py", line, "--contours=25", "--min-area=4.5", "--distance=40", outCommand])

now = time.strftime("%c")
print "Finish date & time: " + now
