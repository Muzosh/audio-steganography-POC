import struct


class MessageHelper:
    """
    Class for methods of message input.
    """

    def encodeMessageIntoCoverFile(self, message, songBytes, fillAll, eachNByte):
        """
        Method for encoding message into cover file (audio file).
        Using method LSB - Last Significant Bit.
        Replace each eighth bit in audio file by bit of message.

        :param message: string which we want to encode to the audio file
        :param songBytes: individual bytes of audio
        :return: bytes of audio file with encrypted message
        """

        print("\n\tProgress: Converting your message into bits", end="")
        if not fillAll:
            message = "#" + message + "#"
        else:
            message = "#" + message + (self.countMessageLength(songBytes, eachNByte) - len(message) - 1) * '#'
        messageBits = self.toBits(message)

        print(" -> Encoding your message into the cover file", end="")

        i = 0
        for bit in messageBits:
            songBytes[i*eachNByte] = (songBytes[i*eachNByte] & 254) | bit
            i += 1

        print(" -> Finished!")
        return bytes(songBytes)

    def decodeMessageFromCoverFile(self, songBytes, eachNByte):
        print("\n\tProgress: Reading all LSBs", end="")
        LSBlist = []
        for i in range(int(len(songBytes)/eachNByte)):
            LSBlist.append(songBytes[i*eachNByte] & 1)

        print(" -> Converting LSBs into message", end="")
        secondHashTag = False
        message = ""
        for i in range(0, len(LSBlist), 16):  # take all LSBs and iterate through them by 16

            intBinChunks = LSBlist[i:i + 16]  # [0,...,0,1,0,1,0,0,1,1]

            strBinChunks = map(str, intBinChunks)  # ['0',...,'0','1','0','1','0','0','1','1']

            charInBinary = "".join(strBinChunks)  # "0...01010011"

            charUnicode = int(charInBinary, 2)  # 83

            char = chr(charUnicode)  # 'S' "#ahoj#

            message = message + char  # "...S"

            if char == '#' and not secondHashTag:
                secondHashTag = True
                continue
            elif char == '#' and secondHashTag:
                break
            elif not secondHashTag:
                raise InterruptedError

        print(" -> Finished")
        if message[0] == '#':
            return message.split('#')[1]
        else:
            raise SyntaxError

    def countMessageLength(self, songBytes, eachNByte):
        """
        Auxiliary method for counting message length

        :param songBytes
        :return: integer
        """

        return int(len(songBytes) / (16*eachNByte)) - 2

    def toBits(self, string):
        """
        Auxiliary method for converting message - string to bits.

        :param str:
        :return result --> list of bits as integers:
        """
        bitArray = []
        for char in string:
            charByte = bin(ord(char)).lstrip('0b').rjust(16, '0')  # "01100001"

            bitArray.append(charByte)  # ["01100001", "01101000",...]

        bitArray = ''.join(bitArray)  # "0110000101101000..."

        return list(map(int, bitArray))  # [0,1,1,0,0,0,0,1,0,1,1,0,1,0,0,0,...]
