#cython: language_level=3
# SPDX-License-Identifier: MIT
from uwcwidth.uwcwidth cimport (wcwidth, wcswidth, wcwidth_uint32,
                                is_EMB, is_EMB_uint32)
