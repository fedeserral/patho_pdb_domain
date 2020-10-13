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

f='5OF4 5GPQ 5T38'
e='5OF4 5GPQ 5T38 5UDS 5L0R 5GY8 5MZJ 5Y79 5W8C 5P92 5MKA 5WDQ 5W9J 5N69 5NPE 5GZY 5X9H 5MZ8 5O4N 5LQ9 5U4Z 5MOC 5X9S 5O5S 5GO2 5NM8 5X4V 5XPZ 5GZS 2M9A 5VPD 5KVB 5P9B 5Y0A 5MYG 5WF9 5U6C 5Y2Y 5VVC 5W93 5N4Q 5VBG 5XHE 2NDB 5LE6 6ALG 5VQ4 5ODR 5H6B 5K9B 5GV3 5MHD 5VP0 5OEJ 5WO8 5T4R 5LLH 5GV2 5U65 5V5N 5VVK 5NGG 5T99 5WHK 5U0D 5MPR 5KU6 5V5K 5OFW 5GV1 5VLL 5TZO 5TI3 5VQ3 5U98 5V60 5XEC 5T9I 5LL9 6AQH 5TY9 5L0A 5N63 5WBM 5VD3 5IXV 5VHS 5XTR 5M3A 5O4E 5MYI 5MFN 5WRJ 5VSH 5X7O 5GS7 5M7M 5U4G'
PDBe_dic=(request_ligand_from_PDBe.ligands_from_pdbs(e))

pfam_pdb_ligand_dic={}

for pdb in PDBe_dic.keys():
    pdb_pfam_list=pdb_dictionary[pdb]
    PDBe_ligand_list=PDBe_dic[pdb]
    ligand_record=[]
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
                ligand_dic={"ligand_id":ligand_id,"chain":ligand_chain, "position": ligand_position}
                ligand_record.append(ligand_dic)


    if pfam_id not in pfam_pdb_ligand_dic.keys():
        pdb_record= {pdb: ligand_record}
        pfam_pdb_ligand_dic[pfam_id]=[pdb_record]
    else:
        pdb_record= {pdb: ligand_record}
        pfam_pdb_ligand_dic[pfam_id].append(pdb_record)



print(json.dumps(pfam_pdb_ligand_dic, indent=4, sort_keys=True))