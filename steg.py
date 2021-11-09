import skimage.io as io
import matplotlib.pyplot as plt

img = io.imread("src/20190504_080233.jpg")

def set_last_bit(arr, pos, level, value):
    shape_size = len(arr.shape)
    if shape_size == 1:
        arr[pos[level]] = arr[pos[level]] & 0xFE
        arr[pos[level]] += value
        return
    set_last_bit(arr[pos[level]], pos, level+1, value)

def read_last_bit(arr, pos, level):
    shape_size = len(arr.shape)
    if shape_size == 1:
        return arr[pos[level]]
    return read_last_bit(arr[pos[level]], pos, level+1)

def inc_pos(pos, shape):
    i = len(shape) - 1
    while(True):
        if pos[0] > shape[0]:
            print("it doesnt fit, get a bigger image")
            exit(1)
        if pos[i] >= shape[i] - 1:
            pos[i] = 0
            i -= 1
        else:
            pos[i] += 1
            return

def skip_pos(pos, shape, count):
    for i in range(0, 8*count):
        inc_pos(pos, shape)

def write_steg(image, str, skip_first_bytes=0):
    shape_size = len(image.shape)
    pos = [0] * shape_size
    size = 0

    skip_pos(pos, image.shape, skip_first_bytes)

    for x in bytearray(str, 'utf-8'):
        for i in range(0, 8):
            val = int(x & (1 << i) > 0)
            set_last_bit(img, pos, 0, val)
            inc_pos(pos, image.shape)
            size = size + 1
    return int(size / 8)


def read_steg(image, size, skip_first_bytes=0):
    str = ''
    shape_size = len(image.shape)
    pos = [0] * shape_size

    skip_pos(pos, image.shape, skip_first_bytes)

    for c in range(0, size):
        ch = 0x00
        for i in range(0, 8):
            b = read_last_bit(image, pos, 0)
            ch += (b & 0x01) << i
            inc_pos(pos, image.shape)
        str += chr(ch)
    return str

size = write_steg(img, "Bla bla bla", 30)
print("text stegg: " + read_steg(img, size, 30))
#input()
