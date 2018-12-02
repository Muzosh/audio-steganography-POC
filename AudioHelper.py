import wave
import ConsoleMenu
from pygame import mixer


class AudioHelper:
    """
    Třída sloužící k práci se zvukovým souborem. Otevřít zvukový soubor, konvertovat byty na zvukový soubor a
    jednoduchý audio player.
    """
    def openAudioFile(self, audioFilePath):
        """
        Metoda sloužící k otevření zvukového .wav souboru. Otevře soubor a do proměnné songFrames zapíše jednotlivé
        framy souboru. Následně se pouze framy překonvertují na list bytů, který se následně vrací
        :param audioFilePath: Absolutní, či relativní cesta k souboru. Pokud uživatel pouze zadá jméno souboru s
            příponou, tento soubor pak musí existovat ve stejné složce jako je projekt. Pokud uživatel vybral soubor
            pomocí číselného výběru, do parametru se vkládá aboslutní cesta.
        :return: Vrací pole bytů, ze tkerých se zvukový soubor skládá
        """
        print("\n\tProgress: Opening chosen file", end="")
        with wave.open(audioFilePath, mode='rb') as audioFile:
            print(" -> Reading song frames", end="")
            songFrames = audioFile.readframes(audioFile.getnframes())
            print(" -> Writing song frames into array", end="")
            songBytes = bytearray(list(songFrames))
            print(" -> Finished!")
            return songBytes

    def convertBytesToAudio(self, encryptedSongBytes, audioFilePath, fillAll, eachNByte):
        """
        Metoda sloužící k převedení již upravených bytů (tedy se zkrytou zprávou) zpět na zvukový soubor.
        Prvně se otevře ještě starý soubor, což je nutné k získání původních parametrů písničky (což je potřebná součást
        správného přehrání .wav souboru). Následně se díky pomocných parametrů zjistí nová absolutní cesta k souboru
        ([:-4] je tam kvůli odstranění přípony .wav). Potom se pomocí knihovny wave nastaví souboru staré parametry
        (chceme, aby zůstaly stejné) a zapíšou se framy pomocí metody, která přijímá vstup jako pole bytů.
        :param encryptedSongBytes: Stream bytů, kde už je na správných místech dosazena správná sekvence bitů, které
            dohromady dávají skrytou zprávu
        :param audioFilePath: absoutní cesta k původnímu zvukovému souboru
        :param fillAll: Boolean, který udává, jestli uživatel na začátku zvolil, jestli se má soubor kódovat až do konce
        :param eachNByte: Integer, který udává, na každý kolikátý byte se zpráva zapsala (tohle je čistě pro nás, aby
            bylo jednodušší ověřit funkčnost souboru
        :return: Nic, metoda je void
        """
        print("\n\tProgress: Opening old file in order to get song parameters", end="")
        song = wave.open(audioFilePath, mode='rb')
        if not fillAll:
            newAudioFilePath = audioFilePath[:-4] + "-encrypted-not-filled-every-{}.-LSB.wav".format(eachNByte)
        else:
            newAudioFilePath = audioFilePath[:-4] + "-encrypted-filled-every-{}.-LSB.wav".format(eachNByte)
        print(" -> Writing into new audio file", end="")
        with wave.open(newAudioFilePath, 'wb') as newFile:
            newFile.setparams(song.getparams())
            newFile.writeframes(encryptedSongBytes)
        song.close()
        print(" -> Finished!")

    def audioPlayer(self, audioFilePath):
        """
        Jednoduchý hudební přehrávač přímo v konzoli. Pomocí wave se získají parametry souboru, který chceme přehrát,
        aby se mohly naparsovat do pygame.music.init(), díky kterému pak soubor můžeme přehrát.
        :param audioFilePath: Absolutní cesta k souboru
        :return: Nic, metoda je void
        """
        with wave.open(audioFilePath, mode='r') as audio:
            songParams = audio.getparams()

        mixer.init(songParams.framerate, -songParams.sampwidth*8, songParams.nchannels, 4096)
        mixer.music.load(audioFilePath)
        mixer.music.set_volume(0.05)
        mixer.music.play(-1)
        mixer.music.pause()

        print("\nSucessfully opened!")

        i = 0
        while True:
            if i % 10 == 0:
                ConsoleMenu.ConsoleMenu.lineSeparator()
                print("\nChoose your option:\n\t1: Play/Unpause\n\t2: Pause\n\t3: Start from the beginning (rewind)"
                      "\n\t4: Increase volume\n\t5: Decrease volume\n\t6: Exit")
            i += 1
            opt = input("Write your option: ")
            if opt == '1' or opt.lower() == 'play' or opt.lower() == 'unpause':
                mixer.music.unpause()
            elif opt == '2' or opt.lower() == 'pause':
                mixer.music.pause()
            elif opt == '3' or opt.lower() == 'rewind':
                mixer.music.stop()
                mixer.music.play(-1)
            elif opt == '4' or opt.lower() == 'volume up' or opt.lower() == 'increase volume':
                mixer.music.set_volume(mixer.music.get_volume() + 0.05)
            elif opt == '5' or opt.lower() == 'volume down' or opt.lower() == 'decrease volume':
                mixer.music.set_volume(mixer.music.get_volume() - 0.05)
            elif opt == '6':
                mixer.music.fadeout(1000)
                return
