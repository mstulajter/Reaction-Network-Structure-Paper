#!/usr/bin/env python3
import networkx as nx
import bz2
import argparse

# Generate a Watts–Strogatz network 
#
# Authors:
#           Miko Stulajter
#
# Version 1.0.0
#

def argParsing():
    parser = argparse.ArgumentParser(description='Generate a Watts–Strogatz network.')
    
    parser.add_argument('-N',
    help="Number of total nodes.",
    dest='N',
    type=int,
    required=True)

    parser.add_argument('-k',
    help="Number of nearest neighbors.",
    dest='k',
    type=int,
    required=True)

    parser.add_argument('-pR',
    help="Probability of rewiring edges.",
    dest='pR',
    type=float,
    required=True)

    parser.add_argument('-ofile',
    help="Output file name with no extension as it will be saved as a '.graphml.bz2' file.",
    dest='ofile',
    type=str,
    required=False)

    return parser.parse_args()


def main():
    ### ~~~~~~ Argument parsing
    args = argParsing()

    ### ~~~~~~ Generate network
    G = nx.watts_strogatz_graph(args.N,args.k,args.pR)

    ### ~~~~~~ Output network
    if (args.ofile):
        filename=args.ofile+'.graphml.bz2'
    else:
        filename="WS_N-"+str(args.N)+"_k-"+str(args.k)+"_pR-"+str(args.pR)+'.graphml.bz2'

    with bz2.open(filename, 'wb') as f:
        nx.write_graphml(G, f)


if __name__ == '__main__':
    main()

