import request_ligand_from_PDBe
import json

# Parseo el archivo de pdb_pfam_mapping.txt" en un diccionario, key:pfam, valor los pdb y sus posiciones

entrada=open("pdb_pfam_mapping.txt")
lines=entrada.readlines()
pfam_pdbs_dictionary={}
for line in lines[1:]:
    line=line.split("\t")
    pdb=line[0]
    chain=line[1]
    position=line[2]+","+line[3]
    pfam=line[4].split(".")[0]
    if pfam not in pfam_pdbs_dictionary.keys():
        pfam_pdbs_dictionary[pfam]=[(pdb,chain,position)]
    else:
        list_aux=pfam_pdbs_dictionary[pfam]
        list_aux.append((pdb,chain,position))
        pfam_pdbs_dictionary[pfam]=list_aux

#pfam_entry=['PF16203','PF04851','PF06777']
pfam_entry=list(pfam_pdbs_dictionary.keys())[10:15]

all_pdbs_of_pfams=[]
for pfam in pfam_entry:
    pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
    all_pdbs_of_pfams=all_pdbs_of_pfams+pdbs_of_pfam_list

pdbs_of_pfam=[pdb[0] for pdb in all_pdbs_of_pfams]
print(len(pdbs_of_pfam))
pdbs_of_pfam=list(set(pdbs_of_pfam))
print(len(pdbs_of_pfam))

pdbs_of_pfam=",".join(pdbs_of_pfam).lower()

#Pedir por pedasos de pdbs, cada 500
#Hacerlo
PDBe_dic=(request_ligand_from_PDBe.ligands_from_pdbs(pdbs_of_pfam))

for pfam in pfam_entry:
    pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
    for pdb in pdbs_of_pfam_list:
        pdb_pfam_id=pdb[0].lower()
        pdb_pfam_chain=pdb[1]
        pdb_pfam_position=pdb[2]
        try:
            pdb_pfam_position_inicio=int(pdb_pfam_position.split(",")[0])
            pdb_pfam_position_final=int(pdb_pfam_position.split(",")[1])
        except:
            #Valores extraños dentro de la posicion
            continue

        try:
            if len(PDBe_dic[pdb_pfam_id])==0:
                # Si esta en el PDBe pero esta vacio, es decir no tiene infomracion sobre los ligandos del pdbi
                continue
            else:
                pdb_pdbe=PDBe_dic[pdb_pfam_id][0]

            pdb_pdbe_residues=pdb_pdbe["site_residues"]
            pdb_pdbe_details=pdb_pdbe["details"].split(" ")[4]
            if pdb_pdbe_details == "":
                # El nombre del ligando esta corrido un lugar
                pdb_pdbe_details=pdb_pdbe["details"].split(" ")[5]

            for ligand in pdb_pdbe_residues:
                posicion_ligando=int(ligand["residue_number"])
                if ligand["chain_id"] == pdb_pfam_chain and posicion_ligando>=pdb_pfam_position_inicio and posicion_ligando<=pdb_pfam_position_final:
                    print(pfam,pdb_pfam_chain,pdb_pfam_position_inicio,pdb_pfam_position_final,pdb_pfam_id,pdb_pdbe_details,ligand["chain_id"],posicion_ligando)
        except:
            #Si no esta ese pdb en el dicionario de PDBe
            continue