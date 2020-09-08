import sys
import os
import numpy as np
import pandas as pd
from pathlib import Path
import getopt
import re
import math
from name_mapping import sp


def distance_matrix_compare(b):
    print("************  result   ********************")
    df = pd.read_excel("alignment_based/influenza.xls",header=0 , index_col=0, sheet_name=0)
    a = df.as_matrix()
    
    a = a.flatten()
    b = b.flatten()
    # print("alignment : " , len(a))
    # print("reality" , len(b))
    a = a[np.logical_not(np.isnan(a))]
    b = b[np.logical_not(np.isnan(b))]
    # print("real alignment : " , len(a))
    # print("real reality" , len(b))
    r = np.corrcoef(a , b)[0,1]
    print("pearson correlarion coeficient: " , r)
    #dot product
    b_modulus = np.sqrt((b*b).sum())
    b = b/b_modulus
    a_modulus = np.sqrt((a*a).sum())
    a = a/a_modulus
    c = np.dot(a,b)
    print("dot product: " , c)    
    # print(a)
    # print(b)
    



def help():
    print("wrong format. type:")
    print ("python3 Run.py -f <single input file> -m <maskname> -s <similarity metric> -o <outputdirectory> -k <word lengh> -rn <region number>")
    print("\nor in case that you have one file for each sequence: \n")
    print ("python3 newRun.py -d <directory of input files> -m <maskname> -s <similarity metric> -o <outputdirectory> -k <word lengh> -rn <region number>")     

def save_to_mega(filename, matrix , species, dir, inputDir , mask , method , k):
    directory = os.getcwd()+"/"+dir+"/"
    Path(directory).mkdir(parents=True, exist_ok=True)
    title = "!Title: " + inputDir + "_" + str(mask) + "_" + method +"_"+str(k)+ ";\n"
    format = "!Format DataType=Distance DataFormat=LowerLeft NTaxa=" + str(len(species)) + ";"
    description = "!Description\n"+ "  No. of Taxa : " + str(len(species)) + "\n  d : Estimate\n" + ";"
    
    f = open(dir+"/"+filename+".meg", "w")
    f.write("#mega\n")
    f.write(title)
    f.write(format)
    f.write(description)
    f.write("\n")
    # print(species)
    for i in range(len(species)):
        # f.write("["+i+"] ")
        f.write("#"+species[i]+ "\n")
    
    for i in range(len(species)):
        for j in range(len(species)):
            if(i<j or i==j):
                continue
            f.write(str(matrix[i][j]))
            f.write("    ")
        f.write("\n")
        
    f.close()
    return 0
    
def naming(line , filename = ""):
    # pat = re.compile('[a-zA-Z]+.fasta')
    # if(re.match(pat , filename)):
    #     return filename[0:-5]
    if('_' in filename):
        return filename[0:-5]
    elif(line in sp):
        return sp[line].replace(" " , "_")
    else:
        return line
        # name = ''.join(line.split(',')[0].split('>')[-1].split(' ')[1:])
        # if(re.search("Infulanza",line)):
        #     name ="_".join(("".join(line.split("(")[2:]).split(")")[0]).split("/"))
        #     name = name.replace(" " , "_")
        #     name = name.replace("'" , "")
        #     name = name.replace("`" , "")
        # if(len(name)>40):
        #     name = name.replace('virus',"")
        #     name = name.replace('strain' , '')

        # return name    
    
    # else:
    #     return line



def look_data(genomes):
    print("look_data")
    for k in [7,8,9,10,11,12]:
        print("for k = " , k)
        overal_count = 0 
        distinct_count = 0
        sum_distinct_count = 0
        sum_overall_count = 0
        mean_overal_count = 0
        mean_distinc_count = 0
        distinct_arr = {}
        overal_distinct={}
        overal_distinct_count = 0
        for genomeT in genomes:
            genome = genomeT[0]
            for i in range(len(genome)-k-1):
                overal_distinct[genome[i:i+k]]=1
                distinct_arr[genome[i:i+k]] = 1
                overal_count +=1
            distinct_count = len(distinct_arr)
            sum_distinct_count += distinct_count
            sum_overall_count += overal_count
            distinct_arr={}
        overal_distinct_count = len(overal_distinct)
        mean_overal_count = sum_overall_count/len(genomes)
        mean_distinct_count = sum_distinct_count/len(genomes)
        print("mean_distinct_count = " , mean_distinct_count)
        # print("mean_overal_count = " , mean_overal_count)
        print("ratio mean_overal_count/mean_distinct_count = " , mean_overal_count/mean_distinct_count)
        print("overla_distinct_count = " , overal_distinct_count)
        print("---------------------------------------------")
