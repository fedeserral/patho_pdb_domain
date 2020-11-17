import requests
import json

def pdb_ligand_data(ligands):
   #
   r = requests.post("https://www.ebi.ac.uk/pdbe/api/pdb/compound/summary/",data=",".join(ligands))
   if r.ok:
       data =  r.json()  
       new_data = []
       for k,v in data.items():
           r = v[0]            
           r2 = {"smiles":r["smiles"][0]["name"],"pdb_ligand":k}
           if "chembl_id" in r:
               r2["chembl_id"] = r["chembl_id"]            
           new_data.append(r2)
       
       return new_data
   raise Exception(r.text)

def search_chembl(chembl_id):
   r = requests.get(f"https://www.ebi.ac.uk/unichem/rest/src_compound_id_all/{chembl_id}/1")
   if r.ok:
       data =  r.json()
       for x in data:
           x["src_name"] = sources[x["src_id"]]
       return data
   raise Exception(r.text)

def pdb_ligand_data_batch(ligands,n=400):    
   ligs_chunks = [ligs[i:i + n] for i in range(0, len(ligs), n)]
   all_pdb_ligands = reduce(list.__add__, [pdb_ligand_data( chunk ) for chunk in tqdm(ligs_chunks)])    
   return all_pdb_ligands

def ligands_from_pdbs(pdbs):
    pdbs_count=len(pdbs)
    response_total={}
    pdbs_per_request=800
    for pdb_index in range(0,pdbs_count,pdbs_per_request):
        final=pdb_index+pdbs_per_request
        if final>pdbs_count:
            final=pdbs_count
        pdb_to_request=pdbs[pdb_index:final]
        pdb_to_request=",".join(pdb_to_request).lower()
        response = requests.post('https://www.ebi.ac.uk/pdbe/api/pdb/entry/binding_sites/',data = pdb_to_request)
        response_total.update(response.json())
    return response_total
