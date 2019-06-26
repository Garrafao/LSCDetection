import sys
sys.path.append('./modules/')

import codecs
from collections import defaultdict
import os
from os.path import basename
import zipfile
from docopt import docopt
import logging
import logging.config
import time
import gensim
from dsm import PathLineSentences_mod



def main():
    """
    Make embedding vector space with Negative Sampling from corpus.
    """

    # Get the arguments
    args = docopt("""Make embedding vector space with Skip-Gram with Negative Sampling from corpus.

    Usage:
        sgns.py [-l] <windowSize> <dim> <k> <t> <minCount> <itera> <corpDir> <outPath> <lowerBound> <upperBound>
        
    Arguments:
       
        <windowSize> = the linear distance of context words to consider in each direction
        <dim> = dimensionality of embeddings
        <k> = number of negative samples parameter (equivalent to shifting parameter for PPMI)
        <t> = threshold for subsampling
        <minCount> = number of occurrences for a word to be included in the vocabulary
        <itera> = number of iterations
        <corpDir> = path to corpus directory with zipped files, each sentence in form 'year\tword1 word2 word3...'
        <outPath> = output path for vectors
        <lowerBound> = lower bound for time period
        <upperBound> = upper bound for time period

    Options:
        -l, --len   normalize final vectors to unit length

    """)

    is_len = args['--len']
    windowSize = int(args['<windowSize>'])    
    dim = int(args['<dim>'])    
    k = int(args['<k>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])        
    minCount = int(args['<minCount>'])    
    itera = int(args['<itera>'])    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']
    lowerBound = int(args['<lowerBound>'])
    upperBound = int(args['<upperBound>'])

    logging.config.dictConfig({'version': 1, 'disable_existing_loggers': True,})
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
         
    # Initialize model
    model = gensim.models.Word2Vec(sg=1, # skipgram
    							   hs=0, # negative sampling
    							   negative=k, # number of negative samples
    							   sample=t, # threshold for subsampling, if None, no subsampling is performed
    							   size=dim, window=windowSize, min_count=minCount, iter=itera, workers=20)

    # Initialize vocabulary
    vocab_sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)
    model.build_vocab(vocab_sentences)

    # Train
    sentences = PathLineSentences_mod(corpDir, lowerBound=lowerBound, upperBound=upperBound)
    model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)

    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)

    # Save the vectors and the model
    model.wv.save_word2vec_format(outPath + '.w2v')
    #model.save(outPath + '.model')

    logging.info("Corpus has size %d" % vocab_sentences.corpusSize)
    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
