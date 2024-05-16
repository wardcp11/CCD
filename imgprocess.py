from PIL import Image
from PIL import ImageFilter
from PIL import ImageColor
import numpy as np
import time
import colorsys



lambdaC = 450 #central wavelength
n_index = 1 #refractive index (if in medium)



if __name__ == '__main__':
    startTime = time.time()
    #put hashtag on which function not using
    #imgProcess_4img()
    imgProcess_7img()

    print("Done in:", time.time() - startTime, "Seconds")



def imgProcess_4img():

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
            RH = OH / n_index
            arrayVals[y,x] = RH

    im1.close()
    im2.close()
    im3.close()
    im4.close()

    array2img(height, width, phaseVals, arrayVals)

def imgProcess_7img():

    imgFile1 = '1.tiff' #I(-3pi/2)
    imgFile2 = '2.tiff' #I(-pi)
    imgFile3 = '3.tiff' #I(-pi/2)
    imgFile4 = '4.tiff' #I(0)
    imgFile5 = '5.tiff' #I(pi/2)
    imgFile6 = '6.tiff' #I(pi)
    imgFile7 = '7.tiff' #I(3pi/2)
    im1 = Image.open(imgFile1)
    im2 = Image.open(imgFile2)
    im3 = Image.open(imgFile3)
    im4 = Image.open(imgFile4)
    im5 = Image.open(imgFile5)
    im6 = Image.open(imgFile6)
    im7 = Image.open(imgFile7)

    width = im1.size[0]
    height = im1.size[1]
    arrayVals = np.empty((height, width))
    phaseVals = np.empty((height, width))

    for y in range(height):
        for x in range(width):
            denominator = (im1.getpixel((x,y)) - 3 *im3.getpixel((x,y)) + 3 * im5.getpixel((x,y)) - im7.getpixel((x,y)))
            numerator = 2 * (-1 * im2.getpixel((x,y)) + 2 * im4.getpixel((x,y)) - im6.getpixel((x,y)))
            if denominator != 0:
                theta = np.arctan(numerator / denominator)
            else:
                if np.sign(numerator) == np.sign(denominator):
                    theta = np.pi / 2
                else:
                    theta = -1 * (np.pi / 2)
            phaseVals[y,x] = theta
            OH = (lambdaC * theta) / (4 * np.pi)
            RH = OH / n_index
            arrayVals[y,x] = RH

    im1.close()
    im2.close()
    im3.close()
    im4.close()
    im5.close()
    im6.close()
    im7.close()

    array2img(height, width, phaseVals, arrayVals)

def array2img(height, width, phaseArry, arrayVals):

    phaseArry = phaseArry + abs(phaseArry.min())
    phaseArry = phaseArry * (255 / np.pi)
    for y in range(height):
        for x in range(width):
            phaseArry[y,x] = int(round(phaseArry[y,x]))
    im = Image.fromarray(phaseArry)
    im = im.convert("RGB")
    im.save("phase.png")
    im.close()

    arrayVals = arrayVals + abs(arrayVals.min())
    max_factor = (lambdaC * (np.pi/2)) / (4 * np.pi)
    arrayVals = arrayVals * (255 / max_factor)
    for y in range(height):
        for x in range(width):
            arrayVals[y,x] = int(round(arrayVals[y,x]))
    im = Image.fromarray(arrayVals)
    im = im.convert("RGB")
    im.save("RH.png")
    im.close()
