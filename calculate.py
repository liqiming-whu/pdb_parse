#!/usr/bin/env python3
import sys
import csv
from itertools import combinations
from parse_pdb import pdbfile
from function import coordinate_mean, coordinate_distance, shortest_distance, build_rna_list


def calculate_internal(rna, path=""):
    csvfile = open(path+str(rna)+".tsv", "w", newline="", encoding="utf-8")
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow(("index1", "base1", "index2", "base2", "ribose_d", "base_d", "shortest_d"))
    for base1_info, base2_info in combinations(rna.base_list, 2):
        if base1_info[2] and base2_info[2]:
            try:
                base1_ribo = coordinate_mean(base1_info[0].ribose_skeleton_coordinate_list())
            except Exception:
                print(base1_info[0].atom_list)
            try:
                base2_ribo = coordinate_mean(base2_info[0].ribose_skeleton_coordinate_list())
            except Exception:
                print(base2_info[0].atom_list)
            ribose_d = coordinate_distance(base1_ribo, base2_ribo)
            base1_base = coordinate_mean(base1_info[0].base_skeleton_coordinate_list())
            base2_base = coordinate_mean(base2_info[0].base_skeleton_coordinate_list())
            base_d = coordinate_distance(base1_base, base2_base)
            shortest_d = shortest_distance(base1_info[0].coordinate_list(), base2_info[0].coordinate_list())
            writer.writerow((base1_info[1], base1_info[0].name, base2_info[1], base2_info[0].name, ribose_d, base_d, shortest_d))
        else:
            writer.writerow((base1_info[1], base1_info[0].name, base2_info[1], base2_info[0].name, "NA", "NA", "NA"))


def calculate(rna1, rna2, path=""):
    csvfile = open(path+str(rna1)+"__"+str(rna2)+".tsv", "w", newline="", encoding="utf-8")
    writer = csv.writer(csvfile, delimiter='\t')
    writer.writerow((str(rna1)+"_index", str(rna1), str(rna2)+"_index", str(rna2), "ribose_d", "base_d", "shortest_d"))
    for base1_info in rna1:
        for base2_info in rna2:
            if base1_info[2] and base2_info[2]:
                base1_ribo = coordinate_mean(base1_info[0].ribose_skeleton_coordinate_list())
                base2_ribo = coordinate_mean(base2_info[0].ribose_skeleton_coordinate_list())
                ribose_d = coordinate_distance(base1_ribo, base2_ribo)
                base1_base = coordinate_mean(base1_info[0].base_skeleton_coordinate_list())
                base2_base = coordinate_mean(base2_info[0].base_skeleton_coordinate_list())
                base_d = coordinate_distance(base1_base, base2_base)
                shortest_d = shortest_distance(base1_info[0].coordinate_list(), base2_info[0].coordinate_list())
                writer.writerow((base1_info[1], base1_info[0].name, base2_info[1], base2_info[0].name, ribose_d, base_d, shortest_d))
            else:
                writer.writerow((base1_info[1], base1_info[0].name, base2_info[1], base2_info[0].name, "NA", "NA", "NA"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
        pdb = pdbfile(path)
        rna_list = build_rna_list(pdb)
        for rna in rna_list:
            calculate_internal(rna)
            print(rna, "length:", len(rna), rna.sequence)
        RNA_V = rna_list[0]
        RNA_W = rna_list[1]
        RNA_U = rna_list[2]
        calculate(RNA_V, RNA_W)
        calculate(RNA_V, RNA_U)
        calculate(RNA_W, RNA_U)
