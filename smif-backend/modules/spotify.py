import SharedMethods
from Person import *
import models 
import re
from lxml import html


logger = SharedMethods.logSetup.log("Spotify","log.txt")

class Spotify(Person):
    def __init__(self, name=None, username=None, playlistUrl=None):
        self.logger = logger
        self.person = Person(name=name, username=username)
        self.session = models.createSession()
        self.persondb = self.person.persondb.searchForPerson(self.session)
        self.playlistUrl = playlistUrl

    def findPlaylistSongsNumber(self, playlistUrl):
        """
            get the numbers of the songs from playlist url

            Args:
                playlistUrl (str) : link to a public spotify playlist 
            Returns:
                int: The number of the playlist song
        """
        response = SharedMethods.BaseClass.sendRequest(playlistUrl)
        if response.status_code == 200:
            tree = html.fromstring(response.content)
            playlistInfo = tree.xpath('/html/head/meta[6]')[0].get("content")
            if 'songs' in playlistInfo.lower():
                return self.extractSongsNumber(playlistInfo)
            else:
                self.logger.error("every thing is ok, but no songs in the playlist info")
        else:
            self.logger.error("Spotify response is not 200 their is an error")
    
    def extractSongsNumber(self, playlistInfo):
        """
            Extracts the number of songs from a string.

            Args:
                results (str): The string containing information about the playlist.

            Returns:
                int: The number of songs if found, otherwise returns None.
        """
        # Regular expression pattern to extract the number of songs
        pattern = r"\b(\d+)\s+songs\b"

        # Search for the pattern in the string
        match = re.search(pattern, playlistInfo)

        # Check if a match is found
        if match:
            # Extract the number of songs from the match
            songsNum = int(match.group(1))
            self.currentNumber = songsNum
            return songsNum
        else:
            return None

    def checkSongsNumChang(self):
        try:
            oldNum = self.persondb.spotifyEntries[0]
            if self.playlistUrl :
                if oldNum.playlistSongsNumber != self.findPlaylistSongsNumber(self.playlistUrl):
                    return True
                else:
                    return False
            else:
                self.logger.error("no playlist url to check")
        except:
            self.logger.error("error during checking songs number change")

    def storeNewNumber(self):
        if self.currentNumber:
            self.persondb.spotifyEntries[0].playlistSongsNumber = self.currentNumber
            self.session.commit()
            return True


if __name__ == "__main__":
    print("hello")
    