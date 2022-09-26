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
        self.mnemonic_mask = None
        self.needed_address = None
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
                  "mnemonic_mask": "change@1 slight@1 alone* south similar nation noble acquire@1 mass grass salmon float coyote hip potato",
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
    l_mask = len(mnemonic_mask_list)
    if l_mask != 12 and l_mask != 15 and l_mask != 18 and l_mask != 21 and l_mask != 24:
        input(f"mnemonic mask does not match 12/15/18/21/24. now {l_mask} Check config file")
        exit(0)

    group = dict()  # "name_group":["word","in","group"]
    group_matr = list()  # [[num_elem,"name_group"],[num_elem2,"name_group2"]]

    # now is list
    queue_tuple = [[i] if i.count('?') + i.count('*') + i.count('@') == 0 else [] for i in mnemonic_mask_list]
    # print(queue_tuple)
    for num_elem, element in enumerate(queue_tuple):
        if element == []:
            if mnemonic_mask_list[num_elem].count("?"):
                queue_tuple[num_elem] = mnemonic_list.copy()

            if mnemonic_mask_list[num_elem].count("*"):
                queue_tuple[num_elem].append(mnemonic_mask_list[num_elem].split("*")[0])
                [queue_tuple[num_elem].append(i) if i not in queue_tuple[num_elem] else None for i in mnemonic_list]

            if mnemonic_mask_list[num_elem].count("@"):
                word_mask = mnemonic_mask_list[num_elem].split("@")
                queue_tuple[num_elem].append(word_mask[0])
                group[word_mask[1]] = [word_mask[0]] if not group.get(word_mask[1]) else group[word_mask[1]] + [
                    word_mask[0]]
                group_matr.append([num_elem, word_mask[1]])

    for i in group_matr:
        [queue_tuple[i[0]].append(word) if not word in queue_tuple[i[0]] else None for word in group[i[1]]]

    return tuple(queue_tuple)


class Counter:

    def __init__(self, queue_tuple):
        self.queue_tuple = queue_tuple
        self.enumerate_mask = self.enumeration_queue(queue_tuple)
        self.stable_count = tuple([len(i) - 1 for i in queue_tuple])
        self.run_count = [0 for i in self.stable_count]
        self.next_count = [0 for i in self.stable_count]

    def get_words(self):
        run_list = ['' for i in self.stable_count]
        for num, elem_enumerate_mask in enumerate(self.enumerate_mask):
            position = elem_enumerate_mask[0]
            run_list[position] = self.queue_tuple[position][self.run_count[position]]
            if num == len(self.enumerate_mask) - 1:
                self.next_count[position] = 1

            while True:
                if self.check_word_position():
                    self.next_count = [0 for i in self.stable_count]
                    break

        return " ".join(run_list)

    def check_word_position(self):
        for position, elem_run_count in enumerate(self.run_count):
            word_pos = elem_run_count + self.next_count[position]
            # print(self.next_count)
            # print(self.run_count)
            if word_pos > self.stable_count[position]:
                if position == self.enumerate_mask[0][0]:
                    print("End. No found")
                    exit(0)
                self.next_count[self.get_previous_enumerate_mask_pos(position)] = 1
                self.next_count[position] = 0
                self.run_count[position] = 0
                return False
            else:
                self.run_count[position] = word_pos
        return True

    def get_previous_enumerate_mask_pos(self, pos):
        for num, element in enumerate(self.enumerate_mask):
            if element[0] == pos:
                return self.enumerate_mask[num - 1][0]

    @staticmethod
    def enumeration_queue(mask):
        def srt(var):
            return var[1]

        # [[0, 2], [1, 3], [2, 1]]
        # [[2, 1], [0, 2], [1, 3]]

        enumerate_mask = [[n, len(i)] for n, i in enumerate(mask)]
        enumerate_mask.sort(key=srt)

        return enumerate_mask


if __name__ == "__main__":
    SS = Settings()
    if SS.online_mode:
        import download_mnemonic

        mnemonic_list = download_mnemonic.get_mnemonic_list()
    else:
        with open("mnemonic", "r") as file:
            mnemonic_list = file.read().strip().split('\n')

    tuple_mask = pars_mnemonic_mask(SS.mnemonic_mask)

    # print(tuple_mask)

    CC = Counter(tuple_mask)
    #
    # print(CC.get_words())
    # print(CC.get_words())

    # exit()
    print("Start Repair")
    num_word = 0
    while True:
        result = check_pool_addresses(CC.get_words(), SS.needed_address, SS.account_depth, SS.address_depth)
        num_word += 1
        if num_word % 1000 == 0:
            print(f'Checked {num_word}')
        if result:
            print(result)
            with open(f'{SS.needed_address}.txt', "w") as founded:
                founded.write(str(result))
            break
    # for num_word, word in enumerate(mnemonic_list):
    #     if num_word % 10 == 0:
    #         print(num_word)
    #     var_mnem = ' '.join([i if i != "?" else word for i in tuple_mask])
    #     result = check_pool_addresses(var_mnem, SS.needed_address, SS.account_depth, SS.address_depth)
    #     if result:
    #         print(result)
    #         break
