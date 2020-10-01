import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from utils_ import Space


def main():
    """
    Mean center matrix.
    """

    # Get the arguments
    args = docopt('''Mean center matrix.

    Usage:
        center.py [-l] [-w] <matrixPath> <outPath>

        <matrixPath> = path to matrix
        <outPath> = output path for space

    Options:
        -l, --len   normalize vectors to unit length before centering
        -w, --w2v   save in word2vec format

    ''')

    is_len = args['--len']
    is_w2v = args['--len']
    matrixPath = args['<matrixPath>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices and rows
    try:
        space = Space(matrixPath, format='npz')   
    except ValueError:
        space = Space(matrixPath, format='w2v')   

    if is_len:
        # L2-normalize vectors
        space.l2_normalize()

    # Mean center    
    space.mean_center()
        
    # Save the matrix
    if is_w2v:
        space.save(outPath, format='w2v')
    else:
        space.save(outPath)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
