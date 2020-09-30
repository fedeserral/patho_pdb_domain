import json
import toMolar

def moad_parse(input_file):
    """Toma la base de datos MOAD y la parsea en un JSON con jerarquias compuestos > pdb > cadena."""
    input_file=open(input_file,"r")
    input_file_lines=input_file.readlines()
    input_file.close()

    compound_dict={}

    for line in input_file_lines:
        line_split=line.split(",")

        if all(value == "" or value == "\n" for value in line_split):
            continue

        if line_split[0]!="":
            continue

        if line_split[2]!="":
            pdb=line_split[2]
            continue

        compound=line_split[3].split(":")[0]

        chain=line_split[3].split(":")[1]
        resid=line_split[3].split(":")[2]
        status=line_split[4]
        if line_split[7] !="":
            afinity=toMolar.toMolar(float(line_split[7]),line_split[8])
        else:
            afinity="None"

        if compound not in compound_dict.keys():
            compound_dict[compound]= { "pdbs": [] }
            record = { "name": pdb, "residues": []  }
            residues = {"chain": chain, "resid" : resid, "status": status, "afinity": afinity}
            
            record["residues"].append(residues)
            compound_dict[compound]["pdbs"].append(record)

        else:
            check=0
            for element in compound_dict[compound]["pdbs"]:
                if pdb == element["name"]:
                    residues = {"chain": chain, "resid" : resid, "status": status, "afinity": afinity}
                    element["residues"].append(residues)
                    check=1
            if check==0:
                residues = {"chain": chain, "resid" : resid, "status": status, "afinity": afinity}
                record = { "name": pdb, "residues": []  }
                record["residues"].append(residues)
                compound_dict[compound]["pdbs"].append(record)

    print(json.dumps(compound_dict, indent=4, sort_keys=True))
    return 0

moad_parse("moad_db.txt")

