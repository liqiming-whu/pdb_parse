#!/usr/bin/env python3
import sys


def run(struc_file, outfile, numfile):
    out = open(outfile, "w")
    out.write("plot_x\tplot_y\n")
    numf = open(numfile, "w")
    flag = False
    for line in open(struc_file):
        if line.startswith("BEGIN_base-pair"):
            flag = True
        if line.startswith("END_base-pair"):
            flag = False
        if not line.startswith("BEGIN_base-pair") and flag:
            fileds = line[0:9].strip().split('_')
            base_L = int(fileds[0])
            base_R = int(fileds[1])
            out.write(f"{base_L-1}\t{base_R-1}\n")
        if line.startswith("  The total base pairs"):
            base_num = int(line[35:39])
            numf.write(f"{base_num}\n")
    out.close()
    numf.close()


if __name__ == "__main__":
    run(*sys.argv[1:])

            