import sys
sys.path.append('./modules/')

import numpy as np
from docopt import docopt
from scipy.sparse import csc_matrix, coo_matrix, linalg
from composes.utils import io_utils
from composes.semantic_space.space import Space
from composes.utils.py_matrix_utils import nonzero_invert
from composes.transformation.scaling.ppmi_weighting import PpmiWeighting
from composes.matrix.sparse_matrix import SparseMatrix
from dsm import save_pkl_files, load_pkl_files
import logging
import time


def main():
    """
    Compute the smoothed and shifted (P)PMI matrix from a co-occurrence matrix. Smoothing is performed as described in

      Omer Levy, Yoav Goldberg, and Ido Dagan. 2015. Improving distributional similarity with lessons learned from word embeddings. Trans. ACL, 3.

    """

    # Get the arguments
    args = docopt('''Compute the smoothed and shifted (P)PMI matrix from a co-occurrence matrix and save it in pickle format.

    Usage:
        ppmi.py [-l] <dsm_prefix> <k> <alpha> <outPath>

        <dsm_prefix> = the prefix for the input files (.sm for the matrix, .rows and .cols) and output files (.ppmi)
        <k> = shifting parameter
        <alpha> = smoothing parameter
        <outPath> = output path for space

    Options:
        -l, --len   normalize final vectors to unit length

    ''')

    is_len = args['--len']
    dsm_prefix = args['<dsm_prefix>']
    k = int(args['<k>'])
    alpha = float(args['<alpha>'])
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Get space with sparse matrix
    dsm = load_pkl_files(dsm_prefix)
    id2row = dsm.get_id2row()
    id2column = dsm.get_id2column()

    # Get probabilities
    matrix_ = dsm.cooccurrence_matrix

    matrix_.assert_positive()
    row_sum = matrix_.sum(axis = 1)
    col_sum = matrix_.sum(axis = 0)

    # Compute smoothed P_alpha(c)
    smooth_col_sum = np.power(col_sum, alpha)
    col_sum = smooth_col_sum/smooth_col_sum.sum()

    # Compute P(w)
    row_sum = nonzero_invert(row_sum)
    col_sum = nonzero_invert(col_sum)
    
    # Apply epmi weighting (without log)
    matrix_ = matrix_.scale_rows(row_sum)
    matrix_ = matrix_.scale_columns(col_sum)

    # Apply log weighting
    matrix_.mat.data = np.log(matrix_.mat.data)

    # Shift values
    matrix_.mat.data -= np.log(k)

    # Eliminate negative counts
    matrix_.mat.data[matrix_.mat.data <= 0] = 0.0

    # Eliminate zero counts
    matrix_.mat.eliminate_zeros()
    
    matrix_ = matrix_.get_mat()
    
    if is_len:
        # L2-normalize vectors
        l2norm1 = linalg.norm(matrix_, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        matrix_ /= l2norm1.reshape(len(l2norm1),1)

    dsm = Space(SparseMatrix(matrix_), id2row, id2column)
   
    # Save the Space object in pickle format
    save_pkl_files(dsm, outPath + ".ppmi.sm", save_in_one_file=False)
    logging.info("--- %s seconds ---" % (time.time() - start_time))                   


if __name__ == '__main__':
    main()
