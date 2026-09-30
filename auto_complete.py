# You’re building the backend for a contacts app. Design a system backed by a BST (keyed by name) that supports:

# 	•	add_contact(name, phone) — insert a contact
# 	•	remove_contact(name) — remove a contact
# 	•	get_contact(name) — exact lookup, return phone number
# 	•	contacts_with_prefix(prefix) — return all contact names starting with a given prefix, in sorted order (e.g. typing “Jo” returns “Joan”, “John”, “Jordan”)
# 	•	contacts_in_range(start_name, end_name) — return all contacts alphabetically between two names (useful for a jump-to-letter scroll UI)

# Constraints:

# 	•	Keep it a plain BST (no need to self-balance) — but be ready to discuss why a real product would want a balanced tree or a trie instead, and what breaks with plain BST if names are inserted in sorted order
# 	•	contacts_with_prefix and contacts_in_range both want you to prune subtrees you can prove don’t contain matches, rather than doing a full in-order traversal and filtering after — that pruning logic is the actual point of the problem
# 	•	remove_contact needs the standard two-children delete case

# This one’s grounded in something you’d actually ship — it’s basically what powers the “jump to contact” search bar — and the prefix/range queries force you to think about BST traversal as a search tool, not just an ordered container.