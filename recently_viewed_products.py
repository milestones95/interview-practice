class UserProducts:

    def __init__(self):
        self.user_products = {}

    
    def view_product(self, user_id:str, product_id: str):

        # check for what the size of the list is
        # check for if the product is already in the list
        # if it's in the list, delete it and insert at the end
        # update the prev and next node pointers
        # update the head
        product_list = None

        if user_id in self.user_products:
            product_list = self.user_products[user_id]
        else:
            product_list = ProductView()
            self.user_products[user_id] = product_list

        product_list = self.user_products[user_id]

        if product_id in product_list:
            # delete node
            product_list = self.delete_node(product_list, product_list[product_id])

        # insert into head

        product_list = self.insert_node(product_list,product_id)
        self.user_products[user_id] = products_list


    
    def delete_node(self, user_list, node):
        # if it's the head
        if node.prev is None:
            user_list.head = node.next
            node.next.prev = None

        # delete if it's not the head by linking the prev and next
        else:
            node.prev.next = node.next
            node.next.prev = node.prev

        # if the current node is the tail
        if node.next is None:
            user_list.tail = node


    def insert_node(self, user_list, product_id: str):

        # if there's already a head

        new_node = LinkedList(product_id)

        if user_list.head:
            head = user_list.head
            new_node.next = head
            head.prev = new_node
            new_node.prev = None
            user_list.head = new_node


        # if there's no head
        else:
            user_list.head = new_node
            user_list.tail = new_node

        return new_node


class ProductView:

    def __init__(self, head, tail):
        self.product_to_node{}
        self.head= head
        self.tail = tail


class LinkedList:
    
    def __init__(self, product_id = None):
        self.prev = None
        self.product_id = product_id
        self.next = None