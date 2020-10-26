import request_ligand_from_PDBe
import json
import argparse
import sys

def pfam_mapping(file):
    file=open(file)
    lines=file.readlines()
    pfam_pdbs_dictionary={}
    for line in lines[1:]:
        line=line.split("\t")
        pdb=line[0]
        chain=line[1]
        # Saco las letras si es que las hay en la posicion
        position=''.join(i for i in line[2] if i.isdigit())+","+''.join(i for i in line[3] if i.isdigit())
        pfam=line[4].split(".")[0]
        if pfam not in pfam_pdbs_dictionary.keys():
            pfam_pdbs_dictionary[pfam]=[(pdb,chain,position)]
        else:
            list_aux=pfam_pdbs_dictionary[pfam]
            list_aux.append((pdb,chain,position))
            pfam_pdbs_dictionary[pfam]=list_aux

    return pfam_pdbs_dictionary

def request(pfam_entry, pfam_pdbs_dictionary):
    all_pdbs_of_pfams=[]
    for pfam in pfam_entry:
        pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
        all_pdbs_of_pfams=all_pdbs_of_pfams+pdbs_of_pfam_list
    pdbs_of_pfam=[pdb[0] for pdb in all_pdbs_of_pfams]
    sys.stderr.write("Warning! Number of pdbs to request: "+str(len(pdbs_of_pfam))+"\n")
    pdbs_of_pfam=list(set(pdbs_of_pfam))
    sys.stderr.write("Warning! Number of uniques pdbs to request: "+str(len(pdbs_of_pfam))+"\n")
    pdbs_of_pfam=",".join(pdbs_of_pfam).lower()
    PDBe_dic=(request_ligand_from_PDBe.ligands_from_pdbs(pdbs_of_pfam))

    return PDBe_dic

def pfam_pdb_ligand(pfam_entry, PDBe_dic, pfam_pdbs_dictionary):
    for pfam in pfam_entry:
        pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
        for pdb in pdbs_of_pfam_list:
            pdb_pfam_id=pdb[0].lower()
            pdb_pfam_chain=pdb[1]
            pdb_pfam_position=pdb[2]
            pdb_pfam_position_inicio=int(pdb_pfam_position.split(",")[0])
            pdb_pfam_position_final=int(pdb_pfam_position.split(",")[1])
            try:
                if len(PDBe_dic[pdb_pfam_id])==0:
                # Si esta en el PDBe pero esta vacio, es decir no tiene informacion sobre los ligandos del pdb
                    sys.stderr.write("Warning! PDB with no data in PDBe: "+pdb_pfam_id+"\n")
                    continue
                else:
                    pdb_pdbe=PDBe_dic[pdb_pfam_id][0]

                pdb_pdbe_residues=pdb_pdbe["site_residues"]
                pdb_pdbe_details=pdb_pdbe["details"].split(" ")[4]
                if pdb_pdbe_details == "":
                # El nombre del ligando esta corrido un lugar
                    pdb_pdbe_details=pdb_pdbe["details"].split(" ")[5]
                for ligand in pdb_pdbe_residues:
                    # Tiene letras el ligando? Las saco si las hay
                    posicion_ligando=str(ligand["author_residue_number"])
                    posicion_ligando=int(''.join(i for i in posicion_ligando if i.isdigit()))
                    if ligand["chain_id"] == pdb_pfam_chain and posicion_ligando>=pdb_pfam_position_inicio and posicion_ligando<=pdb_pfam_position_final:
                        print(pfam,pdb_pfam_chain,pdb_pfam_position_inicio,pdb_pfam_position_final,pdb_pfam_id,pdb_pdbe_details,ligand["chain_id"],posicion_ligando)
            except:
            #Si no esta ese pdb en el dicionario de PDBe
                sys.stderr.write("Warning! PDB is not in PDBe: "+pdb_pfam_id+"\n")
                continue

    return 0

def pfam_entry_handly(file):
    input=open(file,"r")
    line=input.readlines()[0]

    return line.rstrip().split(" ")

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", '--pdb_pfam_mapping', default='pdb_pfam_mapping.txt', help="")
    parser.add_argument('-i','--pfam_input', default='pfam_entry.txt', help="")

    return parser

def main():
    parser=parse_arguments()
    args=parser.parse_args()
    pfams=pfam_entry_handly(args.pfam_input)
    pfam_pdbs_dictionary=pfam_mapping(args.pdb_pfam_mapping)
    PDBe_dic=request(pfams,pfam_pdbs_dictionary)
    pfam_pdb_ligand(pfams, PDBe_dic, pfam_pdbs_dictionary)

    return 0

if __name__=='__main__':
    main()