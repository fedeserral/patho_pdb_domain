import requests
def ligands_from_pdbs(pdbs):
    pdb_ligand_dic={}
    pdbs=pdbs.split(" ")
    for pdb in pdbs:
        pload = pdb
        response = requests.post('https://www.ebi.ac.uk/pdbe/api/pdb/entry/binding_sites/',data = pload)
        sites= response.json()[pdb.lower()]
        ligand_list=[]
        for site in sites:
            site_id_name=site["site_id"]
            site_residues=site["site_residues"]
            site_details=site["details"].split(" ")[4]
            for ligand in site_residues:
                ligand_tuple=(site_details,site_id_name,ligand["chem_comp_id"],ligand["chain_id"],ligand["residue_number"])
                ligand_list.append(ligand_tuple)
        pdb_ligand_dic[pdb]=ligand_list
    return pdb_ligand_dic
#f='5OF4 5GPQ 5T38'
#print(ligands_from_pdbs(f))