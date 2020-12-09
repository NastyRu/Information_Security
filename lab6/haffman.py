import argparse
import sys
from tree import Leaf, LEFT, buildTree
from math import ceil


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', choices=['enc', 'dec'], default='enc', help='type of compress')
    parser.add_argument('-i', '--input', help='file of input message', required=True)
    parser.add_argument('-o', '--output', help='file of output message', required=True)

    return parser


def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, sys.byteorder)


def compress(all_bytes):
    byte_frequencies = getFrequencies(all_bytes)
    leaves, _ = buildTree(byte_frequencies)

    symbol_map = {leaf.data: leaf.code for leaf in leaves}

    output_bits = '1'
    for b in all_bytes:
        output_bits = output_bits + symbol_map[b]
    output_bytes = bitstring_to_bytes(output_bits)

    max_count_bytes = ceil(leaves[-1].freq.bit_length() / 8)
    header_bytes = len(leaves).to_bytes(2, sys.byteorder)
    header_bytes += max_count_bytes.to_bytes(8, sys.byteorder)

    for leaf in leaves:
        header_bytes += leaf.data.to_bytes(1, sys.byteorder)
        header_bytes += leaf.freq.to_bytes(max_count_bytes, sys.byteorder)

    return header_bytes+output_bytes


def getFrequencies(all_bytes):
    byte_frequencies_dict = {b: 0 for b in all_bytes}

    for b in all_bytes:
        byte_frequencies_dict[b] = byte_frequencies_dict[b] + 1

    return sorted(byte_frequencies_dict.items(), key=lambda item: item[1])


def decompress(input_bytes, byte_frequencies):
    _, tree = buildTree(byte_frequencies)
    input_bits = bin(int.from_bytes(input_bytes, sys.byteorder))[3:]
    output_bytes = b''
    current_node = tree
    for bit in input_bits:
        if bit == LEFT:
            current_node = current_node.left
        else:
            current_node = current_node.right

        if type(current_node) is Leaf:
            output_bytes += current_node.data
            current_node = tree

    return output_bytes


def readFile(filename):
    byte_frequencies = []

    with open(filename, 'rb') as input_file:
        leaves_count = int.from_bytes(input_file.read(2), sys.byteorder)
        max_count_bytes = int.from_bytes(input_file.read(8), sys.byteorder)

        while leaves_count > 0:
            symbol = input_file.read(1)
            code = int.from_bytes(input_file.read(max_count_bytes), sys.byteorder)
            byte_frequencies.append((symbol, code))
            leaves_count -= 1

        input_bytes = input_file.read()
    return input_bytes, byte_frequencies


def main():
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.type == 'dec':
        input_bytes, byte_frequencies = readFile(namespace.input)
        gen_bytes = decompress(input_bytes, byte_frequencies)

        with open(namespace.output, 'wb') as out_file:
            out_file.write(gen_bytes)
    else:
        with open(namespace.input, 'rb') as binaryfile:
            all_bytes = binaryfile.read()
        print('Start length: ', len(all_bytes))

        gen_bytes = compress(all_bytes)
        with open(namespace.output, 'wb') as out_file:
            out_file.write(gen_bytes)

        print('End length: ', len(gen_bytes))


if __name__ == "__main__":
    main()
