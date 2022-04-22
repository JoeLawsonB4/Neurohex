#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from gtpinterface import gtpinterface
import sys
from six.moves import input

def main():
	"""
	Main function, simply sends user input on to the gtp interface and prints
	responses.
	"""
	interface = gtpinterface("allInputs")
	while True:
		print("waiting for command")
		command = input()
		print("got command" + command)
		success, response = interface.send_command(command)
		print("= " if success else "? ",response,"\n")
		sys.stdout.flush()
if __name__ == "__main__":
	main()
