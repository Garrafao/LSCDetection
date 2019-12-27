import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import gensim
from gensim.models.word2vec import PathLineSentences


def main():
    """
    Make embedding vector space with Negative Sampling from corpus.
    """

    # Get the arguments
    args = docopt("""Make embedding vector space with Skip-Gram with Negative Sampling from corpus.

    Usage:
        sgns.py [-l] <corpDir> <outPath> <windowSize> <dim> <k> <t> <minCount> <itera>
        
    Arguments:
       
        <corpDir> = path to corpus directory with zipped files
        <outPath> = output path for vectors
        <windowSize> = the linear distance of context words to consider in each direction
        <dim> = dimensionality of embeddings
        <k> = number of negative samples parameter (equivalent to shifting parameter for PPMI)
        <t> = threshold for subsampling
        <minCount> = number of occurrences for a word to be included in the vocabulary
        <itera> = number of iterations

    Options:
        -l, --len   normalize final vectors to unit length

    """)

    is_len = args['--len']
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']
    windowSize = int(args['<windowSize>'])    
    dim = int(args['<dim>'])    
    k = int(args['<k>'])
    if args['<t>']=='None':
        t = None
    else:
        t = float(args['<t>'])        
    minCount = int(args['<minCount>'])    
    itera = int(args['<itera>'])    

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
    vocab_sentences = PathLineSentences(corpDir)
    logging.getLogger('gensim').setLevel(logging.ERROR)    
    model.build_vocab(vocab_sentences)

    # Train
    sentences = PathLineSentences(corpDir)
    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)

    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)

    # Save the vectors and the model
    model.wv.save_word2vec_format(outPath)
    model.save(outPath + '.model')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
