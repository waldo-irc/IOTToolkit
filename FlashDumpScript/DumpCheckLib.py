#!/usr/bin/env python3

def hexDigit(digit):
	c = ord(digit)
	return (c>=48 and c<58) or (c>=65 and c<71)

def checkContent(content, offset, verbose=False):
	lines = content.split()
	length = len(lines)

	x=0
	while x < length:
		line = lines[x]

		#First Check, has a colon
		try:
			expected_number = str(format(x+offset,'x')).upper()
			line_split = line.split(':')
			line_number = line_split[0]
			line_value = line_split[1]
			first_digit = line_value[0]
			second_digit = line_value[1]
		except IndexError:
			if verbose:
				print("BAD - INVALID DATA")
				print("INVALID BYTE: %s" % expected_number)
			return False

		#Second check, ensure the list 2 items, only 1 colon
		if len(line_split) != 2:
			if verbose:
				print("BAD - INVALID DATA")
				print("INVALID BYTE: %s" % expected_number)
			return False

		#Third check, ensure 2 bytes after colon
		if len(line_value) != 2:
			if verbose:
				print("BAD - INVALID DATA")
				print("INVALID BYTE: %s" % expected_number)
			return False

		#Fourth check, ensure 2 bytes are valid uppercase hex
		if not hexDigit(first_digit) or not hexDigit(second_digit):
			if verbose:
				print("BAD - INVALID DATA")
				print("INVALID BYTE: %s" % expected_number)
			return False

		#Check sequentially it is sound
		if line_number != expected_number:
			if verbose:
				print("BAD - MISSING DATA")
				print("SKIPPED BYTE: %s" % expected_number)
			return False

		if verbose:
			print("GOOD: "+line)
		x+=1

	return True


