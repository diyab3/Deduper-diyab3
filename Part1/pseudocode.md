- Define the problem

PCR duplicates are essentially just identical sequencing reads that generated when the original template molecule is over-amplified in PCR during library prep. They introduce bias by making it seem like there is more of a certain sequence present than there actually is. They can also mess up any analysis process where sequences need to be counted.

We need to remove PCR duplicates from our data. We could remove PCR duplicates right after sequencing or quality filtering, but that would require comparing each sequence to every other sequence, which will be too inefficient. Instead, we will do reference-based PCR deduplication, which is when we remove the PCR duplicates after aligning our sequences to the genome. This will allow us to identify and remove PCR duplicates much more efficiently.

samtools sort Sorts by reference sequence, then position, and then the reverse flag 

- Develop your algorithm using pseudocode

Set up args:
Input sam file
Output sam file

Open the output sam file to write to

Function - set chrom, pos, strand variables
chrom: holds the chromosome, 3rd column of the current line, intialize to 0
strand = Function - determining what strand the sequence is on (what val the strand var will have), initialize to fwd?
    strand: holds the strand, 5th bit in the binary version of the bitwise flag (2nd column of the current line)
    - strand will be fwd if the 5th bit is 0
    - strand will be rev if the 5th bit is 1
    * See code in slides for how to isolate a bit
length: holds the length of the sequence, len(column 10), initialize to 0?
pos = Function - determining what the 5' position of the sequence is, initialize to 0?
    pos: holds the 5' position
    - if strand is fwd, it is just the value in column 2
    - if strand is rev, it is the value in column 2 + length
umi = Function - isolating the umi from the read name, initialize to AAAAAAAA
    umi: holds the 8 nucleotide sequence at the end of the read name (read_name[-8:])

Open the input sam file to read
For each line in the input sam file:

    current_seq_pos = Function - determining what the 5' position of the sequence is
    current_seq_strand = Function - determining what strand the sequence is on
    current_umi = Function - isolating the umi from the read name
    If chrom != 2nd column or pos != current_seq_pos or strand != current_seq_strand or umi != current_umi:
        # We do not have a duplicate
        Write the current line to the output sam file
    


    

    If chrom == 2nd column:
        current_seq_pos = Function - determining what the 5' position of the sequence is
        If pos == current_seq_pos:
            current_seq_strand = Function - determining what strand the sequence is on
            If strand == current_seq_strand:
                current_umi = Function - isolating the umi from the read name
                If umi == current_umi:
                    # We have a duplicate!
                    Go to next line of the sam file - ??? How do I make sure I go to the next line and do not write this current line to the output sam file
    Write the 





    If the chrom != 2nd column: 
        # since sam file is sorted, there will be no more duplicates for the sequence currently being stored in the variables, time to reset 
        Function - set chrom, pos, strand variables (this time to the values from the current line)

    Else:
        If pos != 4th column:
        # since sam file is sorted, there will be no more duplicates for the sequence currently being stored in the variables, time to reset

        



