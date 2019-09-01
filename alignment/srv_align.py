import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import numpy as np
from sklearn.random_projection import sparse_random_matrix
from scipy.sparse import lil_matrix, csc_matrix, hstack, vstack
from utils_ import Space


def main():
    """
    Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices as described in:
       Pierpaolo Basile, Annalina Caputo and Giovanni Semeraro, 2014. Analysing Word Meaning over Time by Exploiting Temporal Random Indexing.
    """

    # Get the arguments
    args = docopt('''Create two aligned low-dimensional vector spaces by sparse random indexing from two co-occurrence matrices.

    Usage:
        srv_align.py [-l] (-s <seeds> | -a) <matrixPath1> <matrixPath2> <outPath1> <outPath2> <outPathElement> <dim> <t>

        <seeds> = number of non-zero values in each random vector
        <matrixPath1> = path to matrix1
        <matrixPath2> = path to matrix2
        <outPath1> = output path for aligned space 1
        <outPath2> = output path for aligned space 2
        <outPathElement> = output path for elemental space (context vectors)
        <dim> = number of dimensions for random vectors
        <t> = threshold for downsampling (if t=None, no subsampling is applied)

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
    matrixPath1 = args['<matrixPath1>']
    matrixPath2 = args['<matrixPath2>']
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']
    outPathElement = args['<outPathElement>']
    dim = int(args['<dim>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])

    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrices
    space1 = Space(matrixPath1)   
    matrix1 = space1.matrix
    space2 = Space(matrixPath2)   
    matrix2 = space2.matrix
    
    # Get mappings between rows/columns and words
    rows1 = space1.rows
    id2row1 = space1.id2row
    row2id1 = space1.row2id
    columns1 = space1.columns
    column2id1 = space1.column2id
    rows2 = space2.rows
    id2row2 = space2.id2row
    row2id2 = space2.row2id
    columns2 = space2.columns
    column2id2 = space2.column2id
    
    # Get union of rows and columns in both spaces
    unified_rows = sorted(list(set(rows1).union(rows2)))
    unified_columns = sorted(list(set(columns1).union(columns2)))
    columns_diff1 = sorted(list(set(unified_columns) - set(columns1)))
    columns_diff2 = sorted(list(set(unified_columns) - set(columns2)))
    
    # Get mappings of indices of columns in original spaces to indices of columns in unified space
    c2i = {w: i for i, w in enumerate(unified_columns)}
    cj2i1 = {j: c2i[w] for j, w in enumerate(columns1+columns_diff1)}
    cj2i2 = {j: c2i[w] for j, w in enumerate(columns2+columns_diff2)}

    if t!=None:
        rows_diff1 = list(set(unified_rows) - set(rows1))
        rows_diff2 = list(set(unified_rows) - set(rows2))
        
        r2i = {w: i for i, w in enumerate(unified_rows)}
        rj2i1 = {j: r2i[w] for j, w in enumerate(rows1+rows_diff1)}
        rj2i2 = {j: r2i[w] for j, w in enumerate(rows2+rows_diff2)}
        
        # Build spaces with unified COLUMNS
        new_columns1 = csc_matrix((len(rows1),len(columns_diff1))) # Get empty columns for additional context words
        unified_matrix1 = csc_matrix(hstack((matrix1,new_columns1)))[:,sorted(cj2i1, key=cj2i1.get)] # First concatenate matrix and empty columns and then order columns according to unified_columns
        
        new_columns2 = csc_matrix((len(rows2),len(columns_diff2)))
        unified_matrix2 = csc_matrix(hstack((matrix2,new_columns2)))[:,sorted(cj2i2, key=cj2i2.get)]
    
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
        for i in range(0,int(seeds/2)):
            baseVector[i] = 1.0
        for i in range(int(seeds/2),seeds):
            baseVector[i] = -1.0        
        for i in range(len(unified_columns)): # To-do: make this more efficient by generating random indices for a whole array
            np.random.shuffle(baseVector)
            elementalMatrix[i] = baseVector
    if is_aut:
        elementalMatrix = sparse_random_matrix(dim,len(unified_columns)).T
       
    # Initialize target vectors
    alignedMatrix1 = np.zeros((len(rows1),dim))    
    alignedMatrix2 = np.zeros((len(rows2),dim))


    # Iterate over rows of space, find context words and update aligned matrix with low-dimensional random vectors of these context words
    for (matrix,id2row,cj2i,alignedMatrix) in [(matrix1,id2row1,cj2i1,alignedMatrix1),(matrix2,id2row2,cj2i2,alignedMatrix2)]:
        # Iterate over targets
        for i in id2row:
            # Get co-occurrence values as matrix
            m = matrix[i]
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

    outSpace1 = Space(matrix=alignedMatrix1, rows=rows1, columns=[])
    outSpace2 = Space(matrix=alignedMatrix2, rows=rows2, columns=[])

    if is_len:
        # L2-normalize vectors
        outSpace1.l2_normalize()
        outSpace2.l2_normalize()
    
    # Save the matrices
    outSpace1.save(outPath1)
    outSpace2.save(outPath2)
    Space(matrix=elementalMatrix, rows=unified_columns, columns=[]).save(outPathElement)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
