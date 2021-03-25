# 12. Integer to Roman. 1.47h

class Solution:
    def intToRoman(self, num:int)->str:
        ROMAN_NUM = {"M":1000,"CM":900,"D":500,"CD":400,"C":100,"XC":90,"L":50,"XL":40,"X":10,"IX":9,"V":5,"IV":4,"I":1}
        x = ""
        for roman,numBase in ROMAN_NUM.items():
            x += roman*(num//numBase)
            num %= numBase
        return x

    def intToRoman2(self, num:int)->str:
        M=["","M","MM","MMM"]
        C=["","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"]
        X=["","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"]
        I=["","I","II","III","IV","V","VI","VII","VIII","IX"]
        return M[num//1000]+C[(num//100)]+X[(num//10)%10]+I[num%10]


from datetime import datetime
import random

def test(n=10**6):
    x = random.randrange(4000)
    solution = Solution()
    t = datetime.now()
    for _ in range(n-1):
        solution.intToRoman(x)
    ans = solution.intToRoman(x)
    print(ans,datetime.now() - t)
    t = datetime.now()
    for _ in range(n-1):
        solution.intToRoman2(x)
    ans = solution.intToRoman2(x)
    print(ans,datetime.now() - t)

test()
