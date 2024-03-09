""" Dummy Check Script
Waits a period of time and returns the given message and return code
"""
import argparse
import sys
import time

parser = argparse.ArgumentParser(description="Dummy check script - echos back result code")

parser.add_argument('-m', "--message", required=True, type=str, help="Status message to print to console")
parser.add_argument('-t', "--wait_time", required=False, default=1, type=int, help="Amount of time to wait (seconds) before exiting")
parser.add_argument('-r', "--return_code", required=False, default=0, type=int, choices=[0, 1, 2, 3],
                    help="Exit code to use")

args = parser.parse_args()

time.sleep(args.wait_time)

print(args.message)
sys.exit(args.return_code)
