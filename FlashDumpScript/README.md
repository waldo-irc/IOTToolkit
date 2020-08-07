# DumpFWScript

Custom dump firmware script for utilities that provide "md" in the uart command line.

## Usage
#### This script assumes 1 serial device is connected and just connects to /dev/ttyUSB0
1. DumpFirmware.py FileName.dump (A Regular Dump)
2. DumpFirmware.py FileName.dump -b 1024 (If you cancel a dump at a certain point, enter the position in bytes where you left off to continue)
3. DumpFirmware.py Filename.dump -w allows you to start from scratch

## Notes
1. The MD command outputs line numbers along with the memory information, we use this along with the full size in bytes of the flash memory to perform an integrity check and make sure every byte is accounted for.
2. Nice little graphs are used to monitor time to completion as of a recent update, I may or may not keep this
3. Will add the ability to choose the serial device but im lazy for now, you can easily change it in the script
4. Can also do Jtagulator passthrough (not required on subsequent connections on linux as it remembers the serial connection state)