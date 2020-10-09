import request_ligand_from_PDBe

entrada=open("pdb_pfam_mapping.txt")
lines=entrada.readlines()

pfam_dictionary={}

for line in lines:
