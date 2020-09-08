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
 
# this function produce values of matrix
def count_kmers(sequence, k,r):
    regionLen = round(((len(sequence)-(k-1))/r)+.5)
    d = collections.defaultdict(np.int8)
    p = collections.defaultdict(np.int8)
    c = collections.defaultdict(np.uint32)

    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            d[sequence[i:i+k]] += 1
            p[sequence[i:i+k]] += int(i/regionLen)+1
            c[sequence[i:i+k]] = int(i/regionLen)+1            
    return d , p, c

# this function puts values in the case of FCGR matrix
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

def CGR(data, k , r=16 ,type=["default"]):
    c , rn , rm = count_kmers(data, k , r)
    chaos , picture , code = [] ,[],[]
    if("default" in type):
        chaos = np.full([2**k,2**k],0,dtype=np.uint8) 
        chaos = chaos_game_representation(c, k, chaos)

    if("mean" in type):
        picture = np.full([2**k,2**k],0,dtype=np.uint8)
        picture =  chaos_game_representation(rn, k, picture)

    if("region" in type):
        code = np.full([2**k,2**k],0,dtype=np.uint32)
        code =  chaos_game_representation(rn, k, code)

    return chaos, picture, code
    
def calculate_positon_distribution(c , sequence , k):
    d = collections.defaultdict(float)
    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            d[sequence[i:i+k]] += i/c[sequence[i:i+k]]
    return d

def CGR_coded(data , k, r, type=["code"]):
    word_code = code_countword(data, k , r)
    code_cgr = np.full([2**k,2**k,r],False)
    return chaos_game_representation(word_code , k , code_cgr)



def code_countword(sequence, k , r):
    regionLen = round(((len(sequence)-(k-1))/r)+.5)
    code = collections.defaultdict(np.array)

    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            code[sequence[i:i+k]] = np.full(r , False)              

    for i in range(len(sequence)-(k-1)):
        if "N" not in sequence[i:i+k]:
            code[sequence[i:i+k]][int(i/regionLen)] = True              
    return code