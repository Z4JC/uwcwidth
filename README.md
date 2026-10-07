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
`uwcwidth` should work fine on various scripts such as Cyrillic, Katakana,  and also Emojis in Unicode v16.0. This includes Emojis that use Variation Selector 15 and 16, Zero Width Joiner, Emoji Modifiers for skin type, etc. Overall, `uwcwidth` is probably more accurate than whatever is currently shipping with your OS and whatever your terminal is using in 2024.

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

## Performance: 2.2x faster than `wcwidth`
For CJK languages, `uwcwidth` is about 2.2 times faster than the popular, well-documented and highly tested [wcwidth](https://github.com/jquast/wcwidth) library, while maintaining similar accuracy by skipping some less-common scripts like Devanagari and emoji sequences like VS-15. It is only slightly slower than `cwcwidth`, which does not work on new Emojis and breaks on some other edge cases.

```python3
In [1]: import wcwidth, cwcwidth, uwcwidth
In [2]: %%timeit
   ...: wcwidth.wcswidth("コンニチハ, セカイ!")
125 ns ± 0.822 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)

In [3]: %%timeit
   ...: cwcwidth.wcswidth("コンニチハ, セカイ!")
50.2 ns ± 0.246 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)

In [4]: %%timeit
   ...: uwcwidth.wcswidth("コンニチハ, セカイ!")
57.4 ns ± 0.257 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
```
