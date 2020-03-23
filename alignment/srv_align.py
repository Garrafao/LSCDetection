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
    Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices as described in:
       Pierpaolo Basile, Annalina Caputo and Giovanni Semeraro, 2014. Analysing Word Meaning over Time by Exploiting Temporal Random Indexing.
    """

    # Get the arguments
    args = docopt('''Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices.

    Usage:
        srv_align.py [-l] <matrixPath1> <matrixPath2> <outPath1> <outPath2> <dim>

        <matrixPath1> = path to matrix1
        <matrixPath2> = path to matrix2
        <outPath1> = output path for aligned space 1
        <outPath2> = output path for aligned space 2
        <dim> = number of dimensions for random vectors

    Options:
        -l, --len   normalize final vectors to unit length

    Note:
        Assumes intersected and ordered columns. Paramaters -s, -a and <t> have been removed from an earlier version for efficiency. Also columns are now intersected instead of unified.
  
    References:
        [1] Ping Li, T. Hastie and K. W. Church, 2006,
           "Very Sparse Random Projections".
           http://web.stanford.edu/~hastie/Papers/Ping/KDD06_rp.pdf
        [2] D. Achlioptas, 2001, "Database-friendly random projections",
           http://www.cs.ucsc.edu/~optas/papers/jl.pdf

    ''')
    
    is_len = args['--len']       
    matrixPath1 = args['<matrixPath1>']
    matrixPath2 = args['<matrixPath2>']
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']
    dim = int(args['<dim>'])

    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrices
    countSpace1 = Space(matrixPath1)   
    countMatrix1 = countSpace1.matrix
    rows1 = countSpace1.rows
    columns1 = countSpace1.columns

    countSpace2 = Space(matrixPath2)   
    countMatrix2 = countSpace2.matrix
    rows2 = countSpace2.rows
    columns2 = countSpace2.columns
    
    # Generate random vectors
    randomMatrix = csr_matrix(sparse_random_matrix(dim,len(columns1)).toarray().T)
    
    logging.info("Multiplying matrices")
    reducedMatrix1 = np.dot(countMatrix1,randomMatrix)    
    reducedMatrix2 = np.dot(countMatrix2,randomMatrix)
    
    outSpace1 = Space(matrix=reducedMatrix1, rows=rows1, columns=[])
    outSpace2 = Space(matrix=reducedMatrix2, rows=rows2, columns=[])

    if is_len:
        # L2-normalize vectors
        outSpace1.l2_normalize()
        outSpace2.l2_normalize()
    
    # Save the matrices
    outSpace1.save(outPath1)
    outSpace2.save(outPath2)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
