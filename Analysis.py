#!/usr/bin/env python3
import networkit as nk
import numpy as np
import bz2
import argparse
from scipy.optimize import curve_fit
from random import seed, choice
import statsmodels.api as sm

# Analysis Script
#
# Authors:
#           Miko Stulajter
#
# Version 1.0.0
#

def argParsing():
    parser = argparse.ArgumentParser(description='Analysis a network and report key properties.')
    
    parser.add_argument('-file',
    help="Network file as a '.graphml.bz2' file.",
    dest='file',
    type=str,
    required=True)

    parser.add_argument('-cores',
    help='Number of cores running on (Default is 1).',
    dest='cores',
    default=1,
    type=int,
    required=False)

    return parser.parse_args()


def main():
    ### ~~~~~~ Argument parsing
    args = argParsing()

    ### ~~~~~~ CBB random seed
    seed = None

    ### ~~~~~~ Read and make undirected
    filename=(args.file).rsplit('/', 1)[-1]
    nk.setNumberOfThreads(int(args.cores))
    gmlReader = nk.graphio.GraphMLReader()
    with bz2.open(args.file) as file_tmp:
        G = gmlReader.read(file_tmp)
    H = nk.graphtools.toUndirected(G)
    H.removeMultiEdges()

    ### ~~~~~~~~ Nodes, Edges, Density
    num_nodes=H.numberOfNodes()
    num_edges=H.numberOfEdges()
    density=nk.graphtools.density(H)

    ### ~~~~~~~~ Average Degree
    degree_run=nk.centrality.DegreeCentrality(H)
    degree_run.run()
    ave_degree=np.average(degree_run.scores())

    ### ~~~~~~~~ Square Clustering
    LC4=nk.centrality.LocalSquareClusteringCoefficient(H)
    LC4.run()
    Scores=LC4.scores()
    LC2_Mean=np.mean(Scores)

    ### ~~~~~~~~ Diameter
    diam = nk.distance.Diameter(H,algo=1)
    diam.run()
    diameter=diam.getDiameter()[0]

    # ~~~~~~~~ Compact Box Burning, Path Length, Growth Exponent
    if seed:
        np.random.seed(seed)

    boxes_list = np.empty((diameter+1), dtype=float)
    boxes_list[0]=num_nodes

    for indx in range(1,diameter):
        if indx==1:
            boxes,gamma,num_gamma,num_paths,path_len=CBB_L_GE(H,indx,num_nodes)
        else:
            boxes=CBB_Only(H,indx)
        boxes_list[indx]=boxes

    boxes_list[diameter]=1
    box_length=list(range(1,diameter+2))

    ### ~~~~~~ Calculate Fractal Dimension
    x=np.log(np.array(box_length).reshape((-1, 1)))
    y=np.log(np.array(boxes_list))
    x = sm.add_constant(x)
    CBB_model = sm.OLS(y,x).fit()
    frac_dim=np.abs(CBB_model.params[1])

    ### ~~~~~~ Calculate Average Path Length and Average Growth Factor 
    ave_path_len = path_len/(num_paths+num_nodes/2)
    growth_exp=np.exp(gamma/num_gamma)

    ### ~~~~~~ Print Output
    print(" ")
    print('Network Analyzed : ' + filename)
    print('Number of nodes : ' + str(num_nodes))
    print('Number of edges : ' + str(num_edges))
    print("Density : %.5E" % density)
    print("Average degree : %.5f" % ave_degree)
    print("Average square clustering coefficient : %.5f" % LC2_Mean)
    print('Diameter : ' + str(diameter))
    print("Average path length : %.5f" % ave_path_len)
    print("Fractal dimension : %.5f" % frac_dim)
    print("Growth exponent : %.5f" % growth_exp)


### ~~~~~~ Sigmoid fit function
def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0))) + b
    return (y)


### ~~~~~~ CBB, L, GE Function
def CBB_L_GE(H,el,num_nodes):
    path_len = 0
    num_paths = 0
    gamma = 0
    num_gamma = 0
    boxes = 0
    nodes_list=list(H.iterNodes())
    uncovered_nodes = set(nodes_list)
    while len(uncovered_nodes) > 0:
        candidate_set = uncovered_nodes.copy()
        box = set()
        while len(candidate_set) > 0:
            p = choice(list(candidate_set))
            candidate_set.discard(p)
            box.add(p)
            k_fa = set([])
            spsp = nk.distance.SPSP(H,[p])
            spsp.run()
            dist = spsp.getDistances()
            arr=np.bincount((np.array(dist[0]).astype(int)))
            i=1
            start=i
            ydata=[]
            curr_len=0
            while curr_len != num_nodes:
                curr_len=sum(arr[0 : i+1])
                i+=1
                ydata.append(curr_len)
            xdata=list(range(start,i))
            p0 = [max(ydata), np.median(xdata),1,min(ydata)]
            try:
                popt, pcov = curve_fit(sigmoid, xdata, ydata,p0, method='dogbox')
                gamma+=popt[2]
                num_gamma+=1
            except Exception as e:
                print(e)
            rangeTOcheck=set(range(p+1,num_nodes))
            for k in candidate_set:
                temp = dist[0][k]
                if temp >el:
                    k_fa.add(k)
                if k in  rangeTOcheck:
                    num_paths += 1
                    path_len += temp
                    rangeTOcheck.remove(k)
            for left in rangeTOcheck:
                temp = dist[0][left]
                num_paths += 1
                path_len += temp
            candidate_set = candidate_set - k_fa
            uncovered_nodes.remove(p)
        boxes+=1
    return boxes,gamma,num_gamma,num_paths,path_len


### ~~~~~~ CBB Function only
def CBB_Only(H,el):
    boxes = 0
    nodes_list=list(H.iterNodes())
    uncovered_nodes = set(nodes_list)
    while len(uncovered_nodes) > 0:
        candidate_set = uncovered_nodes.copy()
        box = set()
        while len(candidate_set) > 0:
            p = choice(list(candidate_set))
            candidate_set.discard(p)
            box.add(p)
            k_fa = set([])
            spsp = nk.distance.SPSP(H,[p])
            spsp.run()
            for k in candidate_set:
                if spsp.getDistance(p,k)>el:
                    k_fa.add(k)
            candidate_set = candidate_set - k_fa
            uncovered_nodes.remove(p)
        boxes+=1
    return boxes


if __name__ == '__main__':
    main()
