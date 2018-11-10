from MessageHelper import MessageHelper
from AudioHelper import AudioHelper


# import tkinter as tk
# from tkinter import filedialog

class ConsoleMenu:
    def __init__(self):
        self.__menu()
        self.coverFilePath

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
        mh = MessageHelper()
        ah = AudioHelper()
        audioFilePath = input(
            "Write the path of audio file: pro test stačí jen enter teď")  # ke konci mozna poresit otevirani fileExploreru

        # root = tk.Tk()
        # root.withdraw()

        # audioFilePath = filedialog.askopenfilename()

        audioFilePath = "song.mp3"
        maxLength = ah.countMessageLength(audioFilePath)

        message = input(
            "\n\nYou can use %d characters for your secret message.\nPlease, write your message: " % maxLength)

        while len(message) > maxLength:
            message = input(
                "\n\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        self.coverFilePath = mh.encodeMessageIntoCoverFile(message, audioFilePath)
        print(
            "\n\nMessage encoding into audio file was successful! "
            "Your new audio file is located in the same folder as original file.\n")  # poresit prehravani zvuku rovnou v programu? (pujde to bez GUI?)

    def __decodeMethod(self):
        mh = MessageHelper()
        ah = AudioHelper()
        print(self.coverFilePath)
