# import requests module 
import requests   
# Making a get request 
#https://www.ebi.ac.uk/pdbe/api/doc/pdb.html
#GET : https://www.ebi.ac.uk/pdbe/api/pdb/entry/ligand_monomers/6H8J
response = requests.get('https://api.github.com')   
# print response 
print(response)   
# print json content 
print(response.json()) 
#POST
pload = '1cbs,1bgj'
r = requests.post('https://www.ebi.ac.uk/pdbe/api/pdb/entry/ligand_monomers/',data = pload)
print(r.json())

