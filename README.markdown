# ufloat8 library

This is a small library implementing a custom unsigned floating-point-like
integer format using just 8 bits. I wrote it to send a duration (in time) of a
wide range in just one byte, while keeping precision for smaller values.

Features:

 * Relatively small and fast (even constant time) decode function, designed for
   embedded systems.
 * The maximum range is about 20 bits, with the biggest number being 1015792.
 * For every number about four bits of significance is stored. 1-16 can all be
   stored literally, 16-48 with gaps of one, 48-112 with gaps of three, 112-240
   with gaps of seven, etc. This makes the numbers roughly exponential.
 * There are no two encoded values that decode to the same number.
 * Encoded values are linear, meaning, two decoded values `A` and `B` where
   `A > B` will encode to `a >= b`. Two encoded values `a` and `b` with `a > b`
   will decode to `A > B`. This property makes it easy to simply
   increment/decrement the encoded value resulting in a roughly exponential
   increase/decrease.
 * All numbers are unsigned.
 * There are no extras like NaN or Infinity.

Implementations:

 * Python reference/testing implementation.
 * Small C implementation.
 * Rust implementation, at
   [rust-ufloat8](https://github.com/aykevl/rust-ufloat8).

This library is freely licensed under the BSD 2-clause license (see
LICENSE.txt).
