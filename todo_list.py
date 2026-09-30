class todo_list:

    def __init__(self):
        self.products = None
        self.count = 0
        self.tail = None
        self.head = None

    def add_item(self, name: str, prev: int, nested: bool):

        if not nested:
            id = self.count+1

            # if the list is empty
            if self.tail is None:
                new_node = linked_list(id, name)
                self.tail = new_node
                self.head = new_node
                self.products = new_node


            # if the list isn't empty
            else:
                new_node = linked_list(id, name)

                curr = self.head
                while curr and curr.id != prev:
                    curr = curr.next


                temp = curr.next
                curr.next = new_node
                new_node.next = temp

                if temp is None:
                    self.tail = new_node

        else:

            curr = self.head

            # print("curr: ", curr.name)

            if prev != 0:
                while curr and curr.id != prev:
                    curr = curr.next
                # get the existing node we need to nest under

                if curr and curr.next:
                    curr = curr.next

            nested_items = curr.nested_items

            if nested_items is None:
                curr.nested_items = linked_list(curr.nested_count + 1, name)

            else:
                start = curr.nested_items

                while start and start.next:
                    start = start.next

                start.next = linked_list(curr.nested_count + 1, name)

            curr.nested_count+=1

            


            # self.tail.next = new_node
            # self.tail = new_node


        self.count+=1


class linked_list:

    def __init__(self, id: int, name: str):
        self.prev = None
        self.next = None
        self.id = id
        self.name = name
        self.nested_items = None
        self.nested_count = 0


test = todo_list()

test.add_item("banana",0, False)
test.add_item("apple",1, False) #3
test.add_item("chips",1, False) #2
test.add_item("salsa", 1, True) # 4
test.add_item("pizza", 2, False) #5
test.add_item("peanut butter", 0, True)


curr = test.products

while curr:
    print("item: ", curr.name)
    while curr.nested_items:
        print("item nested: ", curr.nested_items.name, " under: ", curr.name)
        curr.nested_items  = curr.nested_items.next
    curr = curr.next

# test.add_item("apple")