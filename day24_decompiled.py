def step_1(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 13
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 6
    y *= x
    z += y
    return w, x, y, z


def step_2(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 15
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 7
    y *= x
    z += y
    return w, x, y, z


def step_3(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 15
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return w, x, y, z


def step_4(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 11
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 2
    y *= x
    z += y
    return w, x, y, z


def step_5(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += -7
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 15
    y *= x
    z += y
    return w, x, y, z


def step_6(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 10
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 8
    y *= x
    z += y
    return w, x, y, z


def step_7(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 10
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 1
    y *= x
    z += y
    return w, x, y, z


def step_8(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += -5
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return w, x, y, z


def step_9(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 1 != 0
    z //= 1
    x += 15
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 5
    y *= x
    z += y
    return w, x, y, z


def step_10(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += -3
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 3
    y *= x
    z += y
    return w, x, y, z


def step_11(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += 0
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 5
    y *= x
    z += y
    return w, x, y, z


def step_12(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += -5
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 11
    y *= x
    z += y
    return w, x, y, z


def step_13(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += -9
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 12
    y *= x
    z += y
    return w, x, y, z


def step_14(
    w: int, x: int, y: int, z: int, next_digit: int
) -> tuple[int, int, int, int]:
    w = next_digit
    x *= 0
    x += z
    assert x >= 0
    assert 26 > 0
    x %= 26
    assert 26 != 0
    z //= 26
    x += 0
    x = int(x == w)
    x = int(x == 0)
    y *= 0
    y += 25
    y *= x
    y += 1
    z *= y
    y *= 0
    y += w
    y += 10
    y *= x
    z += y
    return w, x, y, z
