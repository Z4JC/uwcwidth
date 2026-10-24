## uwcwidth
*terminal width of Unicode 16.0+Emoji strings in nanoseconds*

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uwcwidth)
[![PyPI - Version](https://img.shields.io/pypi/v/uwcwidth)](https://pypi.org/project/uwcwidth/)
[![PyPI - License](https://img.shields.io/pypi/l/uwcwidth)](https://github.com/Z4JC/uwcwidth/blob/main/LICENSE)
![PyPI - Downloads](https://img.shields.io/pypi/dm/uwcwidth)<br>
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Z4JC/uwcwidth/build_deploy.yml)](https://github.com/Z4JC/uwcwidth/actions/workflows/build_deploy.yml)
[![GitHub branch check runs](https://img.shields.io/github/check-runs/Z4JC/uwcwidth/main)](https://github.com/Z4JC/uwcwidth/actions/workflows/test.yml)
![PyPI - Status](https://img.shields.io/pypi/status/uwcwidth)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/uwcwidth)<br>

Use `uwcwidth` when you want to very quickly find out how many characters a Unicode string takes up in your terminal.

For example, `uwcwidth.wcswidth('Hello🥹')` returns `7` because  your terminal will use 5 places for "Hello" and then 2 places for the "🥹" emoji.

`uwcwidth` is designed to run as fast as standard built-in Python string operations and use a tiny amount of memory.


## Installation

```sh
pip install uwcwidth
```

## Isn't this easy?

Let's take a look at "👩‍🦯‍➡️":

While  `len('\U0001F469\u200d\U0001F9AF\u200d\u27a1\ufe0f')` returns `6` because this string has 6 unicode codepoints, we are looking at a single emoji "👩‍🦯‍➡️". This emoji occupies 2 characters in your terminal. Here I am assuming your terminal knows how to deal with the special Zero-Width Joiner (U+200D) and the Variation Selector-16 Emoji (U+FE0F). Things get worse as there are special modifiers for skin tone, which can be either invisible or standalone characters, etc. Also, you have to deal with other languages and their scripts, etc.

## Correctness
`uwcwidth` works on various scripts such as Cyrillic and Katakana, and on emoji in Unicode 16.0, including Emoji ZWJ sequences, Emoji Modifiers for skin tone, and Variation Selector 16. Known differences from python [wcwidth](https://wcwidth.readthedocs.io/en/latest/intro.html):

- `uwcwidth` measures VS-15 (U+FE0E) text-presentation emoji as wide, while `wcwidth` measures narrow, this is considered "contested" and awaits clarification from unicode.org; see [wcwidth issue #211](https://github.com/jquast/wcwidth/issues/211).
- `uwcwidth` measures Standalone regional indicator symbols (U+1F1E6..U+1F1FF) as narrow, where `wcwidth` measures wide.
- `uwcwidth` measures spacing combining marks (`Mc`, used in Devanagari and other Indic scripts) per codepoint; `wcwidth` applies grapheme cluster rules. For example, `wcswidth('हिन्दी')` is 4 in `wcwidth` and 5 here, while `wcswidth('नमस्ते')` is 4 in both.
- `wcwidth` ships Unicode 18.0 tables, so characters assigned in Unicode 17.0 and 18.0 are outside `uwcwidth`'s 16.0 tables and measure by their default width here.
- `wcwidth` offers [wcstwidth](https://wcwidth.readthedocs.io/en/latest/intro.html#wcstwidth) that provides terminal-specific corrections, described more in [Perfecting Terminal Character Width Using Correction Tables](https://www.jeffquast.com/post/perfecting-terminal-character-width-using-correction-tables/) (2026)

Some edge cases that break other `wc(s)width` libraries and a lot of terminals:

```python3
from uwcwidth import wcswidth
# Should be 8 terminal chars: 🏃🏾‍♂️=🏃️🏾♂
assert wcswidth('\U0001F3C3\U0001F3FE\u200d\u2642\ufe0f'
                '=\U0001F3C3\ufe0f\U0001F3FE\u2642') == 8
# Should be 5 terminal chars: ⛹🏼🏴󠁧󠁢󠁳󠁣󠁴󠁿!
assert wcswidth('\u26f9\U0001F3FC'
                '\U0001F3F4\U000E0067\U000E0062\U000E0073'
                '\U000E0063\U000E0074\U000E007F!') == 5
```

See the `tests` folder for more.

## Tiny footprint and code
`uwcwidth` reserves around 4 KB of memory for its lookup tables. Parts of the storage scheme are derived from an older `wcwidth` implementation in [musl libc](https://musl.libc.org/). Generally sparse or dense bitmaps are used to look things up.
The `uwcwidth.pyx` file is under 100 lines of code, with comments and whitespace.

## Performance: 1.2x faster than `wcwidth` on CJK text
For CJK languages, `uwcwidth` is about 1.2 times faster than the popular, well-documented and highly tested [wcwidth](https://github.com/jquast/wcwidth) library, while maintaining *similar* accuracy by skipping some grapheme handling and emoji behaviour, such as the cluster rules for spacing combining marks (`Mc`) used in Devanagari and other Indic scripts, and VS-15 narrowing. On pure ASCII, `wcwidth` is about 3 times faster than `uwcwidth` owing to some shortcuts.

`wcwidth` ships a compiled extension for the stable ABI (`cp310-abi3`). The stable ABI does not expose the interpreter's internal code-point buffer, so every call copies the string into a UCS4 buffer with `PyUnicode_AsUCS4Copy`, while `uwcwidth` is compiled for each Python version and reads the code points in-place.


```python3
In [1]: import wcwidth, cwcwidth, uwcwidth
In [2]: %%timeit
   ...: wcwidth.wcswidth("コンニチハ, セカイ!")
67.7 ns ± 3.33 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)

In [3]: %%timeit
   ...: cwcwidth.wcswidth("コンニチハ, セカイ!")
52.5 ns ± 0.56 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)

In [4]: %%timeit
   ...: uwcwidth.wcswidth("コンニチハ, セカイ!")
55.6 ns ± 0.43 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)
```

Measured on CPython 3.15.0a5 and 3.14.7, x86-64. The 3.14.7 times are 70.1, 57.1 and 54.6 ns.
