import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import gensim
from gensim.models.word2vec import PathLineSentences
from gensim.models import Word2Vec


def main():
    """
    Make comparable embedding vector spaces with Skip-Gram with Negative Sampling as described in:

       Yoon Kim, Yi-I. Chiu, Kentaro Hanaki, Darshan Hegde, and Slav Petrov. 2014. Temporal analysis of language through neural language models. arXiv preprint arXiv:1405.3515.
    
    """

    # Get the arguments
    args = docopt("""Make comparable embedding vector spaces with Skip-Gram with Negative Sampling and Vector Initialization from corpus.

    Usage:
        sgns_vi.py [-l] <modelPath> <corpDir> <outPath> <windowSize> <dim> <k> <t> <minCount> <itera>
        
    Arguments:
       
        <modelPath> = model for initialization
        <corpDir> = path to corpus directory with zipped files, each sentence in form 'year\tword1 word2 word3...'
        <outPath> = output path for vectors
        <windowSize> = the linear distance of context words to consider in each direction
        <dim> = dimensionality of embeddings
        <k> = number of negative samples parameter (equivalent to shifting parameter for PPMI)
        <t> = threshold for subsampling
        <minCount> = number of occurrences for a word to be included in the vocabulary
        <itera> = number of iterations

    Options:
        -l, --len   normalize final vectors to unit length

    Note:
        This script has been updated considerably compared to the version used in

            Dominik Schlechtweg, Anna Hätty, Marco del Tredici, and Sabine Schulte im Walde. 2019. A Wind of Change: Detecting and Evaluating Lexical Semantic Change across Times and Domains. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pages 732-746, Florence, Italy. ACL.

        The Skip Gram Model consist of three layers, the input layer, hidden layer and output layer. Weights between the input layer and the hidden layer are stored in the Embedding Matrix, which is later used for getting the individual word embeddings by looking at only one column of the Matrix. The Context matrix stores the weights between the hidden layer and the output layer.

        Differences:
        In the original version for training on the second corpus only the previously created Embedding Matrix was loaded into the new model, so the Context matrix is newly initialized with random values. In the updated version the whole model is reused for training on the second corpus, that includes the Embedding Matrix as well as the Context matrix.

        Additionally, vocabulary

    """)
    
    is_len = args['--len']
    modelPath = args['<modelPath>'] 
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
         
    # Load model
    model = Word2Vec.load(modelPath)
    
    # Intersect vocabulary
    vocab_sentences = PathLineSentences(corpDir)
    logging.getLogger('gensim').setLevel(logging.ERROR)    
    model.build_vocab(vocab_sentences, update=True)

    # Train
    sentences = PathLineSentences(corpDir)
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
