Calculator the Right Way
========================

So many people argue on this:

![]( http://i3.kym-cdn.com/photos/images/original/000/206/784/4829%203.jpg)

As a programmer: this **must** be thrown `syntax error`.

As a mathematician: `b` *should* considered a multiplicant of `(c+d)`,
    before all of them being divide by `a`.

Then why not implement it as the mathematician said? Ok, let's figure out.

How to Use?
-----------

Inside this dir, just

    python3 calculator

Here is something I recommend you to try out:

    >>> 9/3(2+1)
    1.0
    >>> a, b, c, d = 48, 2, 9, 3
    >>> a/b(c+d)
    2.0
    >>> 10(9(8(7(6(5(4(3(2(1)))))))))
    3628800
    >>> (1+2j)(3-4j)
    (11+2j)
    >>> 1 + 1/phi
    1.618033988749895
    >>> phi(43)
    42

What's Differ from Python?
--------------------------

- `int`, `float`, `complex` are now callable.
- `real`, `imag`, `conjugate` became functions.

The Problems!
-------------

Since mathematician often use the same symbol in difference context,
    e.g. *φ* (`phi`) can mean for both `golden ratio` and `Euler's totient`.
    At the 1st glance this seems legit -- just use `phi ** 2` as a number,
    while `phi(50)` stands for function calling, -- but since Python is a
    1st class function (also function as object), you can pass those functions
    as argument everywhere. This means you never figure out `omicron(phi)`
    seen `phi` as number or function. Also `phi(5)` and `5(phi)` does yield
    different value and can cuase much confusion to newbie.

So this concept should not be implement into real-world programming at all.

See Also
--------

- <http://knowyourmeme.com/memes/48293>

