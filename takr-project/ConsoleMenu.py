from MessageHelper import MessageHelper
from AudioHelper import AudioHelper

class ConsoleMenu:
    def __init__(self):
        self.__menu()

    # main menu
    def __menu(self):
        menu = None
        while True:
            try:
                menu = int(input("MAIN MENU:\n1: Encode\n2: Decode\n3: Exit\nYour choice: "))
            except ValueError:
                print(
                    "ValueError - incorrect input - you have to use number in range 1-3 as written in main menu.\n\n\n")

            if menu == 1:
                self.__encodeMethod()

            elif menu == 2:
                self.__decodeMethod()

            elif menu == 3:
                exit()

    def __encodeMethod(self):
        mh = MessageHelper()
        ah = AudioHelper()
        audioFile = input("Write the path of audio file: ")  # ke konci mozna poresit otevirani fileExploreru
        maxLength = 5 #ah.countMessageLength(audioFile)

        ah.convertAudioToBinary("ahfchb")

        message = input(
            "\n\nYou can use %d characters for your secret message.\nPlease, write your message: " % maxLength)

        while len(message) > maxLength:
            message = input(
                "\n\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        if mh.encodeMessageIntoCoverFile(message):
            print(
                "\n\nMessage encoding into audio file was successful! "
                "Your new audio file is located in the same folder as original file.\n")  # poresit prehravani zvuku rovnou v programu? (pujde to bez GUI?)
        else:
            print("Message encoding was not successful.")
            # tohle by jsme meli poresit tak, aby teoreticky nikdy nemohlo nastat
            # cili aby ta metoda nikdy nevratila false, poresit vse uz v metode (v pripade chyby vyhodit napr exception, ne vracet false)
            # melo by to byt tak, ze pokud vrati false, tak je to nase chyba, ze jsme tu chybu neporesili uz uvnitr te metody
