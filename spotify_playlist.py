from collections import deque

class playlist:

    def __init__(self):
        self.playlist_songs = deque()
        self.next_queue = deque()
        self.current_song = None


    def add_to_playlist(self, song: str):

        self.playlist_songs.append(song)


    def play_next(self, song: str):

        self.next_queue.append(song)

    def advance(self):
        song = None

        try:
            if len(self.next_queue) > 0:
                song = self.next_queue.popleft()

            elif len(self.playlist_songs) > 0:
                song = self.playlist_songs.popleft()

            else:
                raise ValueError("there are no more songs.")
        except ValueError as error:
            print(error)
        

        self.current_song = song

        return song

    def get_current_song(self):

        if self.current_song is None:
            return ("there are no more songs left to play")

        return self.current_song

    

test = playlist()

test.add_to_playlist("duffle bag boy")
test.play_next("strippers")
test.play_next("entrepreneur")

print("current song: ", test.get_current_song())

next_song = test.advance()
print("advance: ", next_song)
print("current song: ", test.get_current_song())



test.add_to_playlist("all there")
next_song1 = test.advance()
print("advance: ")
print("current song: ", test.get_current_song())



next_song3 = test.advance()
print("advance: ")

print("current song: ", test.get_current_song())


next_song4 = test.advance()

print("advance: ", next_song4)
print("current song: ", test.get_current_song())

test.advance()
print("advance: ")

print("current song: ", test.get_current_song())







