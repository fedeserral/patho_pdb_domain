import argparse
from collections import defaultdict


def PDB_ID(input_file):
    """file with PDB entry list"""
    pdb_ids = open(input_file)
    lines=pdb_ids.readlines()[1:]
    strip_pdb_ids = [line.strip() for line in lines ]

    pdb_ids.close()
    print(strip_pdb_ids)
    return strip_pdb_ids

def pdb_ligands_mapping(input_file):
    """ mapping_ligands_pdb
    columns: 0=PDB_ID; 1=ligands"""
    mapping = open(input_file)
    mapping_lines=mapping.readlines()
    mapping.close()
    dic_out={}
    for line in mapping_lines:
        lines = line.split(':')
        
        key = lines[0].strip()
        value = [x.strip() for x in lines[1].strip().split(";") if x.strip()]
        if key in dic_out:
            dic_out[key] += value
        else:
          dic_out[key] = value
    return dic_out

def id_cross(PDB_data, mapping_data):
    """Cross IDs between inputs file"""

    for pdb in PDB_data:
        if pdb.lower() in mapping_data:
            for ligand in mapping_data[pdb.lower()]:
                print(pdb+"\t"+str(ligand))
    return 0


def parse_arguments():

    parser = argparse.ArgumentParser(description='Extract ligands from PDB entries')
    parser.add_argument("-p", '--PDB_list', default=None, help="Input file should have PDB ID list")
    parser.add_argument("-m", '--mapping_ligands_pdb',  default="lig_pairs.txt", help="Input file of ligands and PDB ID link:http://www.ebi.ac.uk/thornton-srv/databases/pdbsum/data/lig_pairs.lst")

    return parser

def main():

    parser=parse_arguments()
    args=parser.parse_args()

    id_cross(PDB_ID(args.PDB_list), pdb_ligands_mapping(args.mapping_ligands_pdb))
    return 0


if __name__=='__main__':
    main()
