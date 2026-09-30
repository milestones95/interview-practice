class document_outline:

    # the top level list should have the head and tail
    def __init__(self):
        self.item_to_node = {}
        self.count = 0
        self.head = None
        self.tail = None


    def insert_item(self, text: str, insertion_pt = 0):
        id = self.count + 1
        new_node = linked_list(text, id)
        # if completely empty
        if self.tail is None:
            new_node.next = None
            new_node.prev = None
            self.head = new_node
            self.tail = new_node

        else:

            temp = self.tail
            new_node.prev = temp
            self.tail.next = new_node
            new_node.next = None
            self.tail = new_node

        self.item_to_node[id] = new_node
        self.count+=1

        # if insert at top level but not empty


        # if insert at nested child


        # make a top level a child of prev

    def indent_item(self, id_to_move):
        curr_node = self.item_to_node[id_to_move]
        prev = curr_node.prev

        # unlink
        
        # does the node have a parent or is it top level?
        old_head = None
        old_tail = None
        old_next = None


        if curr_node.parent:
            old_head = (curr_node is curr_node.parent.head)
            old_tail = (curr_node is curr_node.parent.tail)
            old_next = curr_node.next


        else:
            old_head = (curr_node is self.head)
            old_tail = (curr_node is self.tail)
            old_next = curr_node.next

        if curr_node.parent:
            if old_head:
                curr_node.parent.head = old_next

            if old_tail:
                curr_node.parent.tail = curr_node.prev 

        else:
            if old_head:
                self.head = old_next

            if old_tail:
                print(" prev old node: ", curr_node.prev)
                self.tail = curr_node.prev 

        curr_node = self.unlink(curr_node, id_to_move)


        

        curr_node.parent = prev

        if prev.children:
            curr_node.next = None
            curr_node.prev = prev.children.tail
            prev.children.tail.next = curr_node
            prev.children.tail = curr_node
        else:
            prev.children = children()
            prev.children.head = curr_node
            prev.children.tail = curr_node
            curr_node.next = None


        self.item_to_node[id_to_move] = curr_node


        
    def unlink(self, node, id):

        # if head:
        if node.prev:
            prev = node.prev
            prev.next = node.next
            
            if node.next:
                node.next.prev = prev

        else:
            if node.next:
                node.next.prev = None

        node.next = None
        node.prev = None

        return node
            



    
    def outdent_item(self, id_to_move):

        # make it the prev sibling of the parent

        curr_node = self.item_to_node[id_to_move]
        print("id to move: ", curr_node.id, " text: ", curr_node.text)
        parent = curr_node.parent # hello (1)

        # remove curr node from child list first

        old_head = (curr_node is parent.children.head)
        old_tail = (curr_node is parent.children.tail)
        old_next = curr_node.next

        curr_node = self.unlink(curr_node, id_to_move)
        curr_node.parent = parent.parent

        if old_head:
            parent.children.head = old_next

        if old_tail:
            parent.children.tail = curr_node.prev


        # put it as a sibling

        temp = parent.next # None
        parent.next = curr_node
        curr_node.next = temp
        curr_node.prev = parent
        if temp:
            temp.prev = curr_node
        

    def get_items(self, node):

        while node:
            if node.parent:
                print("parent: ", node.parent.id, "node text: ", node.text, "id: ", node.id)

            else:
                print("node text: ", node.text, "id: ", node.id)

            if node.children:
                self.get_items(node.children.head)
            node = node.next

        return





class linked_list:

    # we should be able to see the prev and next of an item
    # we want to know the parent of a given node if it exists. This allows us to move a node up a level if needed
    # each node should be able to hand a nested list
    def __init__(self, text: str, id):
        self.prev = None
        self.next = None
        self.parent = None
        self.id = id
        self.text = text
        self.children = None

# 1         -> 2        -> 3
    #4->5           ->6

class children:

    def __init__(self):
        self.head = None
        self.tail = None
        # self.items = None # this will be the linked list



test = document_outline()

test.insert_item("hello")
test.insert_item("bye")
test.insert_item("buenos noches")
test.insert_item("bom dia")

print ("before indent")
test.get_items(test.head)


test.indent_item(4)

print("tail: ", test.tail.text)

test.insert_item("adios")




print ("after indent")

test.get_items(test.head)

# test.outdent_item(2)

# # after outdent
# print("after outdent")
# test.get_items(test.head)




# this was much better and required much less help. i got stuck on infinite loop recursion and i was forgetting to delete or update nodes after unlinking. For example updating the head/tail of the children list
# i also didn't follow complete instructions and initially inserted the child for outdent before the parent instead of after. FInished indent much faster than outdent. Got the structure of the classes to correct pretty quickly