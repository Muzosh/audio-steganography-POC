from AudioHelper import AudioHelper


class MessageHelper:
    """
    Class for methods of message input.
    """

    def encodeMessageIntoCoverFile(self, message, songBytes):
        """
        Method for encoding message into cover file (audio file).
        Using method LSB - Last Significant Bit.
        Replace each eighth bit in audio file by bit of message.

        :param message: string which we want to encode to the audio file
        :param songBytes: individual bytes of audio
        :return: bytes of audio file with encrypted message
        """

        print("\nProgress: converting your message into bits", end="")
        message = message + "#"
        messageBits = self.toBits(message)

        print(" -> encoding your message into the cover file", end="")
        i = 0
        for bit in messageBits:
            songBytes[i] = (songBytes[i] & 254) | bit
            i += 1

        print(" -> Finished!")
        return bytes(songBytes)

    def decodeMessageFromCoverFile(self, songBytes):

        print("\nProgress: Reading all LSBs", end="")
        LSBlist = []
        for i in range(len(songBytes)):
            LSBlist.append(songBytes[i] & 1)

        print(" -> Converting LSBs into message", end="")
        message = ""
        for i in range(0, len(LSBlist), 8):         # take all LSBs and iterate through them by 8

            intBinChunks = LSBlist[i:i+8]           # [0,1,0,1,0,0,1,1]

            strBinChunks = map(str, intBinChunks)   # ['0','1','0','1','0','0','1','1']

            charInBinary = "".join(strBinChunks)    # "01010011"

            charUnicode = int(charInBinary, 2)      # 83

            char = chr(charUnicode)                 # 'S'

            message = message + char                # "...S"
        print(" -> Finished")
        print(message)
        return message.split("#")[0]

    def countMessageLength(self, songBytes):
        """
        Auxiliary method for counting message length

        :param songBytes
        :return: integer
        """

        return int(len(songBytes) / 8) - 1

    def toBits(self, string):
        """
        Auxiliary method for converting message - string to bits.

        :param str:
        :return result --> list of bits as integers:
        """
        bitArray = []
        for char in string:

            charByte = bin(ord(char)).lstrip('0b').rjust(8, '0')    # "01100001"

            bitArray.append(charByte)                               # ["01100001", "01101000",...]

        bitArray = ''.join(bitArray)                                # "0110000101101000..."

        return list(map(int, bitArray))                             # [0,1,1,0,0,0,0,1,0,1,1,0,1,0,0,0,...]
