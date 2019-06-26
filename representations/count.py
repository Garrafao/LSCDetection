import sys
sys.path.append('./modules/')

from collections import defaultdict
from docopt import docopt
import logging
import time
import numpy as np
from dsm import save_pkl_files, PathLineSentences_mod
from scipy.sparse import dok_matrix, csr_matrix, linalg
from composes.semantic_space.space import Space
from composes.matrix.sparse_matrix import SparseMatrix


def main():
    """
    Make count-based vector space from corpus.
    """

    # Get the arguments
    args = docopt("""Make count-based vector space from corpus.

    Usage:
        count.py [-l] <windowSize> <corpDir> <outPath> <lowerBound> <upperBound>
        
    Arguments:
       
        <corpDir> = path to corpus directory with zipped files, each sentence in form 'year\tword1 word2 word3...'
        <outPath> = output path for vectors
        <windowSize> = the linear distance of context words to consider in each direction
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period

    Options:
        -l, --len   normalize final vectors to unit length

    """)
    
    is_len = args['--len']
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']
    windowSize = int(args['<windowSize>'])    
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])
    
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Build vocabulary
    logging.info("Building vocabulary")
    sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)
    vocabulary = list(set([word for sentence in sentences for word in sentence if len(sentence)>1])) # Skip one-word sentences to avoid zero-vectors
    w2i = {w: i for i, w in enumerate(vocabulary)}
    
    # Initialize co-occurrence matrix as dictionary
    cooc_mat = defaultdict(lambda: 0)

    # Get counts from corpus
    sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)
    logging.info("Counting context words")
    for sentence in sentences:
        for i, word in enumerate(sentence):
            lowerWindowSize = max(i-windowSize, 0)
            upperWindowSize = min(i+windowSize, len(sentence))
            window = sentence[lowerWindowSize:i] + sentence[i+1:upperWindowSize+1]
            if len(window)==0: # Skip one-word sentences
                continue
            windex = w2i[word]
            for contextWord in window:
                cooc_mat[(windex,w2i[contextWord])] += 1

    
    # Convert dictionary to sparse matrix
    logging.info("Converting dictionary to matrix")
    cooc_mat_sparse = dok_matrix((len(vocabulary),len(vocabulary)), dtype=float)
    try:
        cooc_mat_sparse.update(cooc_mat)
    except NotImplementedError:
        cooc_mat_sparse._update(cooc_mat)
    
    if is_len:
        # L2-normalize vectors
        l2norm1 = linalg.norm(cooc_mat_sparse, axis=1, ord=2)
        l2norm1[l2norm1==0.0] = 1.0 # Convert 0 values to 1
        cooc_mat_sparse /= l2norm1.reshape(len(l2norm1),1)

    # Make space
    vocabulary = [v.encode('utf-8') for v in vocabulary]
    countSpace = Space(SparseMatrix(cooc_mat_sparse), vocabulary, vocabulary)
    
    # Save the Space object in pickle format
    save_pkl_files(countSpace, outPath, save_in_one_file=False)    
        
    logging.info("Corpus has size %d" % sentences.corpusSize)
    logging.info("--- %s seconds ---" % (time.time() - start_time))

    
if __name__ == '__main__':
    main()
