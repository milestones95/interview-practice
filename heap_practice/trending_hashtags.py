"""
Problem: Trending Hashtags

You're building the backend for a social media "Trending" feature. You have a huge stream of hashtag usage counts — e.g. {"python": 15, "ai": 42, "cats": 8, "coding": 42, "news": 30, "memes": 5} — and you need to return the top k most-used hashtags, sorted from most-used to least. If two hashtags have the same count, break the tie alphabetically (so results are deterministic and reproducible, not just "whatever order the dict happened to iterate in").

you're receiving one big dictionary of counts all at once, not an ongoing stream. Think of it like a nightly batch job: at midnight, some other system hands you the full tally of hashtag usage for the day — {"python": 15, "ai": 42, ...} — and your function needs to return the top k from that snapshot. No new hashtags trickle in while you're computing the answer; you have everything up front.

Given k = 3 and the example above, the answer should be ["ai", "coding", "news"] — ai and coding are tied at 42, so alphabetical order puts ai first.

A few things to reason through before you write anything:

Min-heap or max-heap for this one? Think back to the Kth-largest/Kth-smallest quiz question — the heap type here depends on what you need to evict as you go, not on the fact that you want the "top" (most-used) hashtags.
How do you handle the tiebreak? You've now hit this pattern twice — once with the tuple-comparison crash on the patient objects, once with getting the tiebreak direction backwards on patient_id. What do you push into the heap this time so ties resolve alphabetically without needing a custom comparator?
Is this a heapify-up-front situation, or a heappush-one-at-a-time situation? You just described the rule for this — which case does "I already have a full dictionary of counts" fall into?
"""

# we need to heapify this list first because they aren't already guaranteed to be sorted
# i think we need to use a min heap for this. if we reach the size of k, for a new number coming in, we check if it's greater than the root, if it is, we pop the root and push the new incoming number. if not, we discard the incoming number. This way we at all times contain the highest k numbers

import heapq

class hashtag:

    def __init__(self, hashtag, count):
        self.hashtag = hashtag
        self.count = count

class hashtags:

    def __init__(self):
        self.hashtags = []

    def process_hashtags(self, items, k):

        tags = items.items()

        for key,v in tags:
            ht = hashtag(key,v)


            if len(self.hashtags) < k:
                heapq.heappush(self.hashtags, (ht.count, ht.hashtag, ht))

            else:

                existing_c, new_name, new_tag = self.hashtags[0]

                if ht.count > existing_c:
                    print("min: ", existing_c, " new tag: ", ht.count)
                    # print('len(self.hashtags): ', len(self.hashtags))
                    heapq.heappushpop(self.hashtags, (ht.count, ht.hashtag, ht))

        # heapq.heapify(self.hashtags)

        
    def top_k(self, k):
        
        top_k_hashtags = []

        for i in range(k):
            n = heapq.heappop(self.hashtags, (ht.count, ht.hashtag, ht))
            top_k_hashtags.append(n)


counts = {
    "python": 15,
    "ai": 42,
    "cats": 8,
    "coding": 42,
    "news": 30,
    "memes": 5
}

test = hashtags()

test.process_hashtags(counts, 3)


for tag in test.hashtags:
    count, _, t = tag
    print("tag: ", t.hashtag, " count:  ",count)


# k_elements = test.top_k(3)
# print("----------------------")
# for tag in k_elements:
#     count, _, t = tag
#     print("tag: ", t.hashtag, " count:  ",-count)

# print("elements: ", k_elements)
