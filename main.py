# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
import json
import gen_eth

try:
    with open("conf.json","r") as config_file:
        data = json.loads(config_file.read())
except FileNotFoundError:
    with open("conf.json","w") as config_file:
        config_file.write()
    print("Config file created\nChange configuration in conf.json")



online_mode = False

if online_mode:
    import download_mnemonic
    mnemonic_list = download_mnemonic.get_mnemonic_list()
else:
    with open("mnemonic", "r") as file:
        mnemonic_list = file.read().strip().split('\n')


needed_address = "0x5B2F449F35E37dDe995e51430a7AF9aCa1Af2176"

mnemonic_original = "acquire slight alone south similar nation noble change mass grass salmon float coyote hip potato"

mnemonic_mask = "acquire slight alone south similar    nation noble change mass grass salmon float coyote hip ?"


def check_10x20_addresses(mnemonic, needed_address):
    for account in range(0, 10):
        for index in range(0, 20):
            current_address = gen_eth.mnemonic_to_eth(mnemonic, account_number=account, address_index=index)['address']
            if current_address == needed_address:
                return {"address": needed_address,
                        "mnemonic": mnemonic,
                        "path": f"m/44'/60'/{account}'/0/{index}"}
    else:
        return False


def pars_mnemonic_mask(mnemonic_mask: str) -> tuple:
    mnemonic_mask_list = list()
    [mnemonic_mask_list.append(i) if i != '' else None for i in mnemonic_mask.strip().split(" ")]

    return tuple(mnemonic_mask_list)


tuple_mask = pars_mnemonic_mask(mnemonic_mask)


def option_counter(tuple_mask:tuple) -> int:
    """Тут мы считаем сколько возможных вариантов перебора
        ? не известное слово
        {word}* возможное слово,считаем как ?
        {word}@{int} группа перестановок """
    # пока считаем только "?"
    count = len(mnemonic_list)**tuple_mask.count("?")
    return count
print(option_counter(tuple_mask))

for num_word, word in enumerate(mnemonic_list):
    if num_word%10==0:
        print(num_word)
    var_mnem = ' '.join([i if i!="?" else word for i in tuple_mask])
    result = check_10x20_addresses(var_mnem,needed_address)
    if result:
        print(result)
        break
