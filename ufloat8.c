/* Copyright (c) 2016, Ayke van Laethem
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are
 * met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
 * TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
 * PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 * HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 * LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 * DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 * THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "ufloat8.h"

uint32_t ufloat8_dec(ufloat8 fl) {
  // get the significant digits (mantissa?)
  uint32_t n = fl & 0x0f;
  // get the exponent
  uint8_t exponent = (fl & 0xf0) >> 4;
  // apply the exponent, getting the result value
  uint32_t result = n << exponent;
  return result;
}


ufloat8 ufloat8_enc(uint32_t in) {
  // Initial value:
  //   exponent = 0
  //   mantissa = capped in
  ufloat8 fl = in & 0x0f;
  // The magic value 16 was determined by trial-and-error...
  for (uint8_t i=1; i<16; i++) {
    // Chop off precision bits on the right side each iteration.
    // For exponent=0 this was done in the initialisation above.
    in >>= 1;
    // Check whether the left most bit of the resulting mantissa is
    // set. If so, update the resulting float.
    if (in & 0x08) {
      // there are bits found!
      fl = in & 0x0f;
      fl |= i << 4;
    }
  }
  return fl;
}
