'''
This script reads a .pdb file to extract the B-factor and a CHARMM output file 
to extract the rmsf of the alpha carbons.
Run the script in the same folder as the .pdb and the coor_dyna.out files.

Name:
    extract_bfactor_rmsf.py

Input:
    PROTEIN_CODE - set this to the protein code filename
    MISSING_START - array of the start indices of missing residue segments
    MISSING_END - array of the end indices of missing residue segments

Output:
    [PROTEIN_CODE]_bfactor.csv - contains csv of protein, chain ID, residue
        nubmer, and B-Factor for easier analysis

Author: 
    Aaron Kim

Last Edited:
    Feb 15, 2020

Python Version:
    3.8.1
'''

import math

def main():

    # set to protein code for input and output file naming
    PROTEIN_CODE = '5cjb'

    # indices to ignore because these residues were missing
    MISSING_START = [142]
    MISSING_END = [147]

    # generate ignore residue array
    ignore_residues = []

    for i in range(len(MISSING_START)):
        for j in range(MISSING_START[i], MISSING_END[i] + 1):
            ignore_residues.append(j)

    # initialize data arrays
    protein = []
    chain_ID = []
    residue_num = []
    bfactor = []
    sqrt_bfactor = []
    rmsf = []

    # opens [PROTEIN_CODE].pdb
    with open(PROTEIN_CODE+'.pdb', 'r') as pdb_file:

        # iterates through the pdb file line by line
        for i, line in enumerate(pdb_file):

            # isolates data values
            line_data = line.split()

            # checks if the record is ATOM and the atom type is CA 
            if (line_data[0] == 'ATOM' or line_data[0] == 'HETATM') and \
                line_data[2] == 'CA':
                
                # checks if the pdb line is formatted correctly
                if len(line_data) < 12:
                    print('================== WARNING ==================')
                    print('INCORRECT TEXT FORMATTING DETECTED')
                    print('CHECK LINE: ' + str(i + 1) + ' OF PDB FILE')
                    print('CHECK FOR NUMBERS WITHOUT SPACES BETWEEN THEM')
                    print('EXITING PROGRAM NOW')
                    quit()

                # stores protein, chain ID, residue number, bfactor
                protein.append(line_data[3])
                chain_ID.append(line_data[4])
                residue_num.append(line_data[5])
                bfactor.append(line_data[10])

                # calculate square root of bfactor
                sqrt_bfactor.append(str(math.sqrt(float(line_data[10]))))

    # open coor_dyna.out
    with open('coor_dyna.out', 'r') as rmsf_file:

        # iterates through the rmsf file line by line
        for line in rmsf_file:

            # isolates data values
            line_data = line.split()

            # checks if the line is not empty and contains the rmsf value
            if len(line_data) > 0 and line_data[0] == '(' and \
                int(line_data[3]) not in ignore_residues:

                # stores rmsf 
                rmsf.append(line_data[6])

    # check if data is properly extracted
    check_output = [len(rmsf), len(protein), len(chain_ID), len(residue_num), \
        len(bfactor), len(sqrt_bfactor)]

    # warning output
    if len(set(check_output)) != 1:
        print('================== WARNING ==================')
        print('DATA POINT SIZES DO NOT MATCH')
        print('CHECK WHICH OF THE VARIABLES IS DIFFERENT')
        print('RMSF:         ' + str(check_output[0]))
        print('PROTEIN:      ' + str(check_output[1]))
        print('CHAIN_ID:     ' + str(check_output[2]))
        print('RESIDUE_NUM:  ' + str(check_output[3]))
        print('BFACTOR:      ' + str(check_output[4]))
        print('SQRT_BFACTOR: ' + str(check_output[5]))
        print('EXITING PROGRAM NOW')
        quit()

    # create output .csv file
    with open(PROTEIN_CODE+'_bfactor_rmsf.csv', 'w') as output_file:

        # write headers for output_file
        output_file.write('Protein,Chain ID,Residue Number,RMSF,B-Factor,'\
            'sqrt(B-Factor)\n')
    
        # write data arrays to output_file
        for i in range(len(protein)):
            output_file.write(protein[i] + ',' + chain_ID[i] + ',' + \
            residue_num[i] + ',' + rmsf[i] + ',' + bfactor[i] + ',' + \
            sqrt_bfactor[i] + '\n')

if __name__ == '__main__':
    main()
