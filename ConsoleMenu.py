import pygame
import os
import sys
import wave
from MessageHelper import MessageHelper
from AudioHelper import AudioHelper


class ConsoleMenu:
    """
    Vše potřebné pro komunikaci s uživatelem. Logika se provádí ve třídách Audio a Message Helper,
    které se inicializují v konstruktoruů. Všechny výjimky se zachycují zde, kde se uživateli vypíše, co bylo za
    problém. V samotných Helperech se do konzole pouze vypisuje určitý progress, aby bylo vidět, který proces trvá
    nejdéle a jak dlouho trvá v závislosti na velikosti souboru.
    """
    def __init__(self):
        self.ah = AudioHelper()
        self.mh = MessageHelper()
        self.__menu()

    def __menu(self):
        """
        Hlavní konzolové menu
        :return: Nic, metoda je void
        """
        while True:
            try:
                self.lineSeparator()
                menu = int(input("\nMAIN MENU:\n\t1: Encode\n\t2: Decode\n\t3: Open custom AudioPlayer\n\t4: Exit\nYour choice: "))

                if menu == 1:
                    self.__encodeMethod()

                elif menu == 2:
                    self.__decodeMethod()

                elif menu == 3:
                    self.__play()

                elif menu == 4:
                    exit()
                else:
                    print("\n Wrong value was inserted - please use number in range 1-3.")
            except ValueError:
                print(
                    "\n ValueError - incorrect input - please use number in range 1-3.")

    def __encodeMethod(self):
        """
        Metoda pro komunikaci s uživatelem. Zjišťují se parametry potřebné ke správnému zakódování.
        Prvně se vypíše seznam použitelných souborů ve složce wavSamples (+ kontrola, jestli uživatel zadal
        číslo nebo absolutní cestu k souboru.
        Následně se zjistí, na každý kolikáty byte chce uživatel zapisovat. Poté se zjistí maximální možná délka
        zprávy a vyzve se k zadání zprávy. Ještě se metoda zeptá uživatele, jestli bude chtít zapsat zprávu pouze na
        začátek zvukového souboru nebo jestli chce přepsat úplně každý vybraný byte až do konce souboru.
        Nakonec se zavolají dvě hlavní metody pro kódování: metoda pro vepsání zprávy do bytů a metoda pro převedení
        bytů zpět na zvukový soubor.
        :return: Nic, metoda je void
        """
        self.lineSeparator()
        fileList = self.getAndShowFileList(False)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")

        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) +\
                                "/wavSamples/" + fileList[int(audioFilePath) - 1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        try:
            songBytes = self.ah.openAudioFile(audioFilePath)
        except:
            print(" -> File was not found. Process has ended!")
            return

        self.lineSeparator()
        print("\nUse the LSB of every N-st/nd/rd/th byte. Please specify N: ", end="")
        while True:
            try:
                everyNByte = int(input())
                maxLength = self.mh.countMessageLength(songBytes, everyNByte)
                if maxLength <= 0:
                    print("Chosen file is not big enough to use LSB of every %dth byte!\nPlease specify new N: " %everyNByte, end="")
                    continue
                break
            except ValueError:
                print("Wrong value inserted! Please enter only number: ", end="")

        self.lineSeparator()
        message = input(
            "\nYou can use %d characters for your secret message.\n\t"
            "Be aware, you can't use character '#'.\n\tPlease, write your message: " % maxLength)

        while len(message) > maxLength:
            message = input(
                "\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        self.lineSeparator()
        opt = input("\nWould you like to fill full audio with LSB? (yes/no): ")
        while True:
            if opt.lower() == 'yes':
                fillAll = True
                break
            elif opt.lower() == 'no':
                fillAll = False
                break
            else:
                opt = input("Please write 'yes' or 'no': ")
        try:
            encryptedSongBytes = self.mh.encodeMessageIntoCoverFile(message, songBytes, fillAll, everyNByte)
            self.ah.convertBytesToAudio(encryptedSongBytes, audioFilePath, fillAll, everyNByte)

            print(
                "\nMessage encoding into audio file was successful! "
                "Your new audio file is located in the same folder as original file.")

        except IndexError:
            print(" -> Index out of range. Process has ended!")
        except ValueError:
            print(" -> Value error. Process has ended!")
        except FileExistsError:
            print(" -> File already exists. Process has ended!")

    def __decodeMethod(self):
        """
        Metoda pro komunikaci s uživatelem. Zjišťují se parametry potřebné ke správnému dekódování.
        Prvně se vypíše seznam použitelných souborů ve složce wavSamples (+ kontrola, jestli uživatel zadal
        číslo nebo absolutní cestu k souboru.
        Následně se zjistí, každý kolikátý byte chce uživatel dekódovat (v našem projektu tato informace bude přímo v
        názvu souborum, v reálném použití by to však mohlo zvýšit bezpečnost steganografie). Nakonec se soubor otevře
        a otevřené byty se předají jako parametr metodě, která soubor dekóduje a pokud možno, zobrazí skrytou zprávu.
        :return: Nic, metoda je void
        """
        self.lineSeparator()
        fileList = self.getAndShowFileList(True)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")
        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) + "/wavSamples/" + fileList[int(audioFilePath) - 1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        self.lineSeparator()
        print("\nDecode the LSB of every N-st/nd/rd/th byte. Please specify N: ", end="")
        while True:
            try:
                eachNByte = int(input())
                break
            except ValueError:
                print("Wrong value inserted! Please enter only number: ", end="")

        try:
            songBytes = self.ah.openAudioFile(audioFilePath)
        except wave.Error:
            print(" -> File was not found. Process has ended!")
            return

        try:
            encryptedMessage = self.mh.decodeMessageFromCoverFile(songBytes, eachNByte)
        except SyntaxError:
            print("\n\nThere is no encrypted message in chosen file. Process has ended!")
            return
        except InterruptedError:
            print("\n\nNo secret message was found. Process has ended!")
            return

        print("\n\nYour encrypted message in chosen file is:\n\t" + encryptedMessage)

    def __play(self):
        """
        Metoda, která nejprve zobrazí použitelné soubory a dá uživateli na výběr. Následně zavolá metodu sloužící
        k přehrávání souborů s jednoduchým konzolovým rozhraním.
        :return: Nic, metoda je void
        """
        self.lineSeparator()
        fileList = self.getAndShowFileList(None)
        audioFilePath = input("Please write path of .wav file or write number of chosen file: ")
        try:
            if self.representsInt(audioFilePath):
                audioFilePath = os.path.dirname(sys.modules['__main__'].__file__) + "/wavSamples/" + fileList[int(audioFilePath)-1]
        except IndexError:
            print("\nNo file with such a number. Process has ended!")
            return

        try:
            self.ah.audioPlayer(audioFilePath)
        except pygame.error:
            print("\nFile could not be opened. Process has ended!")
            return
        except FileNotFoundError:
            print("\nFile could not be opened. Process has ended!")
            return

    def getAndShowFileList(self, onlyEncrypted):
        """
        Tato metoda získá list všech souborů ve složce wavSample na základě parametru. List následně vypíše a vrátí
        :param onlyEncrypted: Boolean, který určuje, jaké konkrétní soubory chceme do listu získat. Pro každou metodu
            volající tuhle metodu se hodí totiž jiné soubory. Jednoduše se to pomocí podmínek naparsuje do listu.
        :return: Vrací list stringů, ve kterých jsou názvy použitelných souborů v projektové složce.
        """
        if onlyEncrypted:
            fileList = list(filter(lambda x: "-encrypted" in x or "-encrypted-filled" in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        elif onlyEncrypted == None:
            fileList = list(filter(lambda x: ".wav" in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        else:
            fileList = list(filter(lambda x: ".wav" in x and "-encrypted" not in x and "-encrypted-filled.wav" not in x,
                                   os.listdir(os.path.dirname(sys.modules['__main__'].__file__)+"/wavSamples/")))
        print()
        i = 1
        for song in fileList:
            print("\t" + str(i) + ": " + song)
            i += 1
        return fileList

    def representsInt(self, s):
        """
        Jednoduchý equivalent int.TryParse(string s) z jiných jazyků. Pokusí se do intu naparsovat string a pokud se
        to podaří, vrátí True, pokud ne, vrátí False
        :param s: Vstupní string, který zkoušíme naparsovat do integeru.
        :return: Vrací boolean hodnotu na základě toho, jestli string lze naparsovat.
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def lineSeparator():
        """
        Jednoduchá metoda sloužící ke zkrášlení a zlepšení přehlednosti v konzolovém rozhraní.
        :return: Nic, metoda je void
        """
        print("----------------------------------------------------------"
              "----------------------------------------------------------", end="")
