import sys
sys.path.append('./modules/')

import os
from os.path import basename
from docopt import docopt
from dsm import load_pkl_files, save_pkl_files
import logging
import time
import codecs
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix
from composes.matrix.sparse_matrix import SparseMatrix
from sklearn.random_projection import sparse_random_matrix
from scipy.sparse import lil_matrix, csr_matrix, csc_matrix


def main():
    """
    Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.
    """

    # Get the arguments
    args = docopt('''Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.

    Usage:
        reduce_matrix_ri.py [-l] (-s <seeds> | -a) <dim> <t> <outPath> <outPathElement> <spacePrefix>

        <seeds> = number of non-zero values in each random vector
        <dim> = number of dimensions for random vectors
        <t> = threshold for downsampling (if t=None, no subsampling is applied)
        <outPath> = output path for reduced space 
        <outPathElement> = output path for elemental space (context vectors)
        <spacePrefix> = path to pickled space without suffix

    Options:
        -l, --len   normalize final vectors to unit length
        -s, --see   specify number of seeds manually
        -a, --aut   calculate number of seeds automatically as proposed in [1,2]

    References:
        [1] Ping Li, T. Hastie and K. W. Church, 2006,
           "Very Sparse Random Projections".
           http://web.stanford.edu/~hastie/Papers/Ping/KDD06_rp.pdf
        [2] D. Achlioptas, 2001, "Database-friendly random projections",
           http://www.cs.ucsc.edu/~optas/papers/jl.pdf

    ''')
    
    is_len = args['--len']
    is_seeds = args['--see']
    if is_seeds:
        seeds = int(args['<seeds>'])
    is_aut = args['--aut']
    dim = int(args['<dim>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])
    outPath = args['<outPath>']
    outPathElement = args['<outPathElement>']
    spacePrefix = args['<spacePrefix>']
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input space
    space1 = load_pkl_files(spacePrefix)
    matrix1 = space1.get_cooccurrence_matrix()    

    # Get mappings between rows/columns and words
    id2row1 = space1.get_id2row()
    id2column1 = space1.get_id2column()
    column2id1 = space1.get_column2id()
    
    ## Generate ternary random vectors
    if is_seeds:
        elementalMatrix = np.zeros((len(id2column1),dim))
        # Generate base vector for random vectors 
        baseVector = np.zeros(dim) # Note: Make sure that number of seeds is not greater than dimensions
        for i in range(0,seeds/2):
            baseVector[i] = 1.0
        for i in range(seeds/2,seeds):
            baseVector[i] = -1.0
        for i in range(len(id2column1)):
            np.random.shuffle(baseVector)
            elementalMatrix[i] = baseVector
    if is_aut:
        elementalMatrix = sparse_random_matrix(dim,len(id2column1)).toarray().T

    elementalMatrix = csc_matrix(elementalMatrix)
    # to-do: get rid of transformation into sparse matrices by initializing them as such

    # Initialize target vectors
    reducedMatrix1 = np.zeros((len(id2row1),dim))    

    # Get number of total occurrences of any word
    totalOcc = np.sum(matrix1.get_mat())

    # Define function for downsampling
    downsample = lambda f: np.sqrt(float(t)/f) if f>t else 1.0
    downsample = np.vectorize(downsample)
    
    # Get total normalized co-occurrence frequency of all contexts in space
    context_freqs = np.array(matrix1.sum(axis=0))/totalOcc
    
    #to-do: matrix multiplication is done row-wise, do this matrix-wise
    # Iterate over rows of space, find context words and update reduced matrix with low-dimensional random vectors of these context words
    for (space,matrix,id2row,id2column,column2id,reducedMatrix) in [(space1,matrix1,id2row1,id2column1,column2id1,reducedMatrix1)]:
        # Iterate over targets
        for i, target in enumerate(id2row):
            # Get co-occurrence values as matrix
            m = space.get_row(target).get_mat()
            # Get nonzero indexes and data
            nonzeros = m.nonzero()
            data = m.data            
            # Smooth context distribution
            pos_context_vectors = elementalMatrix[nonzeros[1]]
            if t!=None:
                # Apply subsampling
                rfs = context_freqs[0,nonzeros[1]]
                rfs = downsample(rfs)
                data *= rfs
            data = csc_matrix(data)
            # Weight context vectors by occurrence frequency
            pos_context_vectors = pos_context_vectors.multiply(data.reshape(-1,1))
            pos_context_vectors = np.sum(pos_context_vectors, axis=0)
            # Add up context vectors and store as row for target
            reducedMatrix[i] = pos_context_vectors
              
    if is_len:
        # L2-normalize vectors
        l2norm1 = np.linalg.norm(reducedMatrix1, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        reducedMatrix1 /= l2norm1.reshape(len(l2norm1),1)
    
    # Make spaces
    reducedSpace1 = Space(DenseMatrix(reducedMatrix1), id2row1, [])
    elementalSpace = Space(SparseMatrix(elementalMatrix), id2column1, [])
    
    # Save the Space objects in pickle format
    save_pkl_files(reducedSpace1, outPath + '.ri.dm', save_in_one_file=True, save_as_w2v=True)
    save_pkl_files(elementalSpace, outPathElement + '.sm', save_in_one_file=False)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
