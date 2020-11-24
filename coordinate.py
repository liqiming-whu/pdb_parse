#!/usr/bin/env python3
from collections import namedtuple


ATOM = namedtuple('ATOM', 'index name coordinate element')


class BASE:
    def __init__(self, name=None):
        self.name = name
        self.atom_list = []

    def __repr__(self):
        return self.name

    __str__ = __repr__

    def __iter__(self):
        return iter(self.atom_list)

    def __len__(self):
        return len(self.atom_list)

    def __getitem__(self, index):
        return self.atom_list[index]

    def add_atom(self, atom):
        self.atom_list.append(atom)
        return self.atom_list

    def add_atom_list(self, atom_list):
        self.atom_list += atom_list
        return self.atom_list

    def coordinate_list(self):
        return [atom.coordinate for atom in self.atom_list]

    @staticmethod
    def atom_type(atom):
        if atom.name.startswith('O'):
            return "Oxygen_atom"
        if atom.name == 'P':
            return "Phosphoric_atom"
        if atom.name in ("C1'", "C2'", "C3'", "C4'", "C5'"):
            return "Ribose_skeleton"
        else:
            return "Other"

    def ribose_skeleton_coordinate_list(self):
        return [atom.coordinate for atom in self.atom_list if BASE.atom_type(atom) == 'Ribose_skeleton']

    def base_skeleton_coordinate_list(self):
        index_list = []
        coordinate_list = []
        for atom in self.atom_list:
            if BASE.atom_type(atom) == 'Other':
                name = atom.name
                index = name[1]
                if not (index in index_list):
                    index_list.append(index)
                    coordinate_list.append(atom.coordinate)
        if len(index_list) != len(set(index_list)):
            raise Exception("Base skeleton error.")
        return coordinate_list


class RNA:
    def __init__(self, name):
        self.name = name
        self.base_list = []

    def __repr__(self):
        return "RNA_{}".format(self.name)

    __str__ = __repr__

    def __iter__(self):
        return iter(self.base_list)

    def __len__(self):
        return len(self.base_list)

    def __getitem__(self, index):
        return self.base_list[index][0]

    def add_base(self, base, index, stas):
        self.base_list.append((base, index, stas))

    def add_base_list(self, base_list_with_index):
        self.base_list += base_list_with_index

    def sort(self, key=lambda x: x[1], reverse=False):
        self.base_list.sort(key=key, reverse=reverse)

    @property
    def sequence(self):
        self.sort()
        return "".join(base.name for base, _, _ in self.base_list)
