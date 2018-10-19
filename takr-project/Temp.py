import binascii
import os

filePath = 'C:\\Users\\koncp\\Desktop\\mysong.mp3'
file = open(filePath, "rb")
i = os.path.getsize(filePath)
with file:

        byte = file.read(i)
        hexadecimal = binascii.hexlify(byte)
        decimal = int(hexadecimal, 16)
        binary = bin(decimal)[2:].zfill(8)
        #print("hex: %s, decimal: %s, binary: %s" % (hexadecimal, decimal, binary))
        print( "binary: %s" % binary)