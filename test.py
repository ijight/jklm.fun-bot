import random

def FailBlock(block,letterWait):
    point = random.randint(0, len(block)-1)
    cnt = 0
    print(point)
    for letter in block:
        if cnt == point:
            print(letter)
            print(block[cnt:])
            for unused in range(1, (len(block[cnt:]) + len(letter) + 1)):
                print('Backspace')
            cnt += 1
        print(letter)
        cnt += 1

FailBlock("talent", 1)