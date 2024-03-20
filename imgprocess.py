from PIL import Image
import numpy as np
import multiprocessing as mp
import time

def imgProcess(imgFile1,imgFile2,imgFile3,imgFile4, width, height, shared_array, lambdaC):

    im1 = Image.open(imgFile1)
    im2 = Image.open(imgFile2)
    im3 = Image.open(imgFile3)
    im4 = Image.open(imgFile4)

    for y in range(height):
        for x in range(width):
            denominator = (im1.getpixel((x,y)) - im4.getpixel((x,y)))
            numerator = (im3.getpixel((x,y)) - im2.getpixel((x,y)))
            if denominator != 0:
                theta = np.arctan(numerator / denominator)
            else:
                if np.sign(numerator) == np.sign(denominator):
                    theta = np.pi / 2
                else:
                    theta = -1 * (np.pi / 2)
            OH = (lambdaC * theta) / (4 * np.pi)
            RH = OH / (1.3 - 1)
            shared_array[y * width + x] = RH

def arrayConversion(inArry, width, height):
    arry = [[0 for i in range(width)] for j in range(height)]

    for current in range(len(inArry)):
        x = current % width
        y = current // width
        arry[y][x] = inArry[x+y]

    return arry
    

if __name__ == '__main__':
    startTime = time.time()

    lambdaC = 500 #central wavelength
    imgFile1 = '1.tiff' #I(0)
    imgFile2 = '2.tiff' #I(pi/2)
    imgFile3 = '3.tiff' #I(3pi/2)
    imgFile4 = '4.tiff' #I(pi)
    im1 = Image.open(imgFile1)
    im2 = Image.open(imgFile2)
    im3 = Image.open(imgFile3)
    im4 = Image.open(imgFile4)

    shared_array = mp.Array('f', im1.size[0] * im1.size[1])
    width = im1.size[0]
    height = im1.size[1]

    arrProcess = mp.Process(target=imgProcess, args=(imgFile1,imgFile2,imgFile4,imgFile4, width, height, shared_array, lambdaC))
    arrProcess.start()
    arrProcess.join()

    #print(list(shared_array))

    im1.close()
    im2.close()
    im3.close()
    im4.close()
    #print(list(shared_array))
    #print(arrayConversion(list(shared_array), width, height))

    print("Done in:", time.time() - startTime, "Seconds")
