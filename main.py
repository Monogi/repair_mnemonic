# #!/usr/bin/python3
# encoding=utf8
# -*- coding: utf-8 -*-
import json
import gen_eth


class Settings:
    online_mode = False
    account_depth = 10
    address_depth = 20

    def __init__(self):
        config_file = self.load_config()
        self.pars_config_file(config_file)

    def pars_config_file(self, configfile):
        online_mode = configfile.get("online_mode")
        if online_mode is not bool():
            print("loading encountered problems online_mode. Use online_mode:false")
        else:
            self.online_mode = online_mode

        self.needed_address = configfile.get("needed_address")
        if self.needed_address is None:
            input("loading encountered problems needed_address. Check config file")
            exit(0)

        self.mnemonic_mask = configfile.get("mnemonic_mask")
        if not isinstance(self.mnemonic_mask, str):
            input("loading encountered problems mnemonic_mask. Check config file")
            exit(0)
        if len(self.mnemonic_mask.strip().split(' ')) < 12:
            input("mnemonic phrase < 12. Check config file")
            exit(0)
        if self.mnemonic_mask.count("?") + self.mnemonic_mask.count("*") + self.mnemonic_mask.count("@") == 0:
            input("mnemonic mask is empty. Use ?/*/@ . Check config file")
            exit(0)

        search_depth = configfile.get("search_depth").lower()
        if not isinstance(search_depth, str):
            print("loading encountered problems search_depth. Use standat(10x20)")

        elif search_depth == "standart":
            print("Use standat(10x20)")
        elif search_depth == "minimal":
            print("Use minimal(1x1)")
        elif search_depth.count("x"):
            self.account_depth = int(search_depth.split('x')[0])
            self.address_depth = int(search_depth.split('x')[1])

    @staticmethod
    def load_config():
        try:
            with open("conf.json", "r") as config_file:
                return json.loads(config_file.read())

        except json.decoder.JSONDecodeError as exception:
            input(f"Config is bad: {exception}\nChange configuration in conf.json\nPress any key...")
            exit(0)
        except FileNotFoundError:
            with open("conf.json", "w") as config_file:
                config_file.write("""{
                  "online_mode": false,
                  "needed_address": "0x5B2F449F35E37dDe995e51430a7AF9aCa1Af2176",
                  "mnemonic_mask": "acquire slight alone south similar nation noble change mass grass salmon float coyote hip ?",
                  "search depth": "standart"
                   }""")
            input("Config file created\nChange configuration in conf.json\nPress any key...")
            exit(0)


def check_pool_addresses(mnemonic, needed_address, account_depth: int = 10, address_depth: int = 20):
    for account in range(0, account_depth):
        for index in range(0, address_depth):
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


def option_counter(tuple_mask: tuple) -> int:
    """Тут мы считаем сколько возможных вариантов перебора
        ? не известное слово
        {word}* возможное слово,считаем как ?
        {word}@{int} группа перестановок """
    # пока считаем только "?"
    count = len(mnemonic_list) ** (tuple_mask.count("?") + tuple_mask.count("*"))
    return count






if __name__ == "__main__":
    SS = Settings()
    if SS.online_mode:
        import download_mnemonic
        mnemonic_list = download_mnemonic.get_mnemonic_list()
    else:
        with open("mnemonic", "r") as file:
            mnemonic_list = file.read().strip().split('\n')


    tuple_mask = pars_mnemonic_mask(SS.mnemonic_mask)
    print(option_counter(tuple_mask))

    for num_word, word in enumerate(mnemonic_list):
        if num_word % 10 == 0:
            print(num_word)
        var_mnem = ' '.join([i if i != "?" else word for i in tuple_mask])
        result = check_pool_addresses(var_mnem,SS.needed_address, SS.account_depth, SS.address_depth)
        if result:
            print(result)
            break

