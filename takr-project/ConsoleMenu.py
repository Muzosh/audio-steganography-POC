from BitConvertor import BitConvertor


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
                print("ValueError - incorrect input - you have to use number in range 1-3 as written in main menu.")

            if menu == 1:
                self.__encodeMethod()

            elif menu == 2:
                self.__decodeMethod()

            elif menu == 3:
                exit()

    def __encodeMethod(self):
        bc = BitConvertor()
        audioFile = input("Write the path of audio file: ")
        print("You can use %d characters for your secret message" % bc.countMessageLength(audioFile))

