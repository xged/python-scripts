# 3. Longest Substring Without Repeating Characters

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        maxLen = 0
        substr = ""
        for c in s:
            if c not in substr:
                substr += c
                maxLen = max(maxLen, len(substr))
            else: substr = substr[substr.index(c) + 1:] + c
        return maxLen

#     def lengthOfLongestSubstring2(self, s: str) -> int:
#         maxLen = 0
#         substr = ""
#         for i in range(len(s)):
#             if s[i] not in substr:
#                 substr += s[i]
#                 maxLen = max(maxLen, len(substr))
#             else: substr = substr[i + 1:] + s[i]
#         return maxLen

# from datetime import datetime
# import random
# import string

# def test(size=10**7):
#     s = ''.join(random.choice(string.ascii_lowercase) for _ in range(size))
#     solution = Solution()
#     t1 = datetime.now()
#     print(solution.lengthOfLongestSubstring(s), datetime.now() - t1)
#     t2 = datetime.now()
#     print(solution.lengthOfLongestSubstring2(s), datetime.now() - t2)

# test()
