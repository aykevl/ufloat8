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
    # apply the exponent, getting the result value
    result = n << exponent
    return result

def ufloat8_enc(value):
    # Initial value:
    #   exponent = 0
    #   mantissa = capped value
    fl = value & 0x0f;

    # The magic value 16 was determined by trial-and-error...
    for i in range(1, 16):
        # Chop off precision bits on the right side each iteration. For
        # exponent=0 this was done in the initialisation above.
        value >>= 1
        # Check whether the left most bit of the resulting mantissa is set. If
        # so, update the resulting float.
        if value & 0x08:
            # there are bits found!
            fl = value & 0x0f
            fl |= i << 4

    return fl

def ufloat8_inc(fl, inc):
    '''
    Increment or decrement ufloat8 number.
    WARNING: may wrap around!
    '''
    fl += inc;
    # handle mantissa overflow gracefully
    if fl & 0xf0 != 0:
        if inc > 0 and fl & 0x0f < 0x08:
            fl += 0x08
        elif inc < 0 and fl & 0x0f < 0x08:
            fl -= 0x08
    return fl


def test_base():
    # test all encoded values
    success = True
    for encoded1 in range(256):
        value1 = ufloat8_dec(encoded1)
        encoded2 = ufloat8_enc(value1)
        # it is expected encoded1 and encoded2 will often differ, but they
        # should give the same value
        value2 = ufloat8_dec(encoded2)
        if value1 != value2:
            print('Test fail for encoded value %d (resulting value %d != %d).',
                 encoded1, value1, value2)
            success = False
    if success:
        print('All tests passed.')

def test_inc(increment=1):
    import math
    n = 0
    for i in range(0, 136-increment, increment):
        n_old = n
        n = ufloat8_inc(n, increment)
        if i > 0:
            logIncrease = math.log(ufloat8_dec(n))/math.log(2) - math.log(ufloat8_dec(n_old))/math.log(2)
        else:
            logIncrease = 0
        if n <= n_old:
            raise ValueError('number did not increase')
        if n < 0 or n > 255:
            raise ValueError('number outside range')
        if i > 8:
            if logIncrease > 0.17*increment:
                raise ValueError('logarithmic increase should be below 0.17 for values > 8')
            elif logIncrease <= 0:
                raise ValueError('value did not increase')
        else:
            if n != n_old + increment:
                raise ValueError('increase should be exactly the increment for values <= 8')
        print(ufloat8_dec(n), logIncrease)
    print('Increment test OK.')

def test_dec(decrement=1):
    import math
    n = 255
    while n > decrement:
        n_old = n
        n = ufloat8_inc(n, -decrement)
        logIncrease = math.log(ufloat8_dec(n))/math.log(2) - math.log(ufloat8_dec(n_old))/math.log(2)
        if n >= n_old:
            raise ValueError('number did not decrease')
        if n < 0 or n > 255:
            raise ValueError('number outside range')
        if n > 8:
            if logIncrease < -0.17*decrement:
                raise ValueError('logarithmic decrease should be below 0.17 for values > 8')
            elif logIncrease >= 0:
                raise ValueError('value did not decrease')
        else:
            if n != n_old - decrement:
                raise ValueError('decrease should be exactly the decrement for values <= 8')
        print(ufloat8_dec(n), logIncrease)
    print('Decrement test OK.')

def test_all():
    test_base()
    test_inc()
    test_dec()

if __name__ == '__main__':
    test()
