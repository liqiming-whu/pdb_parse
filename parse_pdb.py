#!/usr/bin/env python3
import sys
from collections import defaultdict


class pdbfile:
    def __init__(self, path):
        self.path = path
        self.rnainfo_list = self.parse()
        self.chain_list = self.chain()
        self.missing_bases = self.missing()
        self.missing_atoms, self.missing_index = self.missing_atom()
        print("Parsing {}".format(self.path))
        if self.chain_list:
            print("Chain list:", " ".join(self.chain_list))
        if self.missing_index:
            print("Missing atoms", self.missing_index)

    def __repr__(self):
        return "rna sequence from {}".format(self.path)

    __str__ = __repr__

    def __iter__(self):
        return iter(self.rnainfo_list)

    def __getitem__(self, index):
        return self.rnainfo_list[index]

    def count(self):
        return len(self.rnainfo_list)

    def get_miss(self, chain):
        for i, miss in self.missing_bases:
            if i == chain:
                return miss

    def parse(self):
        rnainfo = []
        rnainfo_list = []
        with open(self.path) as f:
            for line in f:
                line = line.strip()
                if line[:4] == 'ATOM' and len(line) == 78:
                    residu = line[16:20].strip()
                    if len(residu) == 1 and residu in ('A', 'U', 'G', 'C'):
                        atom_index = int(line[4:11])
                        atom = line[11:16].strip()
                        base = residu
                        chain = line[20:22].strip()
                        base_index = int(line[22:26])
                        x = float(line[30:38])
                        y = float(line[38:46])
                        z = float(line[46:54])
                        element = line[-1]
                        if rnainfo and rnainfo[-1][3] != chain:
                            rnainfo_list.append((rnainfo[-1][3], rnainfo))
                            rnainfo = []
                        rnainfo.append((atom_index, atom, base, chain, base_index, x, y, z, element))
        if rnainfo:
            rnainfo_list.append((rnainfo[-1][3], rnainfo))
        merge_info = defaultdict(list)
        for chain, rna in rnainfo_list:
            merge_info[chain] += rna
        rnainfo_list = [(chain, rna) for chain, rna in merge_info.items()]
        return rnainfo_list

    def chain(self):
        return [chain for chain, _ in self.rnainfo_list]

    def missing(self):
        missing = []
        missing_list = []
        with open(self.path) as f:
            for line in f:
                line = line.strip()
                if line[:6] == 'REMARK' and line[7:10] == '465' and len(line) == 26:
                    chain = line[18:20].strip()
                    if chain in self.chain_list:
                        base = line[17:18]
                        base_index = int(line[20:])

                        if missing and missing[-1][2] != chain:
                            missing_list.append((missing[-1][2], missing))
                            missing = []
                        missing.append((base, base_index, chain))
        if missing:
            missing_list.append((missing[-1][2], missing))

        return missing_list

    def missing_atom(self):
        missing = []
        missing_list = []
        with open(self.path) as f:
            for line in f:
                line = line.strip()
                if line[:6] == 'REMARK' and line[7:10] == '470' and len(line) > 30:
                    try:
                        base_index = int(line[20:24])
                    except ValueError:
                        continue
                    chain = line[18:20].strip()
                    if chain in self.chain_list:
                        base = line[17:18]
                        atoms = line[26:].split()
                        if missing and missing[-1][2] != chain:
                            missing_list.append((missing[-1][2], missing))
                            missing = []
                        missing.append((base, base_index, chain, atoms))
        if missing:
            missing_list.append((missing[-1][2], missing))

        index_list = []
        for miss in missing_list:
            for index in miss[1]:
                index_list.append((index[2], index[1]))
        index_list = list(set(index_list))
        return missing_list, index_list

    def to_file(self):
        for chain, rna_info in self.rnainfo_list:
            with open("rna_info_"+chain+".txt", "w", encoding="utf-8") as f:
                for line in rna_info:
                    f.write(" ".join(map(str, line))+"\n")
        for chain, missing in self.missing_bases:
            with open("missing_"+chain+".txt", "w", encoding="utf-8") as f:
                for line in missing:
                    f.write(" ".join(map(str, line))+"\n")


if __name__ == "__main__":
    path = sys.argv[1]
    pdbfile(path).to_file()
