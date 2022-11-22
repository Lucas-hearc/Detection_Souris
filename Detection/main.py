from m_rcnn import load_inference_model, visualize
import win32file
import win32pipe
from tkinter import *
import numpy as np
from time import sleep
import skimage.io
from datetime import time

HEIGHT = 288
WIDTH = 382

def convert(temp):
    temp = temp.split(",")
    data = np.empty(shape=(HEIGHT,WIDTH,3),dtype=np.uint8)
    for j in range (HEIGHT):
        for i in range(WIDTH):
            data[j][i][0] = int(temp [WIDTH*3*j+(i-1)*3])
            data[j][i][1] = int(temp [WIDTH*3*j+(i-1)*3+1])
            data[j][i][2] = int(temp [WIDTH*3*j+(i-1)*3+2])
    return data

def init():
    pipe_CtoP = win32file.CreateFile(
            "\\\\.\\pipe\\CtoP",
            win32file.GENERIC_READ | win32file.GENERIC_WRITE,
            0,
            None,
            win32file.OPEN_EXISTING,
            win32file.FILE_ATTRIBUTE_NORMAL,
            None
            )

    return pipe_CtoP

def main():
    image = skimage.io.imread("image.jpg")
    mod, inter_config = load_inference_model(1,"mask_rcnn_object_0005.h5")
    print("start")
    mask = mod.detect([image], verbose = 1)
    print("fin")
    #visualize.display_instances(image,mask,'screwdrivers',show_bbox=False)
    # print("fin chargement")
    # dataTemp = ""
    # i = 1
    # while True:
    #     try:
    #         pipeCtoP = init()
    #     except:
    #         #print("erreur")
    #         continue
    #     while True:
    #         try:
    #             dataTemp += (win32file.ReadFile(pipeCtoP, 2000)[1]).decode()
    #         except win32file.error:
    #             break
    #     if (dataTemp.__len__() > 0):
    #         image = convert(dataTemp) 
    #         dataTemp = None
    #         mask = mod.detect([image], verbose = 1)
    #         visualize.display_instances(image,mask,'screwdrivers',show_bbox=False)
    #         print("ok")
    #         pipePtoC = win32pipe.CreateNamedPipe(
    #             "\\\\.\\pipe\\PtoC",
    #             win32pipe.PIPE_ACCESS_DUPLEX,
    #             win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_WAIT,
    #             1, 3, 3,
    #             300,
    #             None)
    #         win32pipe.ConnectNamedPipe(pipePtoC,None)
            
    #         win32file.WriteFile(pipePtoC,str(i).encode())
    #         win32file.FlushFileBuffers(pipePtoC)
    #         i += 1  
    #         dataTemp = ""
    #         win32file.CloseHandle(pipePtoC)

if __name__ == "__main__":
    main()