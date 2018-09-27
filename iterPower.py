#递归
def iterPower(base,exp):
    if exp == 0:
        return 1
    else:
        return base * iterPower(base,exp-1)

print(iterPower(3,2))
print(iterPower(2,3))
print(iterPower(4,2))