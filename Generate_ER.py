#!/usr/bin/env python3
import networkx as nx
import bz2
import argparse

# Generate an Erdős-Rényi network 
#
# Authors:
#           Miko Stulajter
#
# Version 1.0.0
#

def argParsing():
    parser = argparse.ArgumentParser(description='Generate an Erdős-Rényi network.')
    
    parser.add_argument('-N',
        help="Number of total nodes.",
        dest='N',
        type=int,
        required=True)

    parser.add_argument('-E',
        help="Approximate number of edges desired.",
        dest='E',
        type=int,
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

    ### ~~~~~~ Edge creation probability
    eP=args.E/((args.N*(args.N-1))/2)

    ### ~~~~~~ Generate network
    G = nx.erdos_renyi_graph(args.N,eP)

    ### ~~~~~~ Output network
    if (args.ofile):
        filename=args.ofile+'.graphml.bz2'
    else:
        filename="ER_N-"+str(args.N)+"_E-"+str(args.E)+'.graphml.bz2'

    with bz2.open(filename, 'wb') as f:
        nx.write_graphml(G, f)


if __name__ == '__main__':
    main()

