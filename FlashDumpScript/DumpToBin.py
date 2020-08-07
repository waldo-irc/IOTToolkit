#!/usr/bin/env python3
import os, sys

if len(sys.argv) < 2:
	print("Must provide a file to read.")
	print("EX: ./%s firmware.txt" % sys.argv[0])
	exit(0)

def ReadAndPipe(filename):
	with open(filename,"r") as myfile:
		data = myfile.read().split()

		full = ''
		for line in data:
			byte = line.split(':')[1]
			full+='\\x'+byte

		with open("FinalPipe.py","w+") as myfile:
			myfile.write("#!/usr/bin/env python3\n\n")
			myfile.write('data = "%s"\n' % full)
			myfile.write('print(data)')

	os.system("python FinalPipe.py > firmware.bin")
	os.system("rm FinalPipe.py")
	#Remove Newline at end, last point should be 1FFFFF not 200000
	os.system("truncate -s -1 firmware.bin")
	os.system("chmod +x firmware.bin")
	print("firmware.bin Created!")

ReadAndPipe(sys.argv[1])
