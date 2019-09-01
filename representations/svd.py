import sys
sys.path.append('./modules/')

import numpy as np
from docopt import docopt
from sklearn.utils.extmath import randomized_svd
import logging
import time
from utils_ import Space


def main():
    """
    Perform dimensionality reduction on a (normally PPMI) matrix by applying truncated SVD as described in

      Omer Levy, Yoav Goldberg, and Ido Dagan. 2015. Improving distributional similarity with lessons learned from word embeddings. Trans. ACL, 3.

    """

    # Get the arguments
    args = docopt('''Perform dimensionality reduction on a (normally PPMI) matrix by applying truncated SVD and save it in pickle format.

    Usage:
        svd.py [-l] <matrixPath> <outPath> <dim> <gamma>

        <matrixPath> = path to matrix
        <outPath> = output path for space
        <dim> = dimensionality of low-dimensional output vectors
        <gamma> = eigenvalue weighting parameter

    Options:
        -l, --len   normalize final vectors to unit length

    ''')

    is_len = args['--len']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']
    dim = int(args['<dim>'])
    gamma = float(args['<gamma>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrix
    space = Space(matrixPath)   
    matrix = space.matrix
    
    # Get mappings between rows/columns and words
    rows = space.rows
    id2row = space.id2row
    id2column = space.id2column

    # Apply SVD
    u, s, v = randomized_svd(matrix, n_components=dim, n_iter=5, transpose=False)

    # Weight matrix
    if gamma == 0.0:
        matrix_reduced = u
    elif gamma == 1.0:
        #matrix_reduced = np.dot(u, np.diag(s)) # This is equivalent to the below formula (because s is a flattened diagonal matrix)
        matrix_reduced = s * u
    else:
        #matrix_ = np.dot(u, np.power(np.diag(s), gamma)) # This is equivalent to the below formula
        matrix_reduced = np.power(s, gamma) * u
       
    outSpace = Space(matrix=matrix_reduced, rows=rows, columns=[])

    if is_len:
        # L2-normalize vectors
        outSpace.l2_normalize()
        
    # Save the matrix
    outSpace.save(outPath, format='w2v')

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
