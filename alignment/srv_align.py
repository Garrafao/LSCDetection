import sys
sys.path.append('./modules/')

import os
from docopt import docopt
from dsm import load_pkl_files, save_pkl_files
import logging
import time
import codecs
import numpy as np
from composes.semantic_space.space import Space
from composes.matrix.dense_matrix import DenseMatrix
from composes.matrix.sparse_matrix import SparseMatrix
from scipy.sparse import lil_matrix, csr_matrix, csc_matrix, hstack, vstack
from sklearn.random_projection import sparse_random_matrix


def main():
    """
    Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices as described in:
       Pierpaolo Basile, Annalina Caputo and Giovanni Semeraro, 2014. Analysing Word Meaning over Time by Exploiting Temporal Random Indexing.
    """

    # Get the arguments
    args = docopt('''Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices.

    Usage:
        srv_align.py [-l] (-s <seeds> | -a) <dim> <t> <outPath1> <outPath2> <outPathElement> <spacePrefix1> <spacePrefix2>

        <samplesize> = number negative samples, expressed as percentage of positive samples
        <negAlpha> = smoothing parameter for negative sampling
        <seeds> = number of non-zero values in each random vector
        <dim> = number of dimensions for random vectors
        <t> = threshold for downsampling (if t=None, no subsampling is applied)
        <outPath1> = output path for aligned space 1
        <outPath2> = output path for aligned space 2
        <spacePrefix1> = path to pickled space without suffix
        <spacePrefix2> = path to pickled space without suffix
        <outPathElement> = output path for elemental space (context vectors)

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
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']
    outPathElement = args['<outPathElement>']
    spacePrefix1 = args['<spacePrefix1>']
    spacePrefix2 = args['<spacePrefix2>']

    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input spaces
    space1 = load_pkl_files(spacePrefix1)
    space2 = load_pkl_files(spacePrefix2)
    matrix1 = csc_matrix(space1.get_cooccurrence_matrix().get_mat())
    matrix2 = csc_matrix(space2.get_cooccurrence_matrix().get_mat())

    # Get mappings between rows/columns and words
    id2row1 = space1.get_id2row()
    id2row2 = space2.get_id2row()
    row2id_1 = space1.get_row2id()
    row2id_2 = space2.get_row2id()
    id2column1 = space1.get_id2column()
    id2column2 = space2.get_id2column()
    
    # Get union of rows and columns in both spaces
    unified_rows = sorted(list(set(id2row1).union(id2row2)))
    unified_columns = sorted(list(set(id2column1).union(id2column2)))
    columns_diff1 = list(set(unified_columns) - set(id2column1))
    columns_diff2 = list(set(unified_columns) - set(id2column2))
    
    # Get mappings of indices of columns in original spaces to indices of columns in unified space
    c2i = {w: i for i, w in enumerate(unified_columns)}
    cj2i1 = {j: c2i[w] for j, w in enumerate(id2column1+columns_diff1)}
    cj2i2 = {j: c2i[w] for j, w in enumerate(id2column2+columns_diff2)}

    if t!=None:
        rows_diff1 = list(set(unified_rows) - set(id2row1))
        rows_diff2 = list(set(unified_rows) - set(id2row2))
        
        r2i = {w: i for i, w in enumerate(unified_rows)}
        rj2i1 = {j: r2i[w] for j, w in enumerate(id2row1+rows_diff1)}
        rj2i2 = {j: r2i[w] for j, w in enumerate(id2row2+rows_diff2)}
        
        # Build spaces with unified COLUMNS
        new_columns1 = csc_matrix((len(id2row1),len(columns_diff1))) # Get empty columns for additional context words
        unified_matrix1 = hstack((matrix1,new_columns1))[:,sorted(cj2i1, key=cj2i1.get)] # First concatenate matrix and empty columns and then order columns according to unified_columns
        
        new_columns2 = csc_matrix((len(id2row2),len(columns_diff2)))
        unified_matrix2 = hstack((matrix2,new_columns2))[:,sorted(cj2i2, key=cj2i2.get)]
    
        # Build spaces with unified ROWS
        new_rows1 = csc_matrix((len(rows_diff1),len(unified_columns)))
        final_unified_matrix1 = csc_matrix(vstack((unified_matrix1,new_rows1)))[sorted(rj2i1, key=rj2i1.get)]
   
        new_rows2 = csc_matrix((len(rows_diff2),len(unified_columns)))
        final_unified_matrix2 = csc_matrix(vstack((unified_matrix2,new_rows2)))[sorted(rj2i2, key=rj2i2.get)]
        
        # Add up final unified matrices
        common_unified_matrix = np.add(final_unified_matrix1,final_unified_matrix2)

        # Get number of total occurrences of any word
        totalOcc = np.sum(common_unified_matrix)

        # Define function for downsampling
        downsample = lambda f: np.sqrt(float(t)/f) if f>t else 1.0
        downsample = np.vectorize(downsample)

        # Get total normalized co-occurrence frequency of all contexts in both spaces
        context_freqs = np.array(common_unified_matrix.sum(axis=0)/totalOcc)[0]
        

    ## Generate ternary random vectors
    if is_seeds:        
        elementalMatrix = lil_matrix((len(unified_columns),dim))    
        # Generate base vector for random vectors
        baseVector = np.zeros(dim) # Note: Make sure that number of seeds is not greater than dimensions
        for i in range(0,seeds/2):
            baseVector[i] = 1.0
        for i in range(seeds/2,seeds):
            baseVector[i] = -1.0        
        for i in range(len(unified_columns)): # To-do: make this more efficient by generating random indices for a whole array
            np.random.shuffle(baseVector)
            elementalMatrix[i] = baseVector
    if is_aut:
        elementalMatrix = sparse_random_matrix(dim,len(unified_columns)).T
       
    # Initialize target vectors
    alignedMatrix1 = np.zeros((len(id2row1),dim))    
    alignedMatrix2 = np.zeros((len(id2row2),dim))


    # Iterate over rows of space, find context words and update aligned matrix with low-dimensional random vectors of these context words
    for (space,id2row,cj2i,alignedMatrix) in [(space1,id2row1,cj2i1,alignedMatrix1),(space2,id2row2,cj2i2,alignedMatrix2)]:
        # Iterate over targets
        for i, target in enumerate(id2row):
            # Get co-occurrence values as matrix
            m = space.get_row(target).get_mat()
            # Get nonzero indexes
            nonzeros = m.nonzero()
            nonzeros = [cj2i[j] for j in nonzeros[1]]
            data = m.data
            pos_context_vectors = elementalMatrix[nonzeros]
            if t!=None:
                # Apply subsampling
                rfs = context_freqs[nonzeros]
                rfs = downsample(rfs)
                data *= rfs
            # Weight context vectors by occurrence frequency
            pos_context_vectors = pos_context_vectors.multiply(data.reshape(-1,1))
            # Add up context vectors and store as row for target
            alignedMatrix[i] = np.sum(pos_context_vectors, axis=0)
                
    if is_len:
        # L2-normalize vectors
        l2norm1 = np.linalg.norm(alignedMatrix1, axis=1, ord=2)
        l2norm2 = np.linalg.norm(alignedMatrix2, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        l2norm2[l2norm2==0.0] = 1.0 # Convert 0 values to 1
        alignedMatrix1 /= l2norm1.reshape(len(l2norm1),1)
        alignedMatrix2 /= l2norm2.reshape(len(l2norm2),1)
        
    # Make spaces
    alignedSpace1 = Space(DenseMatrix(alignedMatrix1), id2row1, [])
    alignedSpace2 = Space(DenseMatrix(alignedMatrix2), id2row2, [])
    elementalSpace = Space(SparseMatrix(elementalMatrix), unified_columns, [])
    
    # Save the Space objects in pickle format
    save_pkl_files(alignedSpace1, outPath1 + '.dm', save_in_one_file=False)
    save_pkl_files(alignedSpace2, outPath2 + '.dm', save_in_one_file=False)
    save_pkl_files(elementalSpace, outPathElement + '.dm', save_in_one_file=False)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
