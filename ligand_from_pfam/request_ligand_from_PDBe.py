import requests
import json

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