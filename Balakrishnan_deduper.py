# Sort input sam file before running!
# CIGAR strings will have: M, N, D, I, S
# Reads are uniquely mapped, single-end
# Must keep track of the number of wrong UMIs
# Must run script with /usr/bin/time/v

import argparse
import re

# Set args: input sam file, output sam file, UMI file, help message
# How do I set up the help argument?
def get_args():
    parser = argparse.ArgumentParser(description="A program to introduce yourself")
    parser.add_argument("-f", "--file", help="The absolute path of the sorted input sam file", type=str, default="")
    parser.add_argument("-u", "--umi", help="The name of the file containing the list of known UMIs", type=str, default="")
    #parser.add_argument("-h", "--help", action='help', help="User inputted size threshold for the RoCCs", type=int, default=2)
    parser.add_argument("-o", "--outfile", help="The absolute path of the output sam file", type=str, default="")
    return parser.parse_args()

args = get_args()

def get_umi(read_name: str) -> str:
    ''' Isolates and returns the UMI from the end of the RNAME string from a sam file'''
    # split the QNAME at colons
    qname_chunks = read_name.strip().split(':')
    # get the last entry in the list (the UMI comes after the last colon in the QNAME)
    return qname_chunks[len(qname_chunks)-1]

# Not sure if I'm doing this right, also how does this code work because I need to be able to comment it
def get_strand(flag: int) -> str:
    '''Extracts and returns the strand information from the bitwise flag from a sam file'''
    if ((flag & 16) == 16):
        return "rev"
    else:
        return "fwd"
    
def get_five_prime(pos: int, strand: str, cigar: str) -> int:
    ''' Calculates the 5' position of the read given the 1-based leftmost mapping position, strand, 
    and cigar string for the read'''
    pos_5_prime = pos
     # All that matters for calculating 5' pos on the forward strand is if there was soft clipping at the start of the read
    if strand == "fwd": 
        index = 0
        while cigar[index].isdigit():  # We're just checking until we hit the first letter in the CIGAR string
            index += 1

        if cigar[index] == "S":  # If the first letter in the CIGAR string is S
            num_clipped = int(cigar[:index])  # number of nucleotides clipped is the number leading up to S in the CIGAR string
            pos_5_prime -= num_clipped  # we move the 5' pos back to the start of the nucleotides that were soft-clipped off
    else:  # reverse strand
        # if the nucleotides are matches/mismatches or exist only in the reference (deletions/alignment gaps), we need to add
        # that number of nucleotides to our 5' position placeholder variable 
        things_to_add = re.findall('([0-9]+)[MDN]', cigar)  # use regex to get the number of nucleotides before M, D, or N
        for thing_to_add in things_to_add:  # findall returned a list, so we have to parse the list
            pos_5_prime += int(thing_to_add)  # add every number in the list to our 5' position placeholder variable
        # if there were nucleotides soft-clipped at the 5' end of the read, we need to add that number of nucleotides to our 5'
        # position placeholder variable
        end_soft_clipped = re.findall('([0-9]+)S$', cigar)  # use regex to get the number of nucleotides before the S at the end of the cigar string  
        if len(end_soft_clipped) != 0:  # if the end of the read was not soft clipped, findall will return an empty list
            pos_5_prime += int(end_soft_clipped[0])  # if the end of the read was soft clipped, findall will return a list with one number
    
    return pos_5_prime

# Store known UMIs in a set
umi_set = set()
with open(args.umi, 'r') as UMI:
    for line in UMI:
        line = line.strip()
        umi_set.add(line)

with open(args.outfile, 'w') as outfile:
    with open(args.file, 'r') as infile:
        current_chrom = None  # holds the current chromosome reads are on
        seen = set()  # holds the reads we've seen before
        
        # Parse the input file
        for line in infile:
            # If it is a header line
            if line.startswith('@'):
                # write it to the output file
                outfile.write(line)
            # If it is not a header line
            else:
                # Split the line by tabs
                line = line.strip().split()
                #print(len(line))
                # Read name is column 1
                rname = line[0]
                # Bitwise flag is column 2
                flag = int(line[1])
                # Chromosome is column 3
                chrom = line[2]
                # 1-based leftmost mapping position is column 4
                pos = int(line[3])
                # Cigar string is column 6
                cigar = line[5]
                
                # Isolate the UMI from the read name
                umi = get_umi(rname)
                
                #print(rname, flag, chrom, pos, cigar)
                
                # If the UMI is not in the known UMIs set
                # if umi not in umi_set:
                #     continue  # skip to the next read
                # If the UMI is a known UMI
                #else:
                    # If we have moved to a new chromosome
                if chrom != current_chrom:
                    seen.clear()  # reset seen for the new chromosome
                    current_chrom = chrom  # set current chrom to the new chromosome
                
                strand = get_strand(flag)  # Extract the strand from the bitwise flag
                # Get the 5' pos from the 1-based leftmost mapping position, strand, and cigar string
                pos_5_prime = get_5_prime(pos, strand, cigar)  