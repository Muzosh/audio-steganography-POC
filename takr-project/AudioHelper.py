import binascii
import os


class AudioHelper:
    """
    Class AudioHelper contain methods which work with cover file (audio file).
    """

    def convertAudioToBinary(self, filePath):
        """
        Method for converting raw audiofile to list of bits.

        :param filePath:
        :return audioBitList --> list of bits (audi file):
        """
        file = open(filePath, "rb")
        with file:
            contentOfAudio = file.read()
            hexadecimal = binascii.hexlify(contentOfAudio)
            decimal = int(hexadecimal, 16)
            binaryStringAudio = bin(decimal)[2:].zfill(8)
            audioBitList = []

            for bit in binaryStringAudio:
                audioBitList.append(bit)

            # Stejný for, jako nahoře, ale zobrazuje i progress - bohužel mi to přijde trošku pomalejší
            # i = 0
            # for bit in binaryStringAudio:
            #     if i == 0:
            #         print("Progress: 0%")
            #     if i == int(len(binaryStringAudio) * 0.25):
            #         print("Progress: 25%")
            #     if i == int(len(binaryStringAudio) * 0.5):
            #         print("Progress: 50%")
            #     if i == int(len(binaryStringAudio) * 0.75):
            #         print("Progress: 75%")
            #     if i == len(binaryStringAudio) - 1:
            #         print("Progress: 100%")
            #     audioBitList.append(int(bit))
            #     i += 1

        return audioBitList

    def countMessageLength(self, filePath):
        lengthOfAudio = os.path.getsize(filePath)
        return int((lengthOfAudio / 8) - 5)
