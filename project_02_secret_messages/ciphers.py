

class Cipher:
    '''Class containing available ciphers with functionality
    to encrypt or decrypt messages.'''

    def __init__(self):
        '''Constructor'''

    def blocks(self, word):
        l = list(word)
        whole_blocks = int(len(l)/5)
        blocks = []
        while(whole_blocks > 0):
            block = l[:5]
            blocks.append(block)
            del l[:5]
            whole_blocks -= 1
        blocks.append(l)
        blocks_strings = []
        for block in blocks:
            blocks_strings.append("".join(block))
        message_in_blocks = " ".join(blocks_strings)
        print("The encrypted message is: "+message_in_blocks)


class Affine(Cipher):
    '''Class containing Affine cipher functionality for encryption
    and decryption.'''
    pad_d = {}

    def __init__(self):
        super().__init__()
        '''Constructor'''

    def keys_affine(self):
        '''Prompts user for a and b keys of Affine cipher.
        Validates user input. Returns a and b keys of Affine cipher.'''
        print("\n""The keys of the Affine cipher are a and b,"
              "as in the encryption function E(x)=(ax+b)mod m,""\n"
              " where modulus m is the size of the alphabet and"
              " a and b are the key of the cipher.""\n"
              "The value a must be chosen such that a and m"
              " are coprime (m = 26) and a is equal to or greater"
              " than 1 and less than 26.""\n"
              "The value for b can be arbitrary as long as a does"
              " not equal 1 since this is the shift of the cipher.""\n")

        a = input("Please enter the value for a: ")
        while(True):
            possible_coprimes = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
            try:
                a = int(a)
                if a in possible_coprimes:
                    break
                else:
                    a = input("The value a must be chosen such that a and m"
                              " are coprime (m = 26) and a is equal to or"
                              " greater than 1 and less than 26.""\n"
                              "Please try again: ")
                    continue
            except ValueError:
                a = input("The value a must be chosen such that a and m are"
                          " coprime (m = 26) and a is equal to or greater"
                          " than 1 and less than 26.""\n"
                          "Please try again: ")
                continue

        b = input("Please enter the value for b: ")
        while(True):
            try:
                b = int(b)
                if b < 0:
                    b = input("Please enter an integer number equal to"
                              " or higher than 0 for b: ")
                    continue
                else:
                    break
            except ValueError:
                b = input("Please enter an integer number equal to or"
                          " higher than 0 for b: ")
                continue

        keys = (a, b)
        return keys

    def encrypt_word_by_word(self, message, pad):
        print(message, pad)
        '''Splits message into words. Calls encrypt method to encrypt each word
        (loops until all words are encrypted).
        Returns encrypted message with original word order.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        a, b = self.keys_affine()
        word_list = message.split()
        encrypted_list = [self.encrypt(word, a, b) for word in word_list]
        encrypted_message = " ".join(encrypted_list)
        print("The encrypted message is: "+encrypted_message)
        encrypted_message_no_spaces = encrypted_message.replace(" ", "")
        Affine.pad_d[pad] = encrypted_message_no_spaces

    def encrypt_blocks_by_five(self, message, pad):
        '''Removes spaces between words in message and calls the encrypt
        method to encrypt the string (single word). Returns encrypted message
        with letters in blocks by five by calling the blocks method.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        a, b = self.keys_affine()
        word = message.replace(" ", "")
        encrypted_word = self.encrypt(word, a, b)
        self.blocks(encrypted_word)
        Affine.pad_d[pad] = encrypted_word.replace(" ", "")

    def encrypt(self, word, a, b):
        '''Encrypts single word using Affine cipher:
        - Assigns index numbers(values) for letters of the alphabet in a
        dictionary
        - Maps letters in a word to alphabet index numbers
        - Assigns letters of word values calculated by using Affine cipher
        - Maps letters of word to alphabet letters by using calculated
        value to find alphabet letter
        with same index number
        - Returns encrypted word.'''
        a = int(a)
        b = int(b)
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        alphabet_d = {}
        i = 0
        for letter in alphabet:
            alphabet_d[letter] = i
            i += 1
        l = list(word)
        mapped_word = [{letter: alphabet_d[letter]} for letter in l]
        for d in mapped_word:
            for letter, value in d.items():
                d[letter] = (a*value+b) % 26
        encrypted_word = []
        for d in mapped_word:
            for letter, value in d.items():
                for key in alphabet_d.keys():
                    if value == alphabet_d[key]:
                        encrypted_word.append(key)
        encrypted_string = "".join(encrypted_word)
        return encrypted_string

    def decrypt_word_by_word(self, message, pad):
        '''Checks if encrypted message (w/o spaces) & pad number pair exists
        in dictionary. If yes, splits message into words and calls decrypt
        method to decrypt each word (loops until all words are decrypted).
        Returns decrypted message.'''
        message_no_spaces = message.replace(" ", "")
        if pad in Affine.pad_d and Affine.pad_d[pad] == message_no_spaces:
            a, b = self.keys_affine()
            l = message.split()
            decrypted_list = [self.decrypt(word, a, b) for word in l]
            decrypted_message = " ".join(decrypted_list)
            print("The decrypted message is: "+decrypted_message)
        else:
            print("The pad number and the entered message did not match"
                  " with an encrypted message & pad number pair.")

    def decrypt(self, word, a, b):
        '''Creates a dictionary with keys and values of the Affine cypher.
        Loops through letters of word and dictionary to decrypt word.
        Returns decrypted word.'''
        a = int(a)
        b = int(b)
        trasnp_d = {}
        for i in range(26):
            trasnp_d[chr(i+65)] = chr(((a*i+b) % 26)+65)
        l = list(word)
        decryp_l = []
        for letter in l:
            for key in trasnp_d.keys():
                if letter == trasnp_d[key]:
                    decryp_l.append(key)
        decrypted_string = "".join(decryp_l)
        return decrypted_string


class Atbash(Cipher):
    '''Class containing Atbash cipher functionality for
    encryption and decryption.'''
    pad_d = {}

    def __init__(self):
        super().__init__()
        '''Constructor'''

    def encrypt_word_by_word(self, message, pad):
        '''Splits message into words. Calls encrypt method to encrypt each word
        (loops until all words are encrypted).
        Returns encrypted message with original word order.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        word_list = message.split()
        encrypted_list = [self.encrypt(word) for word in word_list]
        encrypted_message = " ".join(encrypted_list)
        print("The encrypted message is: "+encrypted_message)
        encrypted_message_no_spaces = encrypted_message.replace(" ", "")
        Atbash.pad_d[pad] = encrypted_message_no_spaces

    def encrypt_blocks_by_five(self, message, pad):
        '''Removes spaces between words in message and calls the encrypt
        method to encrypt the string (single word). Returns encrypted message
        with letters in blocks by five by calling the blocks method.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        word = message.replace(" ", "")
        encrypted_word = self.encrypt(word)
        self.blocks(encrypted_word)
        Atbash.pad_d[pad] = encrypted_word.replace(" ", "")

    def encrypt(self, word):
        '''Encrypts single word using the Atbash cipher.
        Returns encrypted word.'''
        encryption_d = {}
        for i in range(26):
            encryption_d[chr(i+65)] = chr(90-i)
        l = list(word)
        encryp_l = []
        for letter in l:
            for key in encryption_d.keys():
                if letter == key:
                    encryp_l.append(encryption_d[key])
        encrypted_string = "".join(encryp_l)
        return encrypted_string

    def decrypt_word_by_word(self, message, pad):
        '''Checks if encrypted message (w/o spaces) & pad number pair exists
        in dictionary. If yes, splits message into words and calls decrypt
        method to decrypt each word (loops until all words are decrypted).
        Returns decrypted message.'''
        message_no_spaces = message.replace(" ", "")
        if pad in Atbash.pad_d and Atbash.pad_d[pad] == message_no_spaces:
            l = message.split()
            decrypted_list = [self.decrypt(word) for word in l]
            decrypted_message = " ".join(decrypted_list)
            print("The decrypted message is: "+decrypted_message)
        else:
            print("The pad number and the entered message did not match"
                  " with an encrypted message & pad number pair.")

    def decrypt(self, word):
        '''Creates a dictionary with keys and values of the Atbash cypher.
        Loops through letters of word and dictionary to decrypt word.
        Returns decrypted word.'''
        decryption_d = {}
        for i in range(26):
            decryption_d[chr(i+65)] = chr(90-i)
        l = list(word)
        decryp_l = []
        for letter in l:
            for key in decryption_d.keys():
                if letter == decryption_d[key]:
                    decryp_l.append(key)
        decrypted_string = "".join(decryp_l)
        return decrypted_string


class PolybiusSquare(Cipher):
    '''Class containing Polybius Square cipher functionality for encryption
    and decryption.'''
    pad_d = {}

    def __init__(self):
        super().__init__()
        '''Constructor'''

    def encrypt_word_by_word(self, message, pad):
        '''Splits message into words. Calls encrypt method to encrypt each word
        (loops until all words are encrypted).
        Returns encrypted message with original word order.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        word_list = message.split()
        encrypted_list = [self.encrypt(word) for word in word_list]
        encrypted_message = str(" ".join(encrypted_list))
        print("The encrypted message is: "+encrypted_message)
        encrypted_message_no_spaces = encrypted_message.replace(" ", "")
        PolybiusSquare.pad_d[pad] = encrypted_message_no_spaces

    def encrypt_blocks_by_five(self, message, pad):
        '''Removes spaces between words in message and calls the encrypt
        method to encrypt the string (single word). Returns encrypted message
        with letters in blocks by five by calling the blocks method.
        Adds pad number & encrypted message (w/o spaces) pair to dictionary.'''
        word = message.replace(" ", "")
        encrypted_word = self.encrypt(word)
        self.blocks(encrypted_word)
        PolybiusSquare().pad_d[pad] = encrypted_word.replace(" ", "")

    def encryption_dictionary(self):
        '''Returns dictionary with keys and values for Polybius Square
        cipher encryption/decryption.'''
        l1 = [1, 2, 3, 4, 5]
        l2 = [1, 2, 3, 4, 5]
        five_system_d = {}
        for num1 in l1:
            five_system_d[num1] = l2
        square_coordinates = []
        for key, value in five_system_d.items():
            for item in value:
                square_coordinates.append([key, item])
        alfabet = "ABCDEFHHIKLMNOPQRSTUVWXYZ"
        alfabet_l = list(alfabet)
        encryption_d = {}
        for i in range(25):
            encryption_d[alfabet_l[i]] = square_coordinates[i]
        return encryption_d

    def encrypt(self, word):
        '''Calls encryption_dictionary to get keys and values of the Polybius
        Square cipher. Replaces letters "J" with "I". Loops until all letters
        in word are encrypted. Returns encrypted word.'''
        encryption_d = self.encryption_dictionary()
        l = list(word)
        l = ["I" if item == "J" else item for item in l]
        encryp_l = []
        for letter in l:
            for key in encryption_d.keys():
                if letter == key:
                    encryp_l.append(encryption_d[key])
        encrypted_l2 = []
        for item in encryp_l:
            for num in item:
                encrypted_l2.append(str(num))
        encrypted_result = str("".join(encrypted_l2))
        return encrypted_result

    def pairs(self, word):
        '''Creates a list of pairs out of consecutive characters in a string.
        Returns result.'''
        l = list(word)
        int_l = [int(i) for i in l]
        number_of_pairs = len(int_l)/2
        pairs_l = []
        while(number_of_pairs > 0):
            pair = int_l[:2]
            pairs_l.append(pair)
            del int_l[:2]
            number_of_pairs -= 1
        return pairs_l

    def decrypt(self, message, pad):
        '''Checks if encrypted message (w/o spaces) & pad number pair exists
        in dictionary. If not, function does not decrypt message and prints
        message to user. If yes,
        - calls encryption_d method to get dictionary with encryption keys
        and values (prior to this, spaces between words are removed, but
        this happens already in the function message_content)
        - calls pairs method to list characters in message as pairs of two
        - loops pairs_l and encryption_d to decrypt message
        - returns decrypted message.'''
        if pad in PolybiusSquare.pad_d and PolybiusSquare.pad_d[pad] == message:
            encryption_d = self.encryption_dictionary()
            pairs_l = self.pairs(message)
            decryp_l = []
            for pair in pairs_l:
                for key in encryption_d.keys():
                    if pair == encryption_d[key]:
                        decryp_l.append(key)
            decrypted_message = "".join(decryp_l)
            print("The decrypted message is: "+decrypted_message)
        else:
            print("The pad number and the entered message did not match"
                  " with an encrypted message & pad number pair.")
