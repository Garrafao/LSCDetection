import sys
sys.path.append('./modules/')

import numpy as np
from docopt import docopt
import logging
import time
from utils_ import Space

            
def main():
    """
    Compute number of context types for all rows of a vector space and save their scores.
    """

    # Get the arguments
    args = docopt("""Compute number of context types for all rows of a vector space and save their scores.

    Usage:
        types.py [(-n <normConst>)] <testset> <matrixPath> <outPath>

        <normConst> = normalization constant
        <testset> = path to file with one target per line in first column
        <matrixPath> = path to matrix
        <outPath> = output path for result file

    Options:
        -n, --nrm  normalize values by normalization constant
        
    """)
    
    is_norm = args['--nrm']
    if is_norm:
        normConst = float(args['<normConst>'])
    testset = args['<testset>']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']        

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrix
    space = Space(matrixPath)   
    matrix = space.matrix
    
    # Get rows
    row2id = space.row2id

    # Load targets
    with open(testset, 'r', encoding='utf-8') as f_in:
            targets = [line.strip().split('\t')[0] for line in f_in]
    
    scores = {}
    # Iterate over targets
    for target in targets:
        
        try:
            row = matrix[row2id[target]]
        except KeyError:
            scores[target] = 'nan'
            continue
        
        # Get number of non-zero elements in row
        types = row.getnnz()
        
        scores[target] = types

        
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for target in targets:
            if is_norm:
                scores[target]=float(scores[target])/normConst
            f_out.write('\t'.join((target, str(scores[target])+'\n')))

            
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
