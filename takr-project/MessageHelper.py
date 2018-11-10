from AudioHelper import AudioHelper


class MessageHelper:
    """
    Class for methods of message input.
    """

    def __init__(self):
        self.ah = AudioHelper()

    def encodeMessageIntoCoverFile(self, message, filePath):
        """
        Method for encoding message into cover file (audio file).
        Using method LSB - Last Significant Bit.
        Replace each eighth bit in audio file by bit of message.

        :param message:
        :return:
        """

        messageBits = self.tobits(message)
        coverFileBits = self.ah.convertAudioToBinary(filePath)
        messageLength = len(message)

        # Pro kontrolu - Metoda sloužící pro zobrazení prefixu v bitech (např. 00000000000000000000000000000100)
        # print("{0:032b}".format(messageLength))

        # přidání prefixu na začátek audio zprávy v bitech + přidání postfixu (= NULL v ascii kódu = 8x '0')
        indexMaxLength = 0
        for bit in "{0:032b}".format(messageLength):
            messageBits.insert(indexMaxLength, int(bit))
            indexMaxLength += 1
        messageBits.extend([0, 0, 0, 0, 0, 0, 0, 0])

        # Pro kontrolu - Metoda sloužící pro zobrazení listu zprávy (i s pre/postfixem) v bitech, kterou bude potřeba zašifrovat do audiofile
        #  (např. [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,...])
        # print(messageBits)

        # Pro kontrolu - Metoda pro zobrazení prvních (500) bitů v původním audioFile v bitech
        # (např. [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0,...])
        # string = []
        # for x in range(500):
        #     string.append(coverFileBits[x])
        # print(string)

        # zapsání zprávy v bitech na každou osmou pozici do audioFile v bitech
        i = 1
        for bit in messageBits:
            coverFileBits[(i * 8) - 1] = bit
            i += 1

        encryptedFileBits = coverFileBits

        # Pro kontrolu - Metoda sloužící k vypsání prvních (1200) osmých bitů ve finální audioFile v bitech
        # (např.[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ...])
        # string2 = []
        # i = 1
        # for bit in coverFileBits:
        #     if (i + 1) % 8 == 0:
        #         string2.append(embeddedFileBits[i])
        #     if i == 1200:
        #         break
        #     i += 1
        # print(string2)

        # encryptedFileBits bude finální list bitů, zbývá jej převést zpět na zvukový soubor a uložit
        # cesta k uloženému souboru bude nazvaná coverFilePath
        # na konec poresit return
        coverFilePath = "song - encrypted.mp3"
        return coverFilePath

    def tobits(self, str):
        """
        Auxiliary method for converting message - string to bits.

        :param str:
        :return result --> list of bits:
        """
        result = []
        for c in str:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])
        return result

    def frombits(self, bits):
        """
        Reverse method for converting bits of message back to string

        :param bits:
        :return message string:
        """
        chars = []
        for b in range(int(len(bits) / 8)):
            byte = bits[b * 8:(b + 1) * 8]
            chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
        return ''.join(chars)
