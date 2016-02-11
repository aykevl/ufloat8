#!/usr/bin/python3
#  Copyright (c) 2016, Ayke van Laethem
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
#  TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#  PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

def ufloat8_dec(fl):
    # get the significant digits (mantissa?)
    n = fl & 0x0f
    # get the exponent
    exponent = (fl & 0xf0) >> 4
    # The first part applies the exponent.
    # The second part adds 16, 40, 112 etc. (10000, 110000, 1110000 etc.)
    # That makes the ufloat8 easy to increment, as an increment of the ufloat8
    # always increments the resulting value.
    # The second part might be optimizable on systems that implement arithmetic
    # right shift.
    return (n << exponent) + (0b111111111111111 >> (15-exponent) << 4)

def ufloat8_enc(value):
    overflow = 0
    for exponent in range(16):
        if value < overflow * 2 + 16:
            fl = (value - overflow) >> exponent
            fl += exponent << 4
            return fl

        overflow = overflow * 2 + 16


def test():
    # test all encoded values
    success = True
    previous_value = -1
    for encoded in range(256):
        value = ufloat8_dec(encoded)
        encoded2 = ufloat8_enc(value)
        if encoded != encoded2:
            print('Test fail for encoded value %d (resulting value %d encoded to %d).' % ( encoded, value, encoded2))
            success = False
        if value <= previous_value:
            print('Value did not increase (previous value=%d, value=%d)' % (previous_value, value))
            success = False
    if success:
        print('All tests passed.')
    return success

if __name__ == '__main__':
    try:
        test()
    except BrokenPipeError:
        pass
