# 方法 1
def power2n1(n):
    return 2**n

# 方法 2a：用遞迴
def power2n2(n):
    if n==0: return 1
    return power2n2(n-1)+power2n2(n-1)

# 方法2b：用遞迴
def power2n3(n):
    if n==0: return 1
    return 2*power2n3(n-1)

# 方法 3：用遞迴+查表
def power2n4(n,m={}):
    if n==0: return 1
    if n in m: return m[n]
    a=power2n4(n-1,m)*2
    m[n]=a
    return a

from datetime import datetime

startTime = datetime.now()
print("power2n1(30)=", power2n1(30))
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')

startTime = datetime.now()
print("power2n2(30)=", power2n2(30))
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')

startTime = datetime.now()
print("power2n3(30)=", power2n3(30))
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')

startTime = datetime.now()
print("power2n4(30)=", power2n4(30))
endTime = datetime.now()
seconds = endTime - startTime
print(f'time:{seconds}')

# 程式碼由老師原本給的提示補完，之後分別計算每種方法使用的所需時間
