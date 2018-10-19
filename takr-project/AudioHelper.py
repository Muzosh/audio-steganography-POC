import binascii
import os

class AudioHelper:

    def convertAudioToBinary(self, filePath):
        file = open(filePath, "rb")
        with file:
            contentOfAudio = file.read()
            hexadecimal = binascii.hexlify(contentOfAudio)
            decimal = int(hexadecimal, 16)
            binaryStringAudio = bin(decimal)[2:].zfill(8)

            audioBitList=[]
            for bit in binaryStringAudio:
                audioBitList.append(bit)

        return audioBitList

    def countMessageLength(self, filePath):
        lengthOfAudio = os.path.getsize(filePath)
        return int(lengthOfAudio - 2)
