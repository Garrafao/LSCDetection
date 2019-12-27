"""
Differences between sgns_vi and sgns_vi2:

Introduction:
The Skip Gram Model consist of three layers, the input layer, hidden layer and
output layer. Weights between the input layer and the hidden layer are stored
in the Embedding Matrix, which is later used for getting the individual word
embeddings by looking at only one column of the Matrix. The Context matrix
stores the weights between the hidden layer and the output layer.

Differences:
In sgns_vi for training on the second corpus only the previously
created Embedding Matrix is loaded into the new model, so the Context matrix
is newly initialized with random values.
In sgns_vi2 the whole model is reused for training on the second corpus, that
includes the Embedding Matrix as well as the Context matrix.
"""


import gensim
from gensim.models.word2vec import PathLineSentences
import time
import logging
from docopt import docopt
import sys
sys.path.append('./modules/')


def intersection_dic(t1, t2):
    voc_t1 = [x for xs in t1 for x in xs]
    voc_t2 = [x for xs in t2 for x in xs]
    intersection = list(set(voc_t1) & set(voc_t2))
    # note: gensim wants list of iterables (i.e. list of lists)
    return [[x] for x in intersection]


def main():
    """
    Make comparable embedding vector spaces with Skip-Gram with
    Negative Sampling as described in:

       Yoon Kim, Yi-I. Chiu, Kentaro Hanaki, Darshan Hegde, and
       Slav Petrov. 2014. Temporal analysis of language through
       neural language models. arXiv preprint arXiv:1405.3515.

    """

    # Get the arguments
    args = docopt("""Make comparable embedding vector spaces with Skip-Gram with
    Negative Sampling and Vector Initialization from corpus.

    Usage:
        sgns_vi2.py [-l] <corpDir1> <corpDir2> <outPath1> <outPath2> <windowSize> <dim> <k> <t> <minCount> <itera>

    Arguments:

        <corpDir1> = path to corpus directory with zipped files for first time step
        <corpDir2> = path to corpus directory with zipped files for second time step
        <outPath1> = output path for vectors for first time step
        <outPath2> = output path for vectors for second time step
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
    corpDir1 = args['<corpDir1>']
    corpDir2 = args['<corpDir2>']
    outPath1 = args['<outPath1>']
    outPath2 = args['<outPath2>']
    windowSize = int(args['<windowSize>'])
    dim = int(args['<dim>'])
    k = int(args['<k>'])
    if args['<t>'] == 'None':
        t = None
    else:
        t = float(args['<t>'])
    minCount = int(args['<minCount>'])
    itera = int(args['<itera>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()

    # Initialize model
    model = gensim.models.Word2Vec(sg=1,  # skipgram
                                   hs=0,  # negative sampling
                                   negative=k,  # number of negative samples
                                   sample=t,  # threshold for subsampling, if None, no subsampling is performed
                                   size=dim,
                                   window=windowSize,
                                   min_count=minCount,
                                   iter=itera,
                                   workers=20)

    # Initialize vocabulary
    logging.getLogger('gensim').setLevel(logging.ERROR)
    sentences_t1 = PathLineSentences(corpDir1)
    sentences_t2 = PathLineSentences(corpDir2)
    vocab_intersect = intersection_dic(sentences_t1, sentences_t2)
    model.build_vocab(vocab_intersect)

    # Train on the first corpus
    model.train(sentences_t1, total_examples=model.corpus_count, epochs=model.epochs)
    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)
    # Save the vectors and the model
    model.wv.save_word2vec_format(outPath1)
    # model.save(outPath1 + '.model')

    # Train on the second corpus
    model.train(sentences_t2, total_examples=model.corpus_count, epochs=model.epochs)
    if is_len:
        # L2-normalize vectors
        model.init_sims(replace=True)
    # Save the vectors and the model
    model.wv.save_word2vec_format(outPath2)
    # model.save(outPath2 + '.model')
    logging.info("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()
