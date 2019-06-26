import sys
sys.path.append('./modules/')

import os
from os.path import basename
from docopt import docopt
from dsm import load_pkl_files
import logging
import time
import codecs
import numpy as np
from scipy import spatial
from scipy.sparse import csr_matrix
from composes.matrix.dense_matrix import DenseMatrix
            
def main():
    """
    Compute cosine distance for target pairs from two vector spaces.
    """

    # Get the arguments
    args = docopt("""Compute cosine distance for target pairs from two vector spaces.

    Usage:
        cd.py [(-f | -s)] <spacePrefix1> <spacePrefix2> <outPath> [<testset>]

        <spacePrefix1> = path to pickled space without suffix
        <spacePrefix2> = path to pickled space without suffix
        <testset> = path to file with tab-separated word pairs
        <outPath> = output path for result file

    Options:
        -f, --fst   write only first target in output file
        -s, --scd   write only second target in output file

     Note:
         Important: spaces must be already aligned (columns in same order)!
        
    """)
    
    is_fst = args['--fst']
    is_scd = args['--scd']
    spacePrefix1 = args['<spacePrefix1>']
    spacePrefix2 = args['<spacePrefix2>']
    testset = args['<testset>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load spaces
    space1 = load_pkl_files(spacePrefix1)
    space2 = load_pkl_files(spacePrefix2)
    
    if testset!=None:
        # target vectors in first/second column are computed from space1/space2
        with codecs.open(testset, 'r', 'utf-8') as f_in:
            targets = [(line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in f_in]
    else:
        # If no test set is provided, compute values for all targets occurring in both spaces
        target_intersection = set([target.decode('utf-8') for target in space1.get_row2id()]).intersection([target.decode('utf-8') for target in space2.get_row2id()])
        targets = zip(target_intersection,target_intersection)
        
    scores = {}
    for i, (t1, t2) in enumerate(targets):
        
        # Get row vectors
        try:
            row1 = space1.get_row(t1.encode('utf8'))
            row2 = space2.get_row(t2.encode('utf8'))
        except KeyError:
            scores[(t1, t2)] = 'nan'
            continue

        # Convert to list
        row_vector1 = csr_matrix(row1.get_mat()).toarray()[0].tolist()
        row_vector2 = csr_matrix(row2.get_mat()).toarray()[0].tolist()
        
        # Compute cosine distance of vectors
        distance = spatial.distance.cosine(row_vector1, row_vector2)
        scores[(t1, t2)] = distance
        
        
    with codecs.open(outPath +'.csv', 'w', 'utf-8') as f_out:
        for (t1, t2) in targets:
            if is_fst: # output only first target string
                print >> f_out, '\t'.join((t1, str(float(scores[(t1, t2)]))))
            elif is_scd: # output only second target string
                print >> f_out, '\t'.join((t2, str(float(scores[(t1, t2)]))))            
            else: # standard outputs both target strings    
                print >> f_out, '\t'.join(('%s,%s' % (t1,t2), str(float(scores[(t1, t2)]))))

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    

if __name__ == '__main__':
    main()
