import sys
sys.path.append('./modules/')

from docopt import docopt
from dsm import load_pkl_files, save_pkl_files
from composes.semantic_space.space import Space
from composes.matrix.sparse_matrix import SparseMatrix
from scipy.sparse import linalg
import logging
import time


def main():
    """
    Align two sparse matrices by intersecting their columns.
    """

    # Get the arguments
    args = docopt('''Align two sparse matrices by intersecting their columns.

    Usage:
        ci_align.py [-l] <outPath1> <outPath2> <spacePrefix1> <spacePrefix2>

        <outPath1> = output path for aligned space 1
        <outPath2> = output path for aligned space 2
        <spacePrefix1> = path to pickled space1 without suffix
        <spacePrefix2> = path to pickled space2 without suffix

    Options:
        -l, --len   normalize final vectors to unit length
    
    ''')
    
    is_len = args['--len']
    spacePrefix1 = args['<spacePrefix1>']
    spacePrefix2 = args['<spacePrefix2>']
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    

    # Get the two matrices as spaces and intersect their columns
    space1 = load_pkl_files(spacePrefix1)
    space2 = load_pkl_files(spacePrefix2)
    id2row1 = space1.get_id2row()
    id2row2 = space2.get_id2row()
    id2column1 = space1.get_id2column()
    id2column2 = space2.get_id2column()
    column2id1 = space1.get_column2id()
    column2id2 = space2.get_column2id()
    intersected_columns = list(set(id2column1).intersection(id2column2))
    intersected_columns_id1 = [column2id1[item] for item in intersected_columns]
    intersected_columns_id2 = [column2id2[item] for item in intersected_columns]
    reduced_matrix1 = space1.get_cooccurrence_matrix()[:, intersected_columns_id1].get_mat()
    reduced_matrix2 = space2.get_cooccurrence_matrix()[:, intersected_columns_id2].get_mat()

    if is_len:
        # L2-normalize vectors
        l2norm1 = linalg.norm(reduced_matrix1, axis=1, ord=2)
        l2norm2 = linalg.norm(reduced_matrix2, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        l2norm2[l2norm2==0.0] = 1.0 # Convert 0 values to 1
        reduced_matrix1 /= l2norm1.reshape(len(l2norm1),1)
        reduced_matrix2 /= l2norm2.reshape(len(l2norm2),1)

    # Make new spaces    
    reduced_space1 = Space(SparseMatrix(reduced_matrix1), id2row1, intersected_columns)
    reduced_space2 = Space(SparseMatrix(reduced_matrix2), id2row2, intersected_columns)

    if reduced_space1.get_id2column()!=reduced_space2.get_id2column():
        sys.exit('Two spaces not properly aligned!')

    # Save the Space object in pickle format
    save_pkl_files(reduced_space1, outPath1 + '.sm', save_in_one_file=True)
    save_pkl_files(reduced_space2, outPath2 + '.sm', save_in_one_file=True)

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   

    
if __name__ == '__main__':
    main()
