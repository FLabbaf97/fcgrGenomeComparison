import random
import sys

def rand_delete(seq , start , end , count):
    for i in range(count):
        index = start
        seq = seq[:index] + seq[index+1:]
    return seq

def rand_insert(seq , start , end , count):
    for i in range(count):
        index = start
        N = rand_nucleo()
        seq = seq[:index] + N + seq[index:]
    return seq

def rand_mutate(seq , start , end , count):
    for i in range(count):
        index = random.randint(start, end-1)
        print(index)
        N = rand_nucleo()
        print(N , seq[index])
        seq = seq[:index] + N + seq[index+1:]
    return seq

def transposition(seq, start , end, count):
    index = random.randint(0 , end-count)
    transposed_part = seq[start: start+count]
    newseq = seq[:start]+seq[start+count:]
    newseq = newseq[:index] + transposed_part + seq[index:]
    return newseq

def rand_transpose(seq , start , end , count):
    for i in range(count):
        index = random.randint(start, end-1)
        index2 = random.randint(start, end-1)
        newseq = seq
        newseq[index] = seq[index2]
        newseq[index2] = seq[index]
        seq = newseq
    return seq

def rand_nucleo():
    nucleotides = ["A" , "C" , "T" , "G"]
    return random.choice(nucleotides)

def write_seq_to_file(file_name , seq_name , seq):
    f = open(file_name , "a")
    f.write(">"+ seq_name+"\n")
    f.write(seq+"\n")
    f.close()
    print("write " + seq_name)


def main(argv):
    file_name = "simulated_data_paper_corrected.fasta"
    original_len = 1000
    base_sequence = ""
    A_original = ""
    B_original = ""
    original_mutation = 100
    # A_species_count = 20
    # B_species_count = 10
    f = open(file_name , "w")
    f.write("#original_len =" + str(original_len)+ "\n#original_mutation = "+ str(original_mutation) + "\n")
    f.close()
    nucleotides = ["A" , "C" , "T", "G"]
    
    for i in range(original_len):
        base_sequence += random.choice(nucleotides)
    # write_seq_to_file(file_name , "base_sequence BEFORE" , base_sequence)
    
    A_original = rand_mutate(base_sequence , 0 , original_len-1, original_mutation)
    B_original = rand_mutate(base_sequence , 0 , original_len-1 , original_mutation)

    # write_seq_to_file(file_name , "base_sequence" , base_sequence)
    write_seq_to_file(file_name , "A_original" , A_original)
    write_seq_to_file(file_name , "B_original" , B_original)
    

    A1 = rand_mutate(A_original , 0 , len(A_original), 2)
    write_seq_to_file(file_name , "A1" , A1)
    A2 = rand_mutate(A_original , 0 , len(A_original), 2)
    write_seq_to_file(file_name , "A2" , A2)
    A3 = rand_mutate(A_original , 0 , len(A_original), 5)
    write_seq_to_file(file_name , "A3" , A3)
    A4 = rand_mutate(A_original , 0 , len(A_original), 5)
    write_seq_to_file(file_name , "A4" , A4)
    A5 = rand_mutate(A_original , 0 , len(A_original), 10)
    write_seq_to_file(file_name , "A5" , A5)
    A6 = rand_mutate(A_original , 0 , len(A_original), 10)
    write_seq_to_file(file_name , "A6" , A6)
    B1 = rand_mutate(B_original , 0 , len(A_original), 2)
    write_seq_to_file(file_name , "B1" , B1)
    B2 = rand_mutate(B1 , 0 , len(A_original), 2)
    write_seq_to_file(file_name , "B2" , B2)
    B3 = rand_mutate(B2 , 0 , len(A_original), 10)
    write_seq_to_file(file_name , "B3" , B3)
    B4 = rand_mutate(B3 , 0 , len(A_original), 10)
    write_seq_to_file(file_name , "B4" , B4)
    B5 = rand_mutate(B4 , 0 , len(A_original), 20)
    write_seq_to_file(file_name , "B5" , B5)
    B6 = rand_mutate(B5 , 0 , len(A_original), 20)
    write_seq_to_file(file_name , "B6" , B6)
    B7 = rand_delete(B6 , 51 , 91, 40)
    write_seq_to_file(file_name , "B7" , B7)
    B8 = rand_delete(B7 , 0 , 50, 40)
    write_seq_to_file(file_name , "B8" , B8)
    B9 = rand_insert(B8 , 51 , 71 , 20)
    write_seq_to_file(file_name , "B9" , B9)
    B10 = rand_insert(B9 , 601 , 621, 20)
    write_seq_to_file(file_name , "B10" , B10)
    B11 = transposition(B10 , 0 , len(B_original) , 50)
    write_seq_to_file(file_name , "B11" , B11)
    B12 = transposition(B11 , 650 , len(B_original) , 100)
    write_seq_to_file(file_name , "B12" , B12)

    
if __name__ == "__main__":
   main(sys.argv[1:])




