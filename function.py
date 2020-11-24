#!/usr/bin/env python3
import math
import sys
from coordinate import BASE, RNA, ATOM
from parse_pdb import pdbfile


def coordinate_mean(coordinate_list):
    length = len(coordinate_list)
    x_list = []
    y_list = []
    z_list = []
    for (x, y, z) in coordinate_list:
        x_list.append(x)
        y_list.append(y)
        z_list.append(z)
    return (sum(x_list)/length, sum(y_list)/length, sum(z_list)/length)


def coordinate_distance(x, y):
    x1, x2, x3 = x
    y1, y2, y3 = y

    return math.sqrt((x1-y1)**2+(x2-y2)**2+(x3-y3)**2)


def shortest_distance(c_list1, c_list2):
    shortest = float("inf")
    for x in c_list1:
        for y in c_list2:
            distance = coordinate_distance(x, y)
            if distance < shortest:
                shortest = distance
    return shortest


def build_rna_list(pdb_obj):
    rna_list = []
    missing_atoms = pdb_obj.missing_index
    for chain, rna_info in pdb_obj:
        rna = RNA(name=chain)
        base_index_list = []
        for info in rna_info:
            atom = ATOM(
                index=info[0],
                name=info[1],
                coordinate=(info[5], info[6], info[7]),
                element=info[8])
            if not base_index_list:
                base = BASE(name=info[2])
                base_index_list.append(info[4])
            elif info[4] != base_index_list[-1]:
                if (chain, base_index_list[-1]) in missing_atoms:
                    rna.add_base(base, base_index_list[-1], False)
                else:
                    rna.add_base(base, base_index_list[-1], True)
                base = BASE(name=info[2])
                base_index_list.append(info[4])
            base.add_atom(atom)
        if (chain, base_index_list[-1]) in missing_atoms:
            rna.add_base(base, base_index_list[-1], False)
        else:
            rna.add_base(base, base_index_list[-1], True)
        rna = add_missing(rna, chain, pdb_obj)
        rna_list.append(rna)
    return rna_list


def add_missing(rna, chain, pdb):
    missing_bases = pdb.get_miss(chain)
    if missing_bases:
        for miss in pdb.get_miss(chain):
            base = BASE(name=miss[0])
            rna.add_base(base, miss[1], False)
        rna.sort()
    return rna


if __name__ == "__main__":
    coordinate_list = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    print(coordinate_mean(coordinate_list))
    x = (1, 2, 3)
    y = (4, 5, 6)
    print(coordinate_distance(x, y))
    c_list1 = [(1, 2, 3), (3, 4, 5)]
    c_list2 = [(7, 8, 9), (10, 11, 12)]
    print(shortest_distance(c_list1, c_list2))

    if len(sys.argv) > 1:
        path = sys.argv[1]
        pdb = pdbfile(path)
        rna_list = build_rna_list(pdb)
        for rna in rna_list:
            print(rna, "length:", len(rna), rna.sequence)
