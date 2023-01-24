import os
import sys
import csv
with open(sys.argv[1], "r") as csvfile:
            all_lines = csvfile.readlines()
            print(all_lines)