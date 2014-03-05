#! /usr/bin/env bash
# install root

# 1- configure
./configure \
    linuxx8664gcc \
    --enable-roofit \
    --with-python-incdir=/usr/include/python2.7 \
    --with-python-libdir=/usr/lib \
    --disable-builtin-ftgl \
    --disable-builtin-freetype \
    --disable-builtin-glew \
    --disable-builtin-pcre \
    --disable-builtin-zlib \
    --disable-builtin-lzma

# 2- Compile
make -j4

# 3- Install
#sudo make install
