"""Avoid using magic numbers with these handy constants
   Use the same values in tests, function returns. 
"""
import errno

PROGRAM_NAME = "BallotMaker"
VERSION = "0.1.3"  # incremented September 20, 2022

NO_ERRORS = 0
NO_FILE = errno.ENOENT
NO_DATA = errno.ENODATA
