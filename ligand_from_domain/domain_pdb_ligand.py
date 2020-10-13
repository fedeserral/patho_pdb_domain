import request_ligand_from_PDBe
import json

entrada=open("pdb_pfam_mapping.txt")
lines=entrada.readlines()

pdb_dictionary={}

for line in lines[1:]:
    line=line.split("\t")
    pdb=line[0]
    chain=line[1]
    position=line[2]+"-"+line[3]
    pfam=line[4].split(".")[0]
    if pdb not in pdb_dictionary.keys():
        pdb_dictionary[pdb]=[(pfam,chain,position)]
    else:
        list_aux=pdb_dictionary[pdb]
        list_aux.append((pfam,chain,position))
        pdb_dictionary[pdb]=list_aux

f='5OF4'
e='5LL9 6AQH 5TY9 5L0A 5N63 5WBM 5VD3 5IXV 5VHS 5XTR 5M3A 5O4E 5MYI 5MFN 5WRJ 5VSH 5X7O 5GS7 5M7M 5U4G'
PDBe_dic=(request_ligand_from_PDBe.ligands_from_pdbs(e))

pfam_pdb_ligand_dic={}

for pdb in PDBe_dic.keys():
    pdb_pfam_list=pdb_dictionary[pdb]
    PDBe_ligand_list=PDBe_dic[pdb]
    for ligand_data in PDBe_ligand_list:
        ligand_id=ligand_data[0]
        ligand_chain=ligand_data[3]
        ligand_position=ligand_data[4]
        for pfam_data in pdb_pfam_list:
            pfam_id=pfam_data[0]
            pfam_chain=pfam_data[1]
            pfam_position=pfam_data[2]
            pfam_position_inicio=int(pfam_position.split("-")[0])
            pfam_position_final=int(pfam_position.split("-")[1])
            if ligand_chain == pfam_chain and ligand_position>pfam_position_inicio and ligand_position<pfam_position_final:
                #ligand_dic={"ligand_id":ligand_id,"chain":ligand_chain, "position": ligand_position}
                print(pfam_id,pfam_chain,pfam_position,pdb,ligand_id,ligand_chain,ligand_position)
#print(json.dumps(pfam_pdb_ligand_dic, indent=4, sort_keys=True))