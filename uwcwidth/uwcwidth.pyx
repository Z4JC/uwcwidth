#cython: language_level=3
# (C) 2024 !ZAJC!/GDS
# SPDX-License-Identifier: MIT
from libc.stdint cimport uint8_t, uint32_t
from uwcwidth.tables cimport _TABLE, _WTABLE, _EMBTABLE, _LEN_EMBTABLE


cpdef int wcwidth(unicode uwc):
    if len(uwc) != 1:
        raise ValueError('Need a single unicode codepoint, got %r' % uwc)
    return _wcwidth(uwc[0], _TABLE, _WTABLE)


cpdef int wcswidth(unicode ustr, n=None):
    cdef int i = 0, s = 0, w = 0, l = len(ustr) if n is None else n
    cdef uint32_t wc = 0, wc_last = 0
    while i < l:
        wc = ustr[i]
        if wc == 0x200d:  # skip over ZWJ segment
            i, wc_last = i + 2, wc
            if i < l:
                i += 0x1f3fb <= ustr[i] <= 0x1f3ff or ustr[i] == 0xfe0f
            continue
        if wc == 0xfe0f:  # VS-16 hack: force width to 2
            wc_last, w, s, i = wc, 2, s + (w == 1), i + 1
            continue
        w = ((2 - w) if _is_emoji_modifier(wc_last, wc)  # Emoji Modifier
             else _wcwidth(wc, _TABLE, _WTABLE))         # promotes width to 2
        if w == -1:
            return -1
        s, i, wc_last = s + w, i + 1, wc
    return s


cpdef int wcwidth_uint32(uint32_t wc):
    return _wcwidth(wc, _TABLE, _WTABLE)


cpdef bint is_EMB(unicode uwc):
    if len(uwc) != 1:
        raise ValueError('Need a single unicode codepoint, got %r' % uwc)
    return _is_emoji_modifier(uwc[0], 0x1f3fb)


cpdef bint is_EMB_uint32(uint32_t wc):
    return _is_emoji_modifier(wc, 0x1f3fb)


# Identify emoji modifier base per UTS #51 using the _EMBTABLE bitmap
cdef uint8_t _is_emoji_modifier(uint32_t wc_last, uint32_t wc) noexcept:
    if not (0x1f3fb <= wc <= 0x1f3ff):
        return 0
    if wc_last < 0x1f385:
        return (wc_last == 0x261d or wc_last == 0x26f9
                or 0x270a <= wc_last <= 0x270d)
    cdef unsigned int off  = (wc_last - 0x1f385) >> 3
    return _EMBTABLE[off] & (1 << (off & 7)) if off < _LEN_EMBTABLE else 0


# Derived from Rich Felker's musl wcwidth: changed U+E007F to 0 length
# Tables recomputed for Unicode 16.0 (draft)
cdef int _wcwidth(uint32_t wc, uint8_t *table, uint8_t *wtable) noexcept:
    if wc < 0xff:
        return 1 if (wc + 1 & 0x7f) >= 0x21 else (-1 if wc else 0)
    if wc & 0xfffeffffU < 0xfffe:
        if (table[table[wc >> 8] * 32 + ((wc & 255) >> 3)] >> (wc & 7)) & 1:
            return 0
        if (wtable[wtable[wc >> 8] * 32 + ((wc & 255) >> 3)] >> (wc & 7)) & 1:
            return 2
        return 1
    if (wc & 0xfffe) == 0xfffe:
        return -1
    if wc - 0x20000 < 0x20000:
        return 2
    if wc == 0xe0001 or wc - 0xe0020 <= 0x5f or wc - 0xe0100 < 0xef:
        return 0
    return 1
