"""
This is on your reported Capital One list and hasn't come up yet, so let's do it.

Given an m x n board where each cell has an integer 1-9 representing a candy type (0 means empty), repeatedly do the following until the board stabilizes:

Find matches: if 3 or more candies of the same type are adjacent horizontally or vertically (in a straight line — not L-shaped), mark them all for removal.
Remove them: set all marked cells to 0.
Apply gravity: any non-zero candy above an empty (0) cell falls straight down to fill the gap; new empty cells appear at the top.
Repeat steps 1–3 until a full pass finds no new matches.

Return the final stable board.

Example:

Input:
[[110,5,112,113,114],
 [210,211,5,213,214],
 [310,311,3,313,314],
 [410,411,412,5,414],
 [5,1,512,3,3],
 [610,4,1,613,614],
 [710,1,2,713,714],
 [810,1,2,1,1],
 [1,1,2,2,2],
 [4,1,4,4,1014]]
Output:
[[0,0,0,0,0],
 [0,0,0,0,0],
 [0,0,0,0,0],
 [110,0,0,0,114],
 [210,0,0,0,214],
 [310,0,0,113,314],
 [410,0,0,213,414],
 [610,211,112,313,614],
 [710,311,412,613,714],
 [810,411,512,713,1014]]
 """