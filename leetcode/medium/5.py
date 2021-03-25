# 5. Longest Palindromic Substring

class Solution:
    def longestPalindrome(self, s: str) -> str:
        self.maxPal = s[0]
        def base(left: int, right: int):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            if right - left - 1 > len(self.maxPal): self.maxPal = s[left+1:right]
        for i in range(len(s)-1):
            if i != 0 and s[i-1] == s[i+1]: base(i-2, i+2)  # Uneven
            if s[i] == s[i+1]: base(i-1, i+2)  # Even
        return self.maxPal

# from datetime import datetime
# import random
# import string

# def test(size=10**7):
#     s = ''.join(random.choice(string.ascii_lowercase) for _ in range(size))
#     solution = Solution()
#     t = datetime.now()
#     print(solution.longestPalindrome(s), datetime.now() - t)
#     t = datetime.now()
#     print(solution.longestPalindrome2(s), datetime.now() - t)

# test()
