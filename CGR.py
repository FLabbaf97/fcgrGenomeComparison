import collections
from collections import OrderedDict
from matplotlib import pyplot as plt
from matplotlib import cm
import pylab
import math
import numpy as np



#  A_____________T
#   |            |
#   |            |
#   |            |
#   |            |
#  C--------------G
 
def count_kmers(sequence, k,r):
    regionLen = round(((len(sequence)-(k-1))/r)+.5)
    d = collections.defaultdict(np.int8)
    p = collections.defaultdict(np.int8)
    c = collections.defaultdict(np.uint32)

    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            d[sequence[i:i+k]] += 1
            p[sequence[i:i+k]] += int(i/regionLen)+1
            # c[sequence[i:i+k]] += 2^int(i/regionLen)            
    return d , p , c
  
def chaos_game_representation(probabilities, k , chaos):
    array_size = int(math.sqrt(4**k))
    maxx = array_size
    maxy = array_size
    posx = 1
    posy = 1
    for key, value in probabilities.items():
        for char in key:
            if char == "T":
                posx += maxx / 2
            elif char == "C":
                posy += maxy / 2
            elif char == "G":
                posx += maxx / 2
                posy += maxy / 2
            maxx = maxx / 2
            maxy /= 2
        chaos[int(posy-1)][int(posx-1)] = value
        maxx = array_size
        maxy = array_size
        posx = 1
        posy = 1
 
    return chaos

def CGR(data, k , r = 12):
    chaos = np.full([2**k,2**k],0,dtype=np.uint8) 
    picture = np.full([2**k,2**k],0,dtype=np.uint8)
    code = np.full([2**k,2**k],0,dtype=np.uint32)
    c , rn , rc = count_kmers(data, k , r)
    chaos = chaos_game_representation(c, k, chaos)
    regionPicture =  chaos_game_representation(rn, k, picture)
    regionCode =  chaos_game_representation(rc, k, code)

    return chaos , regionPicture , regionCode

def weightCGR(data,k):
    chaos = np.full([2**k,2**k],0,dtype=np.uint8) 
    c = count_kmers(data, k)
    data_len= len(data)
    chaos = chaos_game_representation(c, k, chaos)

    #weight matrix
    weight = np.full([2**k,2**k],0,dtype=np.uint8) 
    w = calculate_positon_distribution(c , data , k)
    weight = chaos_game_representation(w, k, weight)/data_len
    return chaos, weight
    
def calculate_positon_distribution(c , sequence , k):
    d = collections.defaultdict(float)
    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            d[sequence[i:i+k]] += i/c[sequence[i:i+k]]
    return d