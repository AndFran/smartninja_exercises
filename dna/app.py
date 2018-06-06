hair = {"CCAGCAATCGC": 'black',
        "GCCAGTGCCG": 'brown',
        'TTAGCTATCGC': 'blonde'
        }

face = {"GCCACGG": "Square",
        "ACCACAA": "Round",
        "AGGCCTCA": "Oval"
        }

eyes = {
    "TTGTGGTGGC": "Blue",
    "GGGAGGTGGC": "Green",
    "AAGTAGTGAC": "Brown"
}

gender = {
    "TGAAGGACCTTC": "Female",
    "TGCAGGAACTTC": "Male"
}

race = {
    "AAAACCTCA": "White",
    "CGACTACAG": "Black",
    "CGCGGGCCG": "Asian"
}

sequence = ""

with open('dna.txt', 'r') as f:
    sequence = f.read()

characteristics = [hair, face, eyes, gender, race]
profile = []

for chara in characteristics:
    for attribute in chara.keys():
        if sequence.find(attribute) > 0:
            profile.append(chara[attribute])

print profile
