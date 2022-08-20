import wave
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from MessageHelper import MessageHelper
from AudioHelper import AudioHelper


class ConsoleMenu:
    """
    Class ConsoleMenu show menu in console and call methods of another classes
    """
    def __init__(self):
        self.ah = AudioHelper()
        self.mh = MessageHelper()
        self.__menu()

    # main menu
    def __menu(self):
        """
        contain main menu
        """
        while True:
            try:
                menu = int(input("\nMAIN MENU:\n1: Encode\n2: Decode\n3: Exit\nYour choice: "))

                if menu == 1:
                    self.__encodeMethod()

                elif menu == 2:
                    self.__decodeMethod()

                elif menu == 3:
                    exit()
                else:
                    print("\n Wrong value was inserted - please use number in range 1-3.\n")
            except ValueError:
                print(
                    "\n ValueError - incorrect input - please use number in range 1-3.\n")

    def __encodeMethod(self):
        """
        Method which is called by choosing 1.Encode in main menu
        """

        # Tk().withdraw()
        # audioFilePath = askopenfilename(initialdir="/", title="Select audio file", filetype=[("wav files", "*.wav")])
        audioFilePath = "song.wav"
        if audioFilePath == '':
            print("\n\n")
            return

        songBytes = self.ah.openAudioFile(audioFilePath)

        if songBytes != -1:
            maxLength = self.mh.countMessageLength(songBytes)
        else:
            return

        message = input(
            "\nYou can use %d characters for your secret message.\nPlease, write your message: " % maxLength)


        while len(message) > maxLength:
            message = input(
                "\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        encryptedSongBytes = self.mh.encodeMessageIntoCoverFile(message, songBytes)
        self.ah.convertBytesToAudio(encryptedSongBytes, audioFilePath)
        print(
            "\nMessage encoding into audio file was successful! "
            "Your new audio file is located in the same folder as original file.\n")

    def __decodeMethod(self):
        """
        Method which is called by choosin 2. Decode in main menu
        """

        #Tk().withdraw()
        #audioFilePath = askopenfilename(initialdir="/", title="Select audio file", filetype=[("wav files", "*.wav")])

        audioFilePath = "song-encrypted.wav"

        if audioFilePath == '':
            print("\n\n")
            return

        songBytes = self.ah.openAudioFile(audioFilePath)
        if songBytes != -1:
             encryptedMessage = self.mh.decodeMessageFromCoverFile(songBytes)
        else:
            return

        print("Your encrypted message in chosen file is: " + encryptedMessage)
