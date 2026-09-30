"""
Problem: Top K Frequent Words

You're given a list of words (not pre-counted this time — a raw list with duplicates) and an integer k. Return the k most frequent words, sorted by frequency descending. If two words have the same frequency, they should be sorted alphabetically ascending (not descending like the hashtag problem — pay attention to that difference).

Example:

python
words = ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"]
k = 2

"the" appears 4 times, "is" appears 3 times, "sunny" appears 2 times, "day" appears 1 time. So the answer is ["the", "is"].
"""

# so we need to create the hashmap ourselves since we are receiving an array of words
# take the hashmap of items and translate it into a heap
# sort ties by the words. for example Apple < bear. when we do comparisons we will make every word (lower)
# we should use a min heap
import heapq

class word:

    def __init__(self, text, count):
        self.text = text
        self.count = count

    def __lt__(self, other):
        if self.count != other.count:
            return self.count < other.count

        return self.text > other.text

class word_frequency:

    def __init__(self):
        self.frequencies = []
        self.word_to_freq = {}


    def process_words(self, word_arr, k):

        for w in word_arr:
            self.word_to_freq[w] = self.word_to_freq.get(w, 0) + 1

        for key,v in self.word_to_freq.items(): # get the final word and count from the map

            new_word = word(key,v)
            if len(self.frequencies) <k:
                heapq.heappush(self.frequencies, (v,key, new_word))

            else:
                existing_count,existing_key, ex_word_obj = self.frequencies[0]

                if ex_word_obj < new_word:
                    heapq.heappushpop(self.frequencies, (v,key, new_word))



    def top_k(self, k):

        top_words = []

        for i in range(k):

            count,key,obj = heapq.heappop(self.frequencies)
            top_words.append(key)

        print("top_words: ", top_words)



# did the first part in 20 mins. getting stuck on addressing ties













words = ["the", "day", "is", "sunny", "the", "is", "the", "the", "sunny", "is", "is", "tree", "sand"]
k = 2

test = word_frequency()
test.process_words(words, k)

print("words: ", test.word_to_freq)

for f in test.frequencies:
    c,key,w = f
    print("word: ", w.text, " c: ", c)


test.top_k(k)