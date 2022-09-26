# repair_mnemonic
 
Brute force mnemonic words with Py3 for eth addresses
mnemonic 12 15 18 21 24

# Config file
online_mode: "true/false". Responsible for how we will get a list of mnemonic words from the github repository or locally

needed_address: "0xADDRESS". Target address

mnemonic_mask: "Your@1 Mnemonic* ?  Word@1 Phrase". ? - unknown word, * - maybe this word, @{int} - shift group

search_depth:"standart/minimal/10x20". Standart 10x20, minimal 1x1, your depth "{accounts}x{addresses}"