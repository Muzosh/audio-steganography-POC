from AudioHelper import AudioHelper


class MessageHelper:
    """
    Class for methods of message input.
    """

    def __init__(self):
        self.ah = AudioHelper()

    def encodeMessageIntoCoverFile(self, message, maxLength, filePath):
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

        indexMaxLength = 0
        print("{0:032b}".format(messageLength))
        for bit in "{0:032b}".format(messageLength):
            messageBits.insert(indexMaxLength, int(bit))
            if indexMaxLength != 31:
                indexMaxLength += 1

        print(messageBits)  # po to místo je to dobře

        # indexCoverFileBits = 0
        # indexMessageBits = 0
        #
        # for bit in coverFileBits:
        #
        #     if (indexCoverFileBits + 1) % 8 == 0:
        #         bit = messageBits[indexMessageBits]
        #         indexMessageBits += 1
        #         if indexMessageBits == len(messageBits) - 1:
        #             break
        #
        #     indexCoverFileBits += 1

        # i = 0
        # j = 0
        #
        # for bit in coverFileBits:
        #     if (i + 1) % 8 == 0:
        #         bit = messageBits[j]
        #         j += 1
        #     if i == len(message) * 8 + 32 - 1:
        #         break
        #     i += 1

        embeddedFileBits = coverFileBits

        index = 0
        for x in embeddedFileBits:
            if (index + 1) % 8 == 0:
                print(x)
            if index == 100000:
                break
            index += 1

        # encryptedFileBits bude finální list bitů, zbývá jej převést zpět na zvukový soubor a uložit
        # na konec poresit return
        return True

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
