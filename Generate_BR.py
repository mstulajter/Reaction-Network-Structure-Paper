#!/usr/bin/env python3
import networkx as nx
import bz2
import argparse

# Generate a bipartite random network 
#
# Authors:
#           Miko Stulajter
#
# Version 1.0.0
#

def argParsing():
    parser = argparse.ArgumentParser(description='Generate a bipartite random network.')
    
    parser.add_argument('-N',
        help="Number of total nodes.",
        dest='N',
        type=int,
        required=True)

    parser.add_argument('-E',
        help="Number of edges.",
        dest='E',
        type=int,
        required=True)

    parser.add_argument('-pM',
        help="Percentage of nodes in first bipartite set (Default is 0.5).",
        dest='pM',
        type=float,
        default=0.5,
        required=False)

    parser.add_argument('-ofile',
        help="Output file name with no extension as it will be saved as a '.graphml.bz2' file.",
        dest='ofile',
        type=str,
        required=False)

    return parser.parse_args()


def main():
    ### ~~~~~~ Argument parsing
    args = argParsing()

    ### ~~~~~~ Number of nodes in bipartite sets
    sN=int(args.N*args.pM)
    sM=args.N-sN

    ### ~~~~~~ Generate network
    G = nx.bipartite.gnmk_random_graph(sN,sM,args.E)

    ### ~~~~~~ Output network
    if (args.ofile):
        filename=args.ofile+'.graphml.bz2'
    else:
        filename="BR_N-"+str(args.N)+"_E-"+str(args.E)+"_pM-"+str(args.pM)+'.graphml.bz2'

    with bz2.open(filename, 'wb') as f:
        nx.write_graphml(G, f)


if __name__ == '__main__':
    main()

