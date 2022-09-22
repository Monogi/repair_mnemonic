# repair_mnemonic
 
Lazy brute force repair mnemonic

# Config file
online_mode: "True/False". Responsible for how we will get a list of mnemonic words from the github repository or locally

needed_address: "0xADDRESS". Target address

mnemonic_mask: "Your@1 Mnemonic* ?  Word@1 Phrase". ? - unknown word, * - maybe this word, @{int} - shift group

search_depth:"standart/minimal/10x20". Standart 10x20(10 accounts and 20 addresses), minimal 1x1, your depth "accounts/addresses"