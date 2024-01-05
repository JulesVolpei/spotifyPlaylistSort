import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class PlaylistSort:
    __sp = ""
    __idPlaylist = ""
    __playlist = ""
    __mapTempo = {}
    __uriSorted = []

    def __init__(self, clientID, clietnSecret, url, idPlaylist):
        self.__sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clietnSecret, redirect_uri=url, scope="playlist-read-private"))
        self.__idPlaylist = idPlaylist
        try:
            self.__playlist = self.__sp.user_playlist_tracks(user="ArcEcouteDeLaMusique", playlist_id=self.__idPlaylist)
            print("Accès à la playlist")
        except:
            print("Error : Nom de la playlist invalide ?")

    def sort(self):
        # première partie
        for musique in self.__playlist['items']:
            print(musique['track']['name'])
            self.__mapTempo[musique['track']['uri']] = self.__sp.audio_analysis(musique['track']['uri'])['track'][
                'tempo']

        # restant
        tracks = self.__playlist
        while tracks['next']:
            tracks = self.__sp.next(self.__playlist)
            for musique in tracks['items']:
                print(musique['track']['name'])
                self.__mapTempo[musique['track']['uri']] = self.__sp.audio_analysis(musique['track']['uri'])['track']['tempo']

        test = [0 for i in range(len(self.__mapTempo))]
        sortedMap = dict(sorted(self.__mapTempo.items(), key=lambda item: item[1], reverse=True))
        cmpt = 1
        gauche = 1
        droite = 1
        for track in sortedMap:
            if cmpt == 1:
                test[len(test) // 2] = track
            else:
                if cmpt % 2 == 0:
                    test[len(test) // 2 - gauche] = track
                    gauche += 1
                else:
                    test[len(test) // 2 + droite] = track
                    droite += 1
            cmpt += 1
        self.__uriSorted = test

    def creerPlaylist(self, clientID, clientSecret, url, nomPlaylist):
        assert self.__uriSorted != [], "La playlist doit être triée avant !"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID, client_secret=clientSecret, redirect_uri=url, scope='playlist-modify-private playlist-modify-public'))
        nouvellePlaylist = sp.user_playlist_create(user=sp.me()['id'], name=nomPlaylist, public=False)
        sp.playlist_add_items(playlist_id=nouvellePlaylist['id'], items=self.__uriSorted)

if __name__ == "__main__":
    load_dotenv()

    objet = PlaylistSort(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), "http://localhost:8888/callback", "4BHIQDazmdYH7aqdvVATaW")
    objet.sort()
    objet.creerPlaylist(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), "http://localhost:8888/callback", "Bangz 2022 sorted")
