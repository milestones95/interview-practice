# Problem: Limit Order Book

# Implement OrderBook for buy orders (bids) with:

# add_order(order_id, price, quantity) — Adds an order at a given price. Orders are stored in a BST keyed by price. Multiple orders can share the same price, and within a price level they must be filled in the order they arrived (FIFO) — so each BST node holds a doubly linked list of orders at that price.
# cancel_order(order_id) — Cancels an order in O(1) average time to locate it (hashmap from order_id → some reference letting you jump straight to its price-level node and its position in that node's linked list), then removes it from the linked list. If that price level's linked list becomes empty, delete the BST node for that price entirely.
# get_best_bid() — Returns the highest price level with at least one order, and the order_id of the first order in its FIFO queue (the one that would be filled next). This is a pure search — no mutation.
# get_orders_at_price(price) — Returns all order_ids at that price level, in FIFO order.