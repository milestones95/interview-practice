"""
Problem: Price Drop Alerts

Part 1 — create_alert(user_id, product_id, target_price)
A user watches a product and wants to be notified once its price drops to or below target_price. Returns a unique alert_id.

Part 2 — update_product_price(product_id, new_price)
A product's price changes. Return the list of alert_ids that should now fire (i.e., their target_price >= new_price) for that product — and those alerts should be considered "used up" (they won't fire again on a future price drop). A single product can have thousands of alerts against it, and prices update frequently (think: every few seconds during a flash sale), so scanning every alert on every price update isn't going to hold up.

Part 3 — cancel_alert(alert_id)
A user changes their mind before the price ever drops. Remove their alert. It should no longer be considered in future update_product_price calls.

Part 4 — get_alerts_for_user(user_id)
Return all of a user's currently active (not yet fired, not cancelled) alerts, across all products they're watching.
"""

# i think this can be solved with with a bst and hashmap. We can figure out which alerts are within a given range quickly with bst
# we can delete an alert quickly with bst
# for part  4  this would be o(n) regardless of if we use linked list, or bst or array.

class alert:
    def __init__(self, alert_id, target_price, user_id):
        self.alert_id = alert_id
        self.target_price = target_price
        self.left = None
        self.right = None
        self.was_fired = False


class product:
    def __init__(self, product_id, product_price): # each product will contain alerts that will be stored in a BST
        self.product_id = product_id
        self.product_price = product_price
        self.alerts = None


class alert_system:
    def __init__(self):
        self.user_to_alertlist = {} # we will have the key be user id and the value be the array of products the user has 
        self.alert_id_to_alert = {}




# wasted 24 minutes coming up with the plan
# this was a good gnarly hard one! i got stuck and needed AI's help with the approach