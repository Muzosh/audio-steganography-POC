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
                self.lineSeparator()
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

        audioFilePath = "Initial D - Deja Vu.wav"
        if audioFilePath == '':
            print("\n\n")
            return

        try:
            songBytes = self.ah.openAudioFile(audioFilePath)
        except :
            print(" -> File was not found. Process has ended!")
            return

        maxLength = self.mh.countMessageLength(songBytes)

        self.lineSeparator()
        message = input(
            "\nYou can use %d characters for your secret message.\n"
            "Be aware, you can't use character '#'.\nPlease, write your message: " % maxLength)


        while len(message) > maxLength:
            message = input(
                "\nYour message is longer than limit. Please write new message with max %d characters:\n" % maxLength)

        try:
            encryptedSongBytes = self.mh.encodeMessageIntoCoverFile(message, songBytes)
            self.ah.convertBytesToAudio(encryptedSongBytes, audioFilePath)

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
        Method which is called by choosin 2. Decode in main menu
        """

        # Tk().withdraw()
        #audioFilePath = askopenfilename(initialdir="/", title="Select audio file", filetype=[("wav files", "*.wav")])

        audioFilePath = "Initial D - Deja Vu-encrypted.wav"

        if audioFilePath == '':
            print("\n\n")
            return

        songBytes = self.ah.openAudioFile(audioFilePath)
        if songBytes != -1:
             encryptedMessage = self.mh.decodeMessageFromCoverFile(songBytes)
        else:
            return

        print("\nYour encrypted message in chosen file is: " + encryptedMessage)

    @staticmethod
    def lineSeparator():
        print("----------------------------------------------------------"
              "----------------------------------------------------------", end="")