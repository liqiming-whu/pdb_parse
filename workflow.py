#!/usr/bin/env python3
import os
from parse_pdb import pdbfile
from function import build_rna_list
from rcsb import get_info, get_pdb_file
from itertools import combinations
from calculate import calculate_internal, calculate

pdb_idlist = open("pdb_idlist.txt").read().split()


def get_method(pdb_id):
    method = get_info(pdb_id)['PDBdescription']['PDB']['@expMethod']
    key = method.split()[0]
    if key == 'SOLUTION':
        return "NMR"
    if key == 'ELECTRON':
        return "MICROSCOPY"
    if key == 'X-RAY':
        return 'X-RAY'


for pdb_id in pdb_idlist:
    if not os.path.exists("pdb_file"):
        os.mkdir("pdb_file")
    method = get_method(pdb_id)
    if not os.path.exists("pdb_file/"+method):
        os.mkdir("pdb_file/"+method)
    if not os.path.exists("pdb_file/"+method+"/"+pdb_id+".pdb"):
        with open("pdb_file/"+method+"/"+pdb_id+".pdb", "w") as f:
            f.write(get_pdb_file(pdb_id))
    if not os.path.exists("results"):
        os.mkdir("results")

    rna_list = build_rna_list(pdbfile("pdb_file/"+method+"/"+pdb_id+".pdb"))

    if rna_list:
        if not os.path.exists("results/"+pdb_id):
            os.mkdir("results/"+pdb_id)
        with open("results/"+pdb_id+"/descript.txt", "w", encoding="utf-8") as f:
            for rna in rna_list:
                print(pdb_id, rna, rna.sequence, file=f)
                calculate_internal(rna, "results/"+pdb_id+"/")
        if len(rna_list) > 1:
            for rna1, rna2 in combinations(rna_list, 2):
                calculate(rna1, rna2, "results/"+pdb_id+"/")
