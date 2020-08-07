#!/usr/bin/env python3
import sys
import DumpCheckLib

if len(sys.argv) < 2:
	print('Must provide a filename as an argument.')
	print('EX: ./%s firmware_test.txt' % sys.argv[0])
	exit(0)

with open(sys.argv[1],"r") as myfile:
	file_data = myfile.read()
	if not DumpCheckLib.checkContent(file_data,0,True):
		print("BAD SHIT")
	else:
		print("GOOD SHIT")
