import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import gensim
from gensim.models.word2vec import PathLineSentences
from gensim.models import KeyedVectors


def intersection_dic(t1, t2):
    voc_t1 = [x for xs in t1 for x in xs]
    voc_t2 = [x for xs in t2 for x in xs]
    intersection = list(set(voc_t1) & set(voc_t2))
    return [[x] for x in intersection] # note: gensim wants list of iterables (i.e. list of lists)

def main():
    """
    Make comparable embedding vector spaces with Skip-Gram with Negative Sampling as described in:

       Yoon Kim, Yi-I. Chiu, Kentaro Hanaki, Darshan Hegde, and Slav Petrov. 2014. Temporal analysis of language through neural language models. arXiv preprint arXiv:1405.3515.
    
    """

    # Get the arguments
    args = docopt("""Make comparable embedding vector spaces with Skip-Gram with Negative Sampling and Vector Initialization from corpus.

    Usage:
        sgns_vi.py [-l] <vectorsPath> <corpDir> <outPath> <windowSize> <dim> <k> <t> <minCount> <itera>
        
    Arguments:
       
        <corpDir> = path to corpus directory with zipped files, each sentence in form 'year\tword1 word2 word3...'
        <outPath> = output path for vectors
        <vectorsPath> = vectors on which model should be initialized
        <windowSize> = the linear distance of context words to consider in each direction
        <dim> = dimensionality of embeddings
        <k> = number of negative samples parameter (equivalent to shifting parameter for PPMI)
        <t> = threshold for subsampling
        <minCount> = number of occurrences for a word to be included in the vocabulary
        <itera> = number of iterations

    Options:
        -l, --len   normalize final vectors to unit length

    Note:
        Initialization vectors should be non-length-normalized.

    """)
    
    is_len = args['--len']
    initVectorsPath = args['<vectorsPath>'] 
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
    
    # Receive vectors for initialization
    initVectors = KeyedVectors.load_word2vec_format(initVectorsPath, binary=False)

    # Initialize vocabulary
    vocab_initVectors = initVectors.vocab

    # Intersect vocabulary
    vocab_sentences_t_2 = PathLineSentences(corpDir)
    logging.getLogger('gensim').setLevel(logging.ERROR)    
    vocab_intersect = intersection_dic([[token] for token in vocab_initVectors],vocab_sentences_t_2)
    model.build_vocab(vocab_intersect)

    # Train
    sentences = PathLineSentences(corpDir)
    model.intersect_word2vec_format(initVectorsPath, lockf=1)
    model.train(sentences, total_examples=model.corpus_count, epochs=model.epochs)
    
    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)

    # Save the vectors and the model
    model.wv.save_word2vec_format(outPath)
    #model.save(outPath + '.model')

    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
