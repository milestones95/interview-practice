
""" heaps visually a shown as a tree but they actually are stored as an array

"""
class heap:

    def __init__(self):
        self.nums = [None]
        self.size = 1


    def insert(self, val):
        
        if len(self.nums) == 1:
            self.nums = [None, val]

        else:
            arr = self.nums
            arr.append(None) # the array needs to be one greater than the size with existing elements

            # we need to add a node at the next available right child and then continue swapping up until it is not greater than its parent
            i = len(arr) - 1 # the next available child will be at the last index

            arr[i] = val


            # check to make sure the new inserted value is not less than its parent

            # print("arr: ", arr)

            while i > 1:

                if arr[i] < arr[i//2]:
                    # print("swapping")
                    temp = arr[i]
                    arr[i] = arr[i//2]
                    arr[i//2] = temp

                    i = i//2

                else:
                    break


            self.nums = arr

        self.size+=1


    def remove(self):

        """ for this operation we need to replace the min/top with the right most child. And then do the swapping on the way down to make sure
        it maintains its integrity being a complete tree and in order """

        arr = self.nums

        # first pop the top and replace it with the last right child

        # check if the heap is even empty or if there's just 1 element. 

        if self.size == 1:
            return

        if self.size == 2:
            arr = self.nums[1]
            self.nums[1] = None
            self.size-=1
            return arr

        initial_root = arr[1]
        # otherwise do the swap
        right_most_child = arr[self.size-1]
        arr[1] = right_most_child
        arr[self.size-1] = None
        self.size-=1

        i = 1

        while (i*2) < self.size:
            if (i*2)+1 < self.size and arr[i*2] >= arr[(i*2)+ 1] and arr[i] > arr[(i*2)+1]:
                temp = arr[i]
                arr[i] = arr[(i*2) + 1]
                arr[(i*2) + 1] = temp

                i = (i*2) + 1

            elif arr[i] > arr[i*2]:
                temp = arr[i]
                arr[i] = arr[i*2]
                arr[i*2] = temp
                i = i*2

            else:
                break

        self.nums = arr

        return initial_root

        """
                            2                                   13
                        /       \                              /    \
                    4               6                     ->  4          6. 
                /       \          /    \
            7               8     10      13

"""


test = heap()
test.insert(2)
test.insert(3)
test.insert(7)
test.insert(4)
test.insert(8)
test.insert(1)




print(test.nums)
print(test.size)

test.remove()
print(test.nums)
# print(test.size)

test.remove()
test.remove()
print(test.nums)
