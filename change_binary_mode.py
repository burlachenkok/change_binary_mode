#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016, Konstantin Burlachenko (burlachenkok@gmail.com).  All rights reserved.
# Change 'Subsytem' for Windows PE file. This affect if image-loader should create console window
# Implemented based on available PE specification

import sys
import struct

if len(sys.argv) == 4:
    srcName = sys.argv[1].strip()
    dstName = sys.argv[2].strip()
    mode = sys.argv[3].strip()
elif len(sys.argv) == 3:
    srcName = sys.argv[1].strip()
    dstName = sys.argv[1].strip()
    mode = sys.argv[2].strip()
else:
    print '''Change EXE Run Mode Application by burlachenkok@gmail.com
Not sufficient parameters. Please run as:

1) 'exe_src_name.exe' 'exe_dest_name.exe' 'to_console' or 'to_windows'
or
2) 'exe_src_and_dst_name.exe' 'to_console' or 'to_windows'
'''
    sys.exit(-1)

if srcName != dstName:
    source = open(srcName, "rb")
    dest   = open(dstName, "w+b")
    dest.write(source.read())
else:
    dest   = open(srcName, "r+b")

dest.seek(0x3c)
(PeHeaderOffset,)=struct.unpack("H", dest.read(2))

dest.seek(PeHeaderOffset)
(PeSignature,)=struct.unpack("I", dest.read(4))
if PeSignature != 0x4550:
    print "Error in Find PE header"

dest.seek(PeHeaderOffset + 0x5C)

if mode == "to_console":
    # console mode
    dest.write(struct.pack("H", 0x03))
elif mode == "to_windows":
    # window mode
    dest.write(struct.pack("H", 0x02))
else:
    print "Wrong Format: '" + sys.argv[3] + "'"
    sys.exit(-1)

#source.close()
#dest.close()

print "Completed succesfully. Output binary is: [%s].." % (dstName)
