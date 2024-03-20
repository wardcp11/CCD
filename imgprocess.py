from PIL import Image
import numpy as np
import multiprocessing as mp
import time

def imgProcess(imgFile, width, height, shared_array):

    im = Image.open(imgFile)

    for y in range(height):
        for x in range(width):
            shared_array[y * width + x] = im.getpixel((x,y))

def arrayConversion(inArry, width, height):
    arry = [[0 for i in range(width)] for j in range(height)]

    for current in range(len(inArry)):
        x = current % width
        y = current // width
        arry[y][x] = inArry[x+y]

    return arry
    

if __name__ == '__main__':
    startTime = time.time()

    imgFile = 'bandw.tiff'
    im = Image.open(imgFile)
    shared_array = mp.Array('i', im.size[0] * im.size[1])
    width = im.size[0]
    height = im.size[1]

    arrProcess = mp.Process(target=imgProcess, args=(imgFile, width, height, shared_array))
    arrProcess.start()
    arrProcess.join()

    print(list(shared_array))

    im.close()
    #print(list(shared_array))
    #print(arrayConversion(list(shared_array), width, height))

    print("Done in:", time.time() - startTime, "Seconds")