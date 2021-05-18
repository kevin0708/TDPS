# Untitled - By: lzh‘computer - 周一 3月 22 2021

import pyb
import sensor, image, time
import math
from pyb import UART
kernel_size = 1 # kernel width = (size*2)+1, kernel height = (size*2)+1
kernel = [-1, -1, -1,\
          -1, +2, -1,\
          -1, -1, -1]

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
sensor.set_framesize(sensor.QVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_gainceiling(8)
#uart = UART(3, 19200, timeout_char=100000)


def get_his(b_array):
    his = list()
    for i in range(320):
        his.append(0)
        for j in range(240):
            index = i * 240 + j
            his[i] += b_array[index]
    return his

def bubble_sort(alist):
    length = len(alist)
    line_list = list(range(length))

    for i in range(length - 1):
        # i表示比较多少轮
        for j in range(length - i - 1):
            # j表示每轮比较的元素的范围，因为每比较一轮就会排序好一个元素的位置，
            # 所以在下一轮比较的时候就少比较了一个元素，所以要减去i
            if alist[j] > alist[j + 1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                line_list[j], line_list[j + 1] = line_list[j + 1], line_list[j]
    return alist, line_list



def get_sparse_his(b_array):
    his = list()
    for i in range(39):
        real_column = (i + 1) * 8 - 1
        his.append(0)

        index = real_column

        his[i] += b_array[index] # 为了减少乘法运算量，将第一步不加320的运算在循环之外算

        for j in range(239):
            index = index + 320
            his[i] += b_array[index]
    return his


def get_sparse_middle_line(his):

    sorted_list, sorted_index = bubble_sort(his)
    for i in range(25):
        his[sorted_index[i]] = 0

    half_sum = int(sum(his) / 2)
    temp = 0
    for i in range(39):
        temp += his[i]
        if temp >= half_sum:

            return i

def get_middle_line(his):
    half_sum = int(sum(his) / 2)
    temp = 0
    for i in range(320):
        temp += his[i]
        if temp >= half_sum:
            return i

def transfer_command(middle_line):
    if middle_line>140 and middle_line<180:
        print("go straight\n")
        #uart.write("go straight\n")
    elif middle_line>60 and middle_line<140:
        print("turn left\n")
        #uart.write("turn left\n")
    elif middle_line>180 and middle_line<280:
        print("turn right\n")
        #uart.write("turn right\n")
    else:
        print("error\n")
        #uart.write("error\n")

'''while(True):
        sensor.set_pixformat(sensor.GRAYSCALE)
        img = sensor.snapshot()
        img.median(1, percentile=0.5)
        #img = bytearray(sensor.snapshot().binary(thresholds))
        #img_array = bytearray(img.binary(thresholds))
        img_array = img.find_edges(image.EDGE_CANNY, threshold=(50, 80))
        #print(img)
        his = get_sparse_his(img_array)
        middle_line = (get_sparse_middle_line(his)+1) * 8
        print(his)
        #img.draw_line((middle_line, 0, middle_line, img.height()-1), color = 255, thickness = 2)
'''

# 在原图里画线


# 直接在二值图里画线

counter = 0
next_time = 0
if_color_detection = 0
threshold = (57, 82, 18, 90, 20, 69)
while(True):
    if counter // 10 != 1:
        sensor.set_pixformat(sensor.GRAYSCALE)
        img = sensor.snapshot()
        img_gray = img.copy()
        img_gray.median(1, percentile=0.5)
        #img = bytearray(sensor.snapshot().binary(thresholds))
        #img_array = bytearray(img.binary(thresholds))
        img_array = img_gray.find_edges(image.EDGE_CANNY, threshold=(50, 80))
        #print(img)
        his = get_sparse_his(img_array)
        middle_line = (get_sparse_middle_line(his)+1) * 8

        #transfer_command(middle_line)

    else:
        transfer_command(middle_line)
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
        sensor.set_auto_whitebal(False) # 颜色跟踪必须关闭白平衡
        img_rgb = sensor.snapshot()
        blobs = img_rgb.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10)
        counter = 0
        if_color_detection = 1


    if if_color_detection == 1:
        for blob in blobs:
            img.draw_rectangle(blob.rect(),color=255,thickness=3)
            #img.draw_cross(blob.cx(), blob.cy())
            img.draw_string(blob.cx(), blob.cy(), "Red", color = 255, scale = 2, mono_space = False,
                            char_rotation = 0, char_hmirror = False, char_vflip = False,
                            string_rotation = 0, string_hmirror = False, string_vflip = False)

            if blob.area() >= 20000:
                print('Reach the target distance')
            else:
                print('Distance too far')

    img.draw_line((middle_line, 0, middle_line, img.height()-1), color = 255, thickness = 2)
    counter += 1

