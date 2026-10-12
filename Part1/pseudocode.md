- Define the problem

PCR duplicates are essentially just identical sequencing reads that generated when the original template molecule is over-amplified in PCR during library prep. They introduce bias by making it seem like there is more of a certain sequence present than there actually is. They can also mess up any analysis process where sequences need to be counted.

We need to remove PCR duplicates from our data. We could remove PCR duplicates right after sequencing or quality filtering, but that would require comparing each sequence to every other sequence, which will be too inefficient. Instead, we will do reference-based PCR deduplication, which is when we remove the PCR duplicates after aligning our sequences to the genome. This will allow us to identify and remove PCR duplicates much more efficiently.

samtools sort Sorts by reference sequence, then position, and then the reverse flag 

- Develop your algorithm using pseudocode

Set args: input file, output file, umi size, umi file

Initialize a list that will hold all the umis

Open umi file to read
Parse umi file
    Add each umi to the umi list

Open output file to write

Open input file to read

Initialize a dict that will hold the reads we've seen before
    keys: [chrom, UMI, 5' pos, strand]
    vals: count?

Parse input file
    if line starts with @:
        write to output file
    else:
        umi = last umi_size characters of 1st column (read_name[-umi_size:])
        if umi in umi list:
            chrom = 3rd column
            strand = Function - determining what strand the sequence is on (what val the strand var will have)
                strand: holds the strand, 5th bit in the binary version of the bitwise flag (2nd column of the current line)
                - strand will be fwd if the 5th bit is 0
                - strand will be rev if the 5th bit is 1
                * See code in slides for how to isolate a bit
            pos = Function - determining what the 5' position of the sequence is, initialize to 0?
                pos: holds the 5' position
                pos = 2nd column  # to start
                If strand is rev:
                    index = 0
                    digits = ""
                    while index < len(CIGAR):
                        if CIGAR[index] is a digit:
                            digits += CIGAR[index]
                        if CIGAR[index] == M or D or N:
                            pos += int(digits)
                            digits = ""
                        index += 1
                    pos -= 1    

            if [chrom, umi, pos, strand] not in dict:
                dict[[chrom, umi, pos, strand]] = 1
                write line to output file (INCLUDE NEWLINE)
            else:
                dict[[chrom, umi, pos, strand]] += 1


- Determine high level functions
    - Description
    - Function headers
    - Test examples (for individual functions)
    - Return statement

def determine_strand(bit: int) -> string:
    ''' This function takes the bitwise flag from a read sequence in a sam file and returns which strand the read sequence is on '''

    return strand

determine_strand(0) : should be fwd
determine_strand(99) : should be fwd  64 + 32 + 2 + 1
determine_strand(16) : should be rev  16
determine_strand(83) : should be rev  64 + 16 + 2 + 1

def determine_pos(pos: string, strand: string, cigar: string) -> int:
    ''' This function takes the 1-based leftmost mapping position, strand, and cigar string from a read sequence in a sam file and returns the 5' position of that read sequence on the reference sequence '''

    return 5pos

determine_pos(3, rev, 4M) : should return 6
determine_pos(3, rev, 1S4M) : should return 6
determine_pos(3, rev, 4M1S) : should return 6
determine_pos(3, rev, 3M1I1M) : should return 6
determine_pos(3, rev, 2I4M) : should return 6
determine_pos(3, rev, 4M1I) : should return 6
determine_pos(3, rev, 2M1D1M) : should return 6
determine_pos(3, rev, 2M1N1M) : should return 6
determine_pos(3, fwd, 4M) : should return 3
determine_pos(3, fwd, 1S4M) : should return 3
determine_pos(3, fwd, 4M1S) : should return 3
determine_pos(3, fwd, 3M1I1M) : should return 3
determine_pos(3, fwd, 2I4M) : should return 3
determine_pos(3, fwd, 4M1I) : should return 3
determine_pos(3, fwd, 2M1D1M) : should return 3
determine_pos(3, fwd, 2M1N1M) : should return 3


