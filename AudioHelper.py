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
        try:
            print("\nProgress: opening old file", end="")
            with wave.open(audioFilePath, mode='rb') as oldFile:
                print(" -> Reading song frames", end="")
                songFrames = oldFile.readframes(oldFile.getnframes())
                print(" -> Writing song frames into array", end="")
                songBytes = bytearray(list(songFrames))
                print(" -> Finished!")
        except FileNotFoundError:
            print("\n File was not found!")
            return -1
        finally:
            return songBytes

    def convertBytesToAudio(self, encryptedSongBytes, audioFilePath):

        print("\nProgress: opening old file in order to get song parameters", end="")
        song = wave.open(audioFilePath, mode='rb')
        newAudioFilePath = audioFilePath[:-4] + "-encrypted.wav"
        print(" -> writing into new audio file", end="")
        with wave.open(newAudioFilePath, 'wb') as newFile:
            newFile.setparams(song.getparams())
            newFile.writeframes(encryptedSongBytes)
        song.close()
        print(" -> Finished!")