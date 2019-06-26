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

            
def main():
    """
    Compute number of context types for all rows of a vector space and save their scores.
    """

    # Get the arguments
    args = docopt("""Compute number of context types for all rows of a vector space and save their scores.

    Usage:
        types.py [(-n <normConst>)] <spacePrefix> <outPath> [<testset>]

        <spacePrefix> = path to pickled space without suffix
        <outPath> = output path for result file
        <testset> = path to file with targets in first column
        <normConst> = normalization constant

    Options:
        -n, --nrm  normalize values by normalization constant
        
    """)
    
    is_norm = args['--nrm']
    if is_norm:
        normConst = float(args['<normConst>'])
    spacePrefix = args['<spacePrefix>']
    outPath = args['<outPath>']        
    testset = args['<testset>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    space = load_pkl_files(spacePrefix)

    if testset!=None:
        # target vectors in first/second column are computed from space1/space2
        with codecs.open(testset, 'r', 'utf-8') as f_in:
            targets = [line.strip().split('\t')[0] for line in f_in]
    else:
        # If no test set is provided, compute values for all targets
        targets = [target.decode('utf-8') for target in space.get_row2id()]  
    
    scores = {}
    # Iterate over targets
    for i, v in enumerate(targets):
        
        try:
            row = space.get_row(v.encode('utf8'))
        except KeyError:
            scores[v] = 'nan'
            continue
        
        # Get number of non-zero elements in row
        types = row.get_mat().getnnz()
        
        scores[v] = types

        
    with codecs.open(outPath+'.csv', 'w', 'utf-8') as f_out:
        for word in targets:
            if is_norm:
                scores[word]=float(scores[word])/normConst
            print >> f_out, '\t'.join((word, str(float(scores[word]))))   

            
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
