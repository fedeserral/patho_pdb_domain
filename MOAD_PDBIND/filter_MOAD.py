import json
import argparse

def moad_db(input_file):
    with open(input_file) as a:
         MOAD = json.load(a)
    return MOAD

def ligands(input_file):
    ligands_list= open(input_file)
    read_ligands=ligands_list.readlines()
    ligands = [line.strip() for line in read_ligands ]
    ligands_list.close()
    return ligands

def true_ligands(MOAD,ligands):
    valid_ligands =[]
    for ligand in ligands:
        if ligand in MOAD:
            compound= MOAD[ligand]
            for pdb in compound["pdbs"]:
                for residue in pdb["residues"]:
                    if residue["standard_value"] != "None":
                        valid_ligands.append(ligand)
    unique_valid_ligands= set(valid_ligands)
    return unique_valid_ligands


def parse_arguments():

    parser = argparse.ArgumentParser(description='Extract valid ligands from MOAD DATABASE')
    parser.add_argument("-l", '--ligands_list', default=None, help="Input file should have ligands ID list")
    parser.add_argument("-db", '--moad_database',  default="MOAD.json")


    return parser

def main():

    parser=parse_arguments()
    args=parser.parse_args()

    unique_valid_ligands = true_ligands(moad_db(args.moad_database), ligands(args.ligands_list))
    for ligand in unique_valid_ligands:
        print(ligand)
    return 0


if __name__=='__main__':
    main()
