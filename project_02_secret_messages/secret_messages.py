import sys
from ciphers import Affine, Atbash, PolybiusSquare


if __name__ == '__main__':

    def cipher_name():
        """Validates user input and returns the name of the cipher the user wants
         to use."""
        cipher = input("\n""These are the current available ciphers:""\n""\n"
                       "-Affine""\n"
                       "-Atbash""\n"
                       "-Polybius Square""\n""\n""\n"
                       "Which cipher would you like to use?"
                       " Please enter the name of the cipher"
                       " or \"q\" for quitting: "
                       ).lower()

        available_ciphers = ["affine", "atbash", "polybius square"]

        while(True):
            if cipher in available_ciphers:
                break
            elif cipher == "q":
                print("Bye")
                sys.exit()
            else:
                cipher = input("\n""Did you spell the name"
                               " of the cipher correctly? Please try again. ")
                continue

        return cipher

    def message_content(encrypt_yes, cipher):
        """Validates user input and returns the message to be to be encrypted or
         decrypted."""
        message = input("\n""That's an excellent cipher."
                        " What's the message? ").upper()

        if cipher == "affine" or cipher == "atbash" or cipher == "polybius square" and encrypt_yes is True:
            alphabet_set = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            while(True):
                message_set = set(message.replace(" ", ""))
                if message_set.issubset(alphabet_set) is True:
                    break
                if message_set.issubset(alphabet_set) is False:
                    message = input("The message must contain only"
                                    " letters, not other characters."
                                    " Please try again: "
                                    ).upper()
                    continue

        if cipher == "polybius square" and encrypt_yes is False:
            message = message.replace(" ", "")
            number_set = set("12345")
            while(True):
                message_set = set(message)
                if message_set.issubset(number_set) is True or message_set == number_set is True:
                    break
                if message_set.issubset(number_set) is False:
                    message = input("The message must contain only"
                                    " numbers between 1 and 5, not other characters."
                                    " Please try again: "
                                    ).upper()
                    continue

        return message

    def encrypt_y_n():
        """Validates user input and returns True for encryption
        and False for decryption."""
        encrypt_y_n = input("Are we going to encrypt or decrypt? ")
        while(True):
            if encrypt_y_n.lower() == "encrypt":
                return True
            if encrypt_y_n.lower() == "decrypt":
                return False
            else:
                encrypt_y_n = input("That was probably a typo."
                                    " Did you mean encrypt or decrypt? ")
                continue

    def pad_number(encrypt_yes, cipher):
        """ Validates user input and returns the pad number."""
        pad = input("Please enter the pad number: ")
        while(True):
            try:
                int(pad)
                if cipher == "affine":
                    if encrypt_yes is True and pad not in Affine.pad_d:
                        Affine.pad_d[pad] = None
                        break
                    if encrypt_yes is True and pad in Affine.pad_d:
                        pad = input("This pad number has been already used."
                                    " Please try another one: ")
                    if encrypt_yes is False:
                        break
                if cipher == "atbash":
                    if encrypt_yes is True and pad not in Atbash.pad_d:
                        Affine.pad_d[pad] = None
                        break
                    if encrypt_yes is True and pad in Atbash.pad_d:
                        pad = input("This pad number has been already used."
                                    " Please try another one: ")
                    if encrypt_yes is False:
                        break
                if cipher == "polybius square":
                    if encrypt_yes is True and pad not in PolybiusSquare.pad_d:
                        PolybiusSquare.pad_d[pad] = None
                        break
                    if encrypt_yes is True and pad in PolybiusSquare.pad_d:
                        pad = input("This pad number has been already used."
                                    " Please try another one: ")
                    if encrypt_yes is False:
                        break
            except ValueError:
                pad = input("The pad number must be an integer."
                            " Please try again: ")

        return pad

    def blocks_y_n(encrypt_yes):
        """Validates user input and returns True/False for
         encryption in blocks of 5."""
        if encrypt_yes is True:
            blocks_y_n = input("Encryption in blocks of 5? y/N ").lower()
            if blocks_y_n == "y":
                return True
            else:
                return False

    def cipher_logic(cipher, message, encrypt_yes, pad, blocks_yes):
        """Calls appropriate method for encryption/decryption
        based on user input"""
        if cipher == "affine":
            if encrypt_yes is True and blocks_yes is True:
                Affine().encrypt_blocks_by_five(message, pad)
            if encrypt_yes is True and blocks_yes is False:
                Affine().encrypt_word_by_word(message, pad)
            if encrypt_yes is False:
                Affine().decrypt_word_by_word(message, pad)
        if cipher == "atbash":
            if encrypt_yes is True and blocks_yes is True:
                Atbash().encrypt_blocks_by_five(message, pad)
            if encrypt_yes is True and blocks_yes is False:
                Atbash().encrypt_word_by_word(message, pad)
            if encrypt_yes is False:
                Atbash().decrypt_word_by_word(message, pad)
        if cipher == "polybius square":
            if encrypt_yes is True and blocks_yes is True:
                PolybiusSquare().encrypt_blocks_by_five(message, pad)
            if encrypt_yes is True and blocks_yes is False:
                PolybiusSquare().encrypt_word_by_word(message, pad)
            if encrypt_yes is False:
                PolybiusSquare().decrypt(message, pad)

    def command_menu():
        """Prompts for user input by calling methods to prompt for and
        validate user input. Passes validated user input to cipher_logic
        function for encryption/decryption. Prints encrypted/decrypted
        messages. Contains loop and prompts for user to keep
        encrypting/decrypting messages or to quit program."""
        print("This is the Secret Messages project"
              " for the Treehouse Techdegree.")
        while(True):
            cipher = cipher_name()
            encrypt_yes = encrypt_y_n()
            message = message_content(encrypt_yes, cipher)
            pad = pad_number(encrypt_yes, cipher)
            blocks_yes = blocks_y_n(encrypt_yes)
            cipher_logic(cipher, message, encrypt_yes, pad, blocks_yes)
            something_else = input("\n""Would you like to encrypt/decrypt"
                                   " something else? Please enter Y/n: ")
            if something_else.lower() != "n":
                continue
            else:
                print("Bye")
                sys.exit()

    command_menu()
