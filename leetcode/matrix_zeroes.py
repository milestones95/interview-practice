"""
Set Matrix Zeroes (LeetCode 73)

Given an m x n integer matrix, if an element is 0, set its entire row and column to 0. You must do it in place.

Example:

Input: matrix = [[1,1,1],
                  [1,0,1],
                  [1,1,1]]
Output: [[1,0,1],
         [0,0,0],
         [1,0,1]]

Follow-up constraint to think about: a naive approach would use O(m*n) extra space (a copy of the grid). Can you do it in O(1) extra space? (Hint at the type of challenge, not the solution: the tricky part is that once you start zeroing cells, you lose track of which zeros were "original" vs. ones you just created — so you need to record the rows/columns to zero before you start mutating.)
"""


def update_matrix(grid: list[list[int]]):

    # if we loop through each position in the grid, can we track the columns that have zero and the rows that have zeros using sets

    rows_with_1s = set()
    columns_with_1s = set()

    R_LEN = len(grid)
    C_LEN = len(grid[0])

    for r in range(R_LEN):

        for c in range(C_LEN):

            if grid[r][c] == 0:
                rows_with_1s.add(r)
                columns_with_1s.add(c)


    for r in range(R_LEN):

        for c in range(C_LEN):

            if r in rows_with_1s or c in columns_with_1s:
                grid[r][c] = 0


    for r in range(R_LEN):

        for c in range(C_LEN):

            print(grid[r][c], end=" ")

        print("\n")


            
matrix = [[1,1,1],
        [1,0,1],
        [1,1,1]]


matrix2 = [[1,1,1],
        [1,1,1],
        [1,1,1]]


matrix3 = [[1,0,1],
        [1,0,1],
        [0,1,1]]

matrix4 = [[]]



update_matrix(matrix4)

# finished in 12 minutes the brute force approach