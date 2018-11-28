import wave


class AudioHelper:
    """
    Class AudioHelper contain methods which work with cover file (audio file).
    """

    def openAudioFile(self, audioFilePath):
        """

        :param audioFilePath:
        :return: individual bytes of audio
        """
        print("\n\tProgress: Opening default file", end="")
        with wave.open(audioFilePath, mode='rb') as oldFile:
            print(" -> Reading song frames", end="")
            songFrames = oldFile.readframes(oldFile.getnframes())
            print(" -> Writing song frames into array", end="")
            songBytes = bytearray(list(songFrames))
            print(" -> Finished!")
            return songBytes


    def convertBytesToAudio(self, encryptedSongBytes, audioFilePath):

        print("\n\tProgress: Opening old file in order to get song parameters", end="")
        song = wave.open(audioFilePath, mode='rb')
        newAudioFilePath = audioFilePath[:-4] + "-encrypted.wav"
        print(" -> Writing into new audio file", end="")
        with wave.open(newAudioFilePath, 'wb') as newFile:
            newFile.setparams(song.getparams())
            newFile.writeframes(encryptedSongBytes)
        song.close()
        print(" -> Finished!")