import requests
def ligands_from_pdbs(pdbs):
    response = requests.post('https://www.ebi.ac.uk/pdbe/api/pdb/entry/binding_sites/',data = pdbs)
    return response.json()
