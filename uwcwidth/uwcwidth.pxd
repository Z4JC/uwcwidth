#cython: language_level=3
# SPDX-License-Identifier: MIT
from libc.stdint cimport uint32_t

cpdef int wcwidth(unicode uwc)
cpdef int wcswidth(unicode ustr, n=*)
cpdef int wcwidth_uint32(uint32_t wc)
cpdef bint is_EMB(unicode uwc)
