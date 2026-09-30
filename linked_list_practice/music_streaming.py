"""
Problem: Streaming Queue

Design a system for a music player with:

add_to_queue(song_id, title) — adds a song to the end of the "Up Next" queue. Returns a unique queue_item_id (note: the same song_id can be queued multiple times — e.g. someone requeues their favorite track — so don't assume song identity == queue identity).
play_next() — moves the front of the queue into "Now Playing," pushing whatever was previously playing onto a "History" list. Returns the new now-playing item, or None if queue is empty.
play_previous() — pops the most recent item off History back into Now Playing, and pushes the current Now Playing back onto the front of the Up Next queue.
remove_from_queue(queue_item_id) — O(1) removal of a specific queued item by id, wherever it sits in the queue (not just the ends).
move_to_front(queue_item_id) — bumps a queued item to play next, without rebuilding the queue.
get_queue_titles() — returns titles in current queue order, for sanity-checking your structure.
"""

# so we need to use a hashmap so we can quickly delete in o(1) time from the linkedlist
# need to have a current position pointer

# play next needs to be inserted at the front of current position
class song_node:

    def __init__(self, song_name, song_id):
        self.song_name = song_name
        self.song_id = song_id
        self.prev = None
        self.next = None

class song_queue:

    def __init__(self):
        self.id_to_song = {}
        self.head = None
        self.tail = None
        self.current_position = None
        self.count = 0

# for play next we set current_position to the next song. and next song-> next is the next song in the queue


    def add_song_to_queue(self, song_name):
        song_id = self.count + 1
        # if the list is empty
        new_song = song_node(song_name, song_id)
        if self.tail is None:
            self.head = new_song
            self.tail = new_song
            self.current_position = new_song


        # if the list already has songs
        else:
            self.tail.next = new_song
            new_song.prev = self.tail
            self.tail = new_song
            new_song.next = None

        self.id_to_song[song_id] = new_song
        self.count+=1



    def play_next(self):

        curr = self.current_position

        if curr.next:
            curr = curr.next

        else:
            return None

        self.current_position = curr

        return self.current_position

    def play_previous(self):

        curr = self.current_position

        if curr.prev:
            print("hello")
            curr = curr.prev

        else:
            return None

        self.current_position = curr

        return self.current_position


    
    def get_queue_titles(self):

        curr = self.current_position

        while curr:
            print("curr song: ", curr.song_name, " id: ", curr.song_id)
            curr = curr.next


    def remove_from_queue(self, song_id):
        
        print("hiya")

        try:
            if song_id not in self.id_to_song:
                raise ValueError("song not in queue")

            else:
                song = self.id_to_song[song_id]


                # if song is in the front/ is head
                prev = song.prev
                if prev is None:
                    # None-> 3->4->5 delete 3

                    if song.next is None:
                        self.head = None
                        self.tail = None
                        self.current_position = None
                    else:
                        next_song = song.next # get next song
                        next_song.prev = prev # make the next song point to none as its prev
                        self.current_position = next_song # make the next song the head.
                        self.head = next_song

                # if song is in middle
                else:
                    # print("in else")
                    # print("song next: ", song.next.song_name)

                    # if deleting the tail
                    if song.next is None:
                        prev.next = None
                        self.tail = prev
                    else:
                        prev.next = song.next
                        self.current_position = song.next
                        song.next.prev = prev

                del self.id_to_song[song_id]


        except ValueError as error:
            print(error)




test = song_queue()
test.add_song_to_queue("maybach")
test.add_song_to_queue("old ways")
test.add_song_to_queue("wear my hat")
test.add_song_to_queue("twin fold")
test.add_song_to_queue("slick hater")


test.get_queue_titles()

next_song = test.play_next()
next_song = test.play_next()

# print("playing song: ", next_song.song_name)

# prev_song = test.play_previous()
# prev_song = test.play_previous()

# print("curr song: ", prev_song.song_name)

test.remove_from_queue(5)
print("---------------------")
print("after deletion")

test.get_queue_titles()

prev_song = test.play_previous()

print("curr song: ", prev_song.song_name)

# had a misunderstanding. i sitll had the play next songs so listing the titles was not listing everything since some were already not in the queue. wasted a good 15-20 mins not looking thoroughly on how i was testing. also i wasn't updating current position after making deletions at the head