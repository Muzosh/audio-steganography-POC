class BitConvertor:

    def __init__(self):
        self.filePath = ""
        self.usableBits = 0

    def countMessageLength(self, filePath):
        self.filePath = filePath
        # zde bude kód pro zjištění maximální délky
        # zaroven doplnit zde atribut usableBits, ktery bude pouzit v dalsi metode
        return 5  # zde bude vracen počet charakterů pro skrytou zprávu - bacha, ne vracet usableBits, ale pocet charakteru (usableBits/8)

    def encodeMessageIntoCoverFile(self, message):

        messageBits = self.tobits(message)

        # zde vytvorit list bitu coverFileBits z původního zvukového souboru
        # pro test je to zatím naplněné random hodnotama

        coverFileBits = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        indexCoverFileBits = 0 #
        indexMessageBits = 0

        # implementováno vkládání bitů na každou osmou pozici
        for bit in coverFileBits:

            if (indexCoverFileBits + 1) % 8 == 0:
                bit = messageBits[indexMessageBits]
                indexMessageBits += 1
                print(bit)

            indexCoverFileBits += 1
        else:
            encryptedFileBits = coverFileBits

        # encryptedFileBits bude finální list bitů, zbývá jej převést zpět na zvukový soubor a uložit
        # na konec poresit return
        return True

    def tobits(self, str):
        result = []
        for c in str:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])
        return result

    def frombits(self, bits):
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b * 8:(b + 1) * 8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)
