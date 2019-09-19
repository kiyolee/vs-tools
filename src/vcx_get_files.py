#!/usr/bin/env python3
#
# vcx_get_files.py
#

import os
import sys
import platform

IS_WIN = platform.system() == 'Windows'

PREPEND_ROOT = False
SORT = False
HEADING = False
EXISTS = False
MISSING = False

def is_file_line(l):
    return (l.startswith('<ClCompile Include="')
            or l.startswith('<ClInclude Include="'))

def is_req_file(fn):
    if EXISTS: return os.path.isfile(fn)
    if MISSING: return not os.path.isfile(fn)
    return True

def iter_files(prj):
    root = os.path.dirname(prj)
    rp = root if PREPEND_ROOT else ''
    for l in [ l for l in [ l.strip() for l in open(prj) ] if is_file_line(l)]:
        s = l.split('"', 3)
        assert len(s) == 3
        fp = s[1].split('\\')
        if is_req_file(os.path.join(root, *fp)):
            yield os.path.join(rp, *fp)

def get_files(prj):
    if HEADING: print(prj + ':')
    if SORT:
        fs = list(iter_files(prj))
        fs.sort()
    else:
        fs = iter_files(prj)
    for f in fs:
        if HEADING: print('  ', end='')
        print(f)

def main():
    import getopt
    args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'pshEM',
            [ 'prepend-root', 'sort', 'heading', 'exists', 'missing' ])
    except getopt.error as errmsg:
        print(errmsg)
        return 255

    global PREPEND_ROOT, SORT, HEADING, EXISTS, MISSING

    for opt, val in opts:
        if opt in ( '-p', '--prepend-root' ):
            PREPEND_ROOT = True
        elif opt in ( '-s', '--sort' ):
            SORT = True
        elif opt in ( '-h', '--heading' ):
            HEADING = True
        elif opt in ( '-E', '--exists' ):
            EXISTS = True
            MISSING = False
        elif opt in ( '-M', '--missing' ):
            MISSING = True
            EXISTS = False

    for a in args:
        get_files(a)

if __name__ == '__main__':
    exit(main())

#---eof---
