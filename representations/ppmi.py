import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from utils_ import Space


def main():
    """
    Compute the smoothed and shifted PPMI matrix from a co-occurrence matrix. Smoothing is performed as described in

      Omer Levy, Yoav Goldberg, and Ido Dagan. 2015. Improving distributional similarity with lessons learned from word embeddings. Trans. ACL, 3.

    """

    # Get the arguments
    args = docopt('''Compute the smoothed and shifted PPMI matrix from a co-occurrence matrix and save it.

    Usage:
        ppmi.py [-l] <matrixPath> <outPath> <k> <alpha>

        <matrixPath> = path to matrix
        <outPath> = output path for space
        <k> = shifting parameter
        <alpha> = smoothing parameter

    Options:
        -l, --len   normalize final vectors to unit length

    ''')

    is_len = args['--len']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']
    k = int(args['<k>'])
    alpha = float(args['<alpha>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load input matrix
    space = Space(matrixPath)   

    # Apply EPMI weighting
    space.epmi_weighting(alpha)
    
    # Apply log weighting
    space.log_weighting()

    # Shift values
    space.shifting(k)

    # Eliminate negative counts
    space.eliminate_negative()

    # Eliminate zero counts
    space.eliminate_zeros()
        
    outSpace = Space(matrix=space.matrix, rows=space.rows, columns=space.columns)

    if is_len:
        # L2-normalize vectors
        outSpace.l2_normalize()
        
    # Save the matrix
    outSpace.save(outPath)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
