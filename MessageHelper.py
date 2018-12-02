class MessageHelper:
    """
    Třída sloužící k práci se zprávou a jejím de/kódování. + sloužící k získání maximální délky zprávy a
    prevádění stringů na sekvenci bitů.
    """
    def encodeMessageIntoCoverFile(self, message, songBytes, fillAll, eachNByte):
        """
        Tato metoda zapisuje vybranou zprávu do sekvence bytů. Nejdříve se zpráva doplní o určitý počet '#' na
        základě parametru fillAll. Jeden # se vždy vloží před zprávu a jeden za zprávu (popř. se doplní #-mi na
        maximální možnou délku). Následně se každý zvolený (druhý, třetí, atd.. - záleží na parametru eachNByte)
        zapisuje jednotlivý bit ze zprávy (která je předtím převedena na list bitů) a to následovně:
            Byte zvukového souboru se pomocí operace AND porovná s číslem 254 (jehož "maska" je 11111110). Tím
            zajistíme, že prvních 7 bitů zůstane jako původních a poslední se dá na nulu (nebo zůstane na nule).
            Následně porovnáme pomocí operace OR s našim bitem zpráva (takže "maska" bitu bude 0000000 0/1) a tím
            docílíme toho, že prvních 7 bitů zustane stejně, jako původní byte a poslední se nám přepíše na základě
            toho, jakou hodnotu náš bit má.
        Poté se byteArray převede na stream bytů, které se vrátí zpět.
        :param message: Předaná zpráva, která byla uživatelem zvolena.
        :param songBytes: Pole bytů souboru, který nám zjistila metoda AudioHelper.openAudioFile().
        :param fillAll: Boolean, který udává, co si zvolil uživatel co se doplnění týče.
        :param eachNByte: Integer, který udává, na každý kolikátý byte si uživatel přeje zapisovat.
        :return: Stream už přepsaných bytů.
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
        """
        Metoda prvně přečte úplně všechny Least Significant Bits (tedy každý osmý bit v každém N bytu souboru - kde
        N je parametr eachNByte). Následně tyto bity rozdělí po 16 (protože každý charakter jsme si zvolili nakódovat
        na 16 bitů), předělají na string 0 a 1 a přepočítá na Integer. Následně se charakter získá převedením UniCode
        charakteru a připojí se k finálními stringu, který reprezentuje výslednou skrytou zprávu. Výsledná skrytá zpráva
        se pak ještě rozdělí pomocí '#' a vrátí se pouze string na druhé pozici tohoto listu.
        :param songBytes: Pole bytů souboru, který nám zjistila metoda AudioHelper.openAudioFile().
        :param eachNByte: Integer, který udává, na každý kolikátý byte si uživatel přál zapisovat.
        :return: Vrací výslednou zprávu
        """
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

            char = chr(charUnicode)  # 'S'

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
        Jednoduchá metoda sloužící k výpočtu maximální délky zprávy. Z délky se odečte 2 kvůli dvoum potřebným '#'
        před a na konci zprávy, které budou potřeba vždy.
        :param songBytes: Pole bytů, ze kterých se soubor skládá
        :param eachNByte: Integer, který udává, na každý kolikátý byte si uživatel přál zapisovat (ovlivňuje to
            maximální délku)
        :return: Integer - výpočet maximální délky charakterů.
        """
        return int(len(songBytes) / (16*eachNByte)) - 2

    def toBits(self, string):
        """
        Tato metoda pouze vezme string, ve kterém každý charakter přepočítá na UniCode integer, ten převede na bity
        a poté všechny tyto bity spojí do jednoho pole intů.
        :param string: Předaný string pro převedení na bity
        :return: List bitů
        """
        bitArray = []
        for char in string:
            charByte = bin(ord(char)).lstrip('0b').rjust(16, '0')   # S -> "0000000001100001"

            bitArray.append(charByte)                               # ["0000000001100001", "0000000001101000",...]

        bitArray = ''.join(bitArray)                                # "00000000110000101101000..."

        return list(map(int, bitArray))                             # [0,1,1,0,0,0,0,1,0,1,1,0,1,0,0,0,...]
