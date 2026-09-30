# Create a To-Do List where you can insert items in any part of the list and you can even nest items under another To-Do item 

class item:

    def __init__(self, text, todo_id):
        self.text = text
        self.id = todo_id
        self.prev = None
        self.next = None
        self.children = None
        self.parent = None


class item_list:

    def __init__(self):
        self.head = None
        self.tail = None

class total_list:

    def __init__(self):
        self.item_id_to_item = {}
        self.count = 0
        self.item_list = item_list()


    # insert new item into todo list

    def add_item(self, text, prev_item_id = None, parent_id=None):

        # if there isn't a parent id, it's top level

        new_item = item(text, self.count+1)


        if parent_id is None:

            list_to_insert_into = self.item_list
        else:
            parent_item = self.item_id_to_item[parent_id]
            new_item.parent = parent_item
            if parent_item.children is None:
                parent_item.children = item_list()
                list_to_insert_into = parent_item.children

            else:
                list_to_insert_into = parent_item.children

        if parent_id is None:
            new_item.parent = None

        if parent_id in self.item_id_to_item:
            new_item.parent = self.item_id_to_item[parent_id]

        self.add_item_helper(list_to_insert_into, new_item, prev_item_id)



    def add_item_helper(self, item_list, new_item, prev_item_id):

        # if list is empty
        if item_list.head is None:
            item_list.head = new_item
            item_list.tail = new_item


        # the list already exists
        else:
            
        # if there's a prev element we don't need to know the parent id to insert. 
            # insert at head
            if prev_item_id is None:
                item_list.head.prev = new_item
                new_item.next = item_list.head
                item_list.head = new_item

            else:
                prev_item = self.item_id_to_item[prev_item_id]
                if not prev_item.parent == new_item.parent:
                    print("prev doesn't exist under this parent")
                    return
                if prev_item == item_list.tail:
                    item_list.tail.next = new_item
                    new_item.prev = item_list.tail
                    item_list.tail = new_item
                # if the prev item is present and it's not the tail, then insert in the middle
                else:
                    next_item = prev_item.next
                    prev_item.next = new_item
                    new_item.prev = prev_item
                    new_item.next = next_item
                    next_item.prev = new_item

            # append at the end



        self.item_id_to_item[new_item.id] = new_item



        # increment count
        self.count+=1 




test = total_list()
test.add_item("banana")
test.add_item("apples",1)
test.add_item("salmon",2)
test.add_item("carrots")
test.add_item("peanut butter", None,3)
test.add_item("steak", 1, 5)



node = test.item_id_to_item[5]
print("node: ", node.text)

if node.children:
    print("node parent: ", node.text)

    while node.children.head:
        print("child: ", node.children.head.text)
        node.children.head = node.children.head.next

