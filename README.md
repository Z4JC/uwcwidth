## Overview
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

## Performance: 30x faster than `wcwidth`
`uwcwidth` is about 30 times faster than the popular, well-documented and highly tested [wcwidth](https://github.com/jquast/wcwidth) library, while maintaining similar accuracy. It's also 5 times faster than `cwcwidth`, which does not work on new Emojis and breaks on some other edge cases.

```python3
In [1]: import wcwidth, cwcwidth, uwcwidth
In [2]: %%timeit
   ...: wcwidth.wcswidth("コンニチハ, セカイ!")
1.28 μs ± 6.22 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)

In [3]: %%timeit
   ...: cwcwidth.wcswidth("コンニチハ, セカイ!")
205 ns ± 0.408 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)

In [4]: %%timeit
   ...: uwcwidth.wcswidth("コンニチハ, セカイ!")
38.5 ns ± 0.29 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
```