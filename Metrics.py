from math import sqrt
import numpy as np


def similarity(first , second , method , w =[] , rn = 24):
    mat1 = first[1]
    mat2 = second[1]
    
    d1 = first[2]
    d2 = second[2]

    
    if(method == "regioning"):
        regionPicture1 = first[3]
        regionPicture2 = second[3]
        distance = np.abs(regionPicture1-regionPicture2)
        similarity = rn - distance
        return w_pearson(mat1 , mat2 ,  similarity)
    elif(method == "mean_region"):
        regionPicture1 = first[2]/(mat1+0.00001)
        regionPicture2 = second[2]/(mat2+0.00001)
        mat1 = ((len(mat1)^2)/np.sum(mat1))*mat1
        mat2 = ((len(mat2)^2)/np.sum(mat2))*mat2
        distance = np.abs(regionPicture1-regionPicture2)
        similarity = rn - distance
        return w_pearson(mat1 , mat2 , similarity)
    elif(method == "region_coding"):
        regionCode1 = first[3]
        regionCode2 = second[3]
        # print("regionCode1 shape" , regionCode1.shape)
        return region_code_similarity(mat1 , mat2 , regionCode1 , regionCode2)
    elif(method == "Jaccard"):
        return jaccard_disSimilarity(mat1 , mat2)
    elif(method == "default" or method == "Euclidean"):
        return Euclidean_distance(mat1 , mat2)
    elif(method== "metric1"):
        return metric1(mat1 , mat2)
    elif(method== "pearson"):
        return pearson_correlation(mat1 , mat2)
    elif(method== "w_pearson"):
        return w_pearson(mat1 , mat2 , first[2]+second[2])
    elif(method == "w2_pearson"):
        return w_pearson(first[2] , first[1] , np.multiply(mat1, mat2))
    elif(method == "ncc"):
        return NCC(mat1 , mat2)
    elif(method == "wd_pearson"):
        return pearson_correlation(d1 , d2)

 

    else:
        print(method , " is undefined method")


def region_code_similarity(mat1 , mat2 , regionCode1 , regionCode2):
    #for each word, weight is mumber of shared region 
    # print("compute regional similarity")
    weight_code = np.bitwise_and(regionCode1, regionCode2)
    # print("weigh code shape", weight_code.shape)
    def g(x):
        return np.sum(x)
    weight = np.apply_along_axis(g,2,weight_code)
    # print("weight shape" , weight.shape)
    # print("mat shape" , mat1.shape)
    # print("weight" , weight.shape)
    return w_pearson(mat1, mat2 , weight)
            

def Euclidean_distance(mat1, mat2):
    return sqrt(((mat1-mat2) * (mat1-mat2)).sum())
    

def jaccard_disSimilarity(mat1 , mat2):
    # count of k-mers that one have and another doesnt
    temp = len(mat1)*len(mat2)-(np.multiply(mat1, mat2).sum())
    mat1 = mat1-1
    mat2 = mat2-1
    zero = np.multiply(mat1, mat2).sum()
    return temp-zero
    

def metric1(mat1 , mat2):
    a = 0
    b = 0
    c = 0
    d = 0
    s = 0
    p = 0
    for i in range(len(mat1)):
        for j in range(len(mat1)):
            if(mat1[i][j] > 0 and mat2[i][j] > 0): 
                a+=(mat1[i][j]+mat2[i][j])/2
            elif(mat1[i][j] == 0 and mat2[i][j] > 0):
                b+=mat2[i][j]
            elif(mat2[i][j] == 0 and mat1[i][j] > 0):
                c+=mat1[i][j]
            elif(mat1[i][j] == mat2[i][j] and mat2[i][j] == 0):
                d+=1
    # print(" a, b, c, d:"  , a ,b ,c ,d)
    # d = d/(len(mat1)*len(mat1))
    n = a+b+c+d
    p = (a+b)*(a+c)/(n**2)
    # print("p :" , p)
    if(p == 0 or n == 0 or p == 1):
        return -1
    s = (a-n*p)/sqrt(p*n*(1-p))
    return s


def pearson_correlation(mat1 , mat2):
    mat1 = mat1.flatten()
    mat2 = mat2.flatten()
    corr = 1 - np.corrcoef(mat1, mat2)[1][0]
    return corr

def w_pearson(x, y, w):
    # print(x.shape() , y.shape() , w.shape())
    if(np.all((w == 0))):
        print("خاک بر سرم")
    ret = 1-(cov(x, y, w) / np.sqrt(cov(x, x, w) * cov(y, y, w)))
    # print("distance = " , ret)
    return ret

def cov(x, y, w):
    """Weighted Covariance"""
    res= np.average((x - np.average(x, weights=w)) * (y - np.average(y, weights=w)), weights=w)
    if(res == 0):
        return 1
    return res

def countSetBits(n): 
    count = 0
    while (n): 
        count += np.bitwise_and(n , 1)
        n >>= 1
    return count 

def NCC(mat1, mat2):
    A = mat1.flatten()
    P = mat2.flatten()
    Am = np.mean(A)
    Pm = np.mean(P)
    sum1 = 0
    sum2 = 0
    sqsum2 =0
    sqsum3= 0
    for i in range(len(A)):
        sum1 += (A[i]-Am)*(P[i]-Pm)
        sqsum2 +=pow(A[i]-Am,2)
        sqsum3 +=pow(P[i]-Pm,2)
    return sum1/np.sqrt(sqsum2*sqsum3)