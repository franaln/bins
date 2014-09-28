#! /usr/bin/env bash
# install root

# 1- configure
find . -type f -exec sed -e 's_#!/usr/bin/env python_&2_' \
    -e 's/python -O/python2 -O/g' \
    -e 's/python -c/python2 -c/g' -i {} \;
sed \
    -e 's/python 2/python2 2/g' \
    -i configure
sed \
    -e 's/python $(pkgpyexecdir)/python2 $(pkgpyexecdir)/g' \
    -i cint/reflex/python/genreflex/Makefile.am
sed \
    -e 's/python /python2 /' \
    -i config/genreflex.in config/genreflex-rootcint.in

local sys_libs=""
for sys_lib in ftgl freetype glew pcre zlib lzma; do
    sys_libs+="--disable-builtin-${sys_lib} "
done

./configure \
    linuxx8664gcc \
    --prefix=/usr \
    --libdir=/usr/lib/root \
    --enable-gdml \
    --enable-gsl-shared \
    --enable-minuit2 \
    --enable-soversion \
    --enable-roofit \
    --disable-builtin-afterimage \
    --with-python-incdir=/usr/include/python2.7 \
    --with-python-libdir=/usr/lib \
    ${sys_libs}

# 2- Compile
make -j4

# 3- Install
#sudo make install
