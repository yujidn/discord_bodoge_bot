import random

def dice(num_d_num: str) -> [int, list, dict]:

    def __dice(num, size):
        s = 0
        r = []
        d = {}
        for i in range(size):
            d[str(i+1)] = 0

        for i in range(num):
            v = random.randint(1, size)
            r.append(v)
            d[str(v)] += 1
            s += v
        return s, r, d

    dice_sum = 0
    dice_history = []
    dice_histgram = {}
    # dice
    if 'd' in num_d_num:
        sp = num_d_num.split('d')
        num = int(sp[0])
        size = int(sp[1])
        dice_sum, dice_history, dice_histgram = __dice(num, size)
    elif 'D' in num_d_num:
        sp = num_d_num.split('D')
        num = int(sp[0])
        size = int(sp[1])
        dice_sum, dice_history, dice_histgram = __dice(num, size)

    return dice_sum, dice_history, dice_histgram
