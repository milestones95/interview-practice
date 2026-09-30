
# Here's one that's linked-list focused, for variety:

# Design a browser tab manager with tab groups.

# You're modeling browser tabs as a doubly linked list (so tabs stay in visual left-to-right order and can be reordered), plus a hashmap for O(1) lookup by tab_id.

# Support:

# open_tab(tab_id, url) — opens a new tab immediately to the right of the currently active tab (not necessarily at the end — this is the twist, similmeasure to how a real browser opens a new tab next to the one you're on, not at the far right).
# close_tab(tab_id) — closes a tab. If the closed tab was active, the tab immediately to its right becomes active (or the one to its left, if it was the rightmost tab).
# switch_to(tab_id) — makes the given tab the active one.
# move_tab(tab_id, target_tab_id) — reorders the list so tab_id now sits immediately to the right of target_tab_id (drag-and-drop reordering).