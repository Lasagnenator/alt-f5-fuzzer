#!/bin/sh
# Libraries
#   Pillow => import PIL for jpg usage
#   defusedxml => safe alternative to python builtin xml
#   numpy => vector format
#   scipy => automated gradient descent
pip3 install Pillow defusedxml numpy scipy pdfminer.six

# Assumed to be installed already
#   pwntools
#   gdb binding for pwntools
#   gdb on system
#   objdump on system

# Change permissions on scripts just in case they lost them in unpacking
chmod +x instructions.sh
