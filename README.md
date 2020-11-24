# pdb_parse

    Get rna from wwPDB file.

## usage:
    
    ./workflow.py

    workflow:
        summary.ipynb

    from parse_pdb import pdbfile
    pdb = pdbfile(path)
    rna_info_list = pdb.rnainfo_list # get coordinates
    missing_bases = pdb.missing_bases # get missing residues
    missing_atoms = pdb.missing_atoms # get missing atoms
    from function import build_rna_list
    rna_list = build_rna_list(pdb) # get rna
    for rna in rna_list:
        print(rna.sequence) # get sequence
        base = rna[index]
        print(base, base.coordinate_list()) # get base, atom coordinates([] for missing residues)