include: "MetaInfo.smk"

import os

rule all:
    input:
        expand(os.path.join("structure", "{pdb_file}.log"), pdb_file=pdb_files),
        expand(os.path.join("struc2tsv", "{pdb_file}.tsv"), pdb_file=pdb_files),
        expand(os.path.join("plot", "{pdb_file}.pdf"), pdb_file=pdb_files)


def struc_input(wildcards):
    if wildcards.pdb_file in microscopy:
        return [os.path.join("pdb_file", "MICROSCOPY", "{pdb_file}.pdb")]
    if wildcards.pdb_file in nmr:
        return [os.path.join("pdb_file", "NMR", "{pdb_file}.pdb")]
    if wildcards.pdb_file in x_ray:
        return [os.path.join("pdb_file", "X-RAY", "{pdb_file}.pdb")]

rule structure:
    input:
        struc_input
    output:
        os.path.join("structure", "{pdb_file}.log")
    shell:"""
    rnaview {input} > {output}
    """

def tsv_input(wildcards):
    if wildcards.pdb_file in microscopy:
        return [os.path.join("pdb_file", "MICROSCOPY", "{pdb_file}.pdb.out")]
    if wildcards.pdb_file in nmr:
        if os.path.exists(os.path.join("pdb_file", "NMR", f"{wildcards.pdb_file}.pdb_nmr.pdb.out")):
            return [os.path.join("pdb_file", "NMR", "{pdb_file}.pdb_nmr.pdb.out")]
        else:
            return [os.path.join("pdb_file", "NMR", "{pdb_file}.pdb.out")]
    if wildcards.pdb_file in x_ray:
        return [os.path.join("pdb_file", "X-RAY", "{pdb_file}.pdb.out")]

rule struc2tsv:
    input:
        tsv_input
    output:
        os.path.join("struc2tsv", "{pdb_file}.tsv"),
        os.path.join("struc2tsv", "{pdb_file}_num.txt"),
    shell:"""
    ./structure_tsv.py {input} {output}
    """

rule plot:
    input:
        os.path.join("struc2tsv", "{pdb_file}.tsv"),
        os.path.join("struc2tsv", "{pdb_file}_num.txt"),
    output:
        os.path.join("plot", "{pdb_file}.pdf"),
    shell:"""
    ./plot.R {input} {output}
    """