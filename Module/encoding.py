# Adapted from https://cs.stackexchange.com/a/65744

import string

_default_base = string.digits + string.ascii_letters


def v2r(n: int, base: str = _default_base) -> str:  # value to representation
    """Convert a positive number to its digit representation in a custom base."""
    if n == 0:
        return base[0]
    b = len(base)
    digits = ''
    while n > 0:
        digits = base[n % b] + digits
        n = n // b
    return digits


def r2v(digits: str, base: str = _default_base) -> int:  # representation to value
    """Compute the number represented by string 'digits' in a custom base."""
    b = len(base)
    n = 0
    for d in digits:
        n = b * n + base[:b].index(d)
    return n
