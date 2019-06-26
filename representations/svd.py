import sys
sys.path.append('./modules/')

import numpy as np
from docopt import docopt
from composes.utils import io_utils
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix
from sklearn.utils.extmath import randomized_svd
from dsm import save_pkl_files, load_pkl_files
import logging
import time


def main():
    """
    Perform dimensionality reduction on a (normally PPMI) matrix by applying truncated SVD as described in

      Omer Levy, Yoav Goldberg, and Ido Dagan. 2015. Improving distributional similarity with lessons learned from word embeddings. Trans. ACL, 3.

    """

    # Get the arguments
    args = docopt('''Perform dimensionality reduction on a (normally PPMI) matrix by applying truncated SVD and save it in pickle format.

    Usage:
        svd.py [-l] <dsm_prefix> <dim> <gamma> <outPath>

        <dsm_prefix> = the prefix for the input files (.sm for the matrix, .rows and .cols) and output files (.svd)
        <dim> = dimensionality of low-dimensional output vectors
        <gamma> = eigenvalue weighting parameter
        <outPath> = output path for space

    Options:
        -l, --len   normalize final vectors to unit length

    ''')

    is_len = args['--len']
    dsm_prefix = args['<dsm_prefix>']
    dim = int(args['<dim>'])
    gamma = float(args['<gamma>'])
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Get space with sparse matrix
    dsm = load_pkl_files(dsm_prefix)
    
    id2row = dsm.get_id2row()

    # Get matrix from space
    matrix_ = dsm.get_cooccurrence_matrix()

    # Apply SVD
    u, s, v = randomized_svd(matrix_.get_mat(), n_components=dim, n_iter=5, transpose=False)

    # Weight matrix
    if gamma == 0.0:
        matrix_ = u
    elif gamma == 1.0:
        #matrix_ = np.dot(u, np.diag(s)) # This is equivalent to the below formula (because s is a flattened diagonal matrix)
        matrix_ = s * u        
    else:
        #matrix_ = np.dot(u, np.power(np.diag(s), gamma)) # This is equivalent to the below formula
        matrix_ = np.power(s, gamma) * u

    if is_len:
        # L2-normalize vectors
        l2norm1 = np.linalg.norm(matrix_, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        matrix_ /= l2norm1.reshape(len(l2norm1),1)
        
    dsm = Space(DenseMatrix(matrix_), id2row, [])
            
    # Save the Space object in pickle format
    save_pkl_files(dsm, outPath + ".svd.dm", save_in_one_file=True, save_as_w2v=True)
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   


if __name__ == '__main__':
    main()
