import uuid


class LinkedList:

    def __init__(self, type, bookmark, folder):
        self.prev = None
        self.next = None
        self.type = type
        self.id = None
        self.bookmark = bookmark
        self.folder = folder


class bookmark:

    def __init__(self, link, title):
        self.link = link
        self.title = title

class folder:

    def __init__(self, title, bookmarks):
        self.title = title
        self.bookmarks = bookmarks
        self.head = None
        self.tail = None



class bookmarks:

    def __init__(self):
        self.item_to_node = {}
        self.count = 0
        self.head = None
        self.tail = None


    def add_item(self, type, item, prev = 0, folder_id = None):

        id = self.count + 1
        self.count = id
        container = None

        if type == "bookmark":

            # what happens if we insert in the front when the list isn't empty
            # inserting in front when list is empty
            # inserting in the middle
            # inserting at the end

            new_bookmark = bookmark(item.link, item.title)
            new_node = LinkedList(type, new_bookmark, None)
            new_node.id = id

            if folder_id is None:
                container = self
            
            else:
                container = self.item_to_node[folder_id].folder

        if type == "folder":
            new_folder = folder(item.title, item.bookmarks)
            new_node = LinkedList(type, None, new_folder)
            new_node.id = id

            if folder_id is None:
                container = self
            
            else:
                container = self.item_to_node[folder_id].folder
            
        
        self.insert(new_node, prev, container)

    # for deletion we can delete a bookmark that is nested, or a folder
    # i don't think we need to know if the node is a folder or a bookmark if we are deleting by the id. And both types are a node
    def delete(self, id: int):

        node = self.item_to_node[id]

        if node.prev is None:
            temp = node.next
            node.next.prev = None

        # delete from middle
        elif node.prev and node.next:
            node.prev.next = node.next
            node.next.prev = node.prev

        
        else:
            node.prev.next = None
        

        

        # if first node, update the head

        # if in middle, connect prev.next to node.next and update node.next.prev

        # if deleting the tail, then update the tail to be the node.prev





    def insert(self, new_node, prev, container):
        print("new node: ", new_node.id)

         # if the list is empty
        if container.tail is None:
            # new_node.id = id
            container.tail = new_node
            container.head = new_node
            container.tail.next = None
            container.head.prev = None
            self.item_to_node[new_node.id] = new_node

        # if the list isn't empty
        else:
            # insert at the very front
            if prev == 0:
                temp = container.head # 1->2->3 0
                new_node.next = container.head
                temp.prev = new_node
                container.head = new_node

            else:      
                curr_node = self.item_to_node[prev]
                temp = curr_node.next
                curr_node.next = new_node
                new_node.prev = curr_node
                new_node.next = temp

                # if the new node is the tail
                if temp is None:
                    container.tail = new_node
                    container.tail.next = None

                else:
                    temp.prev = new_node

            self.item_to_node[new_node.id] = new_node

    def get_bookmarks(self, head):
        
        curr = head
        while curr:
            if curr.type == "bookmark":
                print("curr: ", curr.bookmark.title, " id: ", curr.id)
            else:
                "holda"
            if curr.type == "folder":
                print("folder: ", curr.id, " title: ", curr.folder.title)
                folder_curr = curr.folder.head
                if folder_curr:
                    self.get_bookmarks(folder_curr)

            else:
                "nohting"
            curr = curr.next

        return



        


test = bookmarks()
item = bookmark("sierra.com", "Sierra")
list = LinkedList("bookmark", item, None)

item2 = bookmark("homedepot.com", "homedepot")
item3 = bookmark("java.com", "java")
item4 = bookmark("atlassian.com", "atlassian")
item5 = bookmark("browserbase.com", "browserbase")
item6 = bookmark("notion.com", "notion")
item7 = bookmark("anthropic.com", "anthropic")
item8 = bookmark("cursor.com", "cursor")





new_folder = folder("AI companies", None)
test.add_item("folder", new_folder) # ai companies 1

test.add_item("bookmark", item, 0, 1)

test.add_item("bookmark", item2) # home depot 2 -> ai companies 1
test.add_item("bookmark", item3)   # java 3-> home depot 2 -> ai companies 1 
test.add_item("bookmark", item4,4) # java 3-> home depot 2 -> ai companies 1 -> atlassian 4
test.add_item("bookmark", item5,4) # java 3-> home depot 2 -> browserbase 5->  ai companies 1 -> atlassian 4
test.add_item("bookmark", item6,1) # java 3-> home depot 2 -> browserbase ->  ai companies 1 -> atlassian 4

test.add_item("bookmark", item7, 2, 1)
test.add_item("bookmark", item8, 0, 1)





curr = test.head

test.get_bookmarks(curr)

# delete node

# test.delete(7) # passed
# test.delete(5)  # passed

# delete from inside folder
# test.delete(3) # passed

# delete folder
test.delete(1) # failed
print("after deletion")

test.get_bookmarks(curr)


# took one hour and 7 mins


# curr = test.bookmarks

# while curr:
#     print("curr: ", curr.bookmark.title)
#     curr = curr.next




