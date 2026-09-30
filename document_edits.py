class Node:

    def __init__(self, version, content):
        self.prev = None
        self.next = None
        self.version = version # version is unique so basically same as id
        self.content = content
        self.child = None

class document:

    def __init__(self):
        self.version_to_node = {} # use a hashmap to go straight to a specific version
        self.head = None
        self.tail = None
        self.count = 0
        self.current_version = None


    def insert(self, content: str, isRestored = False):
        new_version = self.count + 1

        new_edit = Node(new_version, content)

        # if there are no versions yet

        if self.tail is None:
            new_edit.prev = None
            new_edit.next = None
            self.head = new_edit
            self.tail = new_edit


        else:

            if isRestored:
                curr_node = self.version_to_node[self.current_version]
                curr_node.child = new_edit

            else:
                print("hello there")
                self.tail.next = new_edit
                new_edit.next = None
                new_edit.prev = self.tail
                self.tail = new_edit
        
        self.version_to_node[new_version] = new_edit
        self.current_version = new_version

        self.count+=1



    def undo(self):
    
        version = self.current_version #3, 2
        node = self.version_to_node[version] # node 2 
        prev = node.prev #2, 1


        try:
            if prev: #2
                print("hello")
                self.current_version = prev.version #3->2
                print("version: ", self.current_version)
                # return self.curr_version

            else:
                raise ValueError("there are no earlier edits to go to")
        except ValueError as error:
            print(error)

    def redo(self):
        version = self.current_version #3, 2
        node = self.version_to_node[version] # node 2 
        next_node = node.next #2, 1


        try:
            if next_node: #2
                print("hello")
                self.current_version = next_node.version #3->2
                print("version: ", self.current_version)
                # return self.curr_version

            else:
                raise ValueError("there are no more versions to skip to")
        except ValueError as error:
            print(error)


    def restore(self, version):

        current_node = self.version_to_node[version]

        self.current_version = current_node.version



    
    def get_current_version(self):

        return self.current_version




test = document()
test.insert("hello")
test.insert("goodbye")
test.insert("i'm here")
test.insert("hola")




curr = test.head

while curr:
    print("version: ", curr.version, " ", curr.content)
    curr = curr.next

test.restore(2)
print("current version: ", test.current_version)

test.insert("bom dia", True)
print("current version: ", test.current_version)





# test.undo()
# print("current version: ", test.current_version)

# test.undo()
# print("current version: ", test.current_version)

# test.undo()
# print("current version: ", test.current_version)

# print("redo")
# test.redo()
# print("current version: ", test.current_version)

# print("redo")
# test.redo()
# print("current version: ", test.current_version)



# i got stuck on the undo method for at least 10-15 mins. It's not updating to the previous version if i do multiple undos

