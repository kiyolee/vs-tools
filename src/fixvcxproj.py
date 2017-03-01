#!/usr/bin/env python3
#
# fixvcxproj.py
#

import sys
import os

DO_FIX = False

def fix_vcxproj(fn):
    sz = 0
    fix = False
    with open(fn, 'rb') as fi:
        fi.seek(-2, 2)
        sz = fi.tell()
        eb = fi.read(2)
        #print(fn, sz, eb)
        fix = (eb == b'\r\n')
    if fix:
        if DO_FIX:
            with open(fn, 'rb+') as fo:
                os.ftruncate(fo.fileno(), sz)
            print(fn, 'fixed')
        else:
            print(fn, 'need fix')

def main():
    if sys.argv[1:]:
        if sys.argv[1] == '-f':
            global DO_FIX
            DO_FIX = True
            args = sys.argv[2:]
        else:
            args = sys.argv[1:]
        for a in args:
            fix_vcxproj(a)
    return 0

if __name__ == '__main__':
    exit(main())

#---eof---
