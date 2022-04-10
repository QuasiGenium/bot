from PIL import Image, ImageDraw, ImageFilter

board1 = Image.open('pic/board.png')
w = Image.open('pic/w_pes.png')
mask_im = Image.open('pic/w_pes.png').resize(w.size).convert('L')
board = board1.copy()
board.paste(w, (23 + 60, 2), mask_im)
board.save('pic/board1.png', quality=95)
def make_picture(f):
    pass
