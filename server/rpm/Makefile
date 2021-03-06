# Making a pbench-server RPM requires a few steps
# 1. Generate a version number
# 2. Update the RPM spec file with that version number
# 3. Generate a tar ball of the sources to be used by the RPM building process
# 4. Generate an SRPM that will be uploaded to COPR for building.

CWD = $(shell pwd -L)

SERVER = $(dir ${CWD})
PBENCHTOP = $(shell dirname ${SERVER})
TMPDIR = /tmp/opt

VERSION = $(shell cat ${SERVER}/VERSION)

DISTRO = $(shell uname -r | python -c 'import sys; print(sys.stdin.read().split(".")[-2])')

PYTHON = python3

RPMSRC = ${HOME}/rpmbuild/SOURCES
RPMSRPM = ${HOME}/rpmbuild/SRPMS
RPMSPEC = ${HOME}/rpmbuild/SPECS

prog = pbench-server
arch = noarch

TBDIR = ${TMPDIR}/${prog}-${VERSION}

USE_GIT_SHA1 = yes
sha1 = $(shell git rev-parse --short HEAD)
seqno := $(shell if [ -e ./seqno ] ;then cat ./seqno ;else echo "1" ;fi)

rpm:  srpm
	rpmbuild -bb ${HOME}/rpmbuild/SPECS/${prog}.spec

srpm:	patches tarball
	rm -f ${HOME}/rpmbuild/SRPMS/$(prog)-*.src.rpm
	rpmbuild -bs ${HOME}/rpmbuild/SPECS/$(prog).spec

.PHONY: spec
spec: ${prog}.spec.j2
	mkdir -p ${RPMSPEC}
	if [ -e ./seqno ] ;then expr ${seqno} + 1 > ./seqno ;fi
	jinja2 ${prog}.spec.j2 -D version=${VERSION} -D gdist=g${sha1} -D seqno=${seqno} > ${RPMSPEC}/${prog}.spec
	rpmlint ${RPMSPEC}/${prog}.spec

.PHONY: patches
patches:
	if [ -d ${CWD}/patches ] ;then cp ${CWD}/patches/* ${RPMSRC} ;fi

.PHONY: tarball
tarball: spec
	mkdir -p ${RPMSRC}
	make -C ${PBENCHTOP}/server DESTDIR=${TBDIR}/server install
	make -C ${PBENCHTOP}/web-server DESTDIR=${TBDIR}/web-server install
	sed -i '1s;.*python$$;#!/usr/bin/env python3;' ${TBDIR}/server/bin/pbench-config ${TBDIR}/server/bin/pbench-server 
	echo "${sha1}" > ${TBDIR}/server/SHA1
	echo "${seqno}" > ${TBDIR}/server/SEQNO
	tar zcf ${RPMSRC}/pbench-server-${VERSION}.tar.gz -C ${TMPDIR} ${prog}-${VERSION}
	rm -rf ${TMPDIR}

###########################################################################
# build RPMs in COPR
seqno := $(shell if [ -f seqno ] ;then cat seqno ;else echo 1; fi)

include rpm.mk

clean-sha1:
	rm -f ${upstmtree}/${prog}.SHA1

clean:: localclean

