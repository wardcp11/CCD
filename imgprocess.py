from PIL import Image
from PIL import ImageFilter
from PIL import ImageColor
import numpy as np
import time
import colorsys

def imgProcess():

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
            phaseVals[y,x] = theta
            OH = (lambdaC * theta) / (4 * np.pi)
            RH = OH
            arrayVals[y,x] = RH
    

if __name__ == '__main__':
    startTime = time.time()

    lambdaC = 600 #central wavelength
    imgFile1 = '1.tiff' #I(0)
    imgFile2 = '2.tiff' #I(pi/2)
    imgFile3 = '3.tiff' #I(3pi/2)
    imgFile4 = '4.tiff' #I(pi)
    im1 = Image.open(imgFile1)
    im2 = Image.open(imgFile2)
    im3 = Image.open(imgFile3)
    im4 = Image.open(imgFile4)

    width = im1.size[0]
    height = im1.size[1]
    arrayVals = np.empty((height, width))
    phaseVals = np.empty((height, width))

    imgProcess()

    im1.close()
    im2.close()
    im3.close()
    im4.close()

    phaseVals = phaseVals + (np.pi/2)
    phaseVals = phaseVals * (255 / np.pi)
    for y in range(height):
        for x in range(width):
            phaseVals[y,x] = int(round(phaseVals[y,x]))

    
    print(np.max(phaseVals))
    im = Image.fromarray(phaseVals)
    im = im.convert("RGB")

    #im = im.filter(ImageFilter.GaussianBlur(2)) #image low pass filter with radius

    im.save("filtered.png")
    im.close()

    print("Done in:", time.time() - startTime, "Seconds")
