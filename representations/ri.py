import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import numpy as np
from sklearn.random_projection import sparse_random_matrix
from scipy.sparse import csr_matrix
from utils_ import Space


def main():
    """
    Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.
    """

    # Get the arguments
    args = docopt('''Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.

    Usage:
        ri.py [-l] <matrixPath> <outPath> <dim>

        <matrixPath> = path to matrix
        <outPath> = output path for reduced space 
        <dim> = number of dimensions for random vectors

    Options:
        -l, --len   normalize final vectors to unit length

    Note:
        Paramaters -s, -a and <t> have been removed from an earlier version for efficiency.

    References:
        [1] Ping Li, T. Hastie and K. W. Church, 2006,
           "Very Sparse Random Projections".
           http://web.stanford.edu/~hastie/Papers/Ping/KDD06_rp.pdf
        [2] D. Achlioptas, 2001, "Database-friendly random projections",
           http://www.cs.ucsc.edu/~optas/papers/jl.pdf

    ''')
    
    is_len = args['--len']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']
    dim = int(args['<dim>'])
    
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
    
    # Load input matrix
    countSpace = Space(matrixPath)   
    countMatrix = countSpace.matrix
    rows = countSpace.rows
    columns = countSpace.columns
    
    # Generate random vectors
    randomMatrix = csr_matrix(sparse_random_matrix(dim,len(columns)).toarray().T)

    logging.info("Multiplying matrices")
    reducedMatrix = np.dot(countMatrix,randomMatrix)    
    outSpace = Space(matrix=reducedMatrix, rows=rows, columns=[])
    
    if is_len:
        # L2-normalize vectors
        outSpace.l2_normalize()

    # Save the matrix
    outSpace.save(outPath, format='w2v')

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    
if __name__ == '__main__':
    main()
