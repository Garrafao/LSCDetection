import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
from utils_ import Space


def main():
    """
    Align two sparse matrices by intersecting their columns.
    """

    # Get the arguments
    args = docopt('''Align two sparse matrices by intersecting their columns.

    Usage:
        ci_align.py <matrix1> <matrix2> <outPath1> <outPath2>

        <matrix1> = path to matrix1
        <matrix2> = path to matrix2
        <outPath1> = output path for aligned matrix 1
        <outPath2> = output path for aligned matrix 2
    
    ''')
    
    matrix1 = args['<matrix1>']
    matrix2 = args['<matrix2>']
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Load matrices, rows and columns
    space1 = Space(matrix1)
    space2 = Space(matrix2)
    matrix1 = space1.matrix
    rows1 = space1.rows
    columns1 = space1.columns
    column2id1 = space1.column2id
    matrix2 = space2.matrix
    rows2 = space2.rows
    columns2 = space2.columns
    column2id2 = space2.column2id

    # Intersect columns of matrices
    intersected_columns = sorted(list(set(columns1).intersection(columns2)))
    intersected_columns_id1 = [column2id1[item] for item in intersected_columns]
    intersected_columns_id2 = [column2id2[item] for item in intersected_columns]
    reduced_matrix1 = matrix1[:, intersected_columns_id1]
    reduced_matrix2 = matrix2[:, intersected_columns_id2]

    # Save matrices
    Space(matrix=reduced_matrix1, rows=rows1, columns=intersected_columns).save(outPath1)
    Space(matrix=reduced_matrix2, rows=rows2, columns=intersected_columns).save(outPath2)

    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
