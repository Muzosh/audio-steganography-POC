class BitConvertor:

    def __init__(self):
        self.filePath = ""
        self.usableBits = 0

    def countMessageLength(self, filePath):
        self.filePath = filePath
        # zde bude kód pro zjištění maximální délky
        # zaroven doplnit zde atribut usableBits, ktery bude pouzit v dalsi metode
        return 5 # zde bude vracen počet charakterů pro skrytou zprávu - bacha, ne vracet usableBits, ale pocet charakteru (usableBits/8)

    def encodeMessageIntoFile(self, message):
        # za pouziti promenne filePath a usableBits (ve ktere uz urcite nejaka cesta je z minule metody) implementovat sifrovani
        return True