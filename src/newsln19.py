#!/usr/bin/env python3
#
# newsln19.py
#

import sys
import os

DEFAULT_SLN = r'''
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 16
VisualStudioVersion = 16.0.30611.23
MinimumVisualStudioVersion = 10.0.40219.1
Global
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
EndGlobal
'''

def format_text(fn, text):
    with open(fn, 'wb') as fo:
        fo.write(b'\xef\xbb\xbf')
        fo.write(('\r\n'.join(text.split('\n'))).encode('utf-8'))

def create_sln(n):
    bn = os.path.basename(n)
    sln_fn = n + '.sln'
    if os.path.exists(sln_fn):
        print('%s already exists!' % sln_fn)
        return
    try:
        format_text(sln_fn, DEFAULT_SLN)
        print('created %s.' % sln_fn)
    except IOError as e:
        print(e)

def main():
    args = sys.argv[1:]
    for a in args:
        create_sln(a)
    return 0

if __name__ == '__main__':
    exit(main())

#---eof---
