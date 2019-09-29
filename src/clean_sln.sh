#!/bin/sh
#
# clean_sln.sh
#

FOR_REAL=0

clean_sln(){
  [ $# -eq 0 ] && return 1
  SLNDIR="$1"
  [ ! -d "$SLNDIR" ] && return 1
  if [ $FOR_REAL -eq 0 ]; then
    RM_FRONT="-exec echo rm -v {} ;"
    RM_BACK="cat"
    RMDIR_FRONT="-exec echo rmdir -v {} ;"
    RMDIR_BACK="cat"
  else
    RM_FRONT="-print0"
    RM_BACK="xargs -r -0 -n 1000 rm -v"
    #RMDIR_FRONT="-print0"
    #RMDIR_BACK="xargs -r -0 -n 1000 rmdir -v"
    RMDIR_FRONT="-exec rmdir -v {} ;"
    RMDIR_BACK="cat"
  fi
  find "$SLNDIR" -type f \( \
      -false \
      -o -name '*.embed.manifest' \
      -o -name '*.exp' \
      -o -name '*.extracted.manifest' \
      -o -name '*.idb' \
      -o -name '*.ilk' \
      -o -name '*.intermediate.manifest' \
      -o -name '*.iobj' \
      -o -name '*.ipch' \
      -o -name '*.ipdb' \
      -o -name '*.lastbuildstate' \
      -o -name '*.lastcodeanalysissucceeded' \
      -o -name '*.log' \
      -o -name '*.nativecodeanalysis.all.xml' \
      -o -name '*.nativecodeanalysis.xml' \
      -o -name '*.obj' \
      -o -name '*.pdb' \
      -o -name '*.tlog' \
      -o -name '*.unsuccessfulbuild' \
      -o -name '*.vcxproj.FileListAbsolute.txt' \
      -o -name '*.vcxprojResolveAssemblyReference.cache' \
      -o -name '*_manifest.rc' \
      -o -name 'BuildLog.htm' \
      -o -name 'mt.dep' \
      -o -name 'unsuccessfulbuild' \
      -o \( -name '*.sbr' -a -size 0 \) \
      \) \
      $RM_FRONT | $RM_BACK
  find "$SLNDIR" -depth -mindepth 1 -type d \
      -empty ! -regex '.*\/\.\(svn\|git\|bzr\|hg\)\/.*' \
      $RMDIR_FRONT | $RMDIR_BACK
}

if [ $# -gt 0 ]; then
  if [ $1 = '-f' ]; then
    FOR_REAL=1
    shift
  fi
fi

if [ $# -eq 0 ]; then
  clean_sln .
else
  for i in "$@"; do
    clean_sln "$i"
  done
fi

# vim:sts=2:sw=2:ts=8:et:syntax=sh
