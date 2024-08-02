# 6. ZigZag Conversion

class Solution:
    def convert(self, s: str, nRows: int) -> str:
        if nRows == 1: return s
        matrix = [""]*nRows
        row = 0
        for c in s:
            matrix[row] += c
            if row == 0: forward = True
            elif row == nRows-1: forward = False
            row = row+1 if forward else row-1
        return "".join(matrix)

# from datetime import datetime
# import random
# import string

# def test(size=1000, n=20000):
#     s = ''.join(random.choice(string.ascii_lowercase) for _ in range(size))
#     solution = Solution()
#     t = datetime.now()
#     for _ in range(n):
#         solution.convert(s, random.choice(range(1, 1000)))
#     print(datetime.now() - t)
#     t = datetime.now()
#     for _ in range(n):
#         solution.convert2(s, random.choice(range(1, 1000))) * 10
#     print(datetime.now() - t)

# test()
