import random
import sys
import argparse
from struct import pack


length = 256


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=['file', 'string'], default='string', help='type of input')
    parser.add_argument('-i', '--input', help='file of input message')
    parser.add_argument('-o', '--output', help='file of output message')
    parser.add_argument('-r', '--rotors', nargs=3, help='files of rotors', default=['1', '2', '3'])

    return parser


def create_alphabet():
    alphabet = []
    for i in range(length):
        alphabet.append(chr(i))
    return alphabet


def random_reflector():
    alphabet = create_alphabet()

    reflector = [0] * length
    for i in range(length):
        reflector[i] = chr(length)

    i = 0
    while len(alphabet):
        while (reflector[i] != chr(length)):
            i += 1

        elem = random.choice(alphabet)
        reflector[i] = elem
        reflector[ord(elem)] = chr(i)
        alphabet.remove(elem)
        if alphabet.count(chr(i)):
            alphabet.remove(chr(i))
    return reflector


def random_rotor():
    rotor = create_alphabet()
    random.shuffle(rotor)
    return rotor


def first_rotor(begin, configuration, symbol):
    symbol = (symbol + ord(begin)) % length

    return configuration[symbol]


def second_rotor(begin_first, begin_second, configuration, symbol):
    symbol = (ord(symbol) + ord(begin_second) - ord(begin_first)) % length

    return configuration[symbol]


def third_rotor(begin_second, begin_third, configuration, symbol):
    symbol = (ord(symbol) + ord(begin_third) - ord(begin_second)) % length

    return configuration[symbol]


def first_rotor_rev(begin, configuration, symbol):
    alphabet = create_alphabet()
    symbol = alphabet[configuration.index(symbol)]
    symbol = chr((ord(symbol) - ord(begin)) % length)

    return symbol


def second_rotor_rev(begin_first, begin_second, configuration, symbol):
    alphabet = create_alphabet()
    symbol = alphabet[configuration.index(symbol)]
    symbol = chr((ord(symbol) - ord(begin_second) + ord(begin_first)) % length)

    return symbol


def third_rotor_rev(begin_second, begin_third, configuration, symbol):
    alphabet = create_alphabet()
    symbol = alphabet[configuration.index(symbol)]
    symbol = chr((ord(symbol) - ord(begin_third) + ord(begin_second)) % length)

    return symbol


def reflector(begin_third, configuration, symbol):
    symbol = (ord(symbol) - ord(begin_third)) % length

    return configuration[symbol]


def reflector_rev(begin_third, symbol):
    symbol = chr((ord(symbol) + ord(begin_third)) % length)

    return symbol


def enigma(str, begin_first, configuration_first, begin_second, configuration_second, begin_third, configuration_third, reflector_conf):
    new_str = b""
    for symbol in str:
        begin_first = chr((ord(begin_first) + 1) % length)

        sym = first_rotor(begin_first, configuration_first, symbol)

        if (ord(begin_first) == length - 1):
            begin_second = chr((ord(begin_second) + 1) % length)

        sym = second_rotor(begin_first, begin_second, configuration_second, sym)

        if (ord(begin_second) == length - 1):
            begin_third = chr((ord(begin_third) + 1) % length)

        sym = third_rotor(begin_second, begin_third, configuration_third, sym)

        sym = reflector(begin_third, reflector_conf, sym)

        sym = reflector_rev(begin_third, sym)
        sym = third_rotor_rev(begin_second, begin_third, configuration_third, sym)
        sym = second_rotor_rev(begin_first, begin_second, configuration_second, sym)
        sym = first_rotor_rev(begin_first, configuration_first, sym)

        new_str += pack("B", ord(sym))
    return new_str


def write_rotor_to_file(filename):
    f = open(filename, 'w')
    rotor = random_rotor()
    for i in range(len(rotor) - 1):
        f.write(str(ord(rotor[i])))
        f.write(' ')
    f.write(str(ord(rotor[len(rotor) - 1])))
    f.close()


def read_rotor_from_file(filename):
    data = []
    try:
        with open(filename) as f:
            for line in f:
                data.append([chr(int(x)) for x in line.split()])
    except:
        print('Файл не существует')
        exit()
    return data[0]


def write_reflector_to_file(filename):
    f = open(filename, 'w')
    reflector = random_reflector()
    for i in range(len(reflector) - 1):
        f.write(str(ord(reflector[i])))
        f.write(' ')
    f.write(str(ord(reflector[len(reflector) - 1])))
    f.close()


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    res = namespace.rotors

    configuration_first = read_rotor_from_file('rotor' + res[0] + '.txt')
    begin_first = chr(0)

    configuration_second = read_rotor_from_file('rotor' + res[1] + '.txt')
    begin_second = chr(0)

    configuration_third = read_rotor_from_file('rotor' + res[2] + '.txt')
    begin_third = chr(0)

    reflector_conf = read_rotor_from_file('reflector.txt')

    if (namespace.type == 'file'):
        try:
            file_read = open(namespace.input, 'rb')
        except:
            print('Файл не существует')
            exit()
        file_write = open(namespace.output, 'wb')
        while True:
            char = file_read.read()
            if not char:
                break
            new_char = enigma(char, begin_first, configuration_first, begin_second, configuration_second, begin_third, configuration_third, reflector_conf)
            file_write.write(new_char)
        file_read.close()
        file_write.close()
    else:
        print("Введите строку для шифрования:")
        str = input()
        bstr = b""
        for sym in str:
            bstr += pack("B", ord(sym))
        new_bstr = enigma(bstr, begin_first, configuration_first, begin_second, configuration_second, begin_third, configuration_third, reflector_conf)
        new_str = ""
        for sym in new_bstr:
            new_str += chr(sym)
        print(new_str)


if __name__ == "__main__":
    main()
