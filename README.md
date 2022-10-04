# repair_mnemonic
 
Brute force mnemonic words with Py3 for **Ethereum** addresses

This script pick a mnemonic phrase for the address specified in the config file.

**Does not check balance**

Runs with mnemonic **12 15 18 21 24**

It makes sense to use this if you forgot **1-2** words or forgot the order of words. 


First you need to update conf.json set Account and  mask
* `*` checks first a possible word, then all the others.
* `@group` rearranges words. There may be several groups.
* `?` all words.



# Config file
 Responsible for how we will get a list of mnemonic words from the GitHub repository or locally
    
    online_mode: "true/false".

 Target address

    needed_address: "0xADDRESS".

 Mnemonic words. ? - unknown word, * - maybe this word, @{group} - shift group

    mnemonic_mask: "Your@1 Mnemonic* ?  Word@1 Phrase". 

 search_depth. Standard 1x5, minimal 1x1, your depth "{accounts}x{addresses}"
    
    search_depth:"standart/minimal/10x20". 

# Start
    pip install -r requirements.txt

    python3 main.py

# In the pipeline
logging

multiprocessing

address calculation optimization

usage gpu

notification in tg/email
