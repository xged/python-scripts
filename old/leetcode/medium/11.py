# 11. Container With Most Water

class Solution:
    def maxArea(self, height: list[int]) -> int:
        x = maxI1 = 0
        for i1, a1 in enumerate(height):
            if maxI1 < a1:
                maxI1 = a1
                maxI2 = 0
                for i2 in range(len(height)-1, i1, -1):
                    a2 = height[i2]
                    if a1 <= a2:
                        area = (i2-i1)*a1
                        if x < area: x = area
                        break
                    if maxI2 < a2:
                        maxI2 = a2
                        area = (i2-i1)*a2
                        if x < area: x = area
        return x

# from datetime import datetime
# import random
# import string

# def test(n=1000):
#     x = [random.randrange(10000) for _ in range(random.randrange(2, 10**5))]
#     solution = Solution()
#     t = datetime.now()
#     for _ in range(n-1):
#         solution.maxArea(x)
#     ans = solution.maxArea(x)
#     print(ans, datetime.now() - t)
#     t = datetime.now()
#     for _ in range(n-1):
#         solution.maxArea2(x)
#     ans = solution.maxArea2(x)
#     print(ans, datetime.now() - t)

# test()
