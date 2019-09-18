import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import numpy as np
from sklearn.random_projection import sparse_random_matrix
from scipy.sparse import csc_matrix, lil_matrix
from utils_ import Space


def main():
    """
    Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.
    """

    # Get the arguments
    args = docopt('''Create low-dimensional vector space by sparse random indexing from co-occurrence matrix.

    Usage:
        ri.py [-l] (-s <seeds> | -a) <matrixPath> <outPath> <outPathElement> <dim> <t>

        <seeds> = number of non-zero values in each random vector
        <matrixPath> = path to matrix
        <outPath> = output path for reduced space 
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
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']
    outPathElement = args['<outPathElement>']
    dim = int(args['<dim>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrix
    space = Space(matrixPath)   
    matrix = space.matrix
    
    # Get mappings between rows/columns and words
    rows = space.rows
    id2row = space.id2row
    row2id = space.row2id
    columns = space.columns
    id2column = space.id2column
    column2id = space.column2id

    ## Generate ternary random vectors
    if is_seeds:
        elementalMatrix = lil_matrix((len(columns),dim))
        # Generate base vector for random vectors 
        baseVector = np.zeros(dim) # Note: Make sure that number of seeds is not greater than dimensions
        for i in range(0,int(seeds/2)):
            baseVector[i] = 1.0
        for i in range(int(seeds/2),seeds):
            baseVector[i] = -1.0
        for i in range(len(columns)):
            np.random.shuffle(baseVector)
            elementalMatrix[i] = baseVector
    if is_aut:
        elementalMatrix = sparse_random_matrix(dim,len(columns)).toarray().T

    elementalMatrix = csc_matrix(elementalMatrix)
    # to-do: get rid of transformation into sparse matrices by initializing them as such

    # Initialize target vectors
    reducedMatrix = np.zeros((len(rows),dim))    

    # Get number of total occurrences of any word
    totalOcc = np.sum(matrix)

    # Define function for downsampling
    downsample = lambda f: np.sqrt(float(t)/f) if f>t else 1.0
    downsample = np.vectorize(downsample)
    
    # Get total normalized co-occurrence frequency of all contexts in space
    context_freqs = np.array(matrix.sum(axis=0))/totalOcc
    
    #to-do: matrix multiplication is done row-wise, do this matrix-wise
    # Iterate over rows of space, find context words and update reduced matrix with low-dimensional random vectors of these context words
    for i in id2row:
        # Get co-occurrence values as matrix
        m = matrix[i]
        #print(m)
        # Get nonzero indexes and data
        nonzeros = m.nonzero()
        #print(nonzeros)        
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
    
    outSpace = Space(matrix=reducedMatrix, rows=rows, columns=[])

    if is_len:
        # L2-normalize vectors
        outSpace.l2_normalize()
        
    # Save the matrices
    outSpace.save(outPath, format='w2v')
    Space(matrix=elementalMatrix, rows=columns, columns=[]).save(outPathElement)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    
    
if __name__ == '__main__':
    main()
