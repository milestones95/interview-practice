"""
Spiral Matrix (LeetCode 54)

Given an m x n matrix, return all elements of the matrix in spiral order (starting top-left, going right, then down, then left, then up, spiraling inward).

Example:

Input: matrix = [[1,2,3],
                  [4,5,6],
                  [7,8,9]]
Output: [1,2,3,6,9,8,7,4,5]

This one's a good contrast to the last two — no traversal-between-cells, no marker tricks, just careful boundary management. Think about how you'd track the four edges of your "unvisited" region (top, bottom, left, right) and how those boundaries shrink as you consume each layer.

"""

# check when right column boundary is reached
# check when bottom row is reached
# check when upper boundary is reached
