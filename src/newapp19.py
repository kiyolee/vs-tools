#!/usr/bin/env python3
#
# newvcx17.py
#

import sys
import os
import uuid
import re

DEFAULT_VCXPROJ = r'''<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <VCProjectVersion>16.0</VCProjectVersion>
    <ProjectGuid>%{PROJGUID}%</ProjectGuid>
    <RootNamespace>%{PROJNAME}%</RootNamespace>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup />
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>_DEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>NDEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
    </Link>
  </ItemDefinitionGroup>
%{PROJSRC}%  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>'''

DEFAULT_VCXPROJ_64 = r'''<?xml version="1.0" encoding="utf-8"?>
<Project DefaultTargets="Build" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup Label="ProjectConfigurations">
    <ProjectConfiguration Include="Debug|Win32">
      <Configuration>Debug</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|Win32">
      <Configuration>Release</Configuration>
      <Platform>Win32</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Debug|x64">
      <Configuration>Debug</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
    <ProjectConfiguration Include="Release|x64">
      <Configuration>Release</Configuration>
      <Platform>x64</Platform>
    </ProjectConfiguration>
  </ItemGroup>
  <PropertyGroup Label="Globals">
    <VCProjectVersion>16.0</VCProjectVersion>
    <ProjectGuid>%{PROJGUID}%</ProjectGuid>
    <RootNamespace>%{PROJNAME}%</RootNamespace>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.Default.props" />
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>true</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
  </PropertyGroup>
  <PropertyGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'" Label="Configuration">
    <ConfigurationType>Application</ConfigurationType>
    <UseDebugLibraries>false</UseDebugLibraries>
    <PlatformToolset>v142</PlatformToolset>
    <WholeProgramOptimization>true</WholeProgramOptimization>
  </PropertyGroup>
  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.props" />
  <ImportGroup Label="ExtensionSettings">
  </ImportGroup>
  <ImportGroup Label="Shared">
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <ImportGroup Label="PropertySheets" Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <Import Project="$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props" Condition="exists('$(UserRootDir)\Microsoft.Cpp.$(Platform).user.props')" Label="LocalAppDataPlatform" />
  </ImportGroup>
  <PropertyGroup Label="UserMacros" />
  <PropertyGroup />
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>_DEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|Win32'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>NDEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Debug|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>Disabled</Optimization>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>_DEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
    </Link>
  </ItemDefinitionGroup>
  <ItemDefinitionGroup Condition="'$(Configuration)|$(Platform)'=='Release|x64'">
    <ClCompile>
      <WarningLevel>Level3</WarningLevel>
      <Optimization>MaxSpeed</Optimization>
      <FunctionLevelLinking>true</FunctionLevelLinking>
      <IntrinsicFunctions>true</IntrinsicFunctions>
      <SDLCheck>true</SDLCheck>
      <StringPooling>true</StringPooling>
      <PreprocessorDefinitions>NDEBUG;%(PreprocessorDefinitions)</PreprocessorDefinitions>
    </ClCompile>
    <Link>
      <GenerateDebugInformation>true</GenerateDebugInformation>
      <EnableCOMDATFolding>true</EnableCOMDATFolding>
      <OptimizeReferences>true</OptimizeReferences>
    </Link>
  </ItemDefinitionGroup>
%{PROJSRC}%  <Import Project="$(VCTargetsPath)\Microsoft.Cpp.targets" />
  <ImportGroup Label="ExtensionTargets">
  </ImportGroup>
</Project>'''

DEFAULT_VCXPROJ_FILTERS = r'''<?xml version="1.0" encoding="utf-8"?>
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <ItemGroup>
    <Filter Include="Source Files">
      <UniqueIdentifier>{4FC737F1-C7A5-4376-A066-2A32D752A2FF}</UniqueIdentifier>
      <Extensions>cpp;c;cc;cxx;c++;cppm;ixx;def;odl;idl;hpj;bat;asm;asmx</Extensions>
    </Filter>
    <Filter Include="Header Files">
      <UniqueIdentifier>{93995380-89BD-4b04-88EB-625FBE52EBFB}</UniqueIdentifier>
      <Extensions>h;hh;hpp;hxx;h++;hm;inl;inc;ipp;xsd</Extensions>
    </Filter>
    <Filter Include="Resource Files">
      <UniqueIdentifier>{67DA6AB6-F800-4c08-8B7A-83BB121AAD01}</UniqueIdentifier>
      <Extensions>rc;ico;cur;bmp;dlg;rc2;rct;bin;rgs;gif;jpg;jpeg;jpe;resx;tiff;tif;png;wav;mfcribbon-ms</Extensions>
    </Filter>
  </ItemGroup>
%{PROJFILTSRC}%</Project>'''

DEFAULT_SLN = r'''
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 16
VisualStudioVersion = 16.0.30611.23
MinimumVisualStudioVersion = 10.0.40219.1
Project("%{SLN_PROJGUID_U}%") = "%{PROJNAME}%", "%{PROJNAME}%\%{PROJNAME}%.vcxproj", "%{PROJGUID_U}%"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Win32 = Debug|Win32
		Release|Win32 = Release|Win32
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		%{PROJGUID_U}%.Debug|Win32.ActiveCfg = Debug|Win32
		%{PROJGUID_U}%.Debug|Win32.Build.0 = Debug|Win32
		%{PROJGUID_U}%.Release|Win32.ActiveCfg = Release|Win32
		%{PROJGUID_U}%.Release|Win32.Build.0 = Release|Win32
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = %{SLNGUID_U}%
	EndGlobalSection
EndGlobal
'''

DEFAULT_SLN_64 = r'''
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 16
VisualStudioVersion = 16.0.30611.23
MinimumVisualStudioVersion = 10.0.40219.1
Project("%{SLN_PROJGUID_U}%") = "%{PROJNAME}%", "%{PROJNAME}%\%{PROJNAME}%.vcxproj", "%{PROJGUID_U}%"
EndProject
Global
	GlobalSection(SolutionConfigurationPlatforms) = preSolution
		Debug|Win32 = Debug|Win32
		Debug|x64 = Debug|x64
		Release|Win32 = Release|Win32
		Release|x64 = Release|x64
	EndGlobalSection
	GlobalSection(ProjectConfigurationPlatforms) = postSolution
		%{PROJGUID_U}%.Debug|Win32.ActiveCfg = Debug|Win32
		%{PROJGUID_U}%.Debug|Win32.Build.0 = Debug|Win32
		%{PROJGUID_U}%.Debug|x64.ActiveCfg = Debug|x64
		%{PROJGUID_U}%.Debug|x64.Build.0 = Debug|x64
		%{PROJGUID_U}%.Release|Win32.ActiveCfg = Release|Win32
		%{PROJGUID_U}%.Release|Win32.Build.0 = Release|Win32
		%{PROJGUID_U}%.Release|x64.ActiveCfg = Release|x64
		%{PROJGUID_U}%.Release|x64.Build.0 = Release|x64
	EndGlobalSection
	GlobalSection(SolutionProperties) = preSolution
		HideSolutionNode = FALSE
	EndGlobalSection
	GlobalSection(ExtensibilityGlobals) = postSolution
		SolutionGuid = %{SLNGUID_U}%
	EndGlobalSection
EndGlobal
'''

VCXPROJ_SRC_F = r'''  <ItemGroup>
    <ClCompile Include="'''
VCXPROJ_SRC_B =  r'''" />
  </ItemGroup>
'''

VCXPROJ_FILTERS_SRC_F = r'''  <ItemGroup>
    <ClCompile Include="'''
VCXPROJ_FILTERS_SRC_B = r'''">
      <Filter>Source Files</Filter>
    </ClCompile>
  </ItemGroup>
'''

def format_text(fn, text, param):
    var_pat = re.compile(r'%{(?P<var>\w+)}%')
    def repl(match):
        var = match.group('var')
        return param.get(var, '%{UNKNOWN}%')
    with open(fn, 'wb') as fo:
        fo.write(b'\xef\xbb\xbf')
        fo.write(('\r\n'.join(re.sub(var_pat, repl, text).split('\n'))).encode('utf-8'))

def new_uuid():
    return '{' + str(uuid.uuid4()).upper() + '}'

def create_vcxproj(target, x64support, src=None):
    if os.path.isdir(target):
        basedir = target
        slnname = ''
    else:
        basedir = os.path.dirname(target)
        if not basedir: basedir = os.curdir
        slnname = os.path.basename(target)
    if src:
        src_bn = os.path.basename(src)
        projname = os.path.splitext(src_bn)[0]
        if not slnname: slnname = projname
    else:
        projname = slnname
    if not slnname:
        print('Solution name not given or could not be deduced.', file=sys.stderr)
        return
    if not projname:
        print('Project name not given or could not be deduced.', file=sys.stderr)
        return
    projdir = os.path.join(basedir, projname)
    sln_fn = os.path.join(basedir, slnname + '.sln')
    vcxproj_fn = os.path.join(projdir, projname + '.vcxproj')
    vcxproj_filters_fn = vcxproj_fn + '.filters'
    for fn in ( sln_fn, vcxproj_fn, vcxproj_filters_fn ):
        if os.path.exists(fn):
            print('%s already exists!' % fn)
            return
    slnguid = new_uuid()
    sln_projguid = new_uuid()
    projguid = new_uuid()
    if src:
        if os.path.isfile(src):
            src_fn = os.path.relpath(src, projdir)
        else:
            src_basedir = os.path.dirname(src)
            if os.path.isdir(src_basedir):
                src_bn = os.path.basename(src)
                src_fn = os.path.join(os.path.relpath(src_basedir, projdir), src_bn)
            else:
                src_fn = src
        projsrc = (VCXPROJ_SRC_F + src_fn + VCXPROJ_SRC_B)
        projfiltsrc = (VCXPROJ_FILTERS_SRC_F + src_fn + VCXPROJ_FILTERS_SRC_B)
    else:
        projsrc = ''
        projfiltsrc = ''
    param = { 'SLNNAME': slnname,
              'SLNGUID': slnguid, 'SLNGUID_U': slnguid.upper(),
              'SLN_PROJGUID': sln_projguid, 'SLN_PROJGUID_U': sln_projguid.upper(),
              'PROJNAME': projname,
              'PROJGUID': projguid, 'PROJGUID_U': projguid.upper(),
              'PROJSRC': projsrc, 'PROJFILTSRC': projfiltsrc
               }
    try:
        default_sln = DEFAULT_SLN_64 if x64support else DEFAULT_SLN
        default_vcxproj = DEFAULT_VCXPROJ_64 if x64support else DEFAULT_VCXPROJ
        if not os.path.isdir(projdir):
            os.makedirs(projdir)
        format_text(sln_fn, default_sln, param)
        format_text(vcxproj_fn, default_vcxproj, param)
        format_text(vcxproj_filters_fn, DEFAULT_VCXPROJ_FILTERS, param)
        print('created %s, %s and %s.' % ( sln_fn, vcxproj_fn, vcxproj_filters_fn ))
    except IOError as e:
        print(e)

def main():
    args = sys.argv[1:]
    x64support = True
    if len(args) > 0 and args[0] == '-32':
        x64support = False
        args = args[1:]
    if len(args) == 1:
        create_vcxproj(args[0], x64support)
    elif len(args) == 2:
        create_vcxproj(args[0], x64support, args[1])
    else:
        print('Too many arguments.', file=sys.stderr)
    return 0

if __name__ == '__main__':
    exit(main())

#---eof---
