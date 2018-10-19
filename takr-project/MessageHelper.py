from AudioHelper import AudioHelper

class MessageHelper:

    def __init__(self):
        self.ah = AudioHelper()


    def encodeMessageIntoCoverFile(self, message):

        messageBits = self.tobits(message)
        coverFileBits = self.ah.convertAudioToBinary
        # zde vytvorit list bitu coverFileBits z původního zvukového souboru
        # pro test je to zatím naplněné random hodnotama

        #coverFileBits = [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
        indexCoverFileBits = 0 #
        indexMessageBits = 0

        # pořešit ještě vkládání
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
