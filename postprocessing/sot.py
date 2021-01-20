import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from utils_ import Space


def main():
    """
    Higher-order similarity matrix.
    """

    # Get the arguments
    args = docopt('''Apply the similarity order transformation.

    Usage:
        sot.py [-l] <matrixPath> <outPath> <alpha>

        <matrixPath>    = path to matrix
        <outPath>       = output path for space
        <alpha>         = the desired similarity-order

    Options:
        -l, --len   normalize vectors to unit length before centering

    ''')

    is_len = args['--len']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']
    alpha = float(args['<alpha>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices and rows
    try:
        space = Space(matrixPath, format='npz')   
    except ValueError:
        space = Space(matrixPath, format='w2v')   

    # L2-normalize vectors
    if is_len:
        space.l2_normalize()

    # Similarity matrix   
    space.sim(alpha)
    
    # Save the matrix
    space.save(outPath, format="w2v")

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
