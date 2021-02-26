import sys
sys.path.append('./modules/')

from docopt import docopt
import logging
import time
import gensim
from gensim.models.word2vec import PathLineSentences
from gensim.models import Word2Vec
import numpy as np


def main():
    """
    Make comparable embedding vector spaces with Skip-Gram with Negative Sampling as described in:
    
       Yoon Kim, Yi-I. Chiu, Kentaro Hanaki, Darshan Hegde, and Slav Petrov. 2014. Temporal analysis of language through neural language models. arXiv preprint arXiv:1405.3515.
       Additionally a length normalization step is performed on all word vectors after initializing on the provided model (before the training step), context vectors stay unchanged. This has proven to be effective at reducing the frequency bias. 
       Jens Kaiser, Sinan Kurtyigit, Serge Kotchourko, Dominik Schlechtweg. 2021. Effects of Pre- and Post-Processing in Lexical Semantic Change Detection. In Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics. 
    
    """

    # Get the arguments
    args = docopt("""Make comparable embedding vector spaces with Skip-Gram with Negative Sampling and Vector Initialization from corpus.
    Usage:
        sgns_vi_l2normalie.py [-l] <modelPath> <corpDir> <outPath>
        
    Arguments:
       
        <modelPath> = model for initialization
        <corpDir> = path to corpus directory with zipped files
        <outPath> = output path for vectors
    Options:
        -l, --len   normalize final vectors to unit length
    Note:
        This script has been updated considerably compared to the version used in
            Dominik Schlechtweg, Anna Hätty, Marco del Tredici, and Sabine Schulte im Walde. 2019. A Wind of Change: Detecting and Evaluating Lexical Semantic Change across Times and Domains. In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, pages 732-746, Florence, Italy. ACL.
        The Skip Gram Model consist of three layers, the input layer, hidden layer and output layer. Weights between the input layer and the hidden layer are stored in the Embedding Matrix, which is later used for getting the individual word embeddings by looking at only one column of the Matrix. The Context matrix stores the weights between the hidden layer and the output layer.
        Differences:
        In the original version for training on the second corpus only the previously created Embedding Matrix was loaded into the new model, so the Context matrix is newly initialized with random values. In the updated version the whole model is reused for training on the second corpus, that includes the Embedding Matrix as well as the Context matrix.
        Additionally, the vocabulary of the two corpora are now unified, before they were intersected.
    """)
    
    is_len = args['--len']
    modelPath = args['<modelPath>'] 
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()    
         
    # Load model
    model = Word2Vec.load(modelPath)
    
    # L2 normalization of word vectors
    model.wv.vectors = np.array([v / np.linalg.norm(v) for v in model.wv.vectors], dtype='float32')
    
    # Build vocabulary
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
