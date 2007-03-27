#!/bin/sh

# temporary packaging script
echo Packaging JythonConsole
 
if [ "$1" == "" ]; then
    echo Version? example: 0.0.2 or 0.0.2-SNAPSHOT
    read
    VERSION=${REPLY}
else
    VERSION=$1
fi

DIST=jythonconsole-${VERSION}
mkdir ${DIST}
cp *.py ${DIST}
cp problems.txt ${DIST} 
cp README.txt ${DIST} 
cp COPYING.txt ${DIST} 
zip ${DIST}.zip ${DIST}/*
rm -fr ${DIST}
echo Created ${DIST}.zip
echo Remember to tag the code!