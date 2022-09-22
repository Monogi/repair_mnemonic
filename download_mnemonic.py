# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-

import requests


def get_mnemonic_list(file=False):
    data = requests.get(
        'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt').text.strip()
    if file:
        with open("mnemonic", "w") as file:
            file.write(data)
    return data.split('\n')


if __name__ == '__main__':
    dictionary = get_mnemonic_list(file=True)
    print(dictionary)
