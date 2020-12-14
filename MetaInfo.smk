import os

microscopy = []
nmr = []
x_ray = []

for line in open("pdb_info.txt"):
    toks = line.split()
    pdb = toks[0]
    method = toks[1]
    if method == 'MICROSCOPY':
        microscopy.append(pdb)
    if method == 'NMR':
        nmr.append(pdb)
    if method == 'X-RAY':
        x_ray.append(pdb)

pdb_files = microscopy + nmr + x_ray