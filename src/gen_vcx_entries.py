#!/usr/bin/env python3
#
# vcx_gen_list.py
#

import os
import sys
import uuid

SRC_EXT = set([ '.' + e for e in [ 'cpp', 'c', 'cc', 'cxx', 'c++', 'cppm', 'ixx', 'odl', 'idl' ] ])
HDR_EXT = set([ '.' + e for e in [ 'h', 'hh', 'hpp', 'hxx', 'h++', 'hm', 'inl', 'inc', 'ipp' ] ])

PREFIX = ''

def new_uuid():
    return '{' + str(uuid.uuid4()).upper() + '}'

def climb_dir(fn):
    s = sum([ d.split('/') for d in os.path.dirname(fn).split(os.path.sep) ], [])
    for i in range(len(s)):
        yield os.path.sep.join(s[:i+1])

def get_dirs(fn):
    d = set()
    for f in fn:
        for x in climb_dir(f):
            d.add(x)
    return d

def join_dir(h, t):
    if t: return os.path.join(h, t)
    return h

def main():
    src = []
    hdr = []
    ign = []
    for a in sys.argv[1:]:
        for fn, ext in [ ( l.replace('/', '\\'), os.path.splitext(l)[1].lower() ) for l in  [ l.rstrip() for l in open(a).readlines() ] ]:
            if ext in SRC_EXT:
                src += [ fn ]
            elif ext in HDR_EXT:
                hdr += [ fn ]
            else:
                ign += [ fn ]
    src.sort()
    hdr.sort()
    ign.sort()
    for f in src:
        print(f)
    print()
    sd = list(get_dirs(src))
    sd.sort()
    for d in sd:
        print(d)
    print()
    for f in hdr:
        print(f)
    print()
    hd = list(get_dirs(hdr))
    hd.sort()
    for d in hd:
        print(d)
    #print()
    #for f in ign:
    #    print(f)
    
    prj = open('out.vcxproj', 'w')
    print('  <ItemGroup>', file=prj)
    for f in src:
        print('    <ClCompile Include="' + os.path.join(PREFIX, f) + '" />', file=prj)
    print('  </ItemGroup>', file=prj)
    print('  <ItemGroup>', file=prj)
    for f in hdr:
        print('    <ClInclude Include="' + os.path.join(PREFIX, f) + '" />', file=prj)
    print('  </ItemGroup>', file=prj)
    prj.close()

    flt = open('out.vcxproj.filters', 'w')
    print('  <ItemGroup>', file=flt)
    for d in sd:
        print('    <Filter Include="' + join_dir('Source Files', d) + '">', file=flt)
        print('      <UniqueIdentifier>' + new_uuid() + '</UniqueIdentifier>', file=flt)
        print('    </Filter>', file=flt)
    for d in hd:
        print('    <Filter Include="' + join_dir('Header Files', d) + '">', file=flt)
        print('      <UniqueIdentifier>' + new_uuid() + '</UniqueIdentifier>', file=flt)
        print('    </Filter>', file=flt)
    print('  </ItemGroup>', file=flt)
    print('  <ItemGroup>', file=flt)
    for f in src:
        print('    <ClCompile Include="' + os.path.join(PREFIX, f) + '">', file=flt)
        print('      <Filter>' + join_dir('Source Files', os.path.dirname(f)) + '</Filter>', file=flt)
        print('    </ClCompile>', file=flt)
    print('  </ItemGroup>', file=flt)
    print('  <ItemGroup>', file=flt)
    for f in hdr:
        print('    <ClInclude Include="' + os.path.join(PREFIX, f) + '">', file=flt)
        print('      <Filter>' + join_dir('Header Files', os.path.dirname(f)) + '</Filter>', file=flt)
        print('    </ClInclude>', file=flt)
    print('  </ItemGroup>', file=flt)
    flt.close()

    return 0

if __name__ == '__main__':
    exit(main())
