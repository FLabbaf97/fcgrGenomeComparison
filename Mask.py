import numpy as np


def do_mask(mat , mask):
    if(mask == "Binary"):
        return binaryMask(mat)
    elif(mask == "GrayScale"):
        return grayScaleMask(mat)
    elif(mask == "nomask"):
        return mat
    else:
        print(mask, " is undefined mask")
    

def binaryMask(mat):
    v = lambda x: 1 if(x>0) else 0
    binary = np.vectorize(v)
    return binary(mat)

def grayScaleMask(mat):
    max = mat.max()
    if(max == 0):
        return mat
    scale = 256/max
    gs = (mat*scale).astype(int)
    return gs