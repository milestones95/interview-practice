"""
Rotting Oranges (LeetCode 994)

You're given an m x n grid where each cell has one of three values:

0 — an empty cell
1 — a fresh orange
2 — a rotten orange

Every minute, any fresh orange that is 4-directionally adjacent (up/down/left/right) to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.

Example:

Input: grid = [[2,1,1],
               [1,1,0],
               [0,1,1]]


Input: grid = [[2,1,1],
               [1,1,0],
               [0,0,1]]
Output: 4
"""

def traverse(grid: list[list[int]], r: int, c: int, visited):

    R_LEN = len(grid)
    C_LEN = len(grid[0])

    if min(r,c) < 0:
        return

    if r > R_LEN - 1 or c > C_LEN - 1:
        return

    if grid[r,c] == 0:
        return

    if (r,c) in visited:
        return

    count = 1
    visited.add((r,c))

    directions = [(0,1), (1,0), (-1,0), (0,-1)]

    for dr, dc in directions:

        if (r+dr, c+dc) in visited:
            continue
        
        count += traverse(grid, r+dr, c+dc, visited)

    return count


def rotten_oranges(grid: list[list[int]]):

    r_len = len(grid)
    c_len = len(grid[0])
    visited = set()

    for r in range(r_len):

        for c in range(c_len):

            if grid[r,c] == 2:
                traverse(grid, r, c, set())




    

