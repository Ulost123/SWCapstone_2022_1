import cv2 as cv 
import numpy as np
import random
import os
import time
 
#from filling import compensate
from cut import get_new_gt2, collect_edges

HEIGHT = 500
WIDTH = 500
final_lon = 256

def create_fish(srcImg, k1, k2, k3, k4):
    up = []
    down = []
    left = []
    right = []
    dstImg = np.zeros([HEIGHT, WIDTH, 3], np.uint8) + 255
    #det_uv = np.zeros([HEIGHT, WIDTH, 2], np.int32) + 500

    #x0 = (WIDTH - 1)/ 2. #중앙
    #y0 = (HEIGHT - 1) / 2. #중앙
    
    x0 = random.uniform(195, 203)
    y0 = random.uniform(195, 203)
    
    print("x0 : ", x0, "y0 : ", y0)
    
    min_x = 9999
    cut_r = 0
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            x_d = j - x0
            y_d = i - y0
            rd_2 = pow(x_d, 2) + pow(y_d, 2)
            rd_4 = pow(rd_2, 2)
            rd_6 = pow(rd_2, 3)
            rd_8 = pow(rd_2, 4)
            x = (1 + k1 * rd_2 + k2 * rd_4 + k3 * rd_6 + k4 * rd_8) * x_d
            y = (1 + k1 * rd_2 + k2 * rd_4 + k3 * rd_6 + k4 * rd_8) * y_d

            if (int(y) == int(-y0) and x >= -x0 and x <= x0):
                if (x < min_x):
                    min_x = x
                    cut_r = -x_d

    start = int(x0 - cut_r)
    end = int(x0 + cut_r) + 1
    for i in range(start, end):
        for j in range(start, end):
            x_d = j - x0
            y_d = i - y0
            rd_2 = pow(x_d, 2) + pow(y_d, 2)
            rd_4 = pow(rd_2, 2)
            rd_6 = pow(rd_2, 3)
            rd_8 = pow(rd_2, 4)
            x = (1 + k1 * rd_2 + k2 * rd_4 + k3 * rd_6 + k4 * rd_8) * x_d
            y = (1 + k1 * rd_2 + k2 * rd_4 + k3 * rd_6 + k4 * rd_8) * y_d

            u = int(x + x0)
            v = int(y + y0)
            if (u >= 0 and u < WIDTH) and (v >= 0 and v < HEIGHT):
                dstImg[i, j, 0] = srcImg[v, u, 0]
                dstImg[i, j, 1] = srcImg[v, u, 1]
                dstImg[i, j, 2] = srcImg[v, u, 2]

                up, down, left, right = collect_edges(start, end, j, i, u, v, up, down, left, right)
                cut_r_gt = int(x0 - up[0][0])
                #parameter_c = float(cut_r_gt) / float(cut_r)
                #parameter_b = float(final_lon) / float(cut_r_gt*2)
                #det_uv[v, u, 0] = (((parameter_c * x_d) + x0) - u) * parameter_b
                #det_uv[v, u, 1] = (((parameter_c * y_d) + y0) - v) * parameter_b

    cropImg = dstImg[(int(x0) - int(cut_r)):(int(x0) + int(cut_r)), (int(y0) - int(cut_r)):(int(y0) + int(cut_r))]
    dstImg2 = cv.resize(cropImg, (final_lon, final_lon), interpolation=cv.INTER_LINEAR)

    #det_u = det_uv[:, :, 0] 
    #det_v = det_uv[:, :, 1]

    #det_u = compensate(det_u)
    #det_v = compensate(det_v)

    source_Img = get_new_gt2(srcImg, up, down, left, right)
    source_Img = source_Img[(int(x0) - int(cut_r_gt)):(int(x0) + int(cut_r_gt)), (int(y0) - int(cut_r_gt)):(int(y0) + int(cut_r_gt))]
    source_Img = cv.resize(source_Img, (final_lon, final_lon), interpolation=cv.INTER_LINEAR)

    return dstImg, dstImg2, source_Img

path = "C:/Users/ehy84/Desktop/YUJIN/2022-1/SWCapstone/Code/PCN-main/data_ujin/val_256/val_256/"

k1_top = 1e-4
k1_down = 1e-6

k2_top = 1e-9
k2_down = 1e-11

k3_top = 1e-14
k3_down = 1e-16

k4_top = 1e-19
k4_down = 1e-21

num = 1

if __name__ == "__main__":
    start = time.time()
    #root, dirs, img_list = os.walk(path)
    img_lst = os.listdir(path)

    for files in img_lst[:10]:
        k1 = random.uniform(k1_down, k1_top)
        k2 = random.uniform(k2_down, k2_top)
        k3 = random.uniform(k3_down, k3_top)
        k4 = random.uniform(k4_down, k4_top)
        
        srcImg = cv.imread(path + files)
        
        srcImg = cv.resize(srcImg, (500, 500))
        dstImg, cutImg, source_Img = create_fish(srcImg, k1, k2, k3, k4)

        cv.imwrite("C:/Users/ehy84/Desktop/YUJIN/2022-1/SWCapstone/Code/PCN-main/dataset/experiment/not_middle/" + str(num) + '_data.jpg', cutImg)
        cv.imwrite("C:/Users/ehy84/Desktop/YUJIN/2022-1/SWCapstone/Code/PCN-main/dataset/experiment/not_middle/" + str(num) + '_gt.jpg', source_Img)
        num = num + 1
        
    print("after : ", time.time() - start)  