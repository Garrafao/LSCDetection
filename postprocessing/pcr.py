import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from utils_ import Space


def main():
    """
    Mean center matrix, depending on flag, and remove top n PCA components
    """

    # Get the arguments
    args = docopt('''Depending on the flag, mean centers matrix and applies and removes the top n PCA components.

    Usage:
        pcr.py [-m] <matrixPath> <outPath> <threshold>

        <matrixPath> = path to matrix
        <outPath> = output path for space
        <threshold> = threshold, amount of PCA components

    Options:
        -m, --mean  flag, if mean centering should be applied

    ''')

    matrix_path = args['<matrixPath>']
    out_path = args['<outPath>']
    threshold = args['<threshold>']
    
    is_mean = args['--mean']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    try:
        space = Space(matrix_path, format='npz')
        _format_flag = 'npz'
    except ValueError:
        space = Space(matrix_path, format='w2v')
        _format_flag = 'w2v'

    # MC+PCR
    space.mc_pcr(int(threshold), is_mean)

    # Save the matrix
    space.save(out_path, format=_format_flag)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
