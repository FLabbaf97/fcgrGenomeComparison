import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
import getopt
from PIL import Image
import matplotlib


from CGR import CGR , weightCGR
from Mask import binaryMask , grayScaleMask , do_mask
from Metrics import similarity
from tools import save_to_mega, naming, help, distance_matrix_compare, look_data
import re

#global variables
k=8
inputDir = ""
inputFile = ""
outputDir = "Results"
rn = 32
method = "default"
method_type ="none"



def make_distance_matrix(all_cgr, method):
    index={}
    for i in range (len(all_cgr)):
        index[all_cgr[i][0]] = i
    count = len(all_cgr)
    distance_matrix = np.empty([count,count],dtype=float) 
    # for each in all_cgr:
        # for another in all_cgr:
            # print("distance for each and another")
            # if(index[each[0]] == index[another[0]]):
                # distance_matrix[index[each[0]]][index[another[0]]] = 0
            # if(distance_matrix[index[each[0]]][index[another[0]]] != -1):
                # print("have been calculated")
                # continue
            # distance_matrix[index[each[0]]][index[another[0]]] = similarity(each, another, method, rn)
            # distance_matrix[index[another[0]]][index[each[0]]] = distance_matrix[index[each[0]]][index[another[0]]]
    lcount= 0
    for i in range(count):
        for j in range(count):
            if(i>j):
                lcount+=1
                distance_matrix[i][j] = similarity(all_cgr[i],all_cgr[j], method , rn)
            else:
                distance_matrix[i][j] = np.NaN
    save_to_mega(inputFile+"_"+method+"_k"+str(k)+"_rn"+str(rn), distance_matrix , list(index.keys()), dir=outputDir, inputDir=inputDir, mask=rn, method= method , k = k)
    distance_matrix_compare(distance_matrix)
    return 0

    
def main(argv):
    inputType=""
    weight=[]
# ---------------------this part is to get input as argument from terminal.................................. 
    if(len(argv)<1):
        help()
        return
    try:
        opts, args = getopt.getopt(argv,"f:d:o:rn:s:k:",["directory=","file=","regionnumber=","similarity=","ofile="])
    except getopt.GetoptError:
        help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            help()
            sys.exit()
        elif opt in ("-o", "--ofile"):
            global outputDir 
            outputDir = arg
            print ("outputDir " + outputDir)
        elif opt in ("-k"):
            global k 
            k = int(arg)
            print ("k " , k)
        elif opt in ("-f", "--file"):
            global inputFile
            inputType = "single file" 
            inputFile = arg
            print ("input file " + inputFile)
        elif opt in ("-d", "--directory"):
            global inputDir
            inputType = "folder" 
            inputDir = arg
            print ("input dir " + inputDir)
        elif opt in ("-rn", "--regionnumber"):
            global rn 
            rn = arg
            print("region number "+ rn)
        elif opt in ("-s", "--similarity"):
            global method
            method = arg
            if(arg[0] == 'w'):
                global method_type
                method_type = "weighted"
            print("method " + method)
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------

# -------- actual code --------------------------------------------------------------------
# ----------managing input ----------------------------------------------------------------
    all_fcgr = []
    genomes = []
    if(inputType == "folder"):
        print("folder operation")
        for filename in os.listdir(os.getcwd()+"/"+inputDir+"/"):
            if filename.endswith(".fasta"):
                with open(os.path.join(os.getcwd()+"/"+inputDir+"/", filename), 'r') as f:
                    lines = f.read().split("\n") 
                    name =naming(lines[0],filename)
                    genome = "".join(lines[1:])
                    genomes.append([genome , name])
    
    elif(inputType =="single file"):
        print("do single file operation")
        f = open(inputFile)
        data = f.read().split(">")
        for each in data[1:]:
            lines = each.split("\n")
            name = naming(lines[0])
            genome = "".join(lines[1:])
            genomes.append([genome , name])
    else:
        print("!!!!!!!!" + inputType)
    

#------------------- proccess data for evaluate k -----------------------
# comment this if your goal is only run the code
    # look_data(genomes)

# # ------------------ this is the heart of code ---------------------------------
    for genomeT in genomes:
        genome = genomeT[0]
        name = genomeT[1]
        # print("genome")
        fcgr, regionPicture, regionCode  = CGR(genome, k, rn)
        all_fcgr.append([name, fcgr, regionPicture , regionCode])

               
# ----------- heart of heart ------------------
    make_distance_matrix(all_fcgr , method)

if __name__ == "__main__":
   main(sys.argv[1:])