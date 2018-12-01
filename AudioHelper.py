import wave
import ConsoleMenu
from pygame import mixer


class AudioHelper:
    """
    Class AudioHelper contain methods which work with cover file (audio file).
    """
    def openAudioFile(self, audioFilePath):
        """

        :param audioFilePath:
        :return: individual bytes of audio
        """
        print("\n\tProgress: Opening chosen file", end="")
        with wave.open(audioFilePath, mode='rb') as oldFile:
            print(" -> Reading song frames", end="")
            songFrames = oldFile.readframes(oldFile.getnframes())
            print(" -> Writing song frames into array", end="")
            songBytes = bytearray(list(songFrames))
            print(" -> Finished!")
            return songBytes


    def convertBytesToAudio(self, encryptedSongBytes, audioFilePath, fillAll):

        print("\n\tProgress: Opening old file in order to get song parameters", end="")
        song = wave.open(audioFilePath, mode='rb')
        if not fillAll:
            newAudioFilePath = audioFilePath[:-4] + "-encrypted.wav"
        else:
            newAudioFilePath = audioFilePath[:-4] + "-fullyEncrypted.wav"
        print(" -> Writing into new audio file", end="")
        with wave.open(newAudioFilePath, 'wb') as newFile:
            newFile.setparams(song.getparams())
            newFile.writeframes(encryptedSongBytes)
        song.close()
        print(" -> Finished!")

    def audioPlayer(self, audioFilePath):
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
                mixer.music.set_volume(mixer.music.get_volume() + 0.1)
            elif opt == '5' or opt.lower() == 'volume down' or opt.lower() == 'decrease volume':
                mixer.music.set_volume(mixer.music.get_volume() - 0.1)
            elif opt == '6':
                mixer.music.fadeout(1000)
                return