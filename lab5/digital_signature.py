import argparse
import sys
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', help='a file to sign')
    parser.add_argument('--verify', default='sign', help='sign or check')

    return parser


def sign(data):
    # Получаем хэш файла
    hash = SHA256.new(data)
    # Генерируем ключи
    keys = RSA.generate(1024)

    # Подписываем -- шифруем с помощью закрытого ключа
    signature = pkcs1_15.new(keys).sign(hash)
    # Записываем подпись в файл
    sign_file = open('signature.sig', 'wb')
    sign_file.write(signature)
    sign_file.close()

    # Записываем открытый ключ в файл
    public_key = keys.publickey()
    public_key_file = open('public_key.cer', 'wb')
    public_key_file.write(public_key.exportKey())
    public_key_file.close()


def check(data):
    # Получаем хэш файла
    hash = SHA256.new(data)
    # Получаем открытый ключ
    public_key_file = open('public_key.cer', 'rb')
    public_key = RSA.import_key(public_key_file.read())

    # Считываем подпись
    signature = open('signature.sig', 'rb').read()
    # Сравниваем
    try:
        pkcs1_15.new(public_key).verify(hash, signature)
        print("The signature is authentic.")
    except (ValueError, TypeError):
        print("The signature is not authentic.")


if __name__ == '__main__':
    funcs = {'sign': sign, 'check': check}
    args = create_parser().parse_args(sys.argv[1:])
    with open(args.filename, 'rb') as input_file:
        data = input_file.read()
        chosen_func = funcs[args.verify]
        hash = chosen_func(data)
