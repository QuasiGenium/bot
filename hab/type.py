from hab import make_pic


def is_it_correct(a):
    a1 = a.strip().lower()
    abc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    try:
        if '-' not in a:
            return False
        if a1[0] not in abc or a1.split('-')[1].strip()[0] not in abc:
            return False
        if not (0 < int(a1[1]) < 9 and 0 < int(a1.split('-')[1].strip()[1]) < 9):
            return False
        if len(a1.split('-')[0].strip()) != 2 or len(a1.split('-')[1].strip()) != 2:
            return False
    except Exception as e:
        return False
    return a1.split('-')[0].strip() + ' - ' + a1.split('-')[1].strip()


def pes(a, m):
    n = -1 if m[a[0][1]][a[0][0]][0] == 'w' else 1
    if a[0][1] in [1, 6] and a[0][1] + n + n == a[1][1] and\
            a[0][0] == a[1][0] and (not m[a[1][1]][a[1][0]]) and (not m[a[0][1] + n][a[0][0]]):
        return True
    if a[0][1] + n != a[1][1]:
        return False
    if (not m[a[1][1]][a[1][0]]) and a[0][0] != a[1][0]:
        return False
    if m[a[1][1]][a[1][0]] and a[0][0] != a[1][0] - 1 and a[0][0] != a[1][0] + 1:
        return False
    return True


def lad(a, m):
    if a[0][0] != a[1][0] and a[0][1] != a[1][1]:
        return False
    flag_abc = True if a[0][0] != a[1][0] else False
    for i in range(1, max(abs(a[0][0] - a[1][0]), abs(a[0][1] - a[1][1]))):
        if flag_abc:
            if a[1][0] > a[0][0]:
                if m[a[0][1]][a[0][0] + i]:
                    return False
            else:
                if m[a[0][1]][a[0][0] - i]:
                    return False
        else:
            if a[1][1] > a[0][1]:
                if m[a[0][1] + i][a[0][0]]:
                    return False
            else:
                if m[a[0][1] - i][a[0][0]]:
                    return False
    return True


def hor(a, m):
    if (abs(a[0][0] - a[1][0]) == 1 and abs(a[0][1] - a[1][1]) == 2)\
            or (abs(a[0][0] - a[1][0]) == 2 and abs(a[0][1] - a[1][1]) == 1):
        return True
    return False


def king(a, m):
    if 0 <= abs(a[0][0] - a[1][0]) <= 1 and 0 <= abs(a[0][1] - a[1][1]) <= 1:
        return True
    return False


def ele(a, m):
    if abs(a[0][1] - a[1][1]) != abs(a[1][0] - a[0][0]):
        return False
    ud = 1
    lr = 1
    if a[1][0] < a[0][0]:
        lr = -1
    if a[0][1] > a[1][1]:
        ud = -1
    for i in range(1, abs(a[0][1] - a[1][1])):
        if m[a[0][1] + i * ud][a[0][0] + i * lr]:
            return False
    return True


def fer(a, m):
    return lad(a, m) or ele(a, m)


def try_go(a, b, color, other=''):
    if not is_it_correct(a):
        return False
    if b:
        t = b.split(';')
        f = [make_pic.convert_turn(_) for _ in t]
        m = make_pic.make_map(f, other)
    else:
        m = make_pic.make_map([])
    a = make_pic.convert_turn(a)
    if not m[a[0][1]][a[0][0]]:
        return False

    if m[a[0][1]][a[0][0]][0] != color:
        return False

    if m[a[1][1]][a[1][0]]:
        if m[a[1][1]][a[1][0]][0] == color:
            return False

    if m[a[0][1]][a[0][0]][1] == 'p':
        return pes(a, m)

    if m[a[0][1]][a[0][0]][1] == 'l':
        return lad(a, m)

    if m[a[0][1]][a[0][0]][1] == 'h':
        return hor(a, m)

    if m[a[0][1]][a[0][0]][1] == 'k':
        return king(a, m)

    if m[a[0][1]][a[0][0]][1] == 'f':
        return fer(a, m)

    if m[a[0][1]][a[0][0]][1] == 'e':
        return ele(a, m)


def is_shag(b, other=''):
    s = {'bk': False, 'wk': False}
    if b:
        t = b.split(';')
        f = [make_pic.convert_turn(_) for _ in t]
        m = make_pic.make_map(f, other)
    else:
        return s
    wk = (0, 0)
    bk = (0, 0)
    for i in range(8):
        for j in range(8):
            if m[i][j] == 'wk':
                wk = make_pic.anti_convert((j, i))
            if m[i][j] == 'bk':
                bk = make_pic.anti_convert((j, i))
    for i in range(8):
        for j in range(8):
            if m[i][j]:
                g = make_pic.anti_convert((j, i))
                if g != wk:
                    if try_go(f'{g} - {wk}', b, m[i][j][0], other):
                        s['wk'] = True
                if g != bk:
                    if try_go(f'{g} - {bk}', b, m[i][j][0], other):
                        s['bk'] = True
            if all(s.values()):
                break
        if all(s.values()):
            break
    return s


def rok(b, color, lr, other=''):
    if b:
        t = b.split(';')
        f = [make_pic.convert_turn(_) for _ in t]
        m = make_pic.make_map(f, other)
        for i in m:
            print(i)
    else:
        return False
    if color == 'w':
        if 'e1' in b:
            return False
        if lr == 'l':
            if 'a1' in b:
                return False
            a = [(3, 7), (2, 7), (1, 7)]  # [make_pic.convert_turn(f'a1 - {i}1')[1] for i in ['d', 'c', 'b']]
            for i in a:
                if m[i[1]][i[0]]:
                    return False
            for i in ['', ';e1 - d1', ';e1 - c1']:
                g = is_shag(b + i, other)
                if g['wk']:
                    return False
            return 'e1 - e1;e1 - c1;a1 - d1'
        elif lr == 'r':
            if 'h1' in b:
                return False
            a = [(5, 7), (6, 7)]  # [make_pic.convert_turn(f'a1 - {i}1')[1] for i in ['f', 'g']]
            for i in a:
                if m[i[1]][i[0]]:
                    return False
            for i in ['', ';e1 - f1', ';e1 - g1']:
                g = is_shag(b + i, other)
                if g['wk']:
                    return False
            return 'e1 - e1;e1 - g1;h1 - f1'
    elif color == 'b':
        if 'e8' in b:
            return False
        if lr == 'l':
            if 'a8' in b:
                return False
            a = [(3, 0), (2, 0), (1, 0)]  # [make_pic.convert_turn(f'a8 - {i}8')[1] for i in ['d', 'c', 'b']]
            for i in a:
                if m[i[1]][i[0]]:
                    return False
            for i in ['', ';e8 - d8', ';e8 - c8']:
                g = is_shag(b + i, other)
                if g['bk']:
                    return False
            return 'e8 - e8;e8 - c8;a8 - d8'
        elif lr == 'r':
            if 'h8' in b:
                return False
            a = [(5, 7), (6, 7)]  # [make_pic.convert_turn(f'a8 - {i}8')[1] for i in ['f', 'g']]
            for i in a:
                if m[i[1]][i[0]]:
                    return False
            for i in ['', ';e8 - f8', ';e8 - g8']:
                g = is_shag(b + i, other)
                if g['bk']:
                    return False
            return 'e8 - e8;e8 - g8;h8 - f8'


def is_pes_wanna_transform(b, other):
    if b:
        t = b.split(';')
        a = [make_pic.convert_turn(_) for _ in t]
        m = make_pic.make_map(a, other)
        if 'wp' in m[0] or 'bp' in m[-1]:
            return True
    return False


def trans(b, f, other=''):
    g = len(b.split(';'))
    if other:
        return other + ';' + str(g) + f
    else:
        return str(g) + f
