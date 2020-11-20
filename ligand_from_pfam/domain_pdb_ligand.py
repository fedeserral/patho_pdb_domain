import request_ligand_from_PDBe
import argparse
import sys

def pfam_mapping(pfam_pdb_mapping_handle):
    lines=pfam_pdb_mapping_handle.readlines()
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
        try:
            pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
        except:
            sys.stderr.write("Warning! pfam id not in pdb_pfam_mapping: "+pfam+"\n")
            continue
        all_pdbs_of_pfams=all_pdbs_of_pfams+pdbs_of_pfam_list
    pdbs_of_pfam=[pdb[0] for pdb in all_pdbs_of_pfams]
    sys.stderr.write("Warning! Number of pdbs to request: "+str(len(pdbs_of_pfam))+"\n")
    pdbs_of_pfam=list(set(pdbs_of_pfam))
    sys.stderr.write("Warning! Number of uniques pdbs to request: "+str(len(pdbs_of_pfam))+"\n")
    PDBe_dic=(request_ligand_from_PDBe.ligands_from_pdbs(pdbs_of_pfam))

    return PDBe_dic

def pfam_pdb_ligand(pfam_entry, PDBe_dic, pfam_pdbs_dictionary):
    ligands_list=[]
    for pfam in pfam_entry:
        try:
            pdbs_of_pfam_list=pfam_pdbs_dictionary[pfam]
        except:
            continue
        for pdb in pdbs_of_pfam_list:
            pdb_pfam_id=pdb[0].lower()
            pdb_pfam_chain=pdb[1]
            pdb_pfam_position=pdb[2]
            pdb_pfam_position_inicio=int(pdb_pfam_position.split(",")[0])
            pdb_pfam_position_final=int(pdb_pfam_position.split(",")[1])

            if (pdb_pfam_id not in PDBe_dic) or (len(PDBe_dic[pdb_pfam_id])==0):
            # Si esta en el PDBe pero esta vacio, es decir no tiene informacion sobre los ligandos del pdb
                sys.stderr.write("Warning! PDB with no data in PDBe: "+pdb_pfam_id+"\n")
                pass
            
            else:
                pdb_pdbe=PDBe_dic[pdb_pfam_id]
                for residues in pdb_pdbe:
                    site_residues=residues["site_residues"]
                    author_insertion_code=residues.get("author_insertion_code","None")
                    # Si el details viene vacio. me  salteo la busqueda de ese pdb
                    if residues["details"]==None or residues["details"].split(" ")[0].lower()!="binding":
                        pass
                    else:
                        pdb_pdbe_details=residues["details"].split(" ")[4]
                        if len(residues["details"].split(" ")) == 11:
                        # Puede haber dos ligandos por detail. Cuando pasa eso Tomo los dos
                            two_inOneDetail=True
                            two_inOneDetail_data=residues["details"].split(" ")[8]
                        else:
                            two_inOneDetail=False
                            
                        for site in site_residues:
                            # Tiene letras el ligando? Las saco si las hay
                            posicion_ligando=str(site["author_residue_number"])
                            posicion_ligando=int(''.join(i for i in posicion_ligando if i.isdigit()))
                            if site["chain_id"] == pdb_pfam_chain and posicion_ligando>=pdb_pfam_position_inicio and posicion_ligando<=pdb_pfam_position_final:
                                out=[pfam,pdb_pfam_chain,str(pdb_pfam_position_inicio),str(pdb_pfam_position_final),pdb_pfam_id,pdb_pdbe_details,site["chain_id"],str(posicion_ligando),author_insertion_code]
                                out=" ".join(out)
                                sys.stderr.write(out+"\n")
                                ligands_list.append(pdb_pdbe_details)
                                if two_inOneDetail:
                                    out=[pfam,pdb_pfam_chain,str(pdb_pfam_position_inicio),str(pdb_pfam_position_final),pdb_pfam_id,two_inOneDetail_data,site["chain_id"],str(posicion_ligando),author_insertion_code]
                                    out=" ".join(out)
                                    sys.stderr.write(out+"\n")
                                    ligands_list.append(two_inOneDetail_data)

    ligands_list=list(set(ligands_list))
    
    
    return ligands_list

def pfam_entry_handly(file):
    input=open(file,"r")
    lines=input.readlines()
    output=[]
    for line in lines:
        line=line.rstrip()
        if line[0]!="#":
            output.append(line)
    return output

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument("-f", '--pdb_pfam_mapping', default='pdb_pfam_mapping.txt', help="")
    parser.add_argument('-i','--pfam_input', default='pfam_entry.txt', help="")

    return parser

def domain_pdb_ligand(pfams, pfam_pdb_mapping_handle):
    pfam_pdbs_dictionary=pfam_mapping(pfam_pdb_mapping_handle)
    PDBe_dic=request(pfams,pfam_pdbs_dictionary)
    return pfam_pdb_ligand(pfams, PDBe_dic, pfam_pdbs_dictionary) 
    

def main():
    parser=parse_arguments()
    args=parser.parse_args()
    pfams=pfam_entry_handly(args.pfam_input)
    with open(args.pdb_pfam_mapping) as pdb_pfam_handle:
        ligands = domain_pdb_ligand(pfams, pdb_pfam_handle)
    print("\n".join(ligands))           
    
    
if __name__=='__main__':
    main()
