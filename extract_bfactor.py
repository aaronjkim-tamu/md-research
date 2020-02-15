'''
This script reads a .pdb file and returns the B-Factor of alpha carbons.

Name:
    parse_engine.py

Input:
    protein_code - set this to the protein code filename

Output:
    [protein_code]_bfactor.csv - contains csv of protein, chain ID, residue
        nubmer, and B-Factor for easier analysis

Author: 
    Aaron Kim

Last Edited:
    Feb 15, 2020

Python Version:
    3.8.1
'''

def main():

    # set to protein code for input and output file naming
    PROTEIN_CODE = '5cjb'

    # opens [PROTEIN_CODE].pdb
    with open(PROTEIN_CODE+'.pdb', 'r') as input_file: 

        # create output .csv file
        output_file = open(PROTEIN_CODE+'_bfactor.csv', 'w')

        # write headers for output_file
        output_file.write('Protein,Chain ID,Residue Number,B-Factor\n')

        # iterates through the pdb file line by line
        for line in input_file:

            # isolates data values
            line_data = line.split()

            # checks if the record is ATOM and the atom type is CA 
            if line_data[0] == 'ATOM' and line_data[2] == 'CA':

                # write data to output_file
                output_file.write(line_data[3] + ',' +  line_data[4] + ',' + \
                    line_data[5] + ',' + line_data[10] + '\n')

if __name__ == '__main__':
    main()