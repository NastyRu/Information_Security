import random
import math
import argparse
import sys
from base64 import b32encode, b32decode

_begin = 17
_end = 1000


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='file of input message', required=True)
    parser.add_argument('-e', '--encode', help='file of encode message', required=True)
    parser.add_argument('-d', '--decode', help='file of decode message', required=True)

    return parser


def miller_rabin_test(n):
    k = int(math.log(n, 2) + 1)

    if (n == 2 | n == 3):
        return True

    if (n < 2 | n % 2 == 0):
        return False

    t = n - 1
    s = 0
    while (t % 2 == 0):
        t //= 2
        s += 1

    for i in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, t, n)

        if (x == 1 | x == n - 1):
            continue

        for r in range(1, s):
            x = pow(x, 2, n)
            if (x == 1):
                return False
            if (x == n - 1):
                break

        if (x != n - 1):
            return False

    return True


def get_prime_number(begin, end, not_equal=0):
    a = random.randint(begin, end)
    t = miller_rabin_test(a)
    while not t:
        a = random.randint(begin, end)
        t = miller_rabin_test(a)
        if (a == not_equal):
            t = False
    return a


def gcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a
    return a + b


def find_prime(a):
    b = random.randint(0, _end)
    while (gcd(a, b) != 1):
        b = random.randint(0, _end)
    return b


def mod_number_one(e, f):
    k = 0
    while ((k * f + 1) % e != 0):
        k += 1
    return (k * f + 1) // e


def RSA_params():
    p = get_prime_number(_begin, _end)
    q = get_prime_number(_begin, _end, p)

    n = p * q
    f = (p - 1) * (q - 1)
    e = find_prime(f)  # открытый
    d = mod_number_one(e, f)  # закрытый

    return n, e, d


def RSA(sym, n, e, d, enc=True):
    if (enc):
        return pow(sym, e, n)
    else:
        return pow(sym, d, n)


def RSA_string(string, n, e, d, enc=True):
    res = ""
    for char in string:
        ch = RSA(ord(char), n, e, d, enc)
        res += chr(ch)
    return res


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    file_read = open(namespace.input, 'rb')
    file_write_enc = open(namespace.encode, 'w')
    file_write_dec = open(namespace.decode, 'wb')

    n, e, d = RSA_params()

    data = b32encode(file_read.read())
    str = data.decode("ascii")
    str_enc = RSA_string(str, n, e, d)
    file_write_enc.write(str_enc)

    str_dec = RSA_string(str_enc, n, e, d, False)
    str = b32decode(str_dec)
    file_write_dec.write(str)

    file_read.close()
    file_write_enc.close()
    file_write_dec.close()


if __name__ == "__main__":
    main()
