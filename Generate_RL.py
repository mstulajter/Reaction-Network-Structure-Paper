#!/usr/bin/env python3
import networkx as nx
import bz2
import argparse
import random
import copy

# Generate a lattice network 
#
# Authors:
#           Miko Stulajter
#
# Version 1.0.0
#

def argParsing():
    parser = argparse.ArgumentParser(description='Generate a lattice network.')
    
    parser.add_argument('-l1',
    help="Length of side (used for all dimensions).",
    dest='l1',
    type=int,
    required=True)

    parser.add_argument('-d',
    help="Number of dimensions (up to 4 for bc=2 or rP>0).",
    dest='d',
    type=int,
    required=True)

    parser.add_argument('-bc',
    help="Boundary condition type either '1: periodic' or '2: non-periodic' (Default : 1).",
    dest='bc',
    type=check_bc,
    default=1,
    required=False)

    parser.add_argument('-rp',
    help="Rewiring probability (Default : 0).",
    dest='rp',
    type=float,
    default=0,
    required=False)

    parser.add_argument('-ofile',
    help="Output file name with no extension as it will be saved as a '.graphml.bz2' file.",
    dest='ofile',
    type=str,
    required=False)

    return parser.parse_args()


def check_bc(i_v):
    i_v = int(i_v)
    if i_v not in [1, 2]:
        raise argparse.ArgumentTypeError(f"Invalid choice: {i_v}. Choose either 1 or 2.")
    return i_v


def main():
    ### ~~~~~~ Argument parsing
    args = argParsing()

    ### ~~~~~~ Generate network if non-periodic and rewiring probability is zero
    if args.bc == 1 and args.rp == 0:
        d_list=(args.l1,) * args.d
        G = nx.grid_graph(dim=d_list)

        ### ~~~~~~ Output network
        if (args.ofile):
            filename=args.ofile+'.graphml.bz2'
        else:
            filename="RL-NP_L"+str(args.l1)+"_d-"+str(args.d)+'.graphml.bz2'
        with bz2.open(filename, 'wb') as f:
            nx.write_graphml(G, f)

    ### ~~~~~~ Generate network if non-periodic and rewiring probability is nonzero
    elif args.bc == 1 and args.rp != 0:
        filename="RL-NP_R-"+str(args.rp)+"_L"+str(args.l1)+"_d-"+str(args.d)+'.graphml.bz2'
        if args.d == 1:
            generate_1D_NP_RP(filename,args.l1,args.rp)
        elif  args.d == 2:
            generate_2D_NP_RP(filename,args.l1,args.rp)
        elif  args.d == 3:
            generate_3D_NP_RP(filename,args.l1,args.rp)
        elif  args.d == 4:
            generate_4D_NP_RP(filename,args.l1,args.rp)
        else:
            print("Not a valid dimension for non-periodic boundary conditions with a rewiring probability. Only a value of 1,2,3, and 4 are valid.")

    ### ~~~~~~ Generate network if periodic and rewiring probability is zero
    elif args.bc == 2 and args.rp == 0:
        filename="RL-P_L"+str(args.l1)+"_d-"+str(args.d)+'.graphml.bz2'
        if args.d == 1:
            generate_1D_P(filename,args.l1)
        elif  args.d == 2:
            generate_2D_P(filename,args.l1)
        elif  args.d == 3:
            generate_3D_P(filename,args.l1)
        elif  args.d == 4:
            generate_4D_P(filename,args.l1)
        else:
            print("Not a valid dimension for periodic boundary conditions. Only a value of 1,2,3, and 4 are valid.")

    ### ~~~~~~ Generate network if periodic and rewiring probability is nonzero
    else:
        filename="RL-P_R-"+str(args.rp)+"_L"+str(args.l1)+"_d-"+str(args.d)+'.graphml.bz2'
        if args.d == 1:
            generate_1D_P_RP(filename,args.l1,args.rp)
        elif  args.d == 2:
            generate_2D_P_RP(filename,args.l1,args.rp)
        elif  args.d == 3:
            generate_3D_P_RP(filename,args.l1,args.rp)
        elif  args.d == 4:
            generate_4D_P_RP(filename,args.l1,args.rp)
        else:
            print("Not a valid dimension for periodic boundary conditions with a rewiring probability. Only a value of 1,2,3, and 4 are valid.")


def generate_1D_P(filename,N):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        for i in range(0,N):
            f.write('    <node id="(%d)" />\n' % (i))

        for i in range(0,N):
            if i==Nm1:
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (i,0))
            else:
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (i,i+1))     

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_2D_P(filename,N):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        for i in range(0,N):
            for j in range(0,N):
                f.write('    <node id="(%d, %d)" />\n' % (i,j))

        for i in range(0,N):
            for j in range(0,N):
                if i==Nm1 and j==Nm1:
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i,0))
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,0,j))
                elif i==Nm1:
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i,j+1))
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,0,j))
                elif j==Nm1:
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i,0))
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i+1,j))
                else:
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i,j+1))
                    f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (i,j,i+1,j))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_3D_P(filename,N):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    f.write('    <node id="(%d, %d, %d)" />\n' % (i,j,k))

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    if i==Nm1 and j==Nm1 and k==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,0))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,0,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,0,j,k))
                    elif i==Nm1 and k==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,0))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j+1,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,0,j,k))
                    elif k==Nm1 and j==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,0))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,0,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i+1,j,k))
                    elif i==Nm1 and j==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,k+1))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,0,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,0,j,k))
                    elif i==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,k+1))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j+1,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,0,j,k))
                    elif j==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,k+1))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,0,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i+1,j,k))
                    elif k==Nm1:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,0))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j+1,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i+1,j,k))
                    else:
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j,k+1))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i,j+1,k))
                        f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (i,j,k,i+1,j,k))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_4D_P(filename,N):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        f.write('    <node id="(%d, %d, %d, %d)" />\n' % (i,j,k,m))

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        if i==Nm1 and j==Nm1 and k==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif i==Nm1 and j==Nm1 and k==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif i==Nm1 and j==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif i==Nm1 and k==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif j==Nm1 and k==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif i==Nm1 and j==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif i==Nm1 and k==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif i==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif j==Nm1 and k==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif j==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif k==Nm1 and m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif i==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,0,j,k,m))
                        elif j==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,0,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif k==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,0,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        elif m==Nm1:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,0))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))
                        else:
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k,m+1))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j,k+1,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i,j+1,k,m))
                            f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (i,j,k,m,i+1,j,k,m))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_1D_NP_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            nodes.append([i])
            f.write('    <node id="(%d)" />\n' % (i))

        for i in range(0,N):
            if i==Nm1:
                continue
            else:
                edges.append([i,i+1])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:1]
            tar=ed[1:2]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],tar[0]]
                o2=[tar[0],src[0]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],tar[0]]
                    o2=[tar[0],src[0]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],tar[0]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (src[0],tar[0]))
            else:
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (src[0],tar[0]))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_2D_NP_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                nodes.append([i,j])
                f.write('    <node id="(%d, %d)" />\n' % (i,j))

        for i in range(0,N):
            for j in range(0,N):
                if i==Nm1 and j==Nm1:
                    continue
                elif i==Nm1:
                    edges.append([i,j,i,j+1])
                elif j==Nm1:
                    edges.append([i,j,i+1,j])

                else:
                    edges.append([i,j,i,j+1])
                    edges.append([i,j,i+1,j])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:2]
            tar=ed[2:4]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],tar[0],tar[1]]
                o2=[tar[0],tar[1],src[0],src[1]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],tar[0],tar[1]]
                    o2=[tar[0],tar[1],src[0],src[1]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],tar[0],tar[1]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (src[0],src[1],tar[0],tar[1]))
            else:
                f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (src[0],src[1],tar[0],tar[1]))

        f.write('  </graph>\n')
        f.write('</graphml>')        


def generate_3D_NP_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    nodes.append([i,j,k])
                    f.write('    <node id="(%d, %d, %d)" />\n' % (i,j,k))

        for i in range(0,N):
            for j in range(0,N):
               for k in range(0,N):
                    if i==Nm1 and j==Nm1 and k==Nm1:
                        continue
                    elif i==Nm1 and k==Nm1:
                        edges.append([i,j,k,i,j+1,k])
                    elif k==Nm1 and j==Nm1:
                        edges.append([i,j,k,i+1,j,k])
                    elif i==Nm1 and j==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                    elif i==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,j+1,k])
                    elif j==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i+1,j,k])
                    elif k==Nm1:
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,i+1,j,k])
                    else:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,i+1,j,k])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:3]
            tar=ed[3:6]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],src[2],tar[0],tar[1],tar[2]]
                o2=[tar[0],tar[1],tar[2],src[0],src[1],src[2]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],src[2],tar[0],tar[1],tar[2]]
                    o2=[tar[0],tar[1],tar[2],src[0],src[1],src[2]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],src[2],tar[0],tar[1],tar[2]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (src[0],src[1],src[2],tar[0],tar[1],tar[2]))
            else:
                f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (src[0],src[1],src[2],tar[0],tar[1],tar[2]))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_4D_NP_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        nodes.append([i,j,k,m])
                        f.write('    <node id="(%d, %d, %d, %d)" />\n' % (i,j,k,m))

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        if i==Nm1 and j==Nm1 and k==Nm1 and m==Nm1:
                            continue
                        elif i==Nm1 and j==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                        elif i==Nm1 and j==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k+1,m])
                        elif i==Nm1 and k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j+1,k,m])
                        elif j==Nm1 and k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif i==Nm1 and j==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                        elif i==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j+1,k,m])
                        elif i==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                        elif j==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif j==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif i==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                        elif j==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif m==Nm1:
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        else:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:4]
            tar=ed[4:8]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]]
                o2=[tar[0],tar[1],tar[2],tar[3],src[0],src[1],src[2],src[3]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]]
                    o2=[tar[0],tar[1],tar[2],tar[3],src[0],src[1],src[2],src[3]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]))
            else:
                f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_1D_P_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            nodes.append([i])
            f.write('    <node id="(%d)" />\n' % (i))

        for i in range(0,N):
            if i==Nm1:
                edges.append([i,0])
            else:
                edges.append([i,i+1])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:1]
            tar=ed[1:2]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],tar[0]]
                o2=[tar[0],src[0]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],tar[0]]
                    o2=[tar[0],src[0]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],tar[0]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (src[0],tar[0]))
            else:
                f.write('    <edge source="(%d)" target="(%d)" />\n' % (src[0],tar[0]))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_2D_P_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                nodes.append([i,j])
                f.write('    <node id="(%d, %d)" />\n' % (i,j))

        for i in range(0,N):
            for j in range(0,N):
                if i==Nm1 and j==Nm1:
                    edges.append([i,j,i,0])
                    edges.append([i,j,0,j])
                elif i==Nm1:
                    edges.append([i,j,i,j+1])
                    edges.append([i,j,0,j])
                elif j==Nm1:
                    edges.append([i,j,i,0])
                    edges.append([i,j,i+1,j])

                else:
                    edges.append([i,j,i,j+1])
                    edges.append([i,j,i+1,j])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:2]
            tar=ed[2:4]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],tar[0],tar[1]]
                o2=[tar[0],tar[1],src[0],src[1]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],tar[0],tar[1]]
                    o2=[tar[0],tar[1],src[0],src[1]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],tar[0],tar[1]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (src[0],src[1],tar[0],tar[1]))
            else:
                f.write('    <edge source="(%d, %d)" target="(%d, %d)" />\n' % (src[0],src[1],tar[0],tar[1]))

        f.write('  </graph>\n')
        f.write('</graphml>')        


def generate_3D_P_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    nodes.append([i,j,k])
                    f.write('    <node id="(%d, %d, %d)" />\n' % (i,j,k))

        for i in range(0,N):
            for j in range(0,N):
               for k in range(0,N):
                    if i==Nm1 and j==Nm1 and k==Nm1:
                        edges.append([i,j,k,i,j,0])
                        edges.append([i,j,k,i,0,k])
                        edges.append([i,j,k,0,j,k])
                    elif i==Nm1 and k==Nm1:
                        edges.append([i,j,k,i,j,0])
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,0,j,k])
                    elif k==Nm1 and j==Nm1:
                        edges.append([i,j,k,i,j,0])
                        edges.append([i,j,k,i,0,k])
                        edges.append([i,j,k,i+1,j,k])
                    elif i==Nm1 and j==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,0,k])
                        edges.append([i,j,k,0,j,k])
                    elif i==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,0,j,k])
                    elif j==Nm1:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,0,k])
                        edges.append([i,j,k,i+1,j,k])
                    elif k==Nm1:
                        edges.append([i,j,k,i,j,0])
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,i+1,j,k])
                    else:
                        edges.append([i,j,k,i,j,k+1])
                        edges.append([i,j,k,i,j+1,k])
                        edges.append([i,j,k,i+1,j,k])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:3]
            tar=ed[3:6]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],src[2],tar[0],tar[1],tar[2]]
                o2=[tar[0],tar[1],tar[2],src[0],src[1],src[2]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],src[2],tar[0],tar[1],tar[2]]
                    o2=[tar[0],tar[1],tar[2],src[0],src[1],src[2]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],src[2],tar[0],tar[1],tar[2]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (src[0],src[1],src[2],tar[0],tar[1],tar[2]))
            else:
                f.write('    <edge source="(%d, %d, %d)" target="(%d, %d, %d)" />\n' % (src[0],src[1],src[2],tar[0],tar[1],tar[2]))

        f.write('  </graph>\n')
        f.write('</graphml>')


def generate_4D_P_RP(filename,N,pR):
    Nm1=N-1
    with bz2.open(filename, 'wt') as f:
        f.write("<?xml version='1.0' encoding='utf-8'?>\n")
        f.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n')
        f.write('  <graph edgedefault="undirected">\n')

        nodes=[]
        edges=[]

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        nodes.append([i,j,k,m])
                        f.write('    <node id="(%d, %d, %d, %d)" />\n' % (i,j,k,m))

        for i in range(0,N):
            for j in range(0,N):
                for k in range(0,N):
                    for m in range(0,N):
                        if i==Nm1 and j==Nm1 and k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif i==Nm1 and j==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif i==Nm1 and j==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif i==Nm1 and k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif j==Nm1 and k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif i==Nm1 and j==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif i==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif i==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif j==Nm1 and k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif j==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif k==Nm1 and m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif i==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,0,j,k,m])
                        elif j==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,0,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif k==Nm1:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,0,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        elif m==Nm1:
                            edges.append([i,j,k,m,i,j,k,0])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])
                        else:
                            edges.append([i,j,k,m,i,j,k,m+1])
                            edges.append([i,j,k,m,i,j,k+1,m])
                            edges.append([i,j,k,m,i,j+1,k,m])
                            edges.append([i,j,k,m,i+1,j,k,m])

        cpy_edges = edges[:]
        edgesAdded = copy.deepcopy(edges)
        for ed in cpy_edges:
            src=ed[0:4]
            tar=ed[4:8]
            if random.random() < pR:
                tar = random.choice(nodes)
                o1=[src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]]
                o2=[tar[0],tar[1],tar[2],tar[3],src[0],src[1],src[2],src[3]]
                while tar == src or o1 in edgesAdded or o2 in edgesAdded:
                    o1=[src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]]
                    o2=[tar[0],tar[1],tar[2],tar[3],src[0],src[1],src[2],src[3]]
                    tar = random.choice(nodes)
                edgesAdded.append([src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]])
                edgesAdded.remove(ed)
                f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]))
            else:
                f.write('    <edge source="(%d, %d, %d, %d)" target="(%d, %d, %d, %d)" />\n' % (src[0],src[1],src[2],src[3],tar[0],tar[1],tar[2],tar[3]))

        f.write('  </graph>\n')
        f.write('</graphml>')


if __name__ == '__main__':
    main()

