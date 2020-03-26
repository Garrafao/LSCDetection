from collections import defaultdict
from gensim.models.word2vec import PathLineSentences
from docopt import docopt
import logging
import time


def main():
    """
    Preprocess corpus (remove low-frequency words, etc.).
    """

    # Get the arguments
    args = docopt("""Preprocess corpus (remove low-frequency words, etc.).

    Usage:
        preprocess.py <corpDir> <outPath> <minFreq>
        
    Arguments:
       
        <corpDir> = path to corpus or corpus directory (iterates through files)
        <outPath> = output path
        <minFreq> = minimum frequency threshold
        
    """)
    
    corpDir = args['<corpDir>']
    outPath = args['<outPath>']        
    minFreq = int(args['<minFreq>'])

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.info(__file__.upper())
    start_time = time.time()
    

    # Get sentence iterator
    sentences = PathLineSentences(corpDir)

    # Initialize frequency dictionary
    freqs = defaultdict(int)      

    # Iterate over sentences and words
    for sentence in sentences:
        for word in sentence:
            freqs[word] = freqs[word] + 1

    # Get sentence iterator
    sentences = PathLineSentences(corpDir)            

    # Write output
    with open(outPath, 'w', encoding='utf-8') as f_out:
        for sentence in sentences:
            out_sentence = [word for word in sentence if freqs[word] >= minFreq]
            if len(out_sentence) > 1:
                f_out.write(' '.join(out_sentence)+'\n')

    logging.info("--- %s seconds ---" % (time.time() - start_time))                   
    

if __name__ == '__main__':
    main()
