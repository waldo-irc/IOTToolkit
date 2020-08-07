#!/usr/bin/env python3
#Pip installs
import serial
##Regular TQDM Progress Bar
from tqdm import tqdm
##Experimental TQDM Gui
from tqdm import tqdm_gui
import warnings
warnings.simplefilter("ignore")
#Builtins
import os, argparse
from datetime import datetime, date, time, timedelta
from time import sleep
#Custom Libs
import DumpCheckLib

#TODO
##Args for Chunk Size and total size or chunk size and chunk how many times, can calculate number of chunks by TOTALSIZE/CHUNKSIZE
##Also allow to start at chunk # vs offset
##Automatically do a final file check and pipe to the final bin
##Add logging

#Arguments Check
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='filename', type=str, nargs='+', help='A filename to dump firmware to.')
parser.add_argument('-w', help="Clear file and re-write.", dest="overwrite", action="store_true", default=False)
parser.add_argument('-o', type=int, help="Start at a specific offset. [DEFUALT:0]", dest="offset", action="store", default=0)
args = parser.parse_args()

##Ensure user is root
user = os.getenv("SUDO_USER")
if user is None:
    print("This program needs 'sudo' access.")
    exit(0)

##FileName Argument
filename = args.filename[0]

##Empty File if command line arg 2 is w
if args.overwrite:
	print('Clearing file...')
	with open(filename, "w+") as myfile:
		myfile.write('')

print("Starting at offset %s...." % str(args.offset))

#Open Serial Connection
jtagulator = serial.Serial('/dev/ttyUSB0', 115200)

def enter_uart(jtagulator,voltage="3.3",tx="2",rx="1",baud="38400"):
	#First we enter the UART passthrough to the Target Device if Required
	##Write
	jtagulator.write(b'?\r\n')
	jtagulator.write(b"U\r\n")
	jtagulator.write(b"V\r\n")
	jtagulator.write(b"%s\r\n" % voltage)
	jtagulator.write(b"p\r\n")
	jtagulator.write(b"%s\r\n" % tx)
	jtagulator.write(b"%s\r\n" % rx)
	jtagulator.write(b"%s\r\n" % baud)
	jtagulator.write(b"N\r\n")
	##Read and print
	c = jtagulator.read()
	sleep(1)
	data_left=jtagulator.inWaiting()
	rcvd = c+jtagulator.read(data_left)
	return rcvd.decode()

def chunk(jtagulator,offset,length):
	y=0
	chunk=''
	starting_offset = offset
	#Read each line for this chunk
	while y < length:
		y+=1
		reading = jtagulator.readline().decode().strip('\r').strip('\n')
		len(reading)
		if len(reading) == 0 or reading[0] == '#':
			y-=1
			continue
		offset += 1
		chunk+=reading+'\n'

	#Verify Chunk
	verify = DumpCheckLib.checkContent(chunk,starting_offset)
	if not verify:
		return False, starting_offset
	else:
		return chunk, offset

def avg_time(datetimes):
	#total = sum((dt.seconds/3600) * 3600 + (dt.seconds/60) * 60 + dt.seconds for dt in datetimes)
	total = sum(dt.seconds for dt in datetimes)
	avg = total / len(datetimes)
	minutes, seconds = divmod(int(avg), 60)
	hours, minutes = divmod(minutes, 60)
	return datetime.combine(date(1900, 1, 1), time(hours, minutes, seconds))

#At this point we are in the UART Serial Console
##Set our variables
x=0
length = 4096
num_chunks = 512

input_offset = args.offset
target_chunk = int(input_offset/length)
offset = target_chunk*length
num_chunks-=target_chunk
total_bytes = num_chunks*length

pbar = tqdm(total=num_chunks)
pbar_gui = tqdm_gui(total=num_chunks)
time_averages = []
i = 0

while x < num_chunks:
	#Start timer
	t0 = datetime.now()

	#sleep(2)
	jtagulator.write(b"flash -r%s" % str.encode(format(offset,'x')))
	sleep(2.5)
	jtagulator.write(b" -c%s\r\n" % str.encode(str(length)))
	jtagulator.readline()

	print("Attempting Chunk: %s" % (x+1))

	chunked, offset = chunk(jtagulator,offset,length)
	if not chunked:
		print("CHUNK %s IS CORRUPT - REATTEMPTING" % (x+1))
		continue

	t1 = datetime.now()
	#End Timer, chunk completed

	#Calculate average time of completion
	#datetime.timedelta(hours = 12)
	chunk_completion_time = t1-t0
	if len(time_averages) < 5:
		time_averages.append(chunk_completion_time)
	else:
		time_averages.pop(0)
		time_averages.append(chunk_completion_time)
	avg_time_completion = avg_time(time_averages)
	chunk_time_left = ((avg_time_completion.hour*3600)+(avg_time_completion.minute*60)+avg_time_completion.second)*(num_chunks-(x+1))

	#Write Data to txt file
	with open(filename, "a+") as myfile:
		myfile.write(chunked)

	#Target chunk is whats remaining in chunks
	#Total bytes is total bytes left to read!
	#print(chr(27) + "[2J") #Clear Terminal Alternative
	os.system( 'clear' )
	print("%s of %s: %%%s Completed" % (offset,(num_chunks+target_chunk)*length,100*float(offset)/((num_chunks+target_chunk)*length)))
	print("Bytes left: %s" % (total_bytes))
	print("Chunk: %s/%s" % (x+1,num_chunks))
	print("Chunk Time: %s" % (chunk_completion_time))
	print("Average Chunk Time: %s" % avg_time_completion.time())
	print("Time of Chunk Completion: %s" % (t1))
	print("Estimated Time Left: %s" % timedelta(seconds=chunk_time_left))
	print("Approximate Time of Completion: %s" % (datetime.now()+timedelta(seconds=chunk_time_left)))

	x+=1 #Used with while loop to continue iteration
	total_bytes-=length
	pbar.update(1) #Update progress bar
	pbar_gui.update(1) #Update progress bar

jtagulator.close()
print('DONE')
