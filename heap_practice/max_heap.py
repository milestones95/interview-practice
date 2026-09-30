class heap:

    def __init__(self):
        self.nums = [0]
        self.size = 1 # since we are making the array 1-indexed


    def insert(self, val):
        

        # if heap is empty

        if len(self.nums) == 1:
            self.nums.append(val)


        else:

            # if heap is not empty, set the value as right most child
            arr =  self.nums
            arr.append(val)

            length = len(arr)
            i = length - 1
            while i > 1:
                # swap if the child is greater than its parent
                if arr[i] > arr[i//2]:
                    temp = arr[i]
                    arr[i] = arr[i//2]
                    arr[i//2] = temp
                    i = i//2

                else:
                    break

            self.nums = arr
            

    def remove(self):

        # we need to set the return the top so keep track of it
        # then set the new root to be the right most child and percolate it down

        arr = self.nums
        if  len(self.nums) == 1:
            return None


        top = arr[1]
        right_most_child = arr[len(self.nums)-1]
        arr[ len(self.nums)-1] = None
        arr[1] = right_most_child
        i = 1
        arr.pop()
        while (i*2) <  len(self.nums):

            if (i*2) + 1 < len(self.nums) and arr[(i*2) + 1] > arr[i*2] and arr[(i*2)+1] > arr[i]:
                temp = arr[(i*2) + 1]
                arr[(i*2) + 1] = arr[i]
                arr[i] = temp
                i = (i*2) + 1
            elif arr[i] < arr[i*2]:
                temp = arr[(i*2)]
                arr[(i*2)] = arr[i]
                arr[i] = temp
                i = i*2

            else:
                break

        return top

        

    # """
    #                         6
    #                     /       /
    #                 12             13
    #             /       \         /   /
    #             4       3        5      6

    #             """


test = heap()
test.insert(2)
test.insert(4)
test.insert(7)
test.insert(1)
test.insert(8)
test.insert(3)


print(test.nums)

test.remove()
print(test.nums)
test.insert(15)
print(test.nums)



# took me 20 mins to implement the max_heap insert. hit too many bugs tracking and updating the size of the array and also i was setting the i index to the value of the array instead of the length - 1. took a while to debug

# at 34 mins i did first pass at pop/remove


