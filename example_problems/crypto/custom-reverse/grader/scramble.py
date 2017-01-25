import re


def swap(input, a, b):
    if a.__class__ == int:
        input[a], input[b] = input[b], input[a]
    elif a.__class__ == str:
        tmp = input[input.index(a)]
        bindex = input.index(b)
        input[input.index(a)] = input[input.index(b)]
        input[bindex] = tmp
    return input


def rotate_left(input, count):
    if count > len(input):
        count = count % len(input)
    return input[count:]+input[:count]


def rotate_right(input, count):
    if count > len(input):
        count = count % len(input)
    return input[-count:]+input[:-count]


def rotate(input, letter, right=True):
    index = input.index(letter)
    if index >= 4:
        index += 1
    index += 1
    return rotate_right(input, index)


def reverse_rotate(input, letter):
    # Guess how we rotated the string, based on:
    # * We know what letter was used
    # * All passwords are short
    #
    # So we try rotating by all possible distances
    # The one we used, is the one that can be rotated forwards!
    print input, letter
    for i in range(len(input)):
        guess = rotate_left(input, i)
        if rotate(guess, letter) == input:
            return guess
    return input


def reverse(input, a, b):
    return input[:a]+list(reversed(input[a:b+1]))+input[b+1:]


def move(input, a, b):
    t = input[a]
    del input[a]
    input.insert(b, t)
    return input


def parse(input, lines):
    inp = list(input)
    for line in lines:
        m = re.match(r"swi (\d), (\d)", line)
        if m:
            inp = swap(inp, int(m.group(1)), int(m.group(2)))
        m = re.match(r"swp (\w), (\w)", line)
        if m:
            inp = swap(inp, m.group(1), m.group(2))
        m = re.match(r"rol (\d)", line)
        if m:
            inp = rotate_left(inp, int(m.group(1)))
        m = re.match(r"ror (\d)", line)
        if m:
            inp = rotate_right(inp, int(m.group(1)))
        m = re.match(r"rot (\w)", line)
        if m:
            inp = rotate(inp, m.group(1))
        m = re.match(r"rev (\d), (\d)", line)
        if m:
            inp = reverse(inp, int(m.group(1)), int(m.group(2)))
        m = re.match(r"mov (\d), (\d)", line)
        if m:
            inp = move(inp, int(m.group(1)), int(m.group(2)))

    return "".join(inp)


def reverse_parse(input, lines):
    inp = list(input)
    for line in reversed(lines):
        m = re.match(r"swi (\d), (\d)", line)
        if m:
            inp = swap(inp, int(m.group(2)), int(m.group(1)))
        m = re.match(r"swp (\w), (\w)", line)
        if m:
            inp = swap(inp, m.group(1), m.group(2))
        m = re.match(r"rol (\d)", line)
        if m:
            inp = rotate_right(inp, int(m.group(1)))
        m = re.match(r"ror (\d)", line)
        if m:
            inp = rotate_left(inp, int(m.group(1)))
        m = re.match(r"rot (\w)", line)
        if m:
            inp = reverse_rotate(inp, m.group(1))
        m = re.match(r"rev (\d), (\d)", line)
        if m:
            inp = reverse(inp, int(m.group(1)), int(m.group(2)))
        m = re.match(r"mov (\d), (\d+)", line)
        if m:
            inp = move(inp, int(m.group(2)), int(m.group(1)))
    return "".join(inp)
