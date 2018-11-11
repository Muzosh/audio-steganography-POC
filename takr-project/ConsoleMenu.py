from MessageHelper import MessageHelper
from AudioHelper import AudioHelper


# import tkinter as tk
# from tkinter import filedialog

class ConsoleMenu:
    def __init__(self):
        self.ah = AudioHelper()
        self.mh = MessageHelper()
        self.coverFilePath = ""
        self.__menu()

    # main menu
    def __menu(self):
        while True:
            try:
                menu = int(input("MAIN MENU:\n1: Encode\n2: Decode\n3: Exit\nYour choice: "))

                if menu == 1:
                    self.__encodeMethod()

                elif menu == 2:
                    self.__decodeMethod()

                elif menu == 3:
                    exit()
                else:
                    print("Wrong value was inserted - please use number in range 1-3.\n\n\n\n")
            except ValueError:
                print(
                    "ValueError - incorrect input - please use number in range 1-3.\n\n\n")

    def __encodeMethod(self):
        audioFilePath = input(
            "Write the path of audio file: pro test stačí jen enter teď")  # ke konci mozna poresit otevirani fileExploreru

        # root = tk.Tk()
        # root.withdraw()

        # audioFilePath = filedialog.askopenfilename()

        audioFilePath = "song.mp3" # dočasné
        maxLength = self.ah.countMessageLength(audioFilePath)

        message = input(
            "\n\nYou can use %d characters for your secret message.\nPlease, write your message: " % maxLength)

        while len(message) > maxLength:
            message = input(
                "\n\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        self.coverFilePath = self.mh.encodeMessageIntoCoverFile(message, audioFilePath)
        print(
            "\n\nMessage encoding into audio file was successful! "
            "Your new audio file is located in the same folder as original file.\n")

    def __decodeMethod(self):
        while True:
            try:
                menu2 = int(input("\n\n\nWould you like to immediately decode previously encoded file?"
                                  "\n1: Yes, continue\n2: No, I will choose another file\nYour choice: "))

                if menu2 == 1:
                    if self.coverFilePath != "":
                        encryptedMessage = self.mh.decodeMessageFromCoverFile(self.coverFilePath)
                    else:
                        print("\nThere was no previous encoding.")
                        continue
                    break

                elif menu2 == 2:
                    coverFilePath = input("\nWrite the path of audio file you want to decode: ")
                    encryptedMessage = self.mh.decodeMessageFromCoverFile(coverFilePath)
                    break
                else:
                    print("\nWrong value was inserted - please use number in range 1-2.\n\n\n")
            except ValueError:
                print(
                    "\nValueError - incorrect input - please use number in range 1-2.\n\n\n")

        print(encryptedMessage)