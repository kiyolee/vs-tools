#!/usr/bin/env python3
#
# setdbg.py: https://github.com/kiyolee/vs-tools.git
#
# MIT License
#
# Copyright (c) 2020 Kelvin Lee
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

"""
usage 1: %(__file__)s [options] [devenv-options ...]
    Start specific version of Visual Studio.

options:
    --msvc6, --vc6
        Start MSVC6 if available.
    --vs(2003|2005|2008|2010|2012|2013|2015|2017|2019)
        Start specific version of Visual Studio if available.
    -h, --help
        Print this help.

usage 2: %(__file__)s [-l|--list]
    List all Visual Studio found.
"""

import sys
#assert sys.platform == 'win32'

import os
import subprocess
import re
import winreg

# __file__ is not defined after compiled with cx_Freeze
if '__file__' not in globals(): __file__ = sys.argv[0]

__program__ = os.path.basename(__file__)

__doc__ = __doc__ % globals()

IS_OS64BIT = (os.environ['PROCESSOR_ARCHITECTURE'] == 'AMD64')
IS_WOW64 = False

if not IS_OS64BIT:
    import ctypes
    def _is_wow64():
        k = ctypes.windll.kernel32
        p = k.GetCurrentProcess()
        i = ctypes.c_int()
        if k.IsWow64Process(p, ctypes.byref(i)):
            return i.value != 0
        return False
    IS_OS64BIT = IS_WOW64 = _is_wow64()
    del _is_wow64
    del ctypes
#print('# IS_OS64BIT=' + str(IS_OS64BIT) + ' IS_WOW64=' + str(IS_WOW64))

def get_program_files_directories():
    pf64 = ''
    if IS_OS64BIT:
        pf32 = os.environ['ProgramFiles(x86)']
        if IS_WOW64:
            # 32-bit python on 64-bit windows, cannot rely on ProgramFiles
            # which is the same as ProgramFiles(x86) for 32-bit binaries.
            x86_suffix = ' (x86)'
            if pf32.endswith(x86_suffix):
                pf64 = pf32[:-len(x86_suffix)]
            else:
                pf64 = ''
            del x86_suffix
        else:
            pf64 = os.environ['ProgramFiles']
    else:
        pf32 = os.environ['ProgramFiles']
    return pf32, pf64

VS_KEY = r'Software\Microsoft\VisualStudio'

# MSVC6 (32-bit only)
def get_msdev_exe():
    h, h2 = None, None
    try:
        wowkey = winreg.KEY_WOW64_32KEY if IS_OS64BIT else 0
        vs6_key = VS_KEY + r'\6.0'
        #print('#', vs6_key, wowkey)
        h = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, vs6_key, 0, wowkey | winreg.KEY_READ)
        h2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, vs6_key + r'\Setup', 0, wowkey | winreg.KEY_READ)
        instdir, t = winreg.QueryValueEx(h, 'InstallDir')
        assert t == winreg.REG_SZ
        commondir, t = winreg.QueryValueEx(h2, 'VsCommonDir')
        assert t == winreg.REG_SZ
        assert instdir.startswith(commondir) and (commondir[-1] == os.path.sep or instdir[len(commondir)] == os.path.sep)
        msdev_exe = os.path.join(commondir, 'msdev98', 'bin', 'msdev.exe')
        if os.path.isfile(msdev_exe):
            return msdev_exe
    except WindowsError as err:
        #print(err, file=sys.stderr)
        pass
    finally:
        if h:
            winreg.CloseKey(h)
            del h
        if h2:
            winreg.CloseKey(h2)
            del h2
    return None

# VS2003|2005|2008|2010|2012|2013|2015 (32-bit only)
def get_devenv_exe(vs_ver):
    h, h2 = None, None
    try:
        wowkey = winreg.KEY_WOW64_32KEY if IS_OS64BIT else 0
        vsX_key = VS_KEY + '\\' + vs_ver
        #print('#', suffix[1:], vsX_key, wowkey)
        h = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, vsX_key, 0, wowkey | winreg.KEY_READ)
        h2 = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, vsX_key + r'\Setup\VS', 0, wowkey | winreg.KEY_READ)
        instdir, t = winreg.QueryValueEx(h, 'InstallDir')
        assert t == winreg.REG_SZ
        devenv_exe, t = winreg.QueryValueEx(h2, 'EnvironmentPath')
        assert t == winreg.REG_SZ
        assert devenv_exe.startswith(instdir) and (instdir[-1] == os.path.sep or devenv_exe[len(instdir)] == os.path.sep)
        if os.path.isfile(devenv_exe):
            return devenv_exe
    except WindowsError as err:
        #print(err, file=sys.stderr)
        pass
    finally:
        if h:
            winreg.CloseKey(h)
            del h
        if h2:
            winreg.CloseKey(h2)
            del h2
    return None

def vswhere_get_devenv_exe(devenvs, pf32, pf64):
    vswhere = os.path.join(pf32, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
    if not os.path.exists(vswhere):
        vswhere = os.path.join(pf64, 'Microsoft Visual Studio', 'Installer', 'vswhere.exe')
        if not os.path.exists(vswhere):
            return
    cmdp = subprocess.Popen([ vswhere, '-nologo' ], stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    sout, serr = cmdp.communicate()
    if cmdp.returncode != 0 or serr:
        return
    it = iter(sout.decode('utf-8').split('\r\n'))
    try:
        while True:
            s = next(it).split(': ', 1)
            assert len(s) == 2
            if s[0] == 'instanceId':
                pp, pv = '', ''
                try:
                    while True:
                        s = next(it)
                        if not s: break
                        s = s.split(': ', 1)
                        assert len(s) == 2
                        if s[0] == 'productPath':
                            pp = s[1]
                        elif s[0] == 'catalog_productLineVersion':
                            pv = s[1]
                except StopIteration:
                    pass
                if pp and pv:
                    pv = 'vs' + pv
                    for i in range(1, 99):
                        vs_id = pv if i == 1 else pv + ('_%d' % i)
                        if not vs_id in devenvs:
                            devenvs[vs_id] = pp
                            break
    except StopIteration:
        pass

def get_devenv_list():
    devenvs = {}
    #
    # MSVC6 (32-bit only)
    #
    msdev_exe = get_msdev_exe()
    if msdev_exe: devenvs['msvc6'] = msdev_exe
    #
    # VS2003|2005|2008|2010|2012|2013|2015 (32-bit only)
    #
    for vs_ver, vs_id in [ ( '7.0', 'vs2003' ),
                           ( '7.1', 'vs2003' ),
                           ( '8.0', 'vs2005' ),
                           ( '9.0', 'vs2008' ),
                           ( '10.0', 'vs2010' ),
                           ( '11.0', 'vs2012' ),
                           ( '12.0', 'vs2013' ),
                           ( '14.0', 'vs2015' ),
                           ]:
        devenv_exe = get_devenv_exe(vs_ver)
        if devenv_exe: devenvs[vs_id] = devenv_exe
    #
    pf32, pf64 = get_program_files_directories()
    #
    # VS2017 or later (32-bit only)
    #
    vswhere_get_devenv_exe(devenvs, pf32, pf64)
    #
    return devenvs

def get_vs_id_prioritized(devenvs):
    vs_ids = list(devenvs.keys())
    def _vs_id_to_key(vs_id):
        x = 0 if vs_id.startswith('vs') else -1
        if x == 0 and '_' in vs_id:
            s = vs_id.rsplit('_', 1)
            try:
                return x, s[0], -int(s[1])
            except ValueError:
                pass
        return x, vs_id, 0
    vs_ids.sort(key=_vs_id_to_key, reverse=True)
    return vs_ids

def default_devenv(devenvs):
    try:
        return get_vs_id_prioritized(devenvs)[0]
    except IndexError:
        pass
    return ''

def print_devenvs(devenvs, devdef):
    dk = list(devenvs.keys())
    if dk:
        print('Available Visual Studio %s:' % ('versions' if len(dk) > 1 else 'version'))
        def devkey(k):
            return k + '(default)' if k == devdef else k
        dk.sort()
        kl = [ ( k, devkey(k) ) for k in dk ]
        ml = len(max(kl, key=lambda k: len(k[1]))[1]) + 1
        for k, krem in kl:
            print('%-*s%s' % ( ml, krem, devenvs[k] ))
    else:
        print('No Visual Studio found.')

def clean_env():
    env = dict(os.environ)
    for i in [ 'CommandPromptType',
               'DevEnvDir',
               'ExtensionSdkDir',
               'FSHARPINSTALLDIR',
               'Framework35Version',
               'Framework40Version',
               'FrameworkDIR32',
               'FrameworkDIR64',
               'FrameworkDir',
               'FrameworkVersion32',
               'FrameworkVersion64',
               'FrameworkVersion',
               'HTMLHelpDir',
               'IFCPATH',
               'INCLUDE',
               'LIB',
               'LIBPATH',
               'NETFXSDKDir',
               'Platform',
               'UCRTVersion',
               'UniversalCRTSdkDir',
               'VCIDEInstallDir',
               'VCINSTALLDIR',
               'VCToolsInstallDir',
               'VCToolsRedistDir',
               'VCToolsVersion',
               'VSCMD_ARG_HOST_ARCH',
               'VSCMD_ARG_TGT_ARCH',
               'VSCMD_ARG_app_plat',
               'VSCMD_VER',
               'VSINSTALLDIR',
               'VSSDKINSTALL',
               'VisualStudioVersion',
               'WindowsLibPath',
               'WindowsSDKLibVersion',
               'WindowsSDKVersion',
               'WindowsSDK_ExecutablePath_x64',
               'WindowsSDK_ExecutablePath_x86',
               'WindowsSdkBinPath',
               'WindowsSdkDir',
               'WindowsSdkVerBinPath',
               '__DOTNET_ADD_32BIT',
               '__DOTNET_ADD_64BIT',
               '__DOTNET_PREFERRED_BITNESS',
               '__VSCMD_PREINIT_PATH',
               '__VSCMD_PREINIT_VS150COMNTOOLS',
               '__VSCMD_PREINIT_VS160COMNTOOLS',
               '__VSCMD_script_err_count' ]:
        if i in env: del env[i]
    env['PreferredToolArchitecture'] = 'x64'
    try:
        h = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\ControlSet001\Control\Session Manager\Environment', 0, winreg.KEY_READ)
        syspath, t = winreg.QueryValueEx(h, 'Path')
        assert t == winreg.REG_EXPAND_SZ
    except WindowsError:
        syspath = ''
    try:
        h = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_READ)
        usrpath, t = winreg.QueryValueEx(h, 'Path')
        assert t == winreg.REG_EXPAND_SZ
    except WindowsError:
        usrpath = ''
    if syspath and usrpath:
        def _repl(match):
            v = match.group('var')
            if not v: return '%'
            if not v in env: return match.match
            return env[v]
        pat = re.compile('%(?P<var>\w*)%')
        env['Path'] = ';'.join([ re.sub(pat, _repl, p ) for p in ( syspath.split(';') + usrpath.split(';') ) if p ])
    return env

def main():
    devenvs = get_devenv_list()
    devdef = default_devenv(devenvs)

    vs_opts = list(devenvs.keys())
    vs_opts += [ i[2:] for i in vs_opts if i.startswith('vs') ]
    if 'msvc6' in devenvs: vs_opts += [ 'vc6' ]

    devsel = ''

    import getopt
    args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'lh',
                                   [ 'list', 'help', ] + vs_opts)
    except getopt.error as err:
        print(err, file=sys.stderr)
        return 255

    for opt, val in opts:
        if opt in ( '--msvc6', '--vc6' ):
            assert not devsel
            devsel = 'msvc6'
        elif (opt.startswith('--') and (opt[2:] in devenvs)):
            assert not devsel
            devsel = opt[2:]
        elif (opt.startswith('--') and ('vs' + opt[2:] in devenvs)):
            assert not devsel
            devsel = 'vs' + opt[2:]
        elif opt in ( '-l', '--list' ):
            print_devenvs(devenvs, devdef)
            return 1
        elif opt in ( '-h', '--help' ):
            print(__doc__)
            return 255

    if not devsel: devsel = devdef
    devenv = devenvs[devsel]

    os.execve(devenv, [ '"' + devenv + '"' ] + [ '"' + a + '"' for a in args ],
              clean_env())

    return 0

if __name__ == '__main__':
    sys.exit(main())

#---eof---
