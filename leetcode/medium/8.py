# 8. String to Integer (atoi)

MAX_INT = 2**31-1
MIN_INT = -2**31

class Solution:
    def myAtoi(self, s: str):
        s = s.lstrip()
        if s != "" and s[0] == "+":
            positive = True
            s = s[1:]
        elif s != "" and s[0] == "-":
            positive = False
            s = s[1:]
        else: positive = True
        digits = []
        for c in s:
            if c.isnumeric(): digits.append(c)
            else:
                if len(digits) == 0: return 0
                x = int("".join(digits)) if positive else int("-"+"".join(digits))
                if x > MAX_INT: return MAX_INT
                if x < MIN_INT: return MIN_INT
                return x
