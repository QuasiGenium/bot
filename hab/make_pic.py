from PIL import Image


def convert_turn(s):
    s = s.split(' - ')
    a = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    n = (a[s[0][0].lower()], 8 - int(s[0][1]))
    k = (a[s[1][0].lower()], 8 - int(s[1][1]))
    return n, k


def anti_convert(s):
    abc = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
    return abc[s[0]] + str(8 - s[1])


def make_map(k, other=''):
    m = [['bl', 'bh', 'be', 'bf', 'bk', 'be', 'bh', 'bl'],
         ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['', '', '', '', '', '', '', ''],
         ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
         ['wl', 'wh', 'we', 'wf', 'wk', 'we', 'wh', 'wl']]
    f = {}
    if other:
        other = other.split(';')
        for i in other:
            f[int(i[0])] = i[1]
    for j in range(len(k)):
        i = k[j]
        if m[i[1][1]][i[1][0]] != m[i[0][1]][i[0][0]]:
            m[i[1][1]][i[1][0]] = m[i[0][1]][i[0][0]]
            m[i[0][1]][i[0][0]] = ''
        if j + 1 in f.keys():
            m[i[1][1]][i[1][0]] = m[i[1][1]][i[1][0]][0] + f[j + 1]
    return m


def make_picture(f, other=''):
    sl = {'p': 'pes', 'l': 'lad', 'h': 'hor', 'f': 'fer', 'k': 'king', 'e': 'ele'}
    koory = [2, 60, 119, 178, 237, 295, 353, 412]
    koorx = [28, 85, 145, 204, 261, 321, 377, 439]
    board1 = Image.open('hab/pic/board.png')
    board = board1.copy()
    t = f.split(';')
    a = [convert_turn(_) for _ in t]
    m = make_map(a, other)
    flag = True
    for i in range(8):
        for j in range(8):
            o = m[-i][-j]
            if o:
                h = 0
                while True:
                    try:
                        w = Image.open(rf'hab/pic/{o[0]}_{sl[o[1]]}.png')
                        mask_im = Image.open(rf'hab/pic/{o[0]}_{sl[o[1]]}_mask.png')
                        board.paste(w, (koorx[-j], koory[-i]), mask_im)
                        board.save(r'hab/pic/board1.png', quality=95)
                        board = Image.open(r'hab/pic/board1.png')
                        break
                    except OSError:
                        h += 1
                        print('апчи', end=' ')
                        continue
                if h:
                    print('я пытался ', h, 'раз')



'''
board1 = Image.open('pic/board.png')
w = Image.open('pic/b_hor.png')
mask_im = Image.open('pic/b_hor_mask.png')
board = board1.copy()
board.paste(w, (23 + 60, 2), mask_im)
board.save('pic/board1.png', quality=95)
'''
'''
fs = ['hor', 'ele', 'fer', 'king', 'lad', 'pes']
cl = ['w', 'b']
for a in cl:
    for b in fs:
        w = Image.open(f'pic/{a}_{b}.png')

        p = w.load()
        x, y = w.size
        for i in range(x):
            for j in range(y):
                if p[i, j][3] != 0:
                    p[i, j] = (255, 255, 255, 255)
                    w.save(f'pic/{a}_{b}_mask.png')
'''